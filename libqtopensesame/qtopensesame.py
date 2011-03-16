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
from libqtopensesame import includes,\
	opensesame_ui,\
	update_dialog_ui,\
	tip_dialog,\
	general_widget_ui,\
	pool_widget,\
	qtitem,\
	experiment,\
	new_loop_sequence_dialog
	
import serial
import libopensesame.exceptions
import libopensesame.experiment
import libopensesame.plugins
import libopensesame.misc
import os.path
import os
import sys
import imp
import shutil
import urllib
import tempfile
import subprocess
import random
import time
import libqtopensesame.inline_editor
import libqtopensesame.syntax_highlighter
import openexp.exceptions
import traceback
import optparse

class general_header_widget(qtitem.header_widget):

	"""
	Provides the clickable title and description for
	the experiment
	"""

	def __init__(self, item):
	
		"""
		Constructor
		"""
	
		qtitem.header_widget.__init__(self, item)
		self.label_name.setText("<font size='5'><b>%s</b> - Experiment</font>&nbsp;&nbsp;&nbsp;<font color='gray'><i>Click to edit</i></font>" % self.item.get("title"))		

	def restore_name(self):
	
		"""
		Apply the name change and revert the edit
		back to the label
		"""
	
		self.item.main_window.apply_general_changes()
	
		self.label_name.setText("<font size='5'><b>%s</b> - Experiment</font>&nbsp;&nbsp;&nbsp;<font color='gray'><i>Click to edit</i></font>" % self.item.get("title"))
		self.label_name.show()
		self.edit_name.setText(self.item.get("title"))
		self.edit_name.hide()
				
	def restore_desc(self):			
	
		"""
		Apply the description change and revert the edit
		back to the label
		"""	
		
		self.item.main_window.apply_general_changes()		

		self.label_desc.setText(self.item.get("description"))	
		self.label_desc.show()
		self.edit_desc.setText(self.item.get("description"))		
		self.edit_desc.hide()	

class output_buffer:

	"""
	The output buffer is used to capture the standard
	output and reroute it to the debug window
	"""

	def __init__(self, plaintext):
	
		"""
		Constructor
		"""
	
		self.plaintext = plaintext
		
	def write(self, s):
	
		"""
		Reroute to the debug window
		"""
	
		if s.strip() != "":
			self.plaintext.appendPlainText(s.strip())
			QtGui.QApplication.processEvents()
			
class plugin_action(QtGui.QAction):

	"""
	Menu entry for plugin
	"""

	def __init__(self, main_window, menu, plugin):
	
		"""
		Constructor
		"""
	
		self.main_window = main_window
		icon = QtGui.QIcon(libopensesame.plugins.plugin_icon_large(plugin))
		self.plugin = plugin
		QtGui.QAction.__init__(self, icon, "Add %s" % plugin, menu)
		
		self.triggered.connect(self.add_plugin)
		
	def add_plugin(self, dummy = None):
	
		"""
		When menu item is selected, add the plugin
		to the experiment
		"""
	
		self.main_window.drag_item(self.plugin)			
								
class qtopensesame(QtGui.QMainWindow):

	"""
	The main class of the OpenSesame GUI.
	"""
	
	def __init__(self, parent = None):
		
		"""
		Constructor
		"""
			
		# Construct the parent
		QtGui.QMainWindow.__init__(self, parent)
														
		# Setup the UI
		self.ui = opensesame_ui.Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.toolbar_items.main_window = self
		self.ui.itemtree.main_window = self
						
		# Set some initial variables
		self.current_path = None
		self.version = libopensesame.misc.version
		self.codename = libopensesame.misc.codename
		self.lock_refresh = False
		self.auto_check_update = True
		self.show_startup_tip = True
		self.default_logfile_folder = ""
		self.unsaved_changes = False
				
		# Determine the users home folder
		if os.name == "nt":
			self.home_folder = os.environ["USERPROFILE"]
		else:
			self.home_folder = os.environ["HOME"]

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
		self.ui.action_opensesamerun_exec.triggered.connect(self.set_opensesamerun_exec)
		
		self.ui.action_close_all_tabs.triggered.connect(self.close_all_tabs)
		self.ui.action_close_other_tabs.triggered.connect(self.close_other_tabs)		
		self.ui.action_show_text_in_toolbar.triggered.connect(self.show_text_in_toolbar)
		self.ui.action_show_variable_inspector.triggered.connect(self.refresh_variable_inspector)
		self.ui.action_show_pool.triggered.connect(self.refresh_pool)
		self.ui.action_show_stdout.triggered.connect(self.refresh_stdout)
							
		self.ui.action_help.triggered.connect(self.open_general_help_tab)
		self.ui.action_about.triggered.connect(self.about)
		self.ui.action_contribute.triggered.connect(self.open_contribute_tab)
		self.ui.action_submit_a_bug.triggered.connect(self.open_bug_tab)		
		
		self.ui.action_check_for_update.triggered.connect(self.check_update)
		self.ui.action_set_autosave_interval.triggered.connect(self.set_autosave_interval)
		self.ui.action_open_autosave_folder.triggered.connect(self.open_autosave_folder)
		self.ui.action_immediate_rename.triggered.connect(self.set_immediate_rename)
		
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
		self.ui.action_add_plugin.triggered.connect(self.choose_and_add_plugin)				
		
		self.ui.action_auto_check_update.triggered.connect(self.set_auto_check_update)
		self.ui.action_show_random_tip.triggered.connect(self.show_random_tip)
				
		# Setup the variable inspector
		self.ui.button_help_variables.clicked.connect(self.open_variables_help_tab)		
		self.ui.dock_variable_inspector.visibilityChanged.connect(self.ui.action_show_variable_inspector.setChecked)
		self.ui.edit_variable_filter.textChanged.connect(self.refresh_variable_inspector)

		# Setup the file pool
		self.ui.dock_pool.visibilityChanged.connect(self.ui.action_show_pool.setChecked)
		self.ui.pool_widget = pool_widget.pool_widget(self)
		self.ui.dock_pool.setWidget(self.ui.pool_widget)	
				
		# Setup the debug window
		if os.name == "posix":
			font = QtGui.QFont("mono")
		else:
			font = QtGui.QFont("courier")		
		self.ui.dock_stdout.visibilityChanged.connect(self.ui.action_show_stdout.setChecked)		
		self.ui.button_help_stdout.clicked.connect(self.open_stdout_help_tab)
		self.ui.edit_stdout.setFont(font)
		self.ui.edit_python_command.setFont(font)
		self.ui.edit_python_command.returnPressed.connect(self.execute_interpreter)
		self.ui.button_python_execute.clicked.connect(self.execute_interpreter)		        			

		# Create the initial experiment
		self.experiment = experiment.experiment(self, "New experiment")
		self.experiment.from_string(open(self.experiment.resource("default.opensesame"), "r").read())

		# Initialize the tabs
		self.init_general_tab()
		self.init_unused_tab()
		
		# After starting OpenSesame, the general tab is visible
		self.open_general_tab()
				
		# Refresh all aspects of the GUI
		self.refresh_plugins()
		self.refresh_variable_inspector()
		self.refresh_pool()
		self.refresh_stdout()
		self.refresh()

		# Build the items toolbar		
		self.ui.toolbar_items.build()
					
		self.ui.edit_stdout.setPlainText("You can print to this debug window using the Python 'print [msg]' statement in inline_script items or the interpreter field above.\n")						
		self.set_status("Welcome to OpenSesame %s" % self.version)			
		self.restore_state()		
		self.set_unsaved(False)				
		self.start_autosave_timer()	
				
		# Parse the command line options			
		parser = optparse.OptionParser("usage: opensesame [experiment] [options]", version = "%s '%s'" % (self.version, self.codename))

		parser.set_defaults(debug = False)
		parser.set_defaults(run = False)
		parser.set_defaults(run_in_window = False)
		
		group = optparse.OptionGroup(parser, "Immediately run an experiment")
		group.add_option("-r", "--run", action = "store_true", dest = "run", help = "Run fullscreen")
		group.add_option("-w", "--run-in-window", action = "store_true", dest = "run_in_window", help = "Run in window")		
		parser.add_option_group(group)		
		
		group = optparse.OptionGroup(parser, "Miscellaneous options")
		group.add_option("-d", "--debug", action = "store_true", dest = "debug", help = "Print lots of debugging messages to the standard output")
		parser.add_option_group(group)		
		
		group = optparse.OptionGroup(parser, "Miscellaneous options")
		group.add_option("--pylink", action = "store_true", dest = "pylink", help = "Load PyLink before PyGame (necessary for using the Eyelink plug-ins in non-dummy mode)")				
		parser.add_option_group(group)

		self.options, args = parser.parse_args(sys.argv)
		
		if self.options.run and self.options.run_in_window:
			parser.error("Options -r / --run and -w / --run-in-window are mutually exclusive.")
		
	def restore_state(self):
	
		"""
		Saves the state of the current window
		"""

		if self.experiment.debug:
			print "qtopensesame.restore_state()"

		settings = QtCore.QSettings("cogscinl", "opensesame")		
		settings.beginGroup("MainWindow");
		self.resize(settings.value("size", QtCore.QSize(1000, 600)).toSize())
		self.move(settings.value("pos", QtCore.QPoint(200, 200)).toPoint())
		self.restoreState(settings.value("state").toByteArray())				
		self.auto_check_update = settings.value("auto_check_update", True).toBool()		
		self.show_startup_tip = settings.value("show_startup_tip", True).toBool()		
		self.default_logfile_folder = settings.value("default_logfile_folder", self.home_folder).toString()
		self.autosave_interval = settings.value("autosave_interval", 10 * 60 * 1000).toInt()[0] # Every 10 minutes
		self.immediate_rename = settings.value("immediate_rename", False).toBool()
		self.opensesamerun_exec = str(settings.value("opensesamerun_exec", "").toString())
		self.ui.action_opensesamerun.setChecked(settings.value("opensesamerun", False).toBool())
		
		self.ui.action_auto_check_update.setChecked(self.auto_check_update)
		self.ui.action_opensesamerun_exec.setEnabled(self.ui.action_opensesamerun.isChecked())
		
		settings.endGroup();
		
	def save_state(self):
	
		"""
		Restores the state of the current window
		"""	
	
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
		settings.setValue("immediate_rename", self.immediate_rename)
		settings.setValue("opensesamerun", self.ui.action_opensesamerun.isChecked())
		settings.setValue("opensesamerun_exec", self.opensesamerun_exec)
		settings.endGroup()
		
	def set_opensesamerun_exec(self):
	
		"""
		A dialog for setting the command for opensesamerun
		"""
		
		s, ok = QtGui.QInputDialog.getText(self.ui.centralwidget, "Set run command", "Enter a command to execute for running the experiment as an external process (e.g., 'c:\\Python26\\python.exe opensesamerun' or 'opensesamerun.exe').\nLeave this field blank to let OpenSesame autodetect the opensesamerun command.", text = self.opensesamerun_exec)
		if not ok:
			return

		try:
			self.opensesamerun_exec = str(s)	
		except:
			self.experiment.notify("You entered an invalid string")
			self.opensesamerun = ""
									
	def set_autosave_interval(self):
	
		"""
		A dialog for setting the autosave interval
		"""
		
		i, ok = QtGui.QInputDialog.getInt(self.ui.centralwidget, "Set auto-save interval", "How often (in minutes) do you want OpenSesame to make a backup of your experiment? Enter '0' to turn off auto-save.", self.autosave_interval / (60 * 1000), min = 0)
		if not ok:
			return
			
		# Cancel the old timer if necessary
		if self.autosave_timer != None:
			if self.experiment.debug:
				print "qtopensesame.set_autosave_interval(): cancelling auto-save timer"
			self.autosave_timer.stop()
			self.autosave_timer = None
	
		# Convert the interval to milliseconds
		self.autosave_interval = i * 60 * 1000
			
		# Start the timer
		self.start_autosave_timer()
			
	def open_autosave_folder(self):
	
		"""
		Open the autosave folder in a platform specific way
		"""
		
		if os.name == "nt":
			os.startfile(self.autosave_folder)
		elif os.name == "posix":
			pid = subprocess.Popen(["xdg-open", self.autosave_folder]).pid		
			
	def start_autosave_timer(self):
	
		"""
		Construct the autosave timer, if autosave is enabled
		"""			
		
		# Start auto save timer
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
	
		"""
		Automatically save the experiment
		"""
		
		if not self.unsaved_changes:
			self.set_status("No unsaved changes, skipping backup")
		else:
			
			_current_path = self.current_path
			_unsaved_changes = self.unsaved_changes	
			_window_msg = self.window_msg
		
			self.current_path = os.path.join(self.autosave_folder, "%s.opensesame.tar.gz" % str(time.ctime()).replace(":", "_"))

			if self.experiment.debug:
				print "qtopensesame.autosave(): saving backup as %s" % self.current_path
					
			try:
				self.save_file(False)
				self.set_status("Backup saved as %s" % self.current_path)					
			except:
				self.set_status("Failed to save backup")
		
			autosave_path = self.current_path		
			self.current_path = _current_path
			self.set_unsaved(_unsaved_changes)
			self.window_message(_window_msg)
			
		self.start_autosave_timer()		
		return autosave_path
		
	def save_unsaved_changes(self):
	
		"""
		Ask if unsaved changes should be saved
		"""		
		
		if not self.unsaved_changes:
			return
			
		resp = QtGui.QMessageBox.question(self.ui.centralwidget, "Save changes?", "Your experiment contains unsaved changes. Do you want to save your experiment?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		if resp == QtGui.QMessageBox.Yes:
			self.save_file()
						
	def set_unsaved(self, unsaved_changes = True):
	
		"""
		Remember if there are unsaved changes
		"""
		
		self.unsaved_changes = unsaved_changes
		self.window_message()
		
	def set_status(self, msg, timeout = 5000):
	
		"""
		Put a message on the statusbar
		"""
		
		self.ui.statusbar.showMessage(msg, timeout)			
											
	def window_message(self, msg = None):
	
		"""
		Displays a message in the window title
		"""	
		
		if msg != None:
			self.window_msg = msg		
		
		if self.unsaved_changes:
			self.setWindowTitle("%s [unsaved]" % self.window_msg)
		else:
			self.setWindowTitle("%s" % self.window_msg)
		
	def show_random_tip(self, dummy = None, always = True):
	
		"""
		Show a random tip
		"""
		
		if always or self.show_startup_tip:
			d = tip_dialog.tip_dialog(self)
			d.exec_()
		elif self.experiment.debug:
			print "qtopensesame.show_random_tip(): skipping random tip"
			
	def set_immediate_rename(self):
	
		"""
		Set the immediate_rename based on the menu
		"""
		
		self.immediate_rename = self.ui.action_immediate_rename.isChecked()
		if self.experiment.debug:
			print "qtopensesame.set_immediate_rename(): set to %s" % self.immediate_rename
		
	def update_dialog(self, message):
	
		"""
		Presents a notification dialog
		"""
		
		a = QtGui.QDialog(self)	
		a.ui = update_dialog_ui.Ui_Dialog()
		a.ui.setupUi(a)	
		a.ui.checkbox_auto_check_update.setChecked(self.auto_check_update)		
		a.ui.textedit_notification.setHtml(message)
		a.adjustSize()
		a.exec_()		
		self.auto_check_update = a.ui.checkbox_auto_check_update.isChecked()
		self.ui.action_auto_check_update.setChecked(self.auto_check_update)
		
	def set_auto_check_update(self):
	
		"""
		Set the autocheck update based on the menu
		"""
		
		self.auto_check_update = self.ui.action_auto_check_update.isChecked()
		if self.experiment.debug:
			print "qtopensesame.set_auto_check_update(): set to %s" % self.auto_check_update
		
	def check_update(self, dummy = None, always = True):
	
		"""
		Contacts www.cogsci.nl to check for the
		most recent version
		"""					
		
		if not always and not self.auto_check_update:
			if self.experiment.debug:
				print "qtopensesame.check_update(): skipping update check"				
			return			
		
		if self.experiment.debug:
			print "qtopensesame.check_update(): opening http://files.cogsci.nl/software/opensesame/MOST_RECENT_VERSION.TXT"		
	
		try:
			fd = urllib.urlopen("http://files.cogsci.nl/software/opensesame/MOST_RECENT_VERSION.TXT")
			mrv = float(fd.read().strip())
		except Exception as e:
			if always:
				self.update_dialog("... and is sorry to say that the attempt to check for updates has failed. Please make sure that you are connected to the internet and try again later. If this problem persists, please visit <a href='http://www.cogsci.nl/opensesame'>http://www.cogsci.nl/opensesame</a> for more information.")
			return
			
		try:
			if len(self.version.split("-")) == 2:
				cv = float(self.version.split("-")[0]) - 0.01
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
		Open a help tab for the specified item
		"""
		
		for i in range(self.experiment.ui.tabwidget.count()):
			w = self.experiment.ui.tabwidget.widget(i)
			if hasattr(w, "help_%s" % item):
				self.experiment.ui.tabwidget.setCurrentIndex(i)
				return
						
		
		path = self.experiment.help("%s.html" % item)
		text = libqtopensesame.help_browser.help_browser(path, [("[version]", self.version), ("[codename]", self.codename)])
				
		exec("text.help_%s = True" % item)
		index = self.experiment.ui.tabwidget.addTab(text, self.experiment.icon("help"), title)
		self.experiment.ui.tabwidget.setCurrentIndex(index)
		
	def open_general_help_tab(self):			
	
		self.open_help_tab("Help: General", "general")
		
	def open_stdout_help_tab(self):
	
		self.open_help_tab("Help: Debug window", "stdout")
		
	def open_variables_help_tab(self):
	
		self.open_help_tab("Help: Variable inspector", "variables")				
				
	def open_contribute_tab(self):
	
		self.open_help_tab("Contribute", "contribute")	

	def open_bug_tab(self):
	
		self.open_help_tab("Submit a bug", "submit_a_bug")	
		
	def about(self):
	
		self.open_help_tab("About", "about")
				
	def show_text_in_toolbar(self):
	
		"""
		Toggle the visibility of text in the toolbar
		"""	
		
		if self.ui.action_show_text_in_toolbar.isChecked():
			style = QtCore.Qt.ToolButtonTextUnderIcon
		else:
			style = QtCore.Qt.ToolButtonIconOnly
		
		self.ui.toolbar_main.setToolButtonStyle(style)	
		
	def execute_interpreter(self, dummy = None):
	
		"""
		Runs a command and writes the result to the standard output
		"""	
		
		cmd = str(self.ui.edit_python_command.text())
		
		buf = output_buffer(self.ui.edit_stdout)
		sys.stdout = buf
		
		print "> %s" % cmd
		
		try:
			exec(cmd)
		except Exception as e:
			print "> Error: %s" % e
		sys.stdout = sys.__stdout__		
		
		self.ui.edit_python_command.clear()
		
	def refresh_plugins(self, dummy = None):
	
		"""
		Fills the menu with plugins
		"""
		
		self.populate_plugin_menu(self.ui.menu_items)		
		
	def refresh_stdout(self, dummy = None):
	
		"""
		Updates the stdout viewer
		"""
	
		if not self.ui.action_show_stdout.isChecked():
			self.ui.dock_stdout.setVisible(False)
			return
			
		self.ui.dock_stdout.setVisible(True)			
				
	def refresh_pool(self, make_visible = None):
	
		"""
		Updates the variable inspector if it is visible
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
		Updates the variable inspector if it is visible
		"""
		
		if not self.ui.action_show_variable_inspector.isChecked():
			self.ui.dock_variable_inspector.setVisible(False)
			return
			
		self.ui.dock_variable_inspector.setVisible(True)
		filt = str(self.ui.edit_variable_filter.text())
		
		i = 0
		for var, val, item in self.experiment.var_list(filt):
			self.ui.table_variables.insertRow(i)
			self.ui.table_variables.setCellWidget(i, 0, QtGui.QLabel(" %s " % var))
			self.ui.table_variables.setCellWidget(i, 1, QtGui.QLabel(" %s " % val))								
			self.ui.table_variables.setCellWidget(i, 2, QtGui.QLabel(" %s " % item))
			i += 1				

		self.ui.table_variables.setRowCount(i)		
		
	def restart(self):
	
		"""
		Saves the experiment and restarts opensesame
		"""
		
		resp = QtGui.QMessageBox.question(self.ui.centralwidget, "Restart?", "A restart is required. Do you want to save the current experiment and restart OpenSesame?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		if resp == QtGui.QMessageBox.No:
			return					
			
		self.save_file()			
			
		# A horrifying hack to make sure that opensesame restarts properly under all
		# conditions
	
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
	
		"""
		Close the application
		"""
		
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
		
	def new_file(self):
	
		"""
		Create a new file
		"""
		
		resp = QtGui.QMessageBox.question(self.ui.centralwidget, "New file", "Are you sure you want to create a new experiment? You will lose any unsaved changes to your currently opened experiment.", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		if resp == QtGui.QMessageBox.No:
			return
	
		self.close_all_tabs()
		self.current_path = None
		self.experiment = experiment.experiment(self, "New experiment", open(self.experiment.resource("default.opensesame"), "r").read())		
		self.header_widget.item = self.experiment		
		self.refresh()
		self.open_general_tab()
		self.window_message("New experiment")
		
		self.set_unsaved(True)
		
		self.set_status("Started a new experiment")
		
	def open_file(self, path = None):
	
		"""
		Open a file
		"""		
		
		if path == None:
			path, file_typw = QtGui.QFileDialog.getOpenFileNameAndFilter(self.ui.centralwidget, "Open file", QtCore.QString(), self.file_type_filter)
		if path == None or path == "":
			return				
			
		self.set_status("Opening ...")						
			
		self.close_all_tabs()			
	
		try:
			exp = experiment.experiment(self, "Experiment", str(path))
		except Exception as e:
			self.experiment.notify("<b>Error:</b> Failed to open '%s'<br /><b>Description:</b> %s<br /><br />Make sure that the file is in .opensesame or .opensesame.tar.gz format. If you should be able to open this file, but can't, please go to http://www.cogsci.nl/opensesame to find out how to recover your experiment and file a bug report." % (path, e))
			return						
		
		self.current_path = str(path)		
		self.experiment = exp
		self.header_widget.item = self.experiment
		self.refresh()
		self.open_general_tab()					
		self.window_message(self.current_path)
		
		self.set_status("Opened %s" % self.current_path)					
		self.set_unsaved(False)		
		
		self.default_logfile_folder = os.path.dirname(self.current_path)
				
	def save_file(self, overwrite = True):
	
		"""
		Save a file
		"""
		
		self.set_status("Saving ...")								
	
		if self.current_path == None:
			self.save_file_as()
			return
			
		try:
			self.get_ready()		
			script = self.experiment.to_string()
		except libopensesame.exceptions.script_error as e:
			self.experiment.notify("Could not save file, because the script could not be generated. The following error occured:<br/>%s" % e)
			return
		
		try:
			resp = self.experiment.save(self.current_path, overwrite)	
			self.set_status("Saved as %s" % self.current_path)													
		except Exception as e:
			self.experiment.notify("Failed to save file. Error: %s" % e)
			return
		if resp == False:
			resp = QtGui.QMessageBox.question(self.ui.centralwidget, "File exists", "A file with that name already exists. Overwite?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
			if resp == QtGui.QMessageBox.No:
				self.window_message("Unsaved")
				self.current_path = None
				self.set_status("Not saved")
				return
			else:
				try:
					self.current_path = self.experiment.save(self.current_path, True)
					self.window_message(self.current_path)
					self.set_status("Saved as %s" % self.current_path)										
				except Exception as e:
					self.experiment.notify("Failed to save file. Error: %s" % e)
					self.set_status("Not saved")					
			return

		else:
			self.current_path = resp
			
		self.set_unsaved(False)				
		self.window_message(self.current_path)
				
	def save_file_as(self):
	
		"""
		Save file after asking for file name
		"""
		
		if self.current_path == None:
			path = self.home_folder
		else:
			path = self.current_path
	
		path, file_type = QtGui.QFileDialog.getSaveFileNameAndFilter(self.ui.centralwidget, "Save file as ...", path, self.file_type_filter)
		if path != None and path != "":				
			self.current_path = str(path)
			self.save_file(False)
			
	def close_all_tabs(self):
	
		"""
		Close all tabs
		"""
		
		while self.ui.tabwidget.count() > 0:
			self.close_tab(0)
			
	def close_other_tabs(self):
	
		"""
		Close all tabs except the currently active one
		"""
				
		while self.ui.tabwidget.count() > 0 and self.ui.tabwidget.currentIndex() != 0:
			self.close_tab(0)
			
		while self.ui.tabwidget.count() > 1:
			self.close_tab(1)
		
	def close_tab(self, index):
	
		"""
		Close a tabe
		"""
	
		self.ui.tabwidget.removeTab(index)		
		
	def apply_general_script(self):
	
		"""
		Reloads the experiment based on the script
		"""
		
		script = str(self.edit_script.edit.toPlainText())
			
		try:	
			tmp = experiment.experiment(self, self.experiment.title, script, self.experiment.pool_folder)
		except libopensesame.exceptions.script_error as error:
			self.experiment.notify("Could not parse script: %s" % error)
			self.edit_script.edit.setText(self.experiment.to_string())
			return
			
		self.experiment = tmp	
		self.close_other_tabs()	
		self.edit_script.setModified(False)
		self.refresh()
		
	def update_resolution(self, width, height):
	
		"""
		Updates the resolution in a way that preserves display centering. This
		is kind of a quick hack. First generate the script, change the resolution
		in the script and then re-parse the script.
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
		
	def set_header_label(self):
	
		"""
		Sets the header based on experiment variables
		"""	
		
		self.header_widget.edit_name.setText(self.experiment.title)
		self.header_widget.label_name.setText("<font size='5'><b>%s</b> - Experiment</font>&nbsp;&nbsp;&nbsp;<font color='gray'><i>Click to edit</i></font>" % self.experiment.title)
		self.header_widget.edit_desc.setText(self.experiment.description)
		self.header_widget.label_desc.setText(self.experiment.description)		
		
	def toggle_script_editor(self):
	
		"""
		Hides or shows the script editor based on the
		checkbox state
		"""
		
		show = self.general_ui.checkbox_show_script.isChecked()
		
		self.edit_script.setVisible(show)
		self.general_ui.spacer.setVisible(not show)		
				
	def apply_general_changes(self, dummy = None):
	
		"""
		Sets the experiment variables based on the controls
		"""
		
		if self.ignore_general_changes:
			return
		
		self.ignore_general_changes = True		
		
		title = self.experiment.sanitize(self.header_widget.edit_name.text())
		self.experiment.set("title", title)
		desc = self.experiment.sanitize(self.header_widget.edit_desc.text())
		self.experiment.set("description", desc)	
				
		# Set the start point
		start = self.experiment.sanitize(self.general_ui.combobox_start.currentText())
		self.experiment.set("start", start)
			
		# Set the display width
		width = self.general_ui.spinbox_width.value()
		if self.experiment.get("width") != width:
			self.update_resolution(width, self.experiment.get("height"))
						
		# Set the display height
		height = self.general_ui.spinbox_height.value()
		if self.experiment.get("height") != height:
			self.update_resolution(self.experiment.get("width"), height)
		
		# Set the timing compensation
		comp = self.general_ui.spinbox_compensation.value()
		self.experiment.set("compensation", comp)						
					
		# Set the foreground color
		foreground = self.experiment.sanitize(self.general_ui.edit_foreground.text())
		self.experiment.set("foreground", foreground)									

		# Set the background color
		background = self.experiment.sanitize(self.general_ui.edit_background.text())
		self.experiment.set("background", background)

		self.refresh()
		self.ignore_general_changes = False					
				
	def init_general_tab(self):
	
		"""
		Create the controls in the general tab
		"""
		
		# Set the header, with the icon, label and script button
		self.header_widget = general_header_widget(self.experiment)
		
		button_help = QtGui.QPushButton(self.experiment.icon("help"), "")
		button_help.setIconSize(QtCore.QSize(16, 16))
		button_help.clicked.connect(self.open_general_help_tab)
		button_help.setToolTip("Tell me more about OpenSesame!")
		
		header_hbox = QtGui.QHBoxLayout()
		header_hbox.addWidget(self.experiment.label_image("experiment_large"))
		header_hbox.addWidget(self.header_widget)		
		header_hbox.addStretch()
		header_hbox.addWidget(button_help)
		header_hbox.setContentsMargins(0, 0, 0, 16)	
		
		header_widget = QtGui.QWidget()
		header_widget.setLayout(header_hbox)		
		
		# Script editor		
		self.edit_script = libqtopensesame.inline_editor.inline_editor(self.experiment)
		self.edit_script.apply.clicked.connect(self.apply_general_script)
		libqtopensesame.syntax_highlighter.syntax_highlighter(self.edit_script.edit.document(), libqtopensesame.syntax_highlighter.opensesame_keywords)
						
		# The rest of the controls from the UI file
		w = QtGui.QWidget()
		self.general_ui = general_widget_ui.Ui_Form()
		self.general_ui.setupUi(w)
		self.general_ui.edit_foreground.editingFinished.connect(self.apply_general_changes)
		self.general_ui.edit_background.editingFinished.connect(self.apply_general_changes)	
		self.general_ui.combobox_start.currentIndexChanged.connect(self.apply_general_changes)				
		self.general_ui.spinbox_width.valueChanged.connect(self.apply_general_changes)
		self.general_ui.spinbox_height.valueChanged.connect(self.apply_general_changes)
		self.general_ui.spinbox_compensation.valueChanged.connect(self.apply_general_changes)
		self.general_ui.checkbox_show_script.toggled.connect(self.toggle_script_editor)						
		self.general_ui.label_opensesame.setText(unicode(self.general_ui.label_opensesame.text()).replace("[version]", self.version).replace("[codename]", self.codename))
		
		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(header_widget)
		vbox.addWidget(w)
		vbox.addWidget(self.edit_script)
		vbox.setMargin(16)
		
		self.general_tab_widget = QtGui.QWidget()
		self.general_tab_widget.setLayout(vbox)
		self.general_tab_widget.general_tab = True
		
		self.toggle_script_editor()
		
	def general_widget(self):
	
		"""
		Set the controls of the general tab based on the variables
		"""
		
		if self.experiment.debug:
			print "qtopensesame.general_widget()"
		
		self.ignore_general_changes = True
		
		self.set_header_label()

		# Select the start item		
		self.experiment.item_combobox(self.experiment.start, [], self.general_ui.combobox_start)
		
		# Set the resolution
		try:
			self.general_ui.spinbox_width.setValue(int(self.experiment.width))
			self.general_ui.spinbox_height.setValue(int(self.experiment.height))
		except:
			self.experiment.notify("Failed to parse the resolution. Expecting positive numeric values.")
			
		# Set the timing compensation
		try:
			self.general_ui.spinbox_compensation.setValue(int(self.experiment.compensation))
		except:
			self.experiment.notify("Failed to parse timing compensation. Expecting a numeric value.")
			
		# Set the colors		
		self.general_ui.edit_foreground.setText(str(self.experiment.foreground))
		self.general_ui.edit_background.setText(str(self.experiment.background))
						
		try:
			self.edit_script.edit.setPlainText(self.experiment.to_string())
		except libopensesame.exceptions.script_error as e:
			self.experiment.notify("</>Failed to generate script:</b> %s" % e)
			self.edit_script.edit.setText("Failed to generate script!")

		self.ignore_general_changes = False		
		
	def open_general_tab(self, reopen = False, index = None, focus = True):
	
		"""
		Opens the general tab
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
	
		"""
		Build the unused tab
		"""
		
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
		Open the unused tab
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
	
		"""
		Purge all unused items
		"""		
		
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
		Refresh the item list
		"""
		
		if self.experiment.debug:
			print "qtopensesame.build_item_list(): %s" % name
		
		self.experiment.build_item_tree()
			
	def select_item(self, name):
	
		"""
		Select an item from the itemlist
		"""
		
		if self.experiment.debug:
			print "qtopensesame.select_item(): %s" % name		
	
		if name in self.experiment.unused_items:
			self.experiment.unused_widget.setExpanded(True)
		for item in self.ui.itemtree.findItems(name, QtCore.Qt.MatchFlags(QtCore.Qt.MatchRecursive)):
			self.ui.itemtree.setCurrentItem(item)
		if name in self.experiment.items:
			self.experiment.items[name].open_edit_tab()
					
	def open_item(self, widget, column):
	
		"""
		Open a tab belonging to a widget
		"""
	
		if widget.name == "__general__":
			self.open_general_tab()
		elif widget.name == "__unused__":
			self.open_unused_tab()
		else:
			self.experiment.items[widget.name].open_edit_tab()
						
	def copy_to_pool(self, fname):
	
		"""
		Copy a file to the file pool
		"""
		
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
	
		"""
		Finalize all items, to prepare for running or saving
		"""
		
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
		Runs the experiment as a separate process by
		calling opensesamerun		
		"""
		
		# Temporary file for the standard output
		stdout = tempfile.mktemp(suffix = ".stdout")
		
		# Save the experiment in a temporary location
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
			
		retcode = p.wait()
		
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
		Inform the user that the experiment was successfully terminated
		"""
					
		# Report success and copy the logfile to the filepool if necessary
		resp = QtGui.QMessageBox.question(self.ui.centralwidget, "Finished!", "The experiment is finished and data has been logged to '%s'. Do you want to copy the logfile to the file pool?" % exp.logfile, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		if resp == QtGui.QMessageBox.Yes:
			self.copy_to_pool(exp.logfile)
								
	def run_experiment(self, fullscreen = True):
	
		"""
		Run the experiment		
		"""
				
		# Before we run the experiment, we parse it in three steps
		# 1) Apply any pending changes
		# 2) Convert the experiment to a string
		# 3) Parse the string into a new experiment (with all the GUI stuff stripped off)
		try:
			self.get_ready()
			script = self.experiment.to_string()
			exp = libopensesame.experiment.experiment("Experiment", script, self.experiment.pool_folder)
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
								
		exp.auto_response = self.ui.action_enable_auto_response.isChecked()

		# Reroute the standard output to the debug window
		buf = output_buffer(self.ui.edit_stdout)
		sys.stdout = buf			
		
		if self.ui.action_opensesamerun.isChecked():		
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
		
		# Resume autosave
		if self.autosave_timer != None:
			if self.experiment.debug:
				print "qtopnsesame.run_experiment(): resuming autosave timer"		
			self.autosave_timer.start()
			
		# Restart the experiment if necessary
		if exp.restart:
			self.restart()
			
	def run_experiment_in_window(self):
	
		"""
		Run the experiment in a window
		"""
	
		self.run_experiment(False)
				
	def refresh(self, changed_item = None, refresh_edit = True, refresh_script = True):
	
		"""
		Refresh all parts of the interface that may have changed
		because of a changed item
		"""
		
		# Make sure the refresh does not get caught in
		# a recursive loop
		if self.lock_refresh:
			return			
		self.lock_refresh = True
		
		if self.experiment.debug:
			print "qtopensesame.refresh(): %s" % changed_item
		
		self.set_header_label()
		
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
		
	def hard_refresh(self, changed_item):
	
		"""
		Closes and reopens the script and edit tab for the
		changed item
		"""
		
		# Make sure the refresh does not get caught in
		# a recursive loop
		if self.lock_refresh:
			return			
		self.lock_refresh = True		
		
		if self.experiment.debug:
			print "qtopensesame.hard_refresh(): %s" % changed_item
		
		self.set_header_label()
		
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
		
	def populate_plugin_menu(self, menu):
	
		"""
		Adds a list of plugins to a menu
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
		
	def choose_and_add_plugin(self):
	
		"""
		Ask the user which plugin to add and do it
		"""
		
		menu = QtGui.QMenu()
		self.populate_plugin_menu(menu)			
		menu.exec_(menu.mapFromGlobal(QtGui.QCursor.pos()))
								
	def add_item(self, item_type, refresh = True):
	
		"""
		A generic function to add items
		"""

		name = self.experiment.unique_name("%s" % item_type)
				
		if self.experiment.debug:	
			print "qtopensesame.add_item(): adding %s" % item_type		
					
		if libopensesame.plugins.is_plugin(item_type):
		
			if self.experiment.debug:
				item = libopensesame.plugins.load_plugin(item_type, name, self.experiment, None, self.experiment.item_prefix())				
			else:
				try:
					item = libopensesame.plugins.load_plugin(item_type, name, self.experiment, None, self.experiment.item_prefix())		
				except Exception as e:
					self.experiment.notify("Failed to load plugin '%s'. Error: %s" % (item_type, e))
					return

		else:				
			exec("from libqtopensesame import %s" % item_type)					
			name = self.experiment.unique_name("%s" % item_type)
			item = eval("%s.%s(name, self.experiment)" % (item_type, item_type))
			
		# Ask for a new name
		if self.immediate_rename:
			name, ok = QtGui.QInputDialog.getText(self, "New name", "Please enter a name for the new %s" % item_type, text = name)
			if not ok:
				return None
			name = str(name)
			item.name = name		
			
		self.experiment.items[name] = item
		if refresh:		
			item.open_edit_tab()		
			self.refresh()		
			self.select_item(name)					
			
		return name		
			
	def add_loop(self, refresh = True, parent = None):
	
		"""
		Add a loop item. Also ask for an item to
		fill the loop with.
		"""

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
		Add a sequence item. Also ask for an item to
		fill the sequence with.
		"""

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
		Add a sketchpad item
		"""
		
		return self.add_item("sketchpad", refresh)
		
	def add_feedback(self, refresh = True, parent = None):
	
		"""
		Add a feedback item
		"""
		
		return self.add_item("feedback", refresh)		
		
	def add_sampler(self, refresh = True, parent = None):
	
		"""
		Add a feedback item
		"""
		
		return self.add_item("sampler", refresh)	
		
	def add_synth(self, refresh = True, parent = None):
	
		"""
		Add a feedback item
		"""
		
		return self.add_item("synth", refresh)					
		
	def add_keyboard_response(self, refresh = True, parent = None):
	
		"""
		Add a keyboard item
		"""
				
		return self.add_item("keyboard_response", refresh)
		
	def add_mouse_response(self, refresh = True, parent = None):
	
		"""
		Add a keyboard item
		"""
				
		return self.add_item("mouse_response", refresh)		
		
	def add_logger(self, refresh = True, parent = None):
	
		"""
		Add a logger item
		"""														
		
		return self.add_item("logger", refresh)
		
	def add_inline_script(self, refresh = True, parent = None):
	
		"""
		Add a inline script item
		"""										
		
		return self.add_item("inline_script", refresh)
		
	def drop_item(self, add_func):
		
		"""
		Create a new item based on a drop
		"""
	
		if self.experiment.debug:
			print "qtopensesame.drag_item(): dropping"		
		
		# Check if the overview tree has set a target for the drop
		if self.ui.itemtree.drop_target == None:
			return
		
		# Retrieve the target
		target_item = self.ui.itemtree.drop_target
		target = str(target_item.text(0))
		
		# If the target is not an item, return
		if target not in self.experiment.items:
			return
		
		# If the target is not a loop or sequence, get the underlying loop or sequence
		if self.experiment.items[target].item_type not in ("sequence", "loop"):			
			real_target_item = target_item			
			real_target = target
			target_item = target_item.parent()					
			target = str(target_item.text(0))
				
			# Determine the position in the sequence
			index = 0
			for child in target_item.takeChildren():
				if child == real_target_item:
					break
				index += 1
		
		else:
		
			# By default insert the item at the top of the sequence
			index = 0	 
			
		# If the target is not an item and is not the main experiment, return
		if target not in self.experiment.items and target_item.parent() != None:
			if self.experiment.debug:
				print "qtopensesame.drop_item(): failed to drop onto %s" % target
			return
			
		# Create a new item
		if type(add_func) != str:
			new_item = add_func(False, parent = target)
		else:
			new_item = self.add_item(add_func, False)
			
		# If cancelled, just return
		if new_item == None:
			self.refresh(target)
			return
			
		# If the target has no parent, it is the main experiment. In this case, we have
		# to change the entry point of the experiment
		if target_item.parent() == None:
			
			if self.experiment.debug:
				print "qtopensesame.drop_item(): changing experiment entry point to %s" % target
			self.experiment.set("start", new_item)
			
		# Otherwise we add the new item to the parent sequence or the loop
		else:
		
			if self.experiment.debug:
				print "qtopensesame.drop_item(): dropping onto %s" % target		
			
			# If the target is a sequence insert the new item
			if self.experiment.items[target].item_type == "sequence":
				self.experiment.items[target].items.insert(index, (new_item, "always"))
			
			# If the target is a loop, replace the loop item
			if self.experiment.items[target].item_type == "loop":
				self.experiment.items[target].item = new_item

		self.refresh(target)			
		self.select_item(new_item)		
		
	def drag_item(self, add_func):
	
		"""
		Drag and drop an item type
		"""												
		
		if self.experiment.debug:
			print "qtopensesame.drag_item(): dragging"
		
		# Reset the drop target
		self.ui.itemtree.drop_target = None
		
		# Start the drop action
		d = QtGui.QDrag(self.ui.centralwidget)
		m = QtCore.QMimeData()
		m.setText("new_item")
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
	
		"""
		Drag a new loop
		"""
	
		self.drag_item(self.add_loop)
		
	def drag_sequence(self):
	
		"""
		Drag a new sequence
		"""
	
		self.drag_item(self.add_sequence)		
		
	def drag_sketchpad(self):
	
		"""
		Drag a new sketchpad
		"""
	
		self.drag_item(self.add_sketchpad)		
		
	def drag_feedback(self):
	
		"""
		Drag a new feedback
		"""
	
		self.drag_item(self.add_feedback)		
		
	def drag_sampler(self):
	
		"""
		Drag a new sampler
		"""
	
		self.drag_item(self.add_sampler)		
		
	def drag_synth(self):
	
		"""
		Drag a new synth
		"""
	
		self.drag_item(self.add_synth)		
		
	def drag_keyboard_response(self):
	
		"""
		Drag a new keyboard_response
		"""
	
		self.drag_item(self.add_keyboard_response)		
		
	def drag_mouse_response(self):
	
		"""
		Drag a new mouse_response
		"""
	
		self.drag_item(self.add_mouse_response)		
		
	def drag_logger(self):
	
		"""
		Drag a new logger
		"""
	
		self.drag_item(self.add_logger)
		
	def drag_inline_script(self):
	
		"""
		Drag a new inline_script
		"""
	
		self.drag_item(self.add_inline_script)
		

