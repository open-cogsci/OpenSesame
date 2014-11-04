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

from PyQt4 import QtCore, QtGui
from libqtopensesame.misc import includes, _
from libqtopensesame.misc.base_component import base_component
from libqtopensesame.misc.config import cfg
from libqtopensesame.items import experiment
from libopensesame import debug, misc
from libopensesame.exceptions import osexception
import libopensesame.experiment
import libopensesame.plugins
import libopensesame.misc
import os.path
import os
import sys
import time
import traceback
import subprocess

class qtopensesame(QtGui.QMainWindow, base_component):

	"""The main class of the OpenSesame GUI"""

	# Set to False for release!
	devmode = False

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
			QtGui.QMainWindow.__init__(self, parent, \
				QtCore.Qt.MacWindowToolBarButtonHint)
		else:
			QtGui.QMainWindow.__init__(self, parent)
		self.app = app
		self.first_show = True

	def resume_init(self):

		"""Resume GUI initialization"""

		from libopensesame import misc
		from libqtopensesame.misc import theme
		from libqtopensesame.extensions import extension_manager
		import platform
		import random

		# Set some initial variables
		self.current_path = None
		self.version = misc.version
		self.codename = misc.codename
		self.lock_refresh = False
		self.unsaved_changes = False

		# Make sure that QProgEdit doesn't complain about some standard names
		from QProgEdit import validate
		validate.addPythonBuiltins([u'exp', u'win', u'self'])

		# Initialize random number generator
		random.seed()

		# Check the filesystem encoding for debugging purposes
		debug.msg(u'filesystem encoding: %s' % misc.filesystem_encoding())

		# Parse the command line
		self.parse_command_line()

		# Restore the configuration
		self.restore_config()

		# Setup the UI
		self.load_ui(u'misc.main_window')
		self.ui.itemtree.setup(self)
		self.ui.tabwidget.main_window = self

		# Load a theme
		self.theme = theme.theme(self, self.options._theme)

		# Determine the home folder
		self.home_folder = libopensesame.misc.home_folder()

		# Create .opensesame folder if it doesn't exist yet
		if not os.path.exists(os.path.join(self.home_folder, u".opensesame")):
			os.mkdir(os.path.join(self.home_folder, u".opensesame"))

		# Set the filter-string for opening and saving files
		self.file_type_filter = \
			u"OpenSesame files (*.opensesame.tar.gz *.opensesame);;OpenSesame script and file pool (*.opensesame.tar.gz);;OpenSesame script (*.opensesame)"

		# Set the window message
		self.window_message(_(u"Welcome to OpenSesame %s") % self.version)

		# Set the window icon
		self.setWindowIcon(self.theme.qicon(u"opensesame"))

		# Make the connections
		self.ui.itemtree.structure_change.connect(self.update_overview_area)
		self.ui.action_quit.triggered.connect(self.close)
		self.ui.action_new.triggered.connect(self.new_file)
		self.ui.action_open.triggered.connect(self.open_file)
		self.ui.action_save.triggered.connect(self.save_file)
		self.ui.action_save_as.triggered.connect(self.save_file_as)
		self.ui.action_run.triggered.connect(self.run_experiment)
		self.ui.action_run_in_window.triggered.connect(
			self.run_experiment_in_window)
		self.ui.action_run_quick.triggered.connect(self.run_quick)
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
		self.ui.action_show_variable_inspector.triggered.connect(
			self.refresh_variable_inspector)
		self.ui.action_show_pool.triggered.connect(self.refresh_pool)
		self.ui.action_show_stdout.triggered.connect(self.refresh_stdout)
		self.ui.action_preferences.triggered.connect(
			self.ui.tabwidget.open_preferences)
		self.ui.button_help_stdout.clicked.connect(
			self.ui.tabwidget.open_stdout_help)

		# Setup the overview area
		self.ui.dock_overview.show()
		self.ui.dock_overview.visibilityChanged.connect( \
			self.ui.action_show_overview.setChecked)

		# Setup the variable inspector
		from libqtopensesame.widgets.variable_inspector import \
			variable_inspector
		self.ui.variable_inspector = variable_inspector(self)
		self.ui.dock_variable_inspector.hide()
		self.ui.dock_variable_inspector.visibilityChanged.connect(
			self.ui.action_show_variable_inspector.setChecked)
		self.ui.dock_variable_inspector.setWidget(self.ui.variable_inspector)

		# Setup the file pool
		from libqtopensesame.widgets.pool_widget import pool_widget
		self.ui.dock_pool.hide()
		self.ui.dock_pool.visibilityChanged.connect(
			self.ui.action_show_pool.setChecked)
		self.ui.pool_widget = pool_widget(self)
		self.ui.dock_pool.setWidget(self.ui.pool_widget)

		# Uncheck the debug window button on debug window close
		self.ui.dock_stdout.visibilityChanged.connect( \
			self.ui.action_show_stdout.setChecked)

		# Initialize keyboard shortcuts
		self.ui.shortcut_itemtree = QtGui.QShortcut( \
			QtGui.QKeySequence(), self, self.ui.itemtree.setFocus)
		self.ui.shortcut_tabwidget = QtGui.QShortcut( \
			QtGui.QKeySequence(), self, self.ui.tabwidget.setFocus)
		self.ui.shortcut_stdout = QtGui.QShortcut( \
			QtGui.QKeySequence(), self, self.ui.edit_stdout.setFocus)
		self.ui.shortcut_variables = QtGui.QShortcut( \
			QtGui.QKeySequence(), self, \
			self.ui.variable_inspector.set_focus())
		self.ui.shortcut_pool = QtGui.QShortcut( \
			QtGui.QKeySequence(), self, \
			self.ui.pool_widget.ui.edit_pool_filter.setFocus)

		# Create the initial experiment, which is the default template.
		self.experiment = experiment.experiment(self, u"New experiment", \
			open(misc.resource(os.path.join(u"templates", \
				u"default.opensesame")), u"r").read())
		self.experiment.build_item_tree()

		# Miscellaneous initialization
		self.restore_state()
		self.update_recent_files()
		self.set_unsaved(False)

		# Initialize extensions
		self.extension_manager = extension_manager(self)
		self.extension_manager.fire(u'startup')

	def parse_command_line(self):

		"""Parse command line options"""

		import optparse

		parser = optparse.OptionParser( \
			u"usage: opensesame [experiment] [options]", \
			version = u"%s '%s'" % (self.version, self.codename))
		parser.set_defaults(debug=False)
		parser.set_defaults(run=False)
		parser.set_defaults(run_in_window=False)
		group = optparse.OptionGroup(parser, u"Immediately run an experiment")
		group.add_option(u"-r", u"--run", action=u"store_true", dest=u"run", \
			help=u"Run fullscreen")
		group.add_option(u"-w", u"--run-in-window", action=u"store_true", \
			dest=u"run_in_window", help=u"Run in window")
		parser.add_option_group(group)
		group = optparse.OptionGroup(parser, u"Miscellaneous options")
		group.add_option(u"-c", u"--config", action=u"store", dest=u"_config", \
			help=u"Set a configuration option, e.g, '--config auto_update_check=False;scintilla_font_size=10'. For a complete list of configuration options, please refer to the source of config.py.")
		group.add_option(u"-t", u"--theme", action=u"store", dest=u"_theme", \
			help=u"Specify a GUI theme")
		group.add_option(u"-d", u"--debug", action=u"store_true", dest= \
			u"debug", help= \
			u"Print lots of debugging messages to the standard output")
		group.add_option(u"--start-clean", action=u"store_true", dest= \
			u"start_clean", help= \
			u"Do not load configuration and do not restore window geometry")
		group.add_option(u"-s", u"--stack", action=u"store_true", dest= \
			u"_stack", help=u"Print stack trace (only in debug mode)")
		group.add_option(u"-p", u"--preload", action=u"store_true", dest= \
			u"preload", help=u"Preload Python modules")
		group.add_option(u"--pylink", action=u"store_true", dest=u"pylink", \
			help=u"Load PyLink before PyGame (necessary for using the Eyelink plug-ins in non-dummy mode)")
		group.add_option(u"--ipython", action=u"store_true", dest=u"ipython", \
			help=u"Enable the IPython interpreter")
		group.add_option(u"--locale", action=u"store_true", dest=u"locale", \
			help=u"Specify localization")
		group.add_option(u"--catch-translatables", action=u"store_true", \
			dest=u"catch_translatables", help=u"Log all translatable text")
		group.add_option(u"--no-global-resources", action=u"store_true", dest= \
			u"no_global_resources", help= \
			u"Do not use global resources on *nix")
		parser.add_option_group(group)
		self.options, args = parser.parse_args(sys.argv)
		if self.options.run and self.options.run_in_window:
			parser.error( \
				u"Options -r / --run and -w / --run-in-window are mutually exclusive.")

	def restore_config(self):

		"""Restores the configuration settings, but doesn't apply anything"""

		if self.options.start_clean:
			cfg.clear()
		cfg.restore()

	def restore_state(self):

		"""Restore the current window to the saved state"""

		debug.msg()

		# Force configuration options that were set via the command line
		cfg.parse_cmdline_args(self.options._config)
		self.recent_files = []
		if self.options.start_clean:
			debug.msg(u'Not restoring state')
			return
		self.resize(cfg.size)
		self.move(cfg.pos)
		self.experiment.auto_response = cfg.auto_response
		# Set the keyboard shortcuts
		self.ui.shortcut_itemtree.setKey(QtGui.QKeySequence( \
			cfg.shortcut_itemtree))
		self.ui.shortcut_tabwidget.setKey(QtGui.QKeySequence( \
			cfg.shortcut_tabwidget))
		self.ui.shortcut_stdout.setKey(QtGui.QKeySequence(cfg.shortcut_stdout))
		self.ui.shortcut_pool.setKey(QtGui.QKeySequence(cfg.shortcut_pool))
		self.ui.shortcut_variables.setKey(QtGui.QKeySequence( \
			cfg.shortcut_variables))
		# Unpack the string with recent files and only remember those that exist
		for path in cfg.recent_files.split(u";;"):
			if os.path.exists(path):
				debug.msg(u"adding recent file '%s'" % path)
				self.recent_files.append(path)
			else:
				debug.msg(u"missing recent file '%s'" % path)
		self.ui.action_enable_auto_response.setChecked( \
			self.experiment.auto_response)
		self.ui.action_onetabmode.setChecked(cfg.onetabmode)
		self.ui.action_compact_toolbar.setChecked( \
			cfg.toolbar_size == 16)
		self.ui.tabwidget.toggle_onetabmode()
		if cfg.toolbar_text:
			self.ui.toolbar_main.setToolButtonStyle( \
				QtCore.Qt.ToolButtonTextUnderIcon)
		else:
			self.ui.toolbar_main.setToolButtonStyle( \
				QtCore.Qt.ToolButtonIconOnly)
		self.set_style()
		self.theme.set_toolbar_size(cfg.toolbar_size)

	def restore_window_state(self):

		"""
		This is done separately from the rest of the restoration, because if we
		don't wait until the end, the window gets distorted again.
		"""

		if self.options.start_clean:
			debug.msg(u'Not restoring window state')
			return
		debug.msg()
		self.restoreState(cfg._initial_window_state)
		self.restoreGeometry(cfg._initial_window_geometry)

	def save_state(self):

		"""Restores the state of the current window"""

		debug.msg()
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
			self.set_status(_(u"Busy ..."), status=u"busy")
		else:
			self.set_status(_(u"Done!"))
		QtGui.QApplication.processEvents()

	def set_style(self):

		"""Appply the application style"""

		if cfg.style in QtGui.QStyleFactory.keys():
			self.setStyle(QtGui.QStyleFactory.create(cfg.style))
			debug.msg(u"using style '%s'" % cfg.style)
		else:
			debug.msg(u"ignoring unknown style '%s'" % cfg.style)
			cfg.style = u''

	def set_auto_response(self):

		"""Set the auto response based on the menu action"""

		self.experiment.auto_response = \
			self.ui.action_enable_auto_response.isChecked()
		self.update_preferences_tab()

	def save_unsaved_changes(self):

		"""
		If there are unsaved changes, present a dialog and save the changes if
		requested
		"""

		if not self.unsaved_changes:
			return True
		resp = QtGui.QMessageBox.question(self.ui.centralwidget, \
			_(u"Save changes?"), \
			_(u"Your experiment contains unsaved changes. Do you want to save your experiment?"), \
			QtGui.QMessageBox.Yes, QtGui.QMessageBox.No, \
				QtGui.QMessageBox.Cancel)
		if resp == QtGui.QMessageBox.Cancel:
			return False
		if resp == QtGui.QMessageBox.Yes:
			self.save_file()
		return True

	def set_unsaved(self, unsaved_changes=True):

		"""
		Set the unsaved changes status

		Keyword arguments:
		unsaved_changes -- a boolean indicating if there are unsaved changes
						   (default=True)
		"""

		self.unsaved_changes = unsaved_changes
		self.window_message()
		debug.msg(u"unsaved = %s" % unsaved_changes)

	def set_status(self, msg, timeout=5000, status=u'ready'):

		"""
		Prints a text message to the statusbar.

		Arguments:
		msg			--	The message.

		Keyword arguments:
		timeout		--	A value in milliseconds after which the message is
						removed. (default=5000)
		status		--	The status. (default=u'ready')
		"""

		self.ui.statusbar.set_status(msg, timeout=timeout, status=status)

	def window_message(self, msg=None):

		"""
		Display a message in the window border, including an unsaved message
		indicator.

		Keyword arguments:
		msg		--	An optional message, if the message should be changed.
					(default=None)
		"""

		if msg != None:
			self.window_msg = msg
			if os.name == u'nt':
				self.window_msg = self.window_msg.replace(u'/', u'\\')
		if self.unsaved_changes:
			self.setWindowTitle(_(u"%s [unsaved]") % self.window_msg)
		else:
			self.setWindowTitle(self.window_msg)

	def set_immediate_rename(self):

		"""Set the immediate rename option based on the menu action"""

		cfg.immediate_rename = self.ui.action_immediate_rename.isChecked()
		debug.msg(u"set to %s" % cfg.immediate_rename)

	def update_overview_area(self):

		"""
		desc:
			Refreshes the overview area.
		"""

		self.experiment.build_item_tree()

	def update_preferences_tab(self):

		"""
		If the preferences tab is open, make sure that its controls are updated
		to match potential changes to the preferences
		"""

		w = self.ui.tabwidget.get_widget(u'__preferences__')
		if w != None:
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
		self.ui.dock_stdout.setVisible(True)

	def refresh_pool(self, make_visible=None):

		"""
		Refresh the file pool

		Keyword arguments:
		make_visible -- an optional boolean that sets the visibility of the file
						pool (default = None)
		"""

		if make_visible != None:
			self.ui.action_show_pool.setChecked(make_visible)
		if not self.ui.action_show_pool.isChecked():
			self.ui.dock_pool.setVisible(False)
			return
		self.ui.dock_pool.setVisible(True)
		self.ui.pool_widget.refresh()

	def refresh_variable_inspector(self, dummy=None):

		"""
		Refresh the variable inspector and sets the visibility based on the menu
		action status

		Keyword arguments:
		dummy -- a dummy argument passed by the signal handler
		"""

		if self.ui.action_show_variable_inspector.isChecked():
			self.ui.dock_variable_inspector.setVisible(True)
			self.ui.variable_inspector.refresh()
		else:
			self.ui.dock_variable_inspector.setVisible(False)

	def closeEvent(self, e):

		"""
		desc:
			Process a request to close the application.

		arguments:
			e:
				type:	QCloseEvent
		"""

		if debug.enabled or self.devmode:
			libopensesame.experiment.clean_up(debug.enabled)
			self.save_state()
			e.accept()
			return
		resp = QtGui.QMessageBox.question(self.ui.centralwidget, _(u"Quit?"),
			_(u"Are you sure you want to quit OpenSesame?"),
			QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		if resp == QtGui.QMessageBox.No:
			if not isinstance(e, bool):
				e.ignore()
				return
		if not self.save_unsaved_changes():
			e.ignore()
			return
		self.extension_manager.fire(u'close')
		self.save_state()
		libopensesame.experiment.clean_up(debug.enabled)
		e.accept()

	def update_recent_files(self):

		"""Recreate the list with recent documents"""

		from libqtopensesame.actions import recent_action

		# Add the current path to the front of the list
		if self.current_path != None and os.path.exists(self.current_path):
			if self.current_path in self.recent_files:
				self.recent_files.remove(self.current_path)
			self.recent_files.insert(0, self.current_path)

		# Trim the list
		self.recent_files = self.recent_files[:5]

		# Build the menu
		self.ui.menu_recent_files.clear()
		if len(self.recent_files) == 0:
			a = QtGui.QAction(_(u"(No recent files)"), \
				self.ui.menu_recent_files)
			a.setDisabled(True)
			self.ui.menu_recent_files.addAction(a)
		else:
			for path in self.recent_files:
				self.ui.menu_recent_files.addAction( \
					recent_action.recent_action(path, self, \
					self.ui.menu_recent_files))

	def new_file(self):

		"""Discard the current experiment and start with a new file"""

		self.ui.tabwidget.open_start_new()

	def open_file(self, dummy=None, path=None, add_to_recent=True):

		"""
		Open a .opensesame or .opensesame.tar.gz file

		Keyword arguments:
		dummy -- An unused argument which is passed by the signal (default=None)
		path -- The path to the file. If None, a file dialog is presented
				(default=None)
		"""

		if not self.save_unsaved_changes():
			self.ui.tabwidget.open_general()
			return
		if path == None:
			path = unicode(QtGui.QFileDialog.getOpenFileName(
				self.ui.centralwidget, _(u"Open file"),
				filter=self.file_type_filter, directory=cfg.file_dialog_path))
		if path == None or path == u'' or (not path.lower().endswith(
			u'.opensesame') and not path.lower().endswith(
			u'.opensesame.tar.gz')):
			return
		self.set_status(u"Opening ...", status=u'busy')
		self.ui.tabwidget.close_all()
		cfg.file_dialog_path = os.path.dirname(path)
		try:
			exp = experiment.experiment(self, u"Experiment", path,
				experiment_path=os.path.dirname(path))
		except Exception as e:
			if not isinstance(e, osexception):
				e = osexception(msg=u'Failed to open file', exception=e)
			self.print_debug_window(e)
			self.experiment.notify(e.html(), title=u'Exception')
			return
		self.experiment = exp
		self.experiment.build_item_tree()
		self.ui.tabwidget.open_general()		
		if add_to_recent:
			self.current_path = path
			self.window_message(self.current_path)
			self.update_recent_files()
			cfg.default_logfile_folder = os.path.dirname(self.current_path)
		else:
			self.window_message(u"New experiment")
			self.current_path = None
		self.set_auto_response()
		self.set_unsaved(False)
		self.refresh_pool()
		self.refresh_variable_inspector()
		self.extension_manager.fire(u'open_experiment', path=path)
		self.set_status(u"Opened %s" % path)

	def save_file(self, dummy=None, remember=True, catch=True):

		"""
		Save the current experiment

		Keyword arguments:
		dummy -- a dummy argument passed by the signal handler (default=None)
		remember -- a boolean indicating whether the file should be included in
					the list of recent files (default=True)
		catch -- a boolean indicating whether exceptions should be caught and
				 displayed in a notification (default=True)
		"""

		if self.current_path == None:
			self.save_file_as()
			return
		self.extension_manager.fire(u'save_experiment', path=self.current_path)
		# Indicate that we're busy
		self.set_busy(True)
		QtGui.QApplication.processEvents()
		# Get ready
		try:
			self.get_ready()
		except osexception as e:
			self.print_debug_window(e)
			self.experiment.notify(
				_(u"The following error occured while trying to save:<br/>%s") \
				% e)
			self.set_busy(False)
			return
		# Try to save the experiment if it doesn't exist already
		try:
			resp = self.experiment.save(self.current_path, overwrite=True)
			self.set_status(_(u"Saved as %s") % self.current_path)
		except Exception as e:
			if not catch:
				raise e
			self.print_debug_window(e)
			self.experiment.notify(_(u"Failed to save file. Error: %s") % e)
			self.set_busy(False)
			return
		if remember:
			self.update_recent_files()
		self.set_unsaved(False)
		self.window_message(self.current_path)
		self.set_busy(False)

	def save_file_as(self):

		"""Save the current experiment after asking for a file name"""

		if self.current_path == None:
			cfg.file_dialog_path = os.path.join(self.home_folder, \
				self.experiment.sanitize(self.experiment.title, strict=True, \
				allow_vars=False))
		else:
			cfg.file_dialog_path = self.current_path
		path, file_type = QtGui.QFileDialog.getSaveFileNameAndFilter( \
			self.ui.centralwidget, _(u'Save file as ...'), directory= \
			cfg.file_dialog_path, filter=self.file_type_filter)

		if path != None and path != u"":
			path = unicode(path)
			cfg.file_dialog_path = os.path.dirname(path)

			# If the extension has not been explicitly typed in, set it based
			# on the selected filter and, if no filter has been set, based on
			# whether there is content in the file pool
			if path[-18:].lower() != u".opensesame.tar.gz" and \
				path[-11:].lower() != u".opensesame":
				debug.msg(u"automagically determing file type")
				if u"(*.opensesame)" in file_type:
					path += u".opensesame"
				elif u"(*.opensesame.tar.gz)" in file_type:
					path += u".opensesame.tar.gz"
				elif len(os.listdir(self.experiment.pool_folder)) == 0:
					path += u".opensesame"
				else:
					path += u".opensesame.tar.gz"
				debug.msg(path)
			# Avoid chunking of file extensions. This happens sometimes when
			# file managers (used for the save-file dialog) have difficulty
			# with multi-part extensions.
			path = path.replace(u'.opensesame.opensesame', u'.opensesame')
			path = path.replace(u'.opensesame.tar.opensesame', u'.opensesame')
			path = path.replace(u'.opensesame.tar.gz.opensesame',
				u'.opensesame')
			# Warn if we are saving in .opensesame format and there are files
			# in the file pool.
			if len(os.listdir(self.experiment.pool_folder)) > 0 \
				and path.lower().endswith(u'.opensesame'):
				self.experiment.notify(
					_(u'You have selected the <code>.opensesame</code> format. This means that the file pool has <i>not</i> been saved. To save the file pool along with your experiment, select the <code>.opensesame.tar.gz</code> format.'))
			self.current_path = path
			self.save_file()

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

		debug.msg(u"changing resolution to %d x %d" % (width, height))
		try:
			script = self.experiment.to_string()
		except Exception as e:
			if not isinstance(e, osexception):
				e = osexception(u'Failed to change the display resolution',
					exception=e)
			self.experiment.notify(e.html())
			return
		script = script.replace(u"\nset height \"%s\"\n" % \
			self.experiment.get(u"height"), u"\nset height \"%s\"\n" % height)
		script = script.replace(u"\nset width \"%s\"\n" % \
			self.experiment.get(u"width"), u"\nset width \"%s\"\n" % width)
		try:
			tmp = experiment.experiment(self, name=self.experiment.title,
				string=script, pool_folder=self.experiment.pool_folder,
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

	def select_from_pool(self, parent=None):

		"""
		desc:
			Opens the file-pool selection dialog.

		keywords:
			parent:		The parent QWidget or None to use main window.

		returns:
			A filename or None if no file was selected.
		"""

		from libqtopensesame.widgets import pool_widget
		if parent == None:
			parent = self
		_file = pool_widget.select_from_pool(self, parent=parent)
		if _file == u'':
			return None
		return _file

	def copy_to_pool(self, fname):

		"""
		Copy a file to the file pool

		Arguments:
		fname -- full path to file
		"""

		import shutil

		renamed = False
		_fname = os.path.basename(fname)
		while os.path.exists(os.path.join(self.experiment.pool_folder, _fname)):
			_fname = u"_" + _fname
			renamed = True

		if renamed:
			QtGui.QMessageBox.information(self.ui.centralwidget, \
				_(u"File renamed"), \
				_(u"The file has been renamed to '%s', because the file pool already contains a file named '%s'.") \
				% (_fname, os.path.basename(fname)))

		shutil.copyfile(fname, os.path.join(self.experiment.pool_folder, _fname))
		self.refresh_pool(True)

	def get_ready(self):

		"""Give all items the opportunity to get ready for running or saving"""

		# Redo the get_ready loop until no items report having done
		# anything
		debug.msg()
		redo = True
		done = []
		while redo:
			redo = False
			for item in self.experiment.items:
				if item not in done:
					done.append(item)
					if self.experiment.items[item].get_ready():
						debug.msg(u"'%s' did something" % item)
						redo = True
						break

	def print_debug_window(self, msg):

		"""
		Prints a message to the debug window.

		Arguments:
		msg		--	An object to print to the debug window.
		"""

		from libqtopensesame.widgets import pyterm
		out = pyterm.output_buffer(self)
		out.write(self.experiment.unistr(msg))

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

		from libqtopensesame.widgets import pyterm

		self.extension_manager.fire(u'run_experiment', fullscreen=fullscreen)
		# Disable the entire Window, so that we can't interact with OpenSesame.
		# TODO: This should be more elegant, so that we selectively disable
		# parts of the GUI.
		if sys.platform != 'darwin':
			self.setDisabled(True)
		# Reroute the standard output to the debug window
		buf = pyterm.output_buffer(self.ui.edit_stdout)
		sys.stdout = buf
		# Launch the runner!
		if cfg.runner == u'multiprocess':
			from libqtopensesame.runners import multiprocess_runner as runner
		elif cfg.runner == u'inprocess':
			from libqtopensesame.runners import inprocess_runner as runner
		elif cfg.runner == u'external':
			from libqtopensesame.runners import external_runner as runner
		debug.msg(u'using %s runner' % runner)
		_runner = runner(self)
		_runner.run(quick=quick, fullscreen=fullscreen,
			auto_response=self.experiment.auto_response)
		self.ui.edit_stdout.pyterm.set_workspace_globals(
			_runner.workspace_globals())
		# Undo the standard output rerouting
		sys.stdout = sys.__stdout__
		self.ui.edit_stdout.show_prompt()
		# Re-enable the GUI.
		if sys.platform != 'darwin':
			self.setDisabled(False)
		self.extension_manager.fire(u'end_experiment')

	def run_experiment_in_window(self):

		"""Runs the experiment in a window"""

		self.run_experiment(fullscreen=False)

	def run_quick(self):

		"""Run the experiment without asking for subject nr and logfile"""

		self.run_experiment(fullscreen=False, quick=True)

	def refresh(self, *deprecated, **_deprecated):

		"""
		desc:
			This function used to implement refreshing of the OpenSesame GUI,
			but has been deprecated.
		"""

		debug.msg(reason=u'deprecated')

	def _id(self):

		"""
		returns:
			desc:	A unique id string for this instance of OpenSesame. This
					allows us to distinguish between different instances of the
					program that may be running simultaneously.
			type:	unicode
		"""

		_id = `QtGui.QApplication.instance()`.decode(self.enc)
		return _id
