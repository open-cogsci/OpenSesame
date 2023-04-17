# -*- coding:utf-8 -*-

"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""
from libopensesame.py3compat import *
from qtpy import QtGui, QtCore, QtWidgets
from openexp import resources
from libqtopensesame.misc.base_component import BaseComponent
from libqtopensesame.misc.config import cfg
from libqtopensesame.items.experiment import Experiment
from libopensesame import metadata
from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger
from libopensesame import misc
import os
import sys
import warnings
import platform
import traceback
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'qtopensesame', category=u'core')
oslogger.start(u'gui')


SAVE_FILE_FILTER = u'OpenSesame files (*.osexp)'
OPEN_FILE_FILTER = (
    u'OpenSesame files (*.osexp *.opensesame.tar.gz *.opensesame);;'
    u'Python scripts (*.py);;'
    u'R scripts (*.R);;'
    u'All files (*.*)'
)


class QtOpenSesame(QtWidgets.QMainWindow, BaseComponent):

    """The main class of the OpenSesame GUI"""
    def __init__(self, app, parent=None):
        """
        Constructor. This does very little, except prepare the app to be shown
        as rapidly as possible. The actual GUI initialization is handled by
        resume_init().

        Arguments:
        app -- the QApplication

        Keyword arguments:
        parent -- a link to the parent window
        """
        if sys.platform == 'darwin':
            # Workaround for Qt issue on OS X that causes QMainWindow to
            # hide when adding QToolBar, see
            # https://bugreports.qt-project.org/browse/QTBUG-4300
            QtWidgets.QMainWindow.__init__(
                self,
                parent,
                QtCore.Qt.MacWindowToolBarButtonHint
            )
        else:
            QtWidgets.QMainWindow.__init__(self, parent)
        self._locale = None
        self.app = app
        self.first_show = True
        self.current_path = None
        self.version = metadata.__version__
        self.codename = metadata.codename
        self.lock_refresh = False
        self.unsaved_changes = False
        self._run_status = u'inactive'
        self.block_close_event = False
        self.parse_command_line()
        self.restore_config()

    def resume_init(self):
        """Resume GUI initialization"""
        import opensesame_extensions
        from libopensesame import misc
        from libopensesame.plugin_manager import PluginManager
        from libqtopensesame.misc import theme
        from libqtopensesame.misc.console_bridge import ConsoleBridge
        from libqtopensesame.widgets.pool_widget import PoolWidget
        from libqtopensesame.extensions import ExtensionManager
        import random

        # Make sure that icons are shown in context menu, regardless of the
        # system settings. This is necessary, because Ubuntu doesn't show menu
        # icons by default.
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_DontShowIconsInMenus,
                                            False)
        # Initialize random number generator
        random.seed()
        # Check the filesystem encoding for debugging purposes
        oslogger.debug(f'filesystem encoding: {sys.getfilesystemencoding()}')
        # self.restore_config()
        self.set_style()
        self.set_warnings()
        # Setup the UI
        self.load_ui(u'misc.main_window')
        self.theme = theme.theme(self, self.options._theme)
        self.ui.itemtree.setup(self)
        self.ui.tabwidget.main_window = self

        # Determine the home folder
        self.home_folder = misc.home_folder()

        # Create .opensesame folder if it doesn't exist yet
        if not os.path.exists(os.path.join(self.home_folder, u".opensesame")):
            os.mkdir(os.path.join(self.home_folder, u".opensesame"))

        # Set the window message
        self._read_only = False
        self.window_message(_(u"New experiment"))

        # Set the window icon
        self.setWindowIcon(self.theme.qicon(u"opensesame"))

        # Make the connections
        self.ui.itemtree.structure_change.connect(self.update_overview_area)
        self.ui.action_quit.triggered.connect(self.close)
        self.ui.action_open.triggered.connect(self.open_file)
        self.ui.action_save.triggered.connect(self.save_file)
        self.ui.action_save_as.triggered.connect(self.save_file_as)
        self.ui.action_run.triggered.connect(self.run_experiment)
        self.ui.action_run_in_window.triggered.connect(
            self.run_experiment_in_window)
        self.ui.action_run_quick.triggered.connect(self.run_quick)
        self.ui.action_kill.triggered.connect(self.kill_experiment)
        self.ui.action_close_current_tab.triggered.connect(
            self.ui.tabwidget.close_current)
        self.ui.action_close_all_tabs.triggered.connect(
            self.ui.tabwidget.close_all)
        self.ui.action_close_other_tabs.triggered.connect(
            self.ui.tabwidget.close_other)
        self.ui.action_onetabmode.triggered.connect(
            self.ui.tabwidget.toggle_onetabmode)
        self.ui.action_show_overview.triggered.connect(self.toggle_overview)
        self.ui.action_show_pool.triggered.connect(
            self.toggle_pool)
        self.ui.action_preferences.triggered.connect(
            self.ui.tabwidget.open_preferences)

        # Setup the overview area
        self.ui.dock_overview.show()
        self.ui.dock_overview.visibilityChanged.connect(
            self.ui.action_show_overview.setChecked)

        # Setup the file pool
        self.ui.dock_pool.hide()
        self.ui.dock_pool.visibilityChanged.connect(
            self.ui.action_show_pool.setChecked)
        self.ui.pool_widget = PoolWidget(self)
        self.ui.dock_pool.setWidget(self.ui.pool_widget)
        # Initialize keyboard shortcuts
        self.ui.shortcut_itemtree = self._kb_shortcut(self.focus_overview_area)
        self.ui.shortcut_tabwidget = self._kb_shortcut(self.ui.tabwidget.focus)
        self.ui.shortcut_pool = self._kb_shortcut(self.focus_file_pool)
        # Add shortcuts to tooltips
        self._tooltip_shortcut(self.action_open)
        self._tooltip_shortcut(self.action_save)
        self._tooltip_shortcut(self.action_save_as)
        self._tooltip_shortcut(self.action_run)
        self._tooltip_shortcut(self.action_run_in_window)
        self._tooltip_shortcut(self.action_run_quick)
        self._tooltip_shortcut(self.action_close_other_tabs)
        self._tooltip_shortcut(self.action_onetabmode)
        self._tooltip_shortcut(self.action_show_pool)
        self._tooltip_shortcut(self.action_show_overview)
        # Create the initial experiment, which is the default template.
        with safe_open(resources['templates/default.osexp'], u'r') as fd:
            self.experiment = Experiment(self, u'New experiment', fd.read())
        self.experiment.build_item_tree()
        self.ui.itemtree.default_fold_state()
        # Miscellaneous initialization
        self.restore_state()
        self.update_recent_files()
        self.set_unsaved(False)
        self.init_custom_fonts()
        self.console = ConsoleBridge(self)
        self._unloaded_extension_manager = PluginManager(opensesame_extensions)
        self.extension_manager = ExtensionManager(self)
        self.extension_manager.register_extension(self.ui.toolbar_items)
        self.extension_manager.fire(u'startup')

    @property
    def mode(self):
        r"""A property that determines the application mode, falling back to
        'default'.
        """
        if self.options.mode is None:
            return u'default'
        return self.options.mode

    def _tooltip_shortcut(self, action):
        r"""Adds a shortcut between parentheses to the tooltip of an action.

        Parameters
        ----------
        action
            A QAction
        """
        if not action.shortcut() or action.toolTip()[-1] == u')':
            return
        action.setToolTip(
            u'{} ({})'.format(action.toolTip(), action.shortcut().toString())
        )

    def _kb_shortcut(self, target):
        r"""Builds a simple keybaord shortcut. The key sequence is specified
        later, while restoring the settings.

        Parameters
        ----------
        target
            The target function.
        """
        return QtWidgets.QShortcut(QtGui.QKeySequence(), self, target)

    def focus_overview_area(self):
        r"""Shows and focuses the overview area."""
        self.ui.itemtree.setFocus()
        self.ui.dock_overview.setVisible(True)

    def focus_file_pool(self):
        r"""Shows and focuses the file pool."""
        self.ui.pool_widget.setFocus()
        self.ui.dock_pool.setVisible(True)

    def init_custom_fonts(self):
        r"""Registers the custom OpenSesame fonts, so that they are properly
        displayed in the sketchpad widget.
        """
        from libqtopensesame.widgets.font_widget import font_widget
        # The last element of font_list is the "other" entry
        for font in font_widget.font_list[:-1] + [
                u'RobotoCondensed-Regular',
                u'RobotoSlab-Regular',
                u'RobotoMono-Regular',
                u'Roboto-Regular'
        ]:
            try:
                ttf = resources[f'{font}.ttf']
            except FileNotFoundError:
                oslogger.error(u'failed to find %s' % font)
            else:
                oslogger.debug(u'registering %s (%s)' % (font, ttf))
                id = QtGui.QFontDatabase.addApplicationFont(ttf)
                families = QtGui.QFontDatabase.applicationFontFamilies(id)
                if families:
                    QtGui.QFont.insertSubstitution(font, families[0])

    def parse_command_line(self):
        """Parse command line options"""
        import optparse

        parser = optparse.OptionParser(
            u"usage: opensesame [experiment] [options]",
            version=u"%s '%s'" % (self.version, self.codename))
        parser.set_defaults(debug=False)
        group = optparse.OptionGroup(parser, u"Miscellaneous options")
        group.add_option(
            u"-c",
            u"--config",
            action=u"store",
            dest=u"_config",
            help=(
                u"Set a configuration option, e.g, '--config auto_update_check="
                u"False;scintilla_font_size=10'. For a complete list of "
                u"configuration options, please refer to the source of config.py."
            )
        )
        group.add_option(
            u"-p",
            u"--profile",
            action=u"store",
            dest=u"_config_profile",
            help=(u"Specify a profile with its own configuration")
        )
        group.add_option(
            u"-t",
            u"--theme",
            action=u"store",
            dest=u"_theme",
            help=u"Specify a GUI theme"
        )
        group.add_option(
            u"-d",
            u"--debug",
            action=u"store_true",
            dest=u"debug",
            help=u"Print lots of debugging messages to the standard output"
        )
        group.add_option(
            u"--start-clean",
            action=u"store_true",
            dest=u"start_clean",
            help=u"Do not load configuration and do not restore window geometry"
        )
        group.add_option(
            u"--locale",
            action=u"store_true",
            dest=u"locale",
            help=u"Specify localization"
        )
        group.add_option(
            u"--catch-translatables",
            action=u"store_true",
            dest=u"catch_translatables",
            help=u"Log all translatable text (for developers)"
        )
        group.add_option(
            u"--performance-profile",
            action=u"store_true",
            dest=u"profile",
            help=u"Profile OpenSesame performance (for developers)"
        )
        group.add_option(
            u"--no-global-resources",
            action=u"store_true",
            dest=u"no_global_resources",
            help=u"Do not use global resources on *nix"
        )
        group.add_option(
            u'-w',
            u"--warnings",
            action=u"store_true",
            dest=u"warnings",
            help=u"Show elaborate warnings"
        )
        group.add_option(
            u"--mode",
            action=u"store",
            dest=u"mode",
            help=u"Specify the application mode (default or ide)"
        )
        group.add_option(
            u"--no-chdir",
            action=u"store_true",
            default=u"false",
            dest=u"no_chdir",
            help=u"Don't change the working directory to that of the Pythone executable (Windows only)'"
        )
        parser.add_option_group(group)
        self.options, args = parser.parse_args(sys.argv)

    def set_warnings(self):
        r"""Sets a custom warning function, if specified on the command line."""
        if '-w' not in sys.argv and '--warnings' not in sys.argv:
            return
        warnings.simplefilter(u'always')
        import traceback

        def warn_with_traceback(message, category, filename, lineno, line=None):
            print(u'***startwarning***')
            traceback.print_stack()
            print(
                warnings.formatwarning(
                    message,
                    category,
                    filename,
                    lineno,
                    line
                )
            )
            print(u'***endwarning***')

        warnings.showwarning = warn_with_traceback

    def restore_config(self):
        """Restores the configuration settings, but doesn't apply anything"""
        if self.options.start_clean:
            return
        cfg.restore(
            self.mode
            if self.options._config_profile is None
            else self.options._config_profile
        )

    def restore_state(self):
        """Restore the current window to the saved state"""
        # Force configuration options that were set via the command line
        cfg.parse_cmdline_args(self.options._config)
        self.recent_files = []
        if self.options.start_clean:
            oslogger.info(u'Not restoring state')
            self.theme.set_toolbar_size(cfg.toolbar_size)
            return
        self.resize(cfg.size)
        self.move(cfg.pos)
        # Set the keyboard shortcuts
        self.ui.shortcut_itemtree.setKey(QtGui.QKeySequence(
            cfg.shortcut_itemtree))
        self.ui.shortcut_tabwidget.setKey(QtGui.QKeySequence(
            cfg.shortcut_tabwidget))
        self.ui.shortcut_pool.setKey(QtGui.QKeySequence(cfg.shortcut_pool))

        # Unpack the string with recent files and only remember those that exist
        recent_files = cfg.recent_files
        if hasattr(recent_files, u"split"):
            for path in recent_files.split(u";;"):
                if os.path.exists(path):
                    oslogger.debug(u"adding recent file '%s'" % path)
                    self.recent_files.append(path)
                else:
                    oslogger.debug(u"missing recent file '%s'" % path)
        # On Mac OS we always enable one-tab mode to deal with an issue in
        # Qt that makes the tabbar grow too large.
        if platform.system() == 'Darwin':
            cfg.onetabmode = True
            self.ui.action_onetabmode.setVisible(False)
        self.ui.action_onetabmode.setChecked(cfg.onetabmode)
        self.ui.tabwidget.toggle_onetabmode()
        if cfg.toolbar_text:
            self.ui.toolbar_main.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
        else:
            self.ui.toolbar_main.setToolButtonStyle(
                QtCore.Qt.ToolButtonIconOnly)
        self.theme.set_toolbar_size(cfg.toolbar_size)

    def restore_window_state(self):
        """
        This is done separately from the rest of the restoration, because if we
        don't wait until the end, the window gets distorted again.
        """
        if self.options.start_clean:
            oslogger.info(u'Not restoring window state')
            return
        self.restoreState(cfg._initial_window_state)
        self.restoreGeometry(cfg._initial_window_geometry)

    def save_state(self):
        """Restores the state of the current window"""
        cfg.size = self.size()
        cfg.pos = self.pos()
        cfg._initial_window_geometry = self.saveGeometry()
        cfg._initial_window_state = self.saveState()
        cfg.toolbar_text = self.ui.toolbar_main.toolButtonStyle() == \
            QtCore.Qt.ToolButtonTextUnderIcon
        cfg.recent_files = u";;".join(self.recent_files)
        cfg.save()

    def is_busy(self):
        """
        returns:
                True if the cursos has a busy state, False otherwise
        """
        return QtWidgets.QApplication.overrideCursor() is not None

    def set_busy(self, state=True):
        """
        Show/ hide the busy notification

        Keywords arguments:
        state -- indicates the busy status (default=True)
        """
        if state:
            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(
                QtCore.Qt.WaitCursor))
        else:
            QtWidgets.QApplication.restoreOverrideCursor()
        QtWidgets.QApplication.processEvents()

    def set_style(self):
        """Appply the application style"""
        if cfg.style in QtWidgets.QStyleFactory.keys():
            self.setStyle(QtWidgets.QStyleFactory.create(cfg.style))
            oslogger.debug(u"using style '%s'" % cfg.style)
        else:
            cfg.style = u''

    @property
    def locale(self):

        if self._locale:
            return self._locale
        # If a locale has been explicitly specified, use it; otherwise, use the
        # system default locale.
        locale = (cfg.locale if cfg.locale else QtCore.QLocale().bcp47Name())
        # If a locale has been specified on the command line, it overrides.
        for i, argv in enumerate(sys.argv[:-1]):
            if argv == '--locale':
                locale = safe_decode(sys.argv[i + 1])
        try:
            qm = resources[f'locale/{locale}.qm']
        except FileNotFoundError:
            oslogger.warning(f'no translation file found for {locale}')
            pass
        self._locale = locale
        return self._locale

    def set_locale(self, translators):
        """"Sets the application language.

        Parameters
        ----------
        translators: list of QTranslator
            For some reason, the QTranslator object needs to be created in the
            main function. Therefore it is passed as an argument.
        """
        try:
            qm = resources[f'locale/{self.locale}.qm']
        except FileNotFoundError:
            return
        self.translators = translators
        self._main_translator = self.translators.pop()
        self._main_translator.load(qm)
        QtWidgets.QApplication.installTranslator(self._main_translator)

    def set_unsaved(self, unsaved_changes=True):
        r"""Sets the unsaved changes status.

        Parameters
        ----------
        unsaved_changes : bool, optional
            Indicates if there are unsaved changes.
        """
        self.unsaved_changes = unsaved_changes
        self.window_message()

    def window_message(self, msg=None):
        r"""Display a message in the window border, including an unsaved
        message indicator.

        Parameters
        ----------
        msg : str, NoneType, optional
            A message, or None to refresh the window message.
        """
        if msg is not None:
            self.window_msg = msg
        flags = u''
        if self.unsaved_changes:
            flags += u' *'
        if self.read_only:
            flags += _(u' [read only]')
        self.setWindowTitle(self.window_msg + u'%s - OpenSesame' % flags)

    def update_overview_area(self):
        r"""Refreshes the overview area."""
        self.experiment.build_item_tree()
        item = self.tabwidget.current_item()
        if item is not None:
            self.experiment.items[item].update()

    def update_preferences_tab(self):
        """
        If the preferences tab is open, make sure that its controls are updated
        to match potential changes to the preferences
        """
        w = self.ui.tabwidget.get_widget(u'__preferences__')
        if w is not None:
            w.set_controls()

    def show_text_in_toolbar(self):
        """
        Set the toolbar style (text/ icons only) based on the menu action status
        """
        if self.ui.action_show_text_in_toolbar.isChecked():
            style = QtCore.Qt.ToolButtonTextUnderIcon
        else:
            style = QtCore.Qt.ToolButtonIconOnly
        self.ui.toolbar_main.setToolButtonStyle(style)

    def toggle_overview(self, dummy=None):
        """
        Set the visibility of the overview area based on the state of the
        toolbar action

        Keyword arguments:
        dummy -- a dummy argument passed by the signal handler (default=None)
        """
        if not self.ui.action_show_overview.isChecked():
            self.ui.dock_overview.setVisible(False)
            return
        self.ui.dock_overview.setVisible(True)

    def toggle_pool(self, make_visible):
        """
        Refresh the file pool

        Keyword arguments:
        make_visible -- an optional boolean that sets the visibility of the file
                                        pool (default = None)
        """
        if make_visible is not None:
            self.ui.action_show_pool.setChecked(make_visible)
        if not self.ui.action_show_pool.isChecked():
            self.ui.dock_pool.setVisible(False)
            return
        self.ui.dock_pool.setVisible(True)
        self.ui.pool_widget.setFocus()
        self.ui.pool_widget.refresh()

    def save_unsaved_changes(self):
        r"""Checks whether there are unsaved changes. If so, the user can
        choose to discard or save these changes, or to cancel.

        Returns
        -------
        bool
            False if the user has cancelled, True otherwise.
        """
        from libqtopensesame._input.confirmation import confirmation
        if not self.unsaved_changes:
            return True
        resp = confirmation(
            self,
            msg=_(
                u'Your experiment contains unsaved changes. Do you want to save your experiment?'),
            title=_(u'Save changes?'), allow_cancel=True,
            default=u'cancel'
        ).show()
        if resp is None:
            return False
        if resp:
            self.save_file()
        return True

    def closeEvent(self, e):
        r"""Process a request to close the application.

        Parameters
        ----------
        e : QCloseEvent
        """
        if self.block_close_event:
            e.ignore()
            return
        if not self.save_unsaved_changes():
            e.ignore()
            return
        self.save_state()
        self.experiment.pool.clean_up()
        self.extension_manager.fire(u'close')
        e.accept()

    def update_recent_files(self):
        """Recreate the list with recent documents"""
        from libqtopensesame.actions import recent_action

        # Add the current path to the front of the list
        if self.current_path is not None and os.path.exists(self.current_path):
            if self.current_path in self.recent_files:
                self.recent_files.remove(self.current_path)
            self.recent_files.insert(0, self.current_path)

        # Trim the list
        self.recent_files = self.recent_files[:5]

        # Build the menu
        self.ui.menu_recent_files.clear()
        if len(self.recent_files) == 0:
            a = QtWidgets.QAction(
                _(u"(No recent files)"),
                self.ui.menu_recent_files
            )
            a.setDisabled(True)
            self.ui.menu_recent_files.addAction(a)
        else:
            for path in self.recent_files:
                self.ui.menu_recent_files.addAction(
                    recent_action.recent_action(
                        path,
                        self,
                        self.ui.menu_recent_files
                    )
                )

    def open_file(self, dummy=None, path=None, add_to_recent=True):
        r"""Opens an experiment file.

        Parameters
        ----------
        dummy, optional
            Dummy argument passed by event handler.
        path : str, NoneType, optional
            The path to the file. If None, a file dialog is presented.
        add_to_recent : bool, optional
            Indicates whether the file should be added to the list of recent
            experiments.
        """
        from libopensesame.osexpfile import osexpreader

        if not self.save_unsaved_changes():
            self.ui.tabwidget.open_general()
            return
        if path is None:
            path = QtWidgets.QFileDialog.getOpenFileName(
                self.ui.centralwidget,
                _(u"Open file"),
                filter=OPEN_FILE_FILTER,
                directory=cfg.file_dialog_path
            )
        # In PyQt5, the QFileDialog.getOpenFileName returns a tuple instead of
        # a string, of which the first position contains the path. check for that
        # here.
        if isinstance(path, tuple):
            path = path[0]
        file_handler = self.extension_manager.provide(
            'file_handler',
            path=path
        )
        if file_handler:
            file_handler(path)
            return
        if path is None or not osexpreader.valid_extension(path):
            return
        self.set_busy()
        self.ui.tabwidget.close_all(avoid_empty=False)
        cfg.file_dialog_path = os.path.dirname(path)
        try:
            exp = Experiment(self, u"Experiment", path,
                             experiment_path=os.path.dirname(path))
        except Exception as e:
            md = _(
                u'# Failed to open\n\nFailed to open the file for the '
                u'following reason:\n\n- '
            ) + safe_decode(e)
            self.tabwidget.open_markdown(md)
            traceback.print_exc()
            self.console.write(e)
            self.set_busy(False)
            return
        self.experiment.pool.clean_up()
        self.experiment = exp
        self.experiment.build_item_tree()
        self.ui.itemtree.default_fold_state()
        self.ui.tabwidget.open_general()
        if add_to_recent:
            self.current_path = path
            self.read_only = not os.access(path, os.W_OK)
            self.window_message(self.current_path)
            self.update_recent_files()
            cfg.default_logfile_folder = os.path.dirname(self.current_path)
        else:
            self.window_message(u"New experiment")
            self.current_path = None
        self.set_unsaved(False)
        self.ui.pool_widget.refresh()
        self.extension_manager.fire(u'open_experiment', path=path)
        self.set_busy(False)
        # Process non-fatal errors
        if exp.items.error_log:
            self.tabwidget.open_markdown(
                _(f'Errors occurred while opening the file:\n\n') +
                '\n\n'.join(
                    [str(exc) for exc in exp.items.error_log]
                ),
                title=_(u'Error'),
                icon=u'dialog-error'
            )
            self.window_message(u"New experiment")
            self.current_path = None

    def set_run_status(self, status):

        self._run_status = status

    def run_status(self):

        return self._run_status

    def save_file(self):
        r"""Saves the current experiment.

        Parameters
        ----------
        dummy, optional
            A dummy argument passed by the signal handler.
        remember : bool, optional
            Indicates whether the file should be included in the list of recent
            files.
        catch : bool, optional
            Indicates whether exceptions should be caught and displayed in a
            notification.
        """
        if self.current_path is None:
            self.save_file_as()
            return
        self.extension_manager.fire(u'save_experiment', path=self.current_path)
        # Indicate that we're busy
        self.set_busy(True)
        QtWidgets.QApplication.processEvents()
        # Get ready
        try:
            self.get_ready()
        except OSException as e:
            self.console.write(e)
            self.notify(
                _(u"The following error occured while trying to save:<br/>%s")
                % e
            )
            self.set_busy(False)
            return
        # Try to save the experiment if it doesn't exist already
        try:
            self.experiment.save(self.current_path, overwrite=True)
            self.set_busy(False)
        except Exception as e:
            self.console.write(e)
            self.notify(
                _(u"Failed to save file. Error: %s")
                % safe_decode(e)
            )
            self.set_busy(False)
            return
        self.update_recent_files()
        self.set_unsaved(False)
        self.window_message(self.current_path)
        self.set_busy(False)

    def save_file_as(self):
        r"""Saves the current experiment after asking for a file name."""
        # Choose a default file name based on the experiment title
        if self.current_path is None:
            cfg.file_dialog_path = os.path.join(
                os.path.dirname(cfg.file_dialog_path),
                self.experiment.syntax.sanitize(
                    self.experiment.var.title,
                    strict=True,
                    allow_vars=False
                )
            )
        else:
            cfg.file_dialog_path = self.current_path
        path = QtWidgets.QFileDialog.getSaveFileName(
            self.ui.centralwidget,
            _(u'Save as…'),
            directory=cfg.file_dialog_path,
            filter=SAVE_FILE_FILTER
        )
        # In PyQt5, the QFileDialog.getOpenFileName returns a tuple instead of
        # a string, of which the first position contains the path.
        if isinstance(path, tuple):
            path = path[0]
        if not path:
            return
        if not path.lower().endswith(u'.osexp'):
            path += u'.osexp'
        cfg.file_dialog_path = os.path.dirname(path)
        self.current_path = path
        self.read_only = False
        cfg.default_logfile_folder = os.path.dirname(self.current_path)
        self.save_file()

    def regenerate(self, script):
        r"""Regenerates the current experiment from script, and updates the
        GUI.
        """
        self.extension_manager.fire(u'prepare_regenerate')
        try:
            exp = Experiment(self, name=self.experiment.var.title,
                             string=script,
                             pool_folder=self.experiment.pool.folder(),
                             experiment_path=self.experiment.experiment_path,
                             resources=self.experiment.resources)
        except OSException as e:
            md = _(
                u'# Parsing error\n\nFailed to parse the script for the '
                u'following reason:\n\n- '
            ) + e.markdown()
            self.tabwidget.open_markdown(md)
            self.console.write(e)
            return
        self.experiment = exp
        self.tabwidget.close_all()
        self.experiment.build_item_tree()
        self.extension_manager.fire(u'regenerate')

    def update_resolution(self, width, height):
        r"""Updates the resolution in a way that preserves display centering.
        This is kind of a quick hack. First generate the script, change the
        resolution in the script and then re-parse the script.

        Parameters
        ----------
        width
            The display width in pixels.
        height
            The display height in pixels.
        """
        oslogger.debug(u"changing resolution to %d x %d" % (width, height))
        try:
            script = self.experiment.to_string()
        except Exception as e:
            if not isinstance(e, OSException):
                e = OSException(
                    u'Failed to change the display resolution',
                    exception=e
                )
            md = _(
                u'# Error\n\nFailed to change display resolution for the '
                u'following reason:\n\n- '
            ) + e.markdown()
            self.tabwidget.open_markdown(md)
            return
        old_cmd = self.experiment.syntax.create_cmd(
            u'set', [u'height', self.experiment.var.height])
        new_cmd = self.experiment.syntax.create_cmd(
            u'set', [u'height', height])
        script = script.replace(old_cmd, new_cmd)
        old_cmd = self.experiment.syntax.create_cmd(
            u'set', [u'width', self.experiment.var.width])
        new_cmd = self.experiment.syntax.create_cmd(u'set', [u'width', width])
        script = script.replace(old_cmd, new_cmd)
        try:
            tmp = Experiment(self, name=self.experiment.var.title,
                             string=script,
                             pool_folder=self.experiment.pool.folder(),
                             experiment_path=self.experiment.experiment_path,
                             resources=self.experiment.resources)
        except OSException as error:
            self.notify(_(u"Could not parse script: %s") % error)
            self.edit_script.edit.setText(self.experiment.to_string())
            return
        self.experiment = tmp
        self.ui.tabwidget.close_other()
        self.update_overview_area()
        self.extension_manager.fire(u'regenerate')

    def get_ready(self):
        """Give all items the opportunity to get ready for running or saving"""
        # Redo the get_ready loop until no items report having done
        # anything
        redo = True
        done = []
        while redo:
            redo = False
            for item in self.experiment.items:
                if item not in done:
                    done.append(item)
                    if self.experiment.items[item].get_ready():
                        oslogger.debug(u"'%s' did something" % item)
                        redo = True
                        break

    def kill_experiment(self):
        """Tries to kill a running experiment. This is not supported by all
        runners.
        """
        self._runner.kill()
        self.ui.action_kill.setDisabled(True)

    def run_experiment(self, dummy=None, fullscreen=True, quick=False):
        """
        Runs the current experiment.

        Parameters
        ----------
        dummy
            A dummy argument that is passed by signaler.
                                        (default=None)
        fullscreen : bool, optional
            A boolean to indicate whether the window should be fullscreen.
        quick : bool, optional
            A boolean to indicate whether default should be used for the
            log-file and subject number. Mostly useful while testing the
            experiment.
        """
        self.get_ready()
        self.enable(False)
        print(u'\n')
        oslogger.debug(u'using %s runner' % cfg.runner)
        self._runner = self.runner_cls(self)
        self._runner.run(fullscreen=fullscreen, quick=quick)
        self.enable(True)
    
    def notify(self, msg, title=None, icon=None, **kwargs):
        self.extension_manager.fire('notify', message=msg, **kwargs)

    @property
    def runner_cls(self):
        """
        Returns
        -------
        BaseRunner
            A runner class.
        """
        runner = self.extension_manager.provide('runner')
        if runner is not None:
            return runner
        from libqtopensesame import runners
        return getattr(runners, u'%s_runner' % cfg.runner)

    def run_experiment_in_window(self):
        """Runs the experiment in a window"""
        self.run_experiment(fullscreen=False)

    def run_quick(self):
        """Run the experiment without asking for subject nr and logfile"""
        self.run_experiment(fullscreen=False, quick=True)

    def enable(self, enabled=True):
        r"""Enable or disable parts of the GUI (i.e. those parts that should be
        disabled when the experiment is running.

        Parameters
        ----------
        enabled : bool
        """
        self.block_close_event = not enabled
        self.ui.dock_overview.setEnabled(enabled)
        self.ui.centralwidget.setEnabled(enabled)
        for action in self.ui.toolbar_main.actions():
            # The kill action should be enabled when the experiment is running
            # and the runner supports killing
            action.setEnabled(
                not enabled and self.runner_cls.supports_kill
                if action.objectName() == u'action_kill'
                else enabled
            )
        self.ui.toolbar_items.setEnabled(enabled)
        self.ui.menubar.setEnabled(enabled)
        self.ui.dock_pool.setEnabled(enabled)
        self.ui.dock_overview.setEnabled(enabled)

    def _id(self):
        """
        returns:
                desc:	A unique id string for this instance of OpenSesame. This
                                allows us to distinguish between different instances of the
                                program that may be running simultaneously.
                type:	unicode
        """
        _id = safe_decode(
            repr(QtWidgets.QApplication.instance()), enc=self.enc)
        return _id

    @property
    def read_only(self):
        r"""Getter property for toggling the save action when setting."""
        return self._read_only

    @read_only.setter
    def read_only(self, read_only):
        r"""Setter property for toggling the save action."""
        self._read_only = read_only
        self.ui.action_save.setEnabled(not read_only)


# Alias for backwards compatibility
qtopensesame = QtOpenSesame


if __name__ == u'__main__':

    from libqtopensesame import __main__
    __main__.opensesame()
