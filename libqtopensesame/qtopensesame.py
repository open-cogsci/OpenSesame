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
from libqtopensesame import includes, experiment
import libopensesame.exceptions
import libopensesame.experiment
import libopensesame.plugins
import os.path
import os
import sys
import time
import traceback
import subprocess
from libqtopensesame import config

class plugin_action(QtGui.QAction):

	"""Menu action for a plugin"""

	def __init__(self, main_window, menu, plugin):

		"""
		Constructor

		Arguments:
		main_window -- the main window
		menu -- the menu into which the action should be inserted
		plugin -- the name of the plugin
		"""

		self.main_window = main_window
		icon = QtGui.QIcon(libopensesame.plugins.plugin_icon_large(plugin))
		self.plugin = plugin
		QtGui.QAction.__init__(self, icon, "Add %s" % plugin, menu)

		self.triggered.connect(self.add_plugin)

	def add_plugin(self, dummy = None):

		"""
		Start a drag to add the plugin to the experiment

		Keyword arguments:
		dummy -- a dummy argument passed by the signal handler (default = None)
		"""

		self.main_window.drag_item(self.plugin)

class recent_action(QtGui.QAction):

	"""Menu action for a recently opened file"""

	def __init__(self, path, main_window, menu):

		"""
		Constructor

		Arguments:
		path -- path to the recent file
		main_window -- the main window
		menu -- the menu into which the action should be inserted
		"""

		QtGui.QAction.__init__(self, os.path.basename(path), menu)
		self.main_window = main_window
		self.triggered.connect(self.open_file)
		self.path = path

	def open_file(self, dummy = None):

		"""
		Open the file

		Keyword arguments:
		dummy -- a dummy argument passed by the signal handler (default = None)
		"""

		self.main_window.open_file(path = self.path)

class qtopensesame(QtGui.QMainWindow):

	"""The main class of the OpenSesame GUI"""

	def __init__(self, parent=None):

		"""
		Constructor. This does very little, except prepare the app to be shown
		as rapidly as possible. The actual GUI initialization is handled by
		resume_init().

		Keyword arguments:
		parent -- a link to the parent window
		"""
		
		QtGui.QMainWindow.__init__(self, parent)
		
	def resume_init(self):
	
		"""Resume GUI initialization"""
		
		from libopensesame import misc	
		from libqtopensesame import pool_widget, opensesame_ui
		import platform				
		
		# Setup the UI
		self.ui = opensesame_ui.Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.toolbar_items.main_window = self
		self.ui.itemtree.main_window = self
		self.ui.table_variables.main_window = self

		# Set some initial variables
		self.current_path = None
		self.version = misc.version
		self.codename = misc.codename
		self.lock_refresh = False
		self.auto_check_update = True
		self.show_startup_tip = True
		self.default_logfile_folder = ""
		self.unsaved_changes = False
		
		# Determine the home folder
		if platform.system() == "Windows":
			self.home_folder = os.environ["USERPROFILE"]
		elif platform.system() == "Darwin":
			self.home_folder = os.environ["HOME"]
		elif platform.system() == "Linux":
			self.home_folder = os.environ["HOME"]
		else:
			self.home_folder = os.environ["HOME"]
			print "qtopensesame.__init__(): unknown platform '%s', using '%s' as home folder" \
				% (platform.system(), self.home_folder)

		# Determine autosave_folder		
		if not os.path.exists(os.path.join(self.home_folder, ".opensesame")):
			os.mkdir(os.path.join(self.home_folder, ".opensesame"))
		if not os.path.exists(os.path.join(self.home_folder, ".opensesame", "backup")):
			os.mkdir(os.path.join(self.home_folder, ".opensesame", "backup"))
		self.autosave_folder = os.path.join(self.home_folder, ".opensesame", "backup")

		# Set the filter-string for opening and saving files
		self.file_type_filter = "OpenSesame files (*.opensesame.tar.gz *.opensesame);;OpenSesame script and file pool (*.opensesame.tar.gz);;OpenSesame script (*.opensesame)"

		# Set the window message
		self.window_message("Welcome to OpenSesame %s" % self.version)
		
		# Make the connections
		self.ui.tabwidget.tabCloseRequested.connect(self.close_tab)
		self.ui.itemtree.itemClicked.connect(self.open_item)
		self.ui.action_quit.triggered.connect(self.close)
		self.ui.action_new.triggered.connect(self.new_file)
		self.ui.action_open.triggered.connect(self.open_file)
		self.ui.action_save.triggered.connect(self.save_file)
		self.ui.action_save_as.triggered.connect(self.save_file_as)
		self.ui.action_run.triggered.connect(self.run_experiment)
		self.ui.action_run_in_window.triggered.connect(self.run_experiment_in_window)
		self.ui.action_enable_auto_response.triggered.connect(self.set_auto_response)
		self.ui.action_close_all_tabs.triggered.connect(self.close_all_tabs)
		self.ui.action_close_other_tabs.triggered.connect(self.close_other_tabs)
		self.ui.action_show_variable_inspector.triggered.connect(self.refresh_variable_inspector)
		self.ui.action_show_pool.triggered.connect(self.refresh_pool)
		self.ui.action_show_stdout.triggered.connect(self.refresh_stdout)
		self.ui.action_help.triggered.connect(self.open_general_help_tab)
		self.ui.action_about.triggered.connect(self.about)
		self.ui.action_contribute.triggered.connect(self.open_contribute_tab)
		self.ui.action_submit_a_bug.triggered.connect(self.open_bug_tab)
		self.ui.action_check_for_update.triggered.connect(self.check_update)
		self.ui.action_open_autosave_folder.triggered.connect(self.open_autosave_folder)
		self.ui.action_preferences.triggered.connect(self.open_preferences_tab)
		self.ui.action_add_loop.triggered.connect(self.drag_loop)
		self.ui.action_add_sequence.triggered.connect(self.drag_sequence)
		self.ui.action_add_sketchpad.triggered.connect(self.drag_sketchpad)
		self.ui.action_add_feedback.triggered.connect(self.drag_feedback)
		self.ui.action_add_sampler.triggered.connect(self.drag_sampler)
		self.ui.action_add_synth.triggered.connect(self.drag_synth)
		self.ui.action_add_keyboard_response.triggered.connect(self.drag_keyboard_response)
		self.ui.action_add_mouse_response.triggered.connect(self.drag_mouse_response)
		self.ui.action_add_logger.triggered.connect(self.drag_logger)
		self.ui.action_add_inline_script.triggered.connect(self.drag_inline_script)
		self.ui.action_show_random_tip.triggered.connect(self.show_random_tip)
		self.ui.action_show_info_in_overview.triggered.connect(self.toggle_overview_info)		
		self.ui.button_help_stdout.clicked.connect(self.open_stdout_help_tab)		

		# Setup the variable inspector
		self.ui.dock_variable_inspector.hide()
		self.ui.button_help_variables.clicked.connect(self.open_variables_help_tab)
		self.ui.dock_variable_inspector.visibilityChanged.connect(self.ui.action_show_variable_inspector.setChecked)
		self.ui.edit_variable_filter.textChanged.connect(self.refresh_variable_inspector)

		# Setup the file pool	
		self.ui.dock_pool.hide()
		self.ui.dock_pool.visibilityChanged.connect(self.ui.action_show_pool.setChecked)
		self.ui.pool_widget = pool_widget.pool_widget(self)
		self.ui.dock_pool.setWidget(self.ui.pool_widget)		

		# Uncheck the debug window button on debug window close
		self.ui.dock_stdout.visibilityChanged.connect(self.ui.action_show_stdout.setChecked)

		# On Mac OS (darwin) hide, the run in Window functionality
		if sys.platform == "darwin":
			self.ui.action_run_in_window.setDisabled(True)
		
		# Create the initial experiment
		self.experiment = experiment.experiment(self, "New experiment", \
			open(misc.resource("default.opensesame"), "r").read())
		
		# Initialize the tabs
		self.init_general_tab()
		self.init_unused_tab()
		
		# Set the style sheet
		self.setStyleSheet(open(self.experiment.resource("stylesheet.qss")).read())
		
		# Build the items toolbar
		self.set_status("Welcome to OpenSesame %s" % self.version)
		self.restore_state()
		self.ui.toolbar_items.build()		
		self.refresh_plugins()		
		self.set_unsaved(False)
		self.start_autosave_timer()
		self.update_recent_files()
		self.clean_autosave()					
		self.parse_command_line()
			
	def parse_command_line(self):
	
		"""Parse command line options"""
		
		import optparse
		
		parser = optparse.OptionParser("usage: opensesame [experiment] [options]", \
			version = "%s '%s'" % (self.version, self.codename))
		parser.set_defaults(debug = False)
		parser.set_defaults(run = False)
		parser.set_defaults(run_in_window = False)
		group = optparse.OptionGroup(parser, "Immediately run an experiment")
		group.add_option("-r", "--run", action="store_true", dest="run", \
			help="Run fullscreen")
		group.add_option("-w", "--run-in-window", action="store_true", \
			dest="run_in_window", help="Run in window")
		parser.add_option_group(group)
		group = optparse.OptionGroup(parser, "Miscellaneous options")
		group.add_option("-d", "--debug", action="store_true", dest="debug", \
			help="Print lots of debugging messages to the standard output")
		group.add_option("-p", "--preload", action="store_true", dest="preload", \
			help="Preload Python modules")
		parser.add_option_group(group)
		group = optparse.OptionGroup(parser, "Miscellaneous options")
		group.add_option("--pylink", action="store_true", dest="pylink", \
			help="Load PyLink before PyGame (necessary for using the Eyelink plug-ins in non-dummy mode)")
		parser.add_option_group(group)
		self.options, args = parser.parse_args(sys.argv)
		if self.options.run and self.options.run_in_window:
			parser.error("Options -r / --run and -w / --run-in-window are mutually exclusive.")
			
	def restore_window_state(self):
	
		"""
		This is done separately from the rest of the restoration, because if we
		don't wait until the end, the window gets distorted again.
		"""
	
		self.restoreState(self._initial_window_state)
			
	def restore_state(self):

		"""Restore the current window to the saved state"""

		if self.experiment.debug:
			print "qtopensesame.restore_state()"

		settings = QtCore.QSettings("cogscinl", "opensesame")
		settings.beginGroup("MainWindow");
		self.resize(settings.value("size", QtCore.QSize(1000, 600)).toSize())
		self.move(settings.value("pos", QtCore.QPoint(200, 200)).toPoint())
		self._initial_window_state = settings.value("state").toByteArray()
		self.auto_check_update = settings.value("auto_check_update", True).toBool()
		self.show_startup_tip = settings.value("show_startup_tip", True).toBool()
		self.default_logfile_folder = settings.value("default_logfile_folder", self.home_folder).toString()
		self.autosave_interval = settings.value("autosave_interval", 10 * 60 * 1000).toInt()[0] # Every 10 minutes
		self.autosave_max_age = settings.value("autosave_max_age", 7).toInt()[0]
		self.immediate_rename = settings.value("immediate_rename", False).toBool()
		self.opensesamerun_exec = str(settings.value("opensesamerun_exec", "").toString())
		self.opensesamerun = settings.value("opensesamerun", False).toBool()
		self.experiment.auto_response = settings.value("auto_response", False).toBool()		
		self.style = settings.value("style", "").toString()				

		# Unpack the string with recent files and only remember those that still exist
		self.recent_files = []
		for path in unicode(settings.value("recent_files", "").toString()).split(";;"):
			if os.path.exists(path):
				self.recent_files.append(path)

		self.ui.action_enable_auto_response.setChecked(self.experiment.auto_response)
		self.ui.action_show_info_in_overview.setChecked(settings.value("overview_info", False).toBool())
		self.toggle_overview_info()

		if settings.value("toolbar_text", False).toBool():
			self.ui.toolbar_main.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
		else:
			self.ui.toolbar_main.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
			
		config.restore_config(settings)

		settings.endGroup()
		self.set_style()

	def save_state(self):

		"""Restores the state of the current window"""

		if self.experiment.debug:
			print "qtopensesame.save_state()"

		settings = QtCore.QSettings("cogscinl", "opensesame")
		settings.beginGroup("MainWindow")
		settings.setValue("size", self.size())
		settings.setValue("pos", self.pos())
		settings.setValue("state", self.saveState())
		settings.setValue("auto_check_update", self.auto_check_update)
		settings.setValue("show_startup_tip", self.show_startup_tip)
		settings.setValue("default_logfile_folder", self.default_logfile_folder)
		settings.setValue("autosave_interval", self.autosave_interval)
		settings.setValue("autosave_max_age", self.autosave_max_age)
		settings.setValue("immediate_rename", self.immediate_rename)
		settings.setValue("opensesamerun", self.opensesamerun)
		settings.setValue("opensesamerun_exec", self.opensesamerun_exec)
		settings.setValue("overview_info", self.overview_info)

		settings.setValue("auto_response", self.experiment.auto_response)
		settings.setValue("toolbar_text", self.ui.toolbar_main.toolButtonStyle() == QtCore.Qt.ToolButtonTextUnderIcon)
		settings.setValue("recent_files", ";;".join(self.recent_files))
		settings.setValue("style", self.style)

		config.save_config(settings)

		settings.endGroup()	
		
	def set_busy(self, state=True):
	
		"""
		Show/ hide the busy notification
		
		Keywords arguments:
		state -- indicates the busy status (default=True)
		"""
		
		if state:
			self.set_status("Busy ...", status="busy")
		else:
			self.set_status("Done!")
		QtGui.QApplication.processEvents()
		
	def set_style(self):
	
		"""Appply the application style"""
		
		if self.style in QtGui.QStyleFactory.keys():
			self.setStyle(QtGui.QStyleFactory.create(self.style))
			if self.experiment.debug:
				print "qtopensesame.set_style(): using style '%s'" % self.style
		else:
			if self.experiment.debug:
				print "qtopensesame.set_style(): ignoring unknown style '%s'" % self.style		
			self.style = ""				

	def set_auto_response(self):

		"""Set the auto response based on the menu action"""

		self.experiment.auto_response = self.ui.action_enable_auto_response.isChecked()
		self.update_preferences_tab()

	def open_autosave_folder(self):

		"""Open the autosave folder in a filemanager in a platform specific way"""

		if os.name == "nt":
			os.startfile(self.autosave_folder)
		elif os.name == "posix":
			pid = subprocess.Popen(["xdg-open", self.autosave_folder]).pid

	def start_autosave_timer(self):

		"""If autosave is enabled, construct and start the autosave timer"""

		if self.autosave_interval > 0:
			if self.experiment.debug:
				print "qtopensesame.start_autosave_timer(): starting auto-save timer (interval = %d ms)" % self.autosave_interval
			self.autosave_timer = QtCore.QTimer()
			self.autosave_timer.setInterval(self.autosave_interval)
			self.autosave_timer.setSingleShot(True)
			self.autosave_timer.timeout.connect(self.autosave)
			self.autosave_timer.start()
		else:
			if self.experiment.debug:
				print "qtopensesame.start_autosave_timer(): auto-save disabled"
			self.autosave_timer = None

	def autosave(self):

		"""Autosave the experiment if there are unsaved changes"""

		if not self.unsaved_changes:
			self.set_status("No unsaved changes, skipping backup")
			autosave_path = ""
		else:
			_current_path = self.current_path
			_unsaved_changes = self.unsaved_changes
			_window_msg = self.window_msg
			self.current_path = os.path.join(self.autosave_folder, \
				"%s.opensesame.tar.gz" % str(time.ctime()).replace(":", "_"))
			if self.experiment.debug:
				print "qtopensesame.autosave(): saving backup as %s" \
					% self.current_path
			try:
				self.save_file(False, remember=False, catch=False)
				self.set_status("Backup saved as %s" % self.current_path)
			except:
				self.set_status("Failed to save backup ...")
			autosave_path = self.current_path
			self.current_path = _current_path
			self.set_unsaved(_unsaved_changes)
			self.window_message(_window_msg)
		self.start_autosave_timer()
		return autosave_path
		
	def clean_autosave(self):
	
		"""Remove old files from the back-up folder"""
		
		for path in os.listdir(self.autosave_folder):
			_path = os.path.join(self.autosave_folder, path)		
			t = os.path.getctime(_path)
			age = (time.time() - t)/(60*60*24)
			if age > self.autosave_max_age:
				if self.experiment.debug:
					print "qtopensesame.clean_autosave(): removing '%s'" % path
				try:
					os.remove(_path)
				except:
					if self.experiment.debug:
						print "qtopensesame.clean_autosave(): failed to remove '%s'" % path

	def save_unsaved_changes(self):

		"""If there are unsaved changes, present a dialog and save the changes if requested"""

		if not self.unsaved_changes:
			return
		resp = QtGui.QMessageBox.question(self.ui.centralwidget, "Save changes?", "Your experiment contains unsaved changes. Do you want to save your experiment?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		if resp == QtGui.QMessageBox.Yes:
			self.save_file()

	def set_unsaved(self, unsaved_changes=True):

		"""
		Set the unsaved changes status

		Keyword arguments:
		unsaved_changes -- a boolean indicating if there are unsaved changes
						   (default=True)
		"""

		self.unsaved_changes = unsaved_changes
		self.window_message()

	def set_status(self, msg, timeout=5000, status="ready"):

		"""
		Print a text message to the statusbar

		Arguments:
		msg -- a string with the message

		Keyword arguments:
		timeout -- a value in milliseconds after which the message is removed (default = 5000)
		"""

		self.ui.statusbar.set_status(msg, timeout=timeout, status=status)

	def window_message(self, msg = None):

		"""
		Display a message in the window border, including an unsaved message indicator

		Keyword arguments:
		msg -- an optional message, if the message should be changed (default = None)
		"""

		if msg != None:
			self.window_msg = msg

		if self.unsaved_changes:
			self.setWindowTitle("%s [unsaved]" % self.window_msg)
		else:
			self.setWindowTitle("%s" % self.window_msg)

	def show_random_tip(self, dummy = None, always = True):

		"""
		Show a random tip dialog box

		Keyword arguments:
		dummy -- a dummy argument passed by the signal handler
		always -- a boolean indicating if the tip should be shown regardless
				  of the show tips on startup setting (default = True)
		"""

		from libqtopensesame import tip_dialog
		
		if always or self.show_startup_tip:
			d = tip_dialog.tip_dialog(self)
			d.exec_()
		elif self.experiment.debug:
			print "qtopensesame.show_random_tip(): skipping random tip"

	def start_new_wizard(self, dummy=None):

		"""
		Presents a start new-experiment-wizard type of dialog

		Keywords arguments:
		dummy -- a dummy argument passed by the signal handler (default=None)
		"""
		
		from libqtopensesame import start_new_dialog

		if config.get_config("new_experiment_dialog"):
			d = start_new_dialog.start_new_dialog(self)
			d.exec_()
		else:
			self.open_file(path=self.experiment.resource("default.opensesame"))
			self.window_message("New experiment")
			self.current_path = None
		self.set_auto_response()

	def set_immediate_rename(self):

		"""Set the immediate rename option based on the status of the menu action"""

		self.immediate_rename = self.ui.action_immediate_rename.isChecked()
		if self.experiment.debug:
			print "qtopensesame.set_immediate_rename(): set to %s" % self.immediate_rename

	def toggle_overview_info(self):

		"""Set the visibility of the info column in the overview based on the menu action"""

		self.overview_info = self.ui.action_show_info_in_overview.isChecked()
		if self.overview_info:
			self.ui.itemtree.setColumnCount(2)
			self.ui.itemtree.setHeaderHidden(False)
			self.ui.itemtree.resizeColumnToContents(0)
			if self.ui.itemtree.columnWidth(1) < 20:
				self.ui.itemtree.setColumnWidth(1, 20)
		else:
			self.ui.itemtree.setColumnCount(1)
			self.ui.itemtree.setHeaderHidden(True)
		if self.experiment.debug:
			print "qtopensesame.toggle_overview_info(): set to %s" % self.overview_info

	def update_dialog(self, message):

		"""
		Presents an update dialog

		Arguments:
		message -- the message to be displayed
		"""

		from libqtopensesame import update_dialog_ui
		
		a = QtGui.QDialog(self)
		a.ui = update_dialog_ui.Ui_Dialog()
		a.ui.setupUi(a)
		a.ui.checkbox_auto_check_update.setChecked(self.auto_check_update)
		a.ui.textedit_notification.setHtml(message)
		a.adjustSize()
		a.exec_()
		self.auto_check_update = a.ui.checkbox_auto_check_update.isChecked()
		self.update_preferences_tab()

	def check_update(self, dummy = None, always = True):

		"""
		Contacts www.cogsci.nl to check for the most recent version

		Keyword arguments:
		dummy -- a dummy argument passed by the signal handler
		always -- a boolean indicating if a dialog should be shown
				  regardless of the auto check update setting and the
				  outcome of the update check
		"""
		
		import urllib

		if not always and not self.auto_check_update:
			if self.experiment.debug:
				print "qtopensesame.check_update(): skipping update check"
			return

		if self.experiment.debug:
			print "qtopensesame.check_update(): opening %s" % config.get_config("version_check_url")

		try:
			fd = urllib.urlopen(config.get_config("version_check_url"))
			mrv = float(fd.read().strip())
		except Exception as e:
			if always:
				self.update_dialog("... and is sorry to say that the attempt to check for updates has failed. Please make sure that you are connected to the internet and try again later. If this problem persists, please visit <a href='http://www.cogsci.nl/opensesame'>http://www.cogsci.nl/opensesame</a> for more information.")
			return

		try:
			if len(self.version.split("-")) == 2:
				cv = float(self.version.split("-")[0]) - 0.01 + 0.00001 * int(self.version.split("-")[1][3:])
				if self.experiment.debug:
					print "qtopensesame.check_update(): you are running a pre-release version, identifying as %s" % cv
			else:
				cv = float(self.version)
		except:
			if self.experiment.debug:
				print "qtopensesame.check_update(): version is not numeric"
			return

		if mrv > float(cv):
			self.update_dialog("... and is happy to report that a new version of OpenSesame (%s) is available at <a href='http://www.cogsci.nl/opensesame'>http://www.cogsci.nl/opensesame</a>!" % mrv)
		else:
			if always:
				self.update_dialog(" ... and is happy to report that you are running the most recent version of OpenSesame.")

	def open_help_tab(self, title, item):

		"""
		Open a help tab for the specified item. Looks for a file
		called [item].html in the resources folder.

		Arguments:
		title -- the tab title
		item -- the item for which help should be displayed
		"""

		i = self.get_tab_index("__help__%s__" % item)
		if i != None:
			self.switch_tab(i)
		else:
			from libqtopensesame.help_browser import help_browser
			path = self.experiment.help("%s.html" % item)
			text = help_browser(path, item, [("[version]", self.version), ("[codename]", self.codename)])
			index = self.experiment.ui.tabwidget.addTab(text, self.experiment.icon("help"), title)
			self.switch_tab(index)

	def open_general_help_tab(self):

		"""Open the general help tab"""

		self.open_help_tab("Help: General", "general")

	def open_stdout_help_tab(self):

		"""Open the debug window help tab"""

		self.open_help_tab("Help: Debug window", "stdout")

	def open_variables_help_tab(self):

		"""Open the variable inspector help tab"""

		self.open_help_tab("Help: Variable inspector", "variables")

	def open_contribute_tab(self):

		"""Open the contribute help tab"""

		self.open_help_tab("Contribute", "contribute")

	def open_bug_tab(self):

		"""Open the submit a bug help tab"""

		self.open_help_tab("Submit a bug", "submit_a_bug")

	def about(self):

		"""Open the about help tab"""

		self.open_help_tab("About", "about")

	def open_preferences_tab(self):

		"""Open the preferences tab"""
		
		from  libqtopensesame import preferences_widget

		i = self.get_tab_index("__preferences__")
		if i != None:
			self.switch_tab(i)
		else:
			index = self.experiment.ui.tabwidget.addTab( \
				preferences_widget.preferences_widget(self), \
				self.experiment.icon("options"), "Preferences")
			self.switch_tab(index)

	def update_preferences_tab(self):

		"""If the preferences tab is open, make sure that its controls are updated to match potential changes to the preferences"""

		w = self.get_tab_widget("__preferences__")
		if w != None:
			w.set_controls()

	def get_tab_widget(self, tab_name):

		"""
		Return a specific tab

		Arguments:
		tab_name -- the tab_name of the widget

		Returns:
		The tab widget or None if the tab wasn't found
		"""

		for i in range(self.experiment.ui.tabwidget.count()):
			w = self.experiment.ui.tabwidget.widget(i)
			if hasattr(w, "tab_name") and w.tab_name == tab_name:
				return self.experiment.ui.tabwidget.widget(i)
		return None

	def get_tab_index(self, tab_name):

		"""
		Return the index of a specific tab

		Arguments:
		tab_name -- the tab_name of the widget

		Returns:
		The index of the tab or None if the tab wasn't found
		"""

		for i in range(self.experiment.ui.tabwidget.count()):
			w = self.experiment.ui.tabwidget.widget(i)
			if hasattr(w, "tab_name") and w.tab_name == tab_name:
				return i
		return None

	def switch_tab(self, index):

		"""
		Switch to a tab by index

		Arguments:
		index -- the index of the tab to switch to
		"""

		self.experiment.ui.tabwidget.setCurrentIndex(index)

	def show_text_in_toolbar(self):

		"""
		Set the toolbar style (text/ icons only) based on the menu action status
		"""

		if self.ui.action_show_text_in_toolbar.isChecked():
			style = QtCore.Qt.ToolButtonTextUnderIcon
		else:
			style = QtCore.Qt.ToolButtonIconOnly
		self.ui.toolbar_main.setToolButtonStyle(style)

	def refresh_plugins(self, dummy = None):

		"""
		Populate the menu with plug-in entries

		Keyword arguments:
		dummy -- a dummy argument passed by the signal handler
		"""

		self.populate_plugin_menu(self.ui.menu_items)

	def refresh_stdout(self, dummy = None):

		"""
		Set the visibility of the debug window (stdout) based on
		the menu action status

		Keyword arguments:
		dummy -- a dummy argument passed by the signal handler
		"""

		if not self.ui.action_show_stdout.isChecked():
			self.ui.dock_stdout.setVisible(False)
			return
		self.ui.dock_stdout.setVisible(True)

	def refresh_pool(self, make_visible = None):

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

	def refresh_variable_inspector(self, dummy = None):

		"""
		Refresh the variable inspector and sets the visibility based on the menu
		action status

		Keyword arguments:
		dummy -- a dummy argument passed by the signal handler
		"""

		if self.ui.action_show_variable_inspector.isChecked():
			self.ui.dock_variable_inspector.setVisible(True)
			self.ui.table_variables.refresh()
		else:			
			self.ui.dock_variable_inspector.setVisible(False)			

	def restart(self):

		"""Saves the experiment and restarts opensesame"""

		resp = QtGui.QMessageBox.question(self.ui.centralwidget, "Restart?", "A restart is required. Do you want to save the current experiment and restart OpenSesame?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		if resp == QtGui.QMessageBox.No:
			return

		self.save_file()

		# A horrifying hack to make sure that the proper command the restart opensesame is executed
		cmd = []

		# Under Windows, find the path to the Python intepreter and
		# prepend it
		if sys.argv[0] == "opensesame" and os.name == "nt":
			py_exe = "python.exe"
			for d in sys.path:
				py_exe = os.path.join(d, "python.exe")
				if os.path.exists(py_exe):
					break
			if self.experiment.debug:
				print "qtopensesame.restart(): located python.exe as '%s'" % py_exe
			cmd.append(py_exe)

		if sys.argv[0] == "opensesame" and os.name != "nt":
			cmd.append("python")

		cmd.append(sys.argv[0])
		cmd.append(self.current_path)
		if self.experiment.debug:
			cmd.append("--debug")

		if self.experiment.debug:
			print "qtopensesame.restart(): restarting with command '%s'" % cmd

		libopensesame.experiment.clean_up(self.experiment.debug)
		self.save_state()
		subprocess.Popen(cmd)
		QtCore.QCoreApplication.quit()

	def close(self):

		"""Cleanly close opensesame"""

		resp = QtGui.QMessageBox.question(self.ui.centralwidget, "Quit?", "Are you sure you want to quit OpenSesame?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		if resp == QtGui.QMessageBox.No:
			return
		libopensesame.experiment.clean_up(self.experiment.debug)
		self.save_unsaved_changes()
		self.save_state()
		QtCore.QCoreApplication.quit()

	def closeEvent(self, e):

		"""
		Process a closeEvent, which occurs when the window managers close button is clicked

		Arguments:
		e -- the closeEvent
		"""

		if self.experiment.debug:
			libopensesame.experiment.clean_up(self.experiment.debug)
			self.save_state()
			e.accept()
			return

		resp = QtGui.QMessageBox.question(self.ui.centralwidget, "Quit?", "Are you sure you want to quit OpenSesame?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		if resp == QtGui.QMessageBox.No:
			e.ignore()
		else:
			libopensesame.experiment.clean_up(self.experiment.debug)
			self.save_unsaved_changes()
			self.save_state()
			e.accept()

	def update_recent_files(self):

		"""Recreate the list with recent documents"""

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
			a = QtGui.QAction("(No recent files)", self.ui.menu_recent_files)
			a.setDisabled(True)
			self.ui.menu_recent_files.addAction(a)
		else:
			for path in self.recent_files:
				self.ui.menu_recent_files.addAction(recent_action(path, self, self.ui.menu_recent_files))

	def new_file(self):

		"""Discard the current experiment and start with a new file"""

		self.start_new_wizard() # Simply start the new wizard

	def open_file(self, dummy = None, path = None, add_to_recent = True):

		"""
		Open a .opensesame or .opensesame.tar.gz file

		Keyword arguments:
		dummy -- An unused argument which is passed by the signal (default = None)
		path -- The path to the file. If None, a file dialog is presented (default = None)
		"""

		self.save_unsaved_changes()

		if path == None:
			path, file_type = QtGui.QFileDialog.getOpenFileNameAndFilter(self.ui.centralwidget, "Open file", QtCore.QString(), self.file_type_filter)
		if path == None or path == "":
			return

		path = unicode(path)
		self.set_status("Opening ...")
		self.close_all_tabs()

		try:
			exp = experiment.experiment(self, "Experiment", path)
		except Exception as e:
			self.experiment.notify("<b>Error:</b> Failed to open '%s'<br /><b>Description:</b> %s<br /><br />Make sure that the file is in .opensesame or .opensesame.tar.gz format. If you should be able to open this file, but can't, please go to http://www.cogsci.nl/opensesame to find out how to recover your experiment and file a bug report." % (path, e))
			# Print the traceback in debug mode
			if self.experiment.debug:
				l = traceback.format_exc(e).split("\n")
				for r in l:
					print r
			return
		
		self.experiment = exp
		self.general_tab_widget.header_widget.item = self.experiment
		self.refresh()
		self.open_general_tab()
		self.set_status("Opened %s" % path)
		self.set_unsaved(False)

		if add_to_recent:
			self.current_path = path
			self.window_message(self.current_path)			
			self.update_recent_files()
			self.default_logfile_folder = os.path.dirname(self.current_path)
		else:
			self.window_message("New experiment")			
			self.current_path = None
			
		self.set_auto_response()

	def save_file(self, dummy=None, overwrite=True, remember=True, catch=True):

		"""
		Save the current experiment

		Keyword arguments:
		dummy -- a dummy argument passed by the signal handler (default=None)
		overwrite -- a boolean indicating whether other files should be
					 overwritten without asking (default=True)
		remember -- a boolean indicating whether the file should be included in
					the list of recent files (default=True)
		catch -- a boolean indicating whether exceptions should be caught and
				 displayed in a notification (default=True)
		"""

		if self.current_path == None:
			self.save_file_as()
			return

		self.set_busy(True)
		
		# Get ready, generate the script and see if the script can be
		# re-parsed. If not, throw an error.
		try:
			self.get_ready()
			script = self.experiment.to_string()
			experiment.experiment(self, "Experiment", script) # Re-parse
		except libopensesame.exceptions.script_error as e:
			if not catch:
				raise e
			self.experiment.notify("Could not save file, because the script could not be generated. The following error occured:<br/>%s" % e)
			self.set_busy(False)
			return

		# Try to save the experiment if it doesn't exist already
		try:
			resp = self.experiment.save(self.current_path, overwrite)
			self.set_status("Saved as %s" % self.current_path)
		except Exception as e:
			if not catch:
				raise e
			self.experiment.notify("Failed to save file. Error: %s" % e)
			self.set_busy(False)			
			return

		if resp == False:
			resp = QtGui.QMessageBox.question(self.ui.centralwidget, "File exists", \
				"A file with that name already exists. Overwite?", QtGui.QMessageBox.Yes, \
				QtGui.QMessageBox.No)
			if resp == QtGui.QMessageBox.No:
				self.window_message("Unsaved")
				self.current_path = None
				self.set_status("Not saved")
				self.set_busy(False)				
				return
			else:
				try:
					self.current_path = self.experiment.save(self.current_path, True)
					self.window_message(self.current_path)
					self.set_status("Saved as %s" % self.current_path)
				except Exception as e:
					if not catch:
						raise e
					self.experiment.notify("Failed to save file. Error: %s" % e)
					self.set_status("Not saved")
			self.set_busy(False)				
			return

		else:
			self.current_path = resp

		if remember:
			self.update_recent_files()
		self.set_unsaved(False)
		self.window_message(self.current_path)
		self.set_busy(False)

	def save_file_as(self):

		"""Save the current experiment after asking for a file name"""

		if self.current_path == None:
			path = os.path.join(self.home_folder, self.experiment.sanitize( \
				self.experiment.title, strict=True, allow_vars=False))
		else:
			path = self.current_path
		path, file_type = QtGui.QFileDialog.getSaveFileNameAndFilter(self.ui.centralwidget, \
			"Save file as ...", path, self.file_type_filter)
		if path != None and path != "":			
			path = unicode(path)
			if path[-18:].lower() != ".opensesame.tar.gz" and path[-11:].lower() != ".opensesame":
				path += ".opensesame.tar.gz"
			self.current_path = path			
			self.save_file(overwrite=False)

	def close_all_tabs(self):

		"""Close all tabs"""

		while self.ui.tabwidget.count() > 0:
			self.close_tab(0)

	def close_other_tabs(self):

		"""Close all tabs except the currently active one"""

		while self.ui.tabwidget.count() > 0 and self.ui.tabwidget.currentIndex() != 0:
			self.close_tab(0)

		while self.ui.tabwidget.count() > 1:
			self.close_tab(1)

	def close_tab(self, index):

		"""
		Close a specfic tab

		Arguments:
		index -- the index of the tab to be closed
		"""

		self.ui.tabwidget.removeTab(index)

	def close_item_tab(self, item, close_edit = True, close_script = True):

		"""
		Close all tabs that edit and/ or script tabs of a specific item

		Arguments:
		item -- the name of the item

		Keyword arguments:
		close_edit -- a boolean indicating whether the edit tab should be closed (default = True)
		close_script -- a boolean indicating whether the script tab should be close (default = True)
		"""

		if self.experiment.debug:
			print "qtopensesame.close_item_tab(): closing tabs for '%s'" % item

		# There's a kind of double loop, because the indices change
		# after a deletion
		redo = True
		while redo:
			redo = False
			for i in range(self.ui.tabwidget.count()):
					w = self.ui.tabwidget.widget(i)
					if close_edit and hasattr(w, "edit_item") and w.edit_item == item:
						self.close_tab(i)
						redo = True
						break
					if close_script and hasattr(w, "script_item") and w.script_item == item:
						self.close_tab(i)
						redo = True
						break

	def update_resolution(self, width, height):

		"""
		Updates the resolution in a way that preserves display centering. This
		is kind of a quick hack. First generate the script, change the resolution
		in the script and then re-parse the script.

		Arguments:
		width -- the display width in pixels
		height -- the display height in pixels
		"""

		if self.experiment.debug:
			print "qtopensesame.update_resolution(): changing resolution to %d x %d" % (width, height)

		try:
			script = self.experiment.to_string()
		except libopensesame.exception.script_error as error:
			self.experiment.notify("Failed to change the display resolution:" % error)
			return

		script = script.replace("\nset height \"%s\"\n" % self.experiment.get("height"), "\nset height \"%s\"\n" % height)
		script = script.replace("\nset width \"%s\"\n" % self.experiment.get("width"), "\nset width \"%s\"\n" % width)

		try:
			tmp = experiment.experiment(self, self.experiment.title, script, self.experiment.pool_folder)
		except libopensesame.exceptions.script_error as error:
			self.experiment.notify("Could not parse script: %s" % error)
			self.edit_script.edit.setText(self.experiment.to_string())
			return

		self.experiment = tmp
		self.refresh()

	def init_general_tab(self):

		"""Initializes the general tab"""
		
		from libqtopensesame import general_properties		
		self.general_tab_widget = general_properties.general_properties(self)

	def general_widget(self):

		"""Set the controls of the general tab based on the variables"""
		
		self.general_tab_widget.refresh()

	def open_general_tab(self, reopen = False, index = None, focus = True):

		"""
		Opens the general tab

		Keyword arguments:
		reopen -- a boolean indicating whether the tab should be closed and reopened if it is already open (default = False)
		index -- the position of the tab (default = None)
		focus -- a boolean indicating whether the general tab should receive focus (defaut = True)
		"""
		
		for i in range(self.experiment.ui.tabwidget.count()):
			w = self.ui.tabwidget.widget(i)
			if hasattr(w, "general_tab"):
				if reopen:
					self.ui.tabwidget.removeTab(i)
				else:
					self.ui.tabwidget.setCurrentIndex(i)

		self.general_widget()
		if index == None:
			index = self.ui.tabwidget.addTab(self.general_tab_widget, self.experiment.icon("experiment"), "General properties")
		else:
			self.ui.tabwidget.insertTab(index, self.general_tab_widget, self.experiment.icon("experiment"), "General properties")
		if focus:
			self.ui.tabwidget.setCurrentIndex(index)

	def init_unused_tab(self):

		"""Initializes the unused tab"""

		# Set the header, with the icon, label and script button
		header_hbox = QtGui.QHBoxLayout()
		header_hbox.addWidget(self.experiment.label_image("unused_large"))
		header_label = QtGui.QLabel()
		header_label.setText("<b><font size='5'>Unused</font></b>")
		header_hbox.addWidget(header_label)
		header_hbox.addStretch()
		header_widget = QtGui.QWidget()
		header_widget.setLayout(header_hbox)

		purge_button = QtGui.QPushButton(self.experiment.icon("purge"), "Permanently delete unused items")
		purge_button.setIconSize(QtCore.QSize(16, 16))
		QtCore.QObject.connect(purge_button, QtCore.SIGNAL("clicked()"), self.purge_unused)

		purge_hbox = QtGui.QHBoxLayout()
		purge_hbox.addWidget(purge_button)
		purge_hbox.addStretch()
		purge_widget = QtGui.QWidget()
		purge_widget.setLayout(purge_hbox)

		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(header_widget)
		vbox.addWidget(purge_widget)
		vbox.addStretch()

		self.unused_tab_widget = QtGui.QWidget()
		self.unused_tab_widget.setLayout(vbox)
		self.unused_tab_widget.unused_tab = True

	def open_unused_tab(self, reopen = False, index = None, focus = True):

		"""
		Shows the unused tab

		Keyword arguments:
		reopen -- indicates if the tab should be closed and reopened if it's already open (default = False)
		index -- indicates a specific position where the tab should be inserted (default = None)
		focus -- indocates whether the tab should be shown immediately (default = True)
		"""

		for i in range(self.experiment.ui.tabwidget.count()):
			w = self.ui.tabwidget.widget(i)
			if hasattr(w, "unused_tab"):
				if reopen:
					self.ui.tabwidget.removeTab(i)
				else:
					self.ui.tabwidget.setCurrentIndex(i)

		if index == None:
			index = self.ui.tabwidget.addTab(self.unused_tab_widget, self.experiment.icon("unused"), "General properties")
		else:
			self.ui.tabwidget.insertTab(index, self.unused_tab_widget, self.experiment.icon("unused"), "General properties")

		if focus:
			self.ui.tabwidget.setCurrentIndex(index)

	def purge_unused(self):

		"""Remove all unused items from the items list"""

		resp = QtGui.QMessageBox.question(self.ui.centralwidget, "Permanently delete items?", "Are you sure you want to permanently delete all unused items? This action cannot be undone.", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		if resp == QtGui.QMessageBox.No:
			return

		# We need a loop, because items may become unused
		# by deletion of their unused parent items
		while len(self.experiment.unused_items) > 0:

			for item in self.experiment.unused_items:
				if item in self.experiment.items:
					del self.experiment.items[item]

			self.refresh()

		self.close_all_tabs()
		self.open_general_tab()

	def build_item_list(self, name = None):

		"""
		Refreshes the item list

		Keyword arguments:
		name -- a name of the item that has called the build (default = None)
		"""

		if self.experiment.debug:
			print "qtopensesame.build_item_list(): %s" % name
		self.experiment.build_item_tree()

	def select_item(self, name):

		"""
		Selects an item from the itemlist and opens the corresponding edit tab

		Arguments:
		name -- the name of the item
		"""

		if self.experiment.debug:
			print "qtopensesame.select_item(): %s" % name

		if name in self.experiment.unused_items:
			self.experiment.unused_widget.setExpanded(True)
		for item in self.ui.itemtree.findItems(name, QtCore.Qt.MatchFlags(QtCore.Qt.MatchRecursive)):
			self.ui.itemtree.setCurrentItem(item)
		if name in self.experiment.items:
			self.experiment.items[name].open_edit_tab()

	def open_item(self, widget, dummy = None):

		"""
		Open a tab belonging to a widget in the item tree

		Arguments:
		widget -- a QTreeWidgetItem

		Keyword arguments:
		dummy -- an unused parameter which is passed on automatically by the signaller
		"""

		if widget.name == "__general__":
			self.open_general_tab()
		elif widget.name == "__unused__":
			self.open_unused_tab()
		else:
			self.experiment.items[widget.name].open_tab()

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
			_fname = "_" + _fname
			renamed = True

		if renamed:
			QtGui.QMessageBox.information(self.ui.centralwidget, "File renamed", "The file has been renamed to '%s', because the file pool already contains a file named '%s'." % (_fname, os.path.basename(fname)))

		shutil.copyfile(fname, os.path.join(self.experiment.pool_folder, _fname))
		self.refresh_pool(True)

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
						redo = True
						break

	def call_opensesamerun(self, exp):

		"""
		Runs an experiment using opensesamerun

		Arguments:
		exp -- an instance of libopensesame.experiment.experiment
		"""
		
		import tempfile

		# Temporary file for the standard output and experiment
		stdout = tempfile.mktemp(suffix = ".stdout")
		path = tempfile.mktemp(suffix = ".opensesame.tar.gz")
		exp.save(path, True)
		if self.experiment.debug:
			print "qtopensesame.call_opensesamrun(): experiment saved as '%s'" % path

		# Determine the name of the executable
		if self.opensesamerun_exec == "":
			if os.name == "nt":
				cmd = ["opensesamerun.exe"]
			else:
				cmd = ["opensesamerun"]
		else:
			cmd = self.opensesamerun_exec.split()

		cmd += [path, "--logfile=%s" % exp.logfile, "--subject=%s" % exp.subject_nr]

		if self.experiment.debug:
			cmd.append("--debug")
		if exp.fullscreen:
			cmd.append("--fullscreen")
		if "--pylink" in sys.argv:
			cmd.append("--pylink")

		if self.experiment.debug:
			print "qtopensesame.call_opensesamrun(): spawning opensesamerun as a separate process"

		# Call opensesamerun and wait for the process to complete
		try:
			p = subprocess.Popen(cmd, stdout = open(stdout, "w"))
		except:
			self.experiment.notify("<b>Failed to start opensesamerun</b><br />Please make sure that opensesamerun (or opensesamerun.exe) is present in the path, manually specify the run command, or deselect the 'Run as separate process' option.<br><pre>%s</pre>" % (" ".join(cmd)))
			try:
				os.remove(path)
				os.remove(stdout)
			except:
				pass
			return False

		# Wait for OpenSesame run to complete, process events in the meantime, to make
		# sure that the new process is shown (otherwise it will crash on Windows).
		retcode = None
		while retcode == None:
			retcode = p.poll()
			QtGui.QApplication.processEvents()
			time.sleep(1)

		if self.experiment.debug:
			print "qtopensesame.call_opensesamrun(): opensesamerun returned %d" % retcode

		print
		print open(stdout, "r").read()
		print

		# Clean up the temporary file
		try:
			os.remove(path)
			os.remove(stdout)
		except:
			pass

		return True

	def experiment_finished(self, exp):

		"""
		Presents a dialog informing the user that the experiment is finished and
		ask if the logfile should be copied to the file pool

		Arguments:
		exp -- an instance of libopensesame.experiment.experiment
		"""

		# Report success and copy the logfile to the filepool if necessary
		resp = QtGui.QMessageBox.question(self.ui.centralwidget, "Finished!", "The experiment is finished and data has been logged to '%s'. Do you want to copy the logfile to the file pool?" % exp.logfile, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		if resp == QtGui.QMessageBox.Yes:
			self.copy_to_pool(exp.logfile)

	def run_experiment(self, dummy = None, fullscreen = True):

		"""
		Runs the current experiment

		Keyword arguments:
		dummy -- a dummy argument that is passed by signaler (default = None)
		fullscreen -- a boolean to indicate if the window should be fullscreen (default = True)
		"""
		
		import openexp.exceptions
		from libqtopensesame import pyterm				

		# Before we run the experiment, we parse it in three steps
		# 1) Apply any pending changes
		# 2) Convert the experiment to a string
		# 3) Parse the string into a new experiment (with all the GUI stuff stripped off)
		try:
			self.get_ready()
			script = self.experiment.to_string()
			exp = libopensesame.experiment.experiment("Experiment", script, self.experiment.pool_folder)
			exp.experiment_path = self.experiment.experiment_path
		except libopensesame.exceptions.script_error as e:
			self.experiment.notify(str(e))
			return

		if self.experiment.debug:

			exp.set("subject_nr", 999)
			exp.set("subject_parity", "odd")
			logfile = os.path.join(str(self.default_logfile_folder), "debug.csv")

		else:

			# Get the participant number
			subject_nr, ok = QtGui.QInputDialog.getInt(self.ui.centralwidget, "Subject number", "Please enter the subject number", min = 0)
			if not ok:
				return

			# Set the subject nr and parity
			exp.set_subject(subject_nr)

			# Suggested filename
			suggested_path = os.path.join(str(self.default_logfile_folder), "subject-%d.csv" % subject_nr)

			# Get the data file
			csv_filter = "Comma-separated values (*.csv)"
			logfile = str(QtGui.QFileDialog.getSaveFileName(self.ui.centralwidget, "Choose location for logfile (press 'escape' for default location)", suggested_path, filter = csv_filter, selectedFilter = csv_filter))
			if logfile == "":
				try:
					# Sometimes this fails, e.g. if the default folder is "/"
					logfile = os.path.join(self.default_logfile_folder, "defaultlog.csv")
				except:
					logfile = os.path.join(self.home_folder, "defaultlog.csv")
			else:
				if os.path.splitext(logfile)[1].lower() not in (".csv", ".txt", ".dat", ".log"):
					logfile += ".csv"

		# Check if the logfile is writable
		try:
			open(logfile, "w")
		except:
			self.experiment.notify("The logfile '%s' is not writable. Please choose another location for the logfile." % logfile)
			return

		# Remember the location of the logfile
		self.default_logfile_folder = os.path.split(logfile)[0]

		# Set fullscreen/ window mode
		exp.fullscreen = fullscreen
		exp.logfile = logfile

		# Suspend autosave
		if self.autosave_timer != None:
			if self.experiment.debug:
				print "qtopensesame.run_experiment(): stopping autosave timer"
			self.autosave_timer.stop()

		exp.auto_response = self.experiment.auto_response

		# Reroute the standard output to the debug window
		buf = pyterm.output_buffer(self.ui.edit_stdout)
		sys.stdout = buf

		if self.opensesamerun:
			# Optionally, the experiment is run as a separate process
			if self.call_opensesamerun(exp):
				self.experiment_finished(exp)

		else:
			try:
				exp.run()
				self.experiment_finished(exp)

			except Exception as e:

				# Make sure that the experiment cleans up, even though it crashed
				try:
					exp.end()
				except Exception as _e:
					if self.experiment.debug:
						print "qtopensesame.run_experiment(): experiment.end() caused an exception: %s" % _e

				# Report the error
				if isinstance(e, libopensesame.exceptions.runtime_error):
					self.experiment.notify(str(e))
				elif isinstance(e, openexp.exceptions.openexp_error):
					print str(e)
					self.experiment.notify("<b>Error</b>: OpenExp error<br /><b>Description</b>: %s" % e)
				else:
					self.experiment.notify("An unexpected error occurred, which was not caught by OpenSesame. This should not happen! Message:<br/><b>%s</b>" % e)
					for s in traceback.format_exc(e).split("\n"):
						print s

		# Undo the standard output rerouting
		sys.stdout = sys.__stdout__
		self.ui.edit_stdout.show_prompt()

		# Resume autosave, but not if opensesamerun is called
		if self.autosave_timer != None:
			if self.experiment.debug:
				print "qtopensesame.run_experiment(): resuming autosave timer"
			self.autosave_timer.start()

		# Restart the experiment if necessary
		if exp.restart:
			self.restart()

	def run_experiment_in_window(self):

		"""Runs the experiment in a window"""

		self.run_experiment(fullscreen = False)

	def refresh(self, changed_item=None, refresh_edit=True, refresh_script=True):

		"""
		Refreshes all parts of the interface that may have changed because of a
		changed item

		Keyword arguments:
		changed_item -- the name of a specific item that should be refreshed
						(default = None)
		refresh_edit -- a boolean to indicate if the edit tabs should be
						refreshed (default = True)
		refresh_script -- a boolean to indicate if the script tabs should be
						  refreshed (default = True)
		"""

		# Make sure the refresh does not get caught in
		# a recursive loop
		if self.lock_refresh:
			return
		self.lock_refresh = True

		self.set_busy(True)
		if self.experiment.debug:
			print "qtopensesame.refresh(): %s" % changed_item

		self.general_tab_widget.set_header_label()

		index = self.ui.tabwidget.currentIndex()
		for i in range(self.ui.tabwidget.count()):
				w = self.ui.tabwidget.widget(i)
				if hasattr(w, "general_tab"):
					self.general_widget()
				# For now the unused tab doesn't need to be refreshed
				if hasattr(w, "unused_tab"):
					pass
				if refresh_edit and hasattr(w, "edit_item") and (changed_item == None or w.edit_item == changed_item):
					if w.edit_item in self.experiment.items:
						self.experiment.items[w.edit_item].edit_widget()
				if refresh_script and hasattr(w, "script_item") and (changed_item == None or w.script_item == changed_item):
					if w.script_item in self.experiment.items:
						self.experiment.items[w.script_item].script_widget()

		self.ui.tabwidget.setCurrentIndex(index)
		self.build_item_list()
		self.refresh_variable_inspector()
		self.refresh_pool()
		self.set_unsaved()
		self.lock_refresh = False
		self.set_busy(False)		

	def hard_refresh(self, changed_item):

		"""
		Closes and reopens the tabs for a changed item. This is different
		from the normal refresh in the sense that here the tabs are
		reinitialized from scratch which is necessary if a new instance of the
		item has been created.

		Arguments:
		changed_item -- the name of the changed item
		"""		

		# Make sure the refresh does not get caught in
		# a recursive loop
		if self.lock_refresh:
			return
		self.lock_refresh = True
		
		self.set_busy(True)
		if self.experiment.debug:
			print "qtopensesame.hard_refresh(): %s" % changed_item

		self.general_tab_widget.set_header_label()

		index = self.ui.tabwidget.currentIndex()

		for i in range(self.ui.tabwidget.count()):

				w = self.ui.tabwidget.widget(i)

				if hasattr(w, "edit_item") and (changed_item == None or w.edit_item == changed_item) and w.edit_item in self.experiment.items:
					if self.experiment.debug:
						print "qtopensesame.hard_refresh(): reopening edit tab %s" % changed_item
					self.ui.tabwidget.removeTab(i)
					self.experiment.items[w.edit_item].open_edit_tab(i, False)
					w = self.ui.tabwidget.widget(i)
					w.edit_item = changed_item

				if hasattr(w, "script_item") and (changed_item == None or w.script_item == changed_item) and w.script_item in self.experiment.items:
					if self.experiment.debug:
						print "qtopensesame.hard_refresh(): reopening script tab %s" % changed_item
					self.ui.tabwidget.removeTab(i)
					self.experiment.items[w.script_item].open_script_tab(i, False)
					w = self.ui.tabwidget.widget(i)
					w.script_item = changed_item

		self.ui.tabwidget.setCurrentIndex(index)

		self.lock_refresh = False
		self.set_busy(False)		

	def populate_plugin_menu(self, menu):

		"""
		Adds a list of plugins to a menu

		Arguments:
		menu -- a QMenu instance
		"""

		cat_menu = {}
		for plugin in libopensesame.plugins.list_plugins():
			if self.experiment.debug:
				print "qtopensesame.refresh_plugins(): found plugin '%s'" % plugin
			cat = libopensesame.plugins.plugin_category(plugin)
			if cat not in cat_menu:
				cat_menu[cat] = QtGui.QMenu(cat)
				cat_menu[cat] = menu.addMenu(self.experiment.icon("plugins_large"), cat)
			cat_menu[cat].addAction(plugin_action(self, cat_menu[cat], plugin))

	def add_item(self, item_type, refresh=True, name=None):

		"""
		Adds a new item to the item list

		Arguments:
		item_type -- the type of the item to add

		Keyword arguments:
		refresh -- a bool to indicate if the interface should be refreshed
				   (default=True)
		name -- a custom name to give the item (default=None)

		Returns:
		The name of the new item
		"""

		# Get a unique name if none has been specified
		name = self.experiment.unique_name("%s" % item_type)
			
		if self.experiment.debug:
			print "qtopensesame.add_item(): adding %s (%s)" % (name, item_type)

		# If the item type is a plugin, we need to use the plugin mechanism
		if libopensesame.plugins.is_plugin(item_type):

			# In debug mode, exceptions are not caught
			if self.experiment.debug:
				item = libopensesame.plugins.load_plugin(item_type, name, self.experiment, None, self.experiment.item_prefix())
			else:
				try:
					item = libopensesame.plugins.load_plugin(item_type, name, self.experiment, None, self.experiment.item_prefix())
				except Exception as e:
					self.experiment.notify("Failed to load plugin '%s'. Error: %s" % (item_type, e))
					return

		else:
			# Load a core item
			exec("from libqtopensesame import %s" % item_type)
			name = self.experiment.unique_name("%s" % item_type)
			item = eval("%s.%s(name, self.experiment)" % (item_type, item_type))

		# Optionally, ask for a new name right away
		if self.immediate_rename:
			name, ok = QtGui.QInputDialog.getText(self, "New name", "Please enter a name for the new %s" % item_type, text = name)
			if not ok:
				return None
			name = str(name)
			item.name = name

		# Add the item to the item list
		self.experiment.items[name] = item

		# Optionally, refresh the interface
		if refresh:
			self.refresh()
			self.select_item(name)

		return name

	def add_loop(self, refresh = True, parent = None):

		"""
		Add a loop item and ask for an item to fill the loop with

		Keyword arguments:
		refresh -- a bool to indicate if the interface should be refreshed (default = True)
		parent -- the parent item for the new loop (default = None)

		Returns:
		The name of the new loop
		"""

		from libqtopensesame import new_loop_sequence_dialog
		
		d = new_loop_sequence_dialog.new_loop_sequence_dialog(self, self.experiment, "loop", parent)
		d.exec_()
		if d.action == "cancel":
			return None
		loop = self.add_item("loop", False)
		if d.action == "new":
			item_name = self.add_item(d.item_type, False)
			self.experiment.items[loop].set("item", item_name)
		else:
			self.experiment.items[loop].set("item", d.item_name)
		if refresh:
			self.refresh()
			self.select_item(loop)
		return loop

	def add_sequence(self, refresh = True, parent = None):

		"""
		Add a sequence item and ask for an item to fill the loop with

		Keyword arguments:
		refresh -- a bool to indicate if the interface should be refreshed (default = True)
		parent -- the parent item for the new sequence (default = None)

		Returns:
		The name of the new sequence
		"""
		
		from libqtopensesame import new_loop_sequence_dialog

		d = new_loop_sequence_dialog.new_loop_sequence_dialog(self, self.experiment, "sequence", parent)
		d.exec_()
		if d.action == "cancel":
			return None
		seq = self.add_item("sequence", False)
		if d.action == "new":
			item_name = self.add_item(d.item_type, False)
			self.experiment.items[seq].items.append((item_name, "always"))
		else:
			self.experiment.items[seq].items.append((d.item_name, "always"))
		if refresh:
			self.refresh()
			self.select_item(seq)

		return seq

	def add_sketchpad(self, refresh = True, parent = None):

		"""
		Add a sketchpad item and ask for an item to fill the loop with

		Keyword arguments:
		refresh -- a bool to indicate if the interface should be refreshed (default = True)
		parent -- the parent item for the new item (default = None)

		Returns:

		The name of the new item
		"""

		return self.add_item("sketchpad", refresh)

	def add_feedback(self, refresh = True, parent = None):

		"""
		Add a feedback item and ask for an item to fill the loop with

		Keyword arguments:
		refresh -- a bool to indicate if the interface should be refreshed (default = True)
		parent -- the parent item for the new item (default = None)

		Returns:
		The name of the new item
		"""
		return self.add_item("feedback", refresh)

	def add_sampler(self, refresh = True, parent = None):

		"""
		Add a sampler item and ask for an item to fill the loop with

		Keyword arguments:
		refresh -- a bool to indicate if the interface should be refreshed (default = True)
		parent -- the parent item for the new item (default = None)

		Returns:
		The name of the new item
		"""

		return self.add_item("sampler", refresh)

	def add_synth(self, refresh = True, parent = None):

		"""
		Add a synth item and ask for an item to fill the loop with

		Keyword arguments:
		refresh -- a bool to indicate if the interface should be refreshed (default = True)
		parent -- the parent item for the new item (default = None)

		Returns:
		The name of the new item
		"""

		return self.add_item("synth", refresh)

	def add_keyboard_response(self, refresh = True, parent = None):

		"""
		Add a keyboard_response item and ask for an item to fill the loop with

		Keyword arguments:
		refresh -- a bool to indicate if the interface should be refreshed (default = True)
		parent -- the parent item for the new item (default = None)

		Returns:
		The name of the new item
		"""

		return self.add_item("keyboard_response", refresh)

	def add_mouse_response(self, refresh = True, parent = None):

		"""
		Add a mouse_response item and ask for an item to fill the loop with

		Keyword arguments:
		refresh -- a bool to indicate if the interface should be refreshed (default = True)
		parent -- the parent item for the new item (default = None)

		Returns:
		The name of the new item
		"""

		return self.add_item("mouse_response", refresh)

	def add_logger(self, refresh = True, parent = None):

		"""
		Add a logger item and ask for an item to fill the loop with

		Keyword arguments:
		refresh -- a bool to indicate if the interface should be refreshed (default = True)
		parent -- the parent item for the new item (default = None)

		Returns:
		The name of the new item
		"""

		return self.add_item("logger", refresh)

	def add_inline_script(self, refresh = True, parent = None):

		"""
		Add an inline_script item and ask for an item to fill the loop with

		Keyword arguments:
		refresh -- a bool to indicate if the interface should be refreshed (default = True)
		parent -- the parent item for the new item (default = None)

		Returns:
		The name of the new item
		"""

		return self.add_item("inline_script", refresh)
		
	def drop_item(self, add_func):

		"""
		Create a new item after an item has been dragged and dropped from the
		toolbar. The necessary information is stored in the itemtree.

		Arguments:
		add_func -- a function to call to create the new item
		"""
		
		from libqtopensesame import draggables
		
		if self.experiment.debug:
			print "qtopensesame.drop_item(): dropping from toolbar"		
		
		# Determine the drop target
		target, index, select = draggables.drop_target

		# Create a new item and return if it fails
		if type(add_func) != str:
			new_item = add_func(False, parent = target)
		else:
			new_item = self.add_item(add_func, False)
		if new_item == None:
			self.refresh(target)
			return
			
		if target == "__start__":
			self.experiment.start = new_item
		else:
			self.experiment.items[target].items.insert(index, (new_item, "always"))		
			
		self.refresh(target)
		if select:
			self.select_item(new_item)					

	def drag_item(self, add_func):

		"""
		Drag an item from the item toolbar

		Arguments:
		add_func -- a function to create a new item, if the item is dropped
		"""
		
		from libqtopensesame import draggables
		
		if self.experiment.debug:
			print "qtopensesame.drag_item(): dragging"

		# Reset the drop target
		draggables.drop_target = None

		# Start the drop action
		d = QtGui.QDrag(self.ui.centralwidget)
		m = QtCore.QMimeData()
		m.setText("__osnew__ %s" % add_func)
		d.setMimeData(m)

		# Check if the drop was successful
		if d.start(QtCore.Qt.CopyAction) == QtCore.Qt.CopyAction:
			self.drop_item(add_func)
		else:
			# Create a new item
			if type(add_func) != str:
				new_item = add_func(False)
			else:
				new_item = self.add_item(add_func, False)

			if new_item != None:

				if self.experiment.debug:
					print "qtopensesame.drag_item(): adding to unused"

				self.refresh()
				self.select_item(new_item)

	def drag_loop(self):

		"""Drag a new loop"""

		self.drag_item(self.add_loop)

	def drag_sequence(self):

		"""Drag a new sequence"""

		self.drag_item(self.add_sequence)

	def drag_sketchpad(self):

		"""Drag a new sketchpad"""

		self.drag_item(self.add_sketchpad)

	def drag_feedback(self):

		"""Drag a new feedback"""

		self.drag_item(self.add_feedback)

	def drag_sampler(self):

		"""Drag a new sampler"""

		self.drag_item(self.add_sampler)

	def drag_synth(self):

		"""Drag a new synth"""

		self.drag_item(self.add_synth)

	def drag_keyboard_response(self):

		"""Drag a new keyboard_response"""

		self.drag_item(self.add_keyboard_response)

	def drag_mouse_response(self):

		"""Drag a new mouse_response"""

		self.drag_item(self.add_mouse_response)

	def drag_logger(self):

		"""Drag a new logger"""

		self.drag_item(self.add_logger)

	def drag_inline_script(self):

		"""Drag a new inline_script"""

		self.drag_item(self.add_inline_script)

