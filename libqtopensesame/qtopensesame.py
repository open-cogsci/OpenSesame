#-*- coding:utf-8 -*-

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
from libqtopensesame.misc.base_component import base_component
from libqtopensesame.misc.config import cfg
from libqtopensesame.items import experiment
from libopensesame import debug, metadata
from libopensesame.exceptions import osexception
from libopensesame.oslogging import oslogger
import libopensesame.experiment
import libopensesame.plugins
import libopensesame.misc
import os
import sys
import warnings
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'qtopensesame', category=u'core')
oslogger.start(u'gui')

class qtopensesame(QtWidgets.QMainWindow, base_component):

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
			QtWidgets.QMainWindow.__init__(self, parent, \
				QtCore.Qt.MacWindowToolBarButtonHint)
		else:
			QtWidgets.QMainWindow.__init__(self, parent)
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

		from libopensesame import misc
		from libqtopensesame.misc import theme
		from libqtopensesame.extensions import extension_manager
		import random

		# Make sure that icons are shown in context menu, regardless of the
		# system settings. This is necessary, because Ubuntu doesn't show menu
		# icons by default.
		QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_DontShowIconsInMenus,
			False)
		# Do a few things to customize QProgEdit behavior:
		# - Register the bundled monospace font (Droid Sans Mono)
		# - Make sure that QProgEdit doesn't complain about some standard names
		# - Ignore undefined name warnings, which don't play well with
		#   OpenSesame's single workspace
		QtGui.QFontDatabase.addApplicationFont(misc.resource(u'mono.ttf'))
		from QProgEdit import validate
		validate.addPythonBuiltins([u'exp', u'win', u'self'])
		if hasattr(validate, u'setPyFlakesFilter'):
			validate.setPyFlakesFilter(
				lambda msg: msg.message == u'undefined name %r')
		# Initialize random number generator
		random.seed()

		# Check the filesystem encoding for debugging purposes
		oslogger.debug(u'filesystem encoding: %s' % misc.filesystem_encoding())

		# # Parse the command line
		# self.parse_command_line()
		#
		# # Restore the configuration
		# self.restore_config()
		self.set_style()
		self.set_warnings()
		# self.set_locale()

		# Setup the UI
		self.load_ui(u'misc.main_window')
		self.theme = theme.theme(self, self.options._theme)
		self.ui.itemtree.setup(self)
		self.ui.console.setup(self)
		self.ui.tabwidget.main_window = self

		# Determine the home folder
		self.home_folder = libopensesame.misc.home_folder()

		# Create .opensesame folder if it doesn't exist yet
		if not os.path.exists(os.path.join(self.home_folder, u".opensesame")):
			os.mkdir(os.path.join(self.home_folder, u".opensesame"))

		# Set the filter-string for opening and saving files
		self.save_file_filter =u'OpenSesame files (*.osexp)'
		self.open_file_filter = \
			u'OpenSesame files (*.osexp *.opensesame.tar.gz *.opensesame)'

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
		self.ui.action_enable_auto_response.triggered.connect(
			self.set_auto_response)
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
		self.ui.action_show_stdout.triggered.connect(self.refresh_stdout)
		self.ui.action_preferences.triggered.connect(
			self.ui.tabwidget.open_preferences)

		# Setup console
		self.ui.button_help_console.clicked.connect(
			self.ui.tabwidget.open_stdout_help)
		self.ui.button_reset_console.clicked.connect(
			self.ui.console.reset)

		# Setup the overview area
		self.ui.dock_overview.show()
		self.ui.dock_overview.visibilityChanged.connect(
			self.ui.action_show_overview.setChecked)

		# Setup the file pool
		from libqtopensesame.widgets.pool_widget import pool_widget
		self.ui.dock_pool.hide()
		self.ui.dock_pool.visibilityChanged.connect(
			self.ui.action_show_pool.setChecked)
		self.ui.pool_widget = pool_widget(self)
		self.ui.dock_pool.setWidget(self.ui.pool_widget)

		# Uncheck the debug window button on debug window close
		self.ui.dock_stdout.hide()
		self.ui.dock_stdout.visibilityChanged.connect(
			self.ui.action_show_stdout.setChecked)

		# Initialize keyboard shortcuts
		self.ui.shortcut_itemtree = QtWidgets.QShortcut(QtGui.QKeySequence(), self,
			self.focus_overview_area)
		self.ui.shortcut_tabwidget = QtWidgets.QShortcut(
			QtGui.QKeySequence(), self, self.ui.tabwidget.focus)
		self.ui.shortcut_stdout = QtWidgets.QShortcut(QtGui.QKeySequence(), self,
			self.focus_debug_window)
		self.ui.shortcut_pool = QtWidgets.QShortcut(QtGui.QKeySequence(), self,
			self.focus_file_pool)

		# Create the initial experiment, which is the default template. Because
		# not all backends are supported under Python 3, we use a different
		# backend for each.
		if py3:
			tmpl = u'default-py3.osexp'
		else:
			tmpl = u'default.osexp'
		with safe_open(misc.resource(os.path.join(u'templates', tmpl)), u'r') as fd:
			self.experiment = experiment.experiment(self, u'New experiment',
				fd.read())
		self.experiment.build_item_tree()
		self.ui.itemtree.default_fold_state()
		# Miscellaneous initialization
		self.restore_state()
		self.update_recent_files()
		self.set_unsaved(False)
		self.init_custom_fonts()
		self.extension_manager = extension_manager(self)
		self.extension_manager.fire(u'startup')
		self.ui.console.start()

	def focus_debug_window(self):

		"""
		desc:
			Shows and focuses the debug window.
		"""

		self.ui.console.focus()
		self.ui.dock_stdout.setVisible(True)

	def focus_overview_area(self):

		"""
		desc:
			Shows and focuses the overview area.
		"""

		self.ui.itemtree.setFocus()
		self.ui.dock_overview.setVisible(True)

	def focus_file_pool(self):

		"""
		desc:
			Shows and focuses the file pool.
		"""

		self.ui.pool_widget.setFocus()
		self.ui.dock_pool.setVisible(True)

	def init_custom_fonts(self):

		"""
		desc:
			Registers the custom OpenSesame fonts, so that they are properly
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
				ttf = self.experiment.resource(u'%s.ttf' % font)
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
		group.add_option(u"-c", u"--config", action=u"store", dest=u"_config",
			help=\
			u"Set a configuration option, e.g, '--config auto_update_check="
			u"False;scintilla_font_size=10'. For a complete list of "
			u"configuration options, please refer to the source of config.py.")
		group.add_option(u"-t", u"--theme", action=u"store", dest=u"_theme",
			help=u"Specify a GUI theme")
		group.add_option(u"-d", u"--debug", action=u"store_true",
			dest=u"debug", help= \
			u"Print lots of debugging messages to the standard output")
		group.add_option(u"--start-clean", action=u"store_true",
			dest=u"start_clean", help=\
			u"Do not load configuration and do not restore window geometry")
		group.add_option(u"--locale", action=u"store_true", dest=u"locale",
			help=u"Specify localization")
		group.add_option(u"--catch-translatables", action=u"store_true",
			dest=u"catch_translatables", help=u"Log all translatable text")
		group.add_option(u"--no-global-resources", action=u"store_true",
			dest=u"no_global_resources",
			help=u"Do not use global resources on *nix")
		group.add_option(u'-w', u"--warnings", action=u"store_true",
			dest=u"warnings", help=u"Show elaborate warnings")
		parser.add_option_group(group)
		self.options, args = parser.parse_args(sys.argv)

	def set_warnings(self):

		"""
		desc:
			Sets a custom warning function, if specified on the command line.
		"""

		if '-w' not in sys.argv and '--warnings' not in sys.argv:
			return
		warnings.simplefilter(u'always')
		import traceback
		def warn_with_traceback(message, category, filename, lineno, line=None):
			print(u'***startwarning***')
			traceback.print_stack()
			print
			print(warnings.formatwarning(message, category, filename, lineno,
				line))
			print(u'***endwarning***')
		warnings.showwarning = warn_with_traceback

	def restore_config(self):

		"""Restores the configuration settings, but doesn't apply anything"""

		if not self.options.start_clean:
			cfg.restore()

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
		self.experiment.auto_response = cfg.auto_response
		# Set the keyboard shortcuts
		self.ui.shortcut_itemtree.setKey(QtGui.QKeySequence(
			cfg.shortcut_itemtree))
		self.ui.shortcut_tabwidget.setKey(QtGui.QKeySequence(
			cfg.shortcut_tabwidget))
		self.ui.shortcut_stdout.setKey(QtGui.QKeySequence(cfg.shortcut_stdout))
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
		self.ui.action_enable_auto_response.setChecked(
			self.experiment.auto_response)
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
		cfg.auto_response = self.experiment.auto_response
		cfg.toolbar_text = self.ui.toolbar_main.toolButtonStyle() == \
			QtCore.Qt.ToolButtonTextUnderIcon
		cfg.recent_files =  u";;".join(self.recent_files)
		cfg.save()

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

	def set_locale(self, translator):

		""""
		desc:
			Sets the application language.

		arguments:
			translator:
				desc:	For some reason, the QTranslator object needs to be
						created in the main function. Therefore it is passed
						as an argument.
				type:	QTranslator
		"""

		# If a locale has been explicitly specified, use it; otherwise, use the
		# system default locale.
		locale = cfg.locale if cfg.locale != u'' else \
			QtCore.QLocale().system().name()
		# If a locale has been specified on the command line, it overrides.
		for i, argv in enumerate(sys.argv[:-1]):
			if argv == '--locale':
				locale = safe_decode(sys.argv[i+1])
		qm = libopensesame.misc.resource(
			os.path.join(u'locale', locale) + u'.qm')
		# Say that we're trying to load de_AT, and it is not found, then we'll
		# try de_DE as fallback.
		if qm is None:
			l = locale.split(u'_')
			if l:
				_locale = l[0] +  u'_' + l[0].upper()
				qm = libopensesame.misc.resource(
					os.path.join(u'locale', _locale + u'.qm'))
				if qm is not None:
					locale = _locale
		self._locale = locale
		translator.load(qm)
		QtWidgets.QApplication.installTranslator(translator)

	def set_auto_response(self):

		"""Set the auto response based on the menu action"""

		self.experiment.auto_response = \
			self.ui.action_enable_auto_response.isChecked()
		self.update_preferences_tab()

	def set_unsaved(self, unsaved_changes=True):

		"""
		desc:
			Sets the unsaved changes status.

		keywords:
			unsaved_changes:
			 	desc:	Indicates if there are unsaved changes.
				type:	bool
		"""

		self.unsaved_changes = unsaved_changes
		self.window_message()

	def window_message(self, msg=None):

		"""
		desc:
			Display a message in the window border, including an unsaved message
			indicator.

		keywords:
			msg:
				desc:	A message, or None to refresh the window message.
				type:	[str, NoneType]
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

		"""
		desc:
			Refreshes the overview area.
		"""

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

	def refresh_stdout(self, dummy=None):

		"""
		Set the visibility of the debug window (stdout) based on
		the menu action status

		Keyword arguments:
		dummy -- a dummy argument passed by the signal handler (default=None)
		"""

		if not self.ui.action_show_stdout.isChecked():
			self.ui.dock_stdout.setVisible(False)
			return
		self.ui.console.focus()
		self.ui.dock_stdout.setVisible(True)

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

		"""
		desc:
			Checks whether there are unsaved changes. If so, the user can
			choose to discard or save these changes, or to cancel.

		returns:
			desc:	False if the user has cancelled, True otherwise.
			type:	bool
		"""

		from libqtopensesame._input.confirmation import confirmation
		if not self.unsaved_changes:
			return True
		resp = confirmation(self,
			msg=_(u'Your experiment contains unsaved changes. Do you want to save your experiment?'),
			title=_(u'Save changes?'), allow_cancel=True,
			default=u'cancel').show()
		if resp is None:
			return False
		if resp:
			self.save_file()
		return True

	def closeEvent(self, e):

		"""
		desc:
			Process a request to close the application.

		arguments:
			e:
				type:	QCloseEvent
		"""

		if self.block_close_event:
			e.ignore()
			return
		if not self.save_unsaved_changes():
			e.ignore()
			return
		self.extension_manager.fire(u'close')
		self.save_state()
		self.experiment.pool.clean_up()
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
			a = QtWidgets.QAction(_(u"(No recent files)"), \
				self.ui.menu_recent_files)
			a.setDisabled(True)
			self.ui.menu_recent_files.addAction(a)
		else:
			for path in self.recent_files:
				self.ui.menu_recent_files.addAction( \
					recent_action.recent_action(path, self, \
					self.ui.menu_recent_files))

	def open_file(self, dummy=None, path=None, add_to_recent=True):

		"""
		desc:
			Opens an experiment file.

		keywords:
			dummy:		Dummy argument passed by event handler.
			path:
			 	desc:	The path to the file. If None, a file dialog is
						presented.
				type:	[str, NoneType]
			add_to_recent:
				desc:	Indicates whether the file should be added to the list
						of recent experiments.
				type:	bool
		"""

		if not self.save_unsaved_changes():
			self.ui.tabwidget.open_general()
			return
		if path is None:
			path = QtWidgets.QFileDialog.getOpenFileName(self.ui.centralwidget,
				_(u"Open file"), filter=self.open_file_filter,
				directory=cfg.file_dialog_path)
		# In PyQt5, the QFileDialog.getOpenFileName returns a tuple instead of
		# a string, of which the first position contains the path. check for that
		# here.
		if isinstance(path,tuple):
			path = path[0]
		if path is None or path == u'' or ( \
			not path.lower().endswith(u'.opensesame') and \
			not  path.lower().endswith(u'.opensesame.tar.gz') and \
			not path.lower().endswith(u'.osexp')):
			return
		self.set_busy()
		self.ui.tabwidget.close_all(avoid_empty=False)
		cfg.file_dialog_path = os.path.dirname(path)
		try:
			exp = experiment.experiment(self, u"Experiment", path,
				experiment_path=os.path.dirname(path))
		except Exception as e:
			if not isinstance(e, osexception):
				e = osexception(msg=u'Failed to open file', exception=e)
			md = _(u'# Failed to open\n\nFailed to open the file for the '
				u'following reason:\n\n- ') + e.markdown()
			self.tabwidget.open_markdown(md)
			self.ui.console.write(e)
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
		self.set_auto_response()
		self.set_unsaved(False)
		self.ui.pool_widget.refresh()
		self.ui.console.reset()
		self.extension_manager.fire(u'open_experiment', path=path)
		self.set_busy(False)
		# Process non-fatal errors
		if exp.items.error_log:
			self.tabwidget.open_markdown(
				_(u'Errors occurred while opening the file:\n\n') + \
				u'\n---\n'.join([exc.markdown() for exc in exp.items.error_log]),
				title=_(u'Error'), icon=u'dialog-error')
			self.window_message(u"New experiment")
			self.current_path = None

	def set_run_status(self, status):

		self._run_status = status

	def run_status(self):

		return self._run_status

	def save_file(self):

		"""
		desc:
			Saves the current experiment.

		keywords:
			dummy:		A dummy argument passed by the signal handler.
			remember:
				desc:	Indicates whether the file should be included in the
						list of recent files.
				type:	bool
			catch:
			 	desc:	Indicates whether exceptions should be caught and
				 		displayed in a notification.
				type:	bool
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
		except osexception as e:
			self.ui.console.write(e)
			self.experiment.notify(
				_(u"The following error occured while trying to save:<br/>%s") \
				% e)
			self.set_busy(False)
			return
		# Try to save the experiment if it doesn't exist already
		try:
			self.experiment.save(self.current_path, overwrite=True)
			self.set_busy(False)
		except Exception as e:
			self.ui.console.write(e)
			self.experiment.notify(_(u"Failed to save file. Error: %s") % e)
			self.set_busy(False)
			return
		self.update_recent_files()
		self.set_unsaved(False)
		self.window_message(self.current_path)
		self.set_busy(False)

	def save_file_as(self):

		"""
		desc:
			Saves the current experiment after asking for a file name.
		"""

		# Choose a default file name based on the experiment title
		if self.current_path is None:
			cfg.file_dialog_path = os.path.join(self.home_folder,
				self.experiment.syntax.sanitize(self.experiment.var.title,
				strict=True, allow_vars=False))
		else:
			cfg.file_dialog_path = self.current_path
		path = QtWidgets.QFileDialog.getSaveFileName(self.ui.centralwidget,
			_(u'Save as…'), directory=cfg.file_dialog_path,
			filter=self.save_file_filter)
		# In PyQt5, the QFileDialog.getOpenFileName returns a tuple instead of
		# a string, of which the first position contains the path.
		if isinstance(path,tuple):
			path = path[0]
		if path is None or path == u"":
			return
		if not path.lower().endswith(u'.osexp'):
			path += u'.osexp'
		cfg.file_dialog_path = os.path.dirname(path)
		self.current_path = path
		self.read_only = False
		cfg.default_logfile_folder = os.path.dirname(self.current_path)
		self.save_file()

	def regenerate(self, script):

		"""
		desc:
			Regenerates the current experiment from script, and updates the GUI.

		argument:
			script:
				desc:	The new experiment script.
				type:	str
		"""

		try:
			exp = experiment.experiment(self, name=self.experiment.var.title,
				string=script, pool_folder=self.experiment.pool.folder(),
				experiment_path=self.experiment.experiment_path,
				resources=self.experiment.resources)
		except osexception as e:
			md = _(u'# Parsing error\n\nFailed to parse the script for the '
				u'following reason:\n\n- ') + e.markdown()
			self.tabwidget.open_markdown(md)
			self.console.write(e)
			return
		self.extension_manager.fire(u'prepare_regenerate')
		self.experiment = exp
		self.tabwidget.close_all()
		self.experiment.build_item_tree()
		self.extension_manager.fire(u'regenerate')

	def update_resolution(self, width, height):

		"""
		desc:
			Updates the resolution in a way that preserves display centering.
			This is kind of a quick hack. First generate the script, change the
			resolution in the script and then re-parse the script.

		arguments:
			width:		The display width in pixels.
			height:		The display height in pixels.
		"""

		oslogger.debug(u"changing resolution to %d x %d" % (width, height))
		try:
			script = self.experiment.to_string()
		except Exception as e:
			if not isinstance(e, osexception):
				e = osexception(u'Failed to change the display resolution',
					exception=e)
			md = _(u'# Error\n\nFailed to change display resolution for the '
				u'following reason:\n\n- ') + e.markdown()
			self.tabwidget.open_markdown(md)
			return
		old_cmd = self.experiment.syntax.create_cmd(
			u'set', [u'height', self.experiment.var.height])
		new_cmd = self.experiment.syntax.create_cmd(u'set', [u'height', height])
		script = script.replace(old_cmd, new_cmd)
		old_cmd = self.experiment.syntax.create_cmd(
			u'set', [u'width', self.experiment.var.width])
		new_cmd = self.experiment.syntax.create_cmd(u'set', [u'width', width])
		script = script.replace(old_cmd, new_cmd)
		try:
			tmp = experiment.experiment(self, name=self.experiment.var.title,
				string=script, pool_folder=self.experiment.pool.folder(),
				experiment_path=self.experiment.experiment_path,
				resources=self.experiment.resources)
		except osexception as error:
			self.experiment.notify(_(u"Could not parse script: %s") % error)
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

	def run_experiment(self, dummy=None, fullscreen=True, quick=False):

		"""
		Runs the current experiment.

		Keyword arguments:
		dummy 		--	A dummy argument that is passed by signaler.
						(default=None)
		fullscreen	--	A boolean to indicate whether the window should be
						fullscreen. (default=True)
		quick		--	A boolean to indicate whether default should be used for
						the log-file and subject number. Mostly useful while
						testing the experiment. (default=False)
		"""

		self.enable(False)
		print(u'\n')
		oslogger.debug(u'using %s runner' % cfg.runner)
		self._runner = self.runner_cls(self)
		self._runner.run(quick=quick, fullscreen=fullscreen,
			auto_response=self.experiment.auto_response)
		self.enable(True)

	@property
	def runner_cls(self):

		"""
		returns:
			desc:	A runner class.
			type:	base_runner
		"""

		# Multiprocessing dus not work if opensesame is packaged as an app
		# under OSX. For now just display a warning message and do nothing
		# For the same reason, inOSX the default runner is set to inprocess
		# for now in misc.config
		if cfg.runner == u'multiprocess' and sys.platform == "darwin" \
			and getattr(sys, 'frozen', None) and sys.version_info < (3,4):
			self.experiment.notify(u'Multiprocessing does not work in the '
				u'OSX app version yet. Please change the runner to '
				u'\'inprocess\' in the preferences panel')
		from libqtopensesame import runners
		return getattr(runners, u'%s_runner' % cfg.runner)

	def run_experiment_in_window(self):

		"""Runs the experiment in a window"""

		self.run_experiment(fullscreen=False)

	def run_quick(self):

		"""Run the experiment without asking for subject nr and logfile"""

		self.run_experiment(fullscreen=False, quick=True)

	def enable(self, enabled=True):

		"""
		desc:
			Enable or disable parts of the GUI (i.e. those parts that should be
			disabled when the experiment is running.

		arguments:
			enabled:
				type:	bool
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

	def refresh(self, *deprecated, **_deprecated):

		"""
		desc:
			This function used to implement refreshing of the OpenSesame GUI,
			but has been deprecated.
		"""

		oslogger.warning(u'qtopensesame.refresh() is deprecated')

	def _id(self):

		"""
		returns:
			desc:	A unique id string for this instance of OpenSesame. This
					allows us to distinguish between different instances of the
					program that may be running simultaneously.
			type:	unicode
		"""

		_id = safe_decode(repr(QtWidgets.QApplication.instance()), enc=self.enc)
		return _id

	@property
	def read_only(self):

		"""
		desc:
			Getter property for toggling the save action when setting.
		"""

		return self._read_only

	@read_only.setter
	def read_only(self, read_only):

		"""
		desc:
			Setter property for toggling the save action.
		"""

		self._read_only = read_only
		self.ui.action_save.setEnabled(not read_only)
