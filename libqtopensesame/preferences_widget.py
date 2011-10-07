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

import libqtopensesame.preferences_widget_ui
from libqtopensesame import config
from libopensesame import plugins
from PyQt4 import QtCore, QtGui
import os

class preferences_widget(QtGui.QWidget):

	"""The widget displayed in the preferences tab"""

	def __init__(self, parent):
	
		"""
		Constructor
		
		Arguments:
		parent -- the parent widget
		"""
		
		QtGui.QWidget.__init__(self, parent)
		self.tab_name = "__preferences__"					
		self.main_window = parent
		
		# Setup the GUI
		self.ui = libqtopensesame.preferences_widget_ui.Ui_Form()
		self.ui.setupUi(self)
		self.lock = False
		
		# Connect the controls
		self.ui.checkbox_immediately_rename.toggled.connect(self.apply)
		self.ui.checkbox_autoresponse.toggled.connect(self.apply)
		self.ui.checkbox_show_random_tips.toggled.connect(self.apply)
		self.ui.checkbox_toolbar_text.toggled.connect(self.apply)
		self.ui.checkbox_enable_autosave.toggled.connect(self.apply)
		self.ui.spinbox_autosave_interval.valueChanged.connect(self.apply)
		self.ui.spinbox_autosave_max_age.valueChanged.connect(self.apply)
		self.ui.checkbox_auto_update_check.toggled.connect(self.apply)		
		self.ui.checkbox_opensesamerun.toggled.connect(self.apply)
		self.ui.checkbox_auto_opensesamerun_exec.toggled.connect(self.apply)						
		self.ui.edit_opensesamerun_exec.editingFinished.connect(self.apply)			
		self.ui.button_browse_autosave.clicked.connect(self.main_window.open_autosave_folder)	
		self.ui.button_update_check.clicked.connect(self.main_window.check_update)
		self.ui.combobox_style.currentIndexChanged.connect(self.apply)
		
		self.ui.checkbox_new_experiment_dialog.toggled.connect(self.apply)
		self.ui.checkbox_scintilla_auto_indent.toggled.connect(self.apply)
		self.ui.checkbox_scintilla_brace_match.toggled.connect(self.apply)
		self.ui.checkbox_scintilla_custom_font.toggled.connect(self.apply)
		self.ui.checkbox_scintilla_eol_visible.toggled.connect(self.apply)
		self.ui.checkbox_scintilla_folding.toggled.connect(self.apply)
		self.ui.checkbox_scintilla_indentation_guides.toggled.connect(self.apply)
		self.ui.checkbox_scintilla_line_numbers.toggled.connect(self.apply)
		self.ui.checkbox_scintilla_right_margin.toggled.connect(self.apply)
		self.ui.checkbox_scintilla_syntax_highlighting.toggled.connect(self.apply)
		self.ui.checkbox_scintilla_whitespace_visible.toggled.connect(self.apply)
		self.ui.font_scintilla_font_family.currentFontChanged.connect(self.apply)
		self.ui.spinbox_scintilla_font_size.valueChanged.connect(self.apply)
		
		# Construct the plugin section
		self.checkbox_plugins = {}		
		self.ui.edit_plugin_folders.setText("; ".join(plugins.plugin_folders(only_existing=False)))
		for plugin in sorted(plugins.list_plugins(filter_disabled=False)):
			self.checkbox_plugins[plugin] = QtGui.QCheckBox(plugin)
			self.checkbox_plugins[plugin].toggled.connect(self.apply)
			self.ui.layout_plugin_list.addWidget(self.checkbox_plugins[plugin])
		
		try:
			import libqtopensesame.inline_editor_qscintilla as dummy
		except:
			self.ui.groupbox_scintilla.hide()
			
		self.set_controls()						
				
	def set_controls(self):
	
		"""Update the controls"""
		
		if self.lock:
			return
		self.lock = True
		
		if self.main_window.experiment.debug:
			print "preferences_widget.set_controls(): setting controls"
		
		self.ui.checkbox_immediately_rename.setChecked(self.main_window.immediate_rename)
		self.ui.checkbox_autoresponse.setChecked(self.main_window.experiment.auto_response)
		self.ui.checkbox_show_random_tips.setChecked(self.main_window.show_startup_tip)
		self.ui.checkbox_toolbar_text.setChecked(self.main_window.ui.toolbar_main.toolButtonStyle() == QtCore.Qt.ToolButtonTextUnderIcon)		
		self.ui.checkbox_enable_autosave.setChecked(self.main_window.autosave_interval > 0)
		self.ui.spinbox_autosave_interval.setValue(self.main_window.autosave_interval / 60000) # Show in minutes, not milliseconds
		self.ui.spinbox_autosave_max_age.setValue(self.main_window.autosave_max_age)
		self.ui.checkbox_auto_update_check.setChecked(self.main_window.auto_check_update)		
		self.ui.checkbox_opensesamerun.setChecked(self.main_window.opensesamerun)				
		self.ui.checkbox_auto_opensesamerun_exec.setChecked(self.main_window.opensesamerun_exec == "")
		self.ui.edit_opensesamerun_exec.setText(self.main_window.opensesamerun_exec)
		
		self.ui.checkbox_new_experiment_dialog.setChecked(config.get_config("new_experiment_dialog"))
		self.ui.checkbox_scintilla_auto_indent.setChecked(config.get_config("scintilla_auto_indent"))
		self.ui.checkbox_scintilla_brace_match.setChecked(config.get_config("scintilla_brace_match"))
		self.ui.checkbox_scintilla_custom_font.setChecked(config.get_config("scintilla_custom_font"))
		self.ui.checkbox_scintilla_eol_visible.setChecked(config.get_config("scintilla_eol_visible"))
		self.ui.checkbox_scintilla_folding.setChecked(config.get_config("scintilla_folding"))
		self.ui.checkbox_scintilla_indentation_guides.setChecked(config.get_config("scintilla_indentation_guides"))
		self.ui.checkbox_scintilla_line_numbers.setChecked(config.get_config("scintilla_line_numbers"))
		self.ui.checkbox_scintilla_right_margin.setChecked(config.get_config("scintilla_right_margin"))
		self.ui.checkbox_scintilla_auto_indent.setChecked(config.get_config("scintilla_auto_indent"))
		self.ui.checkbox_scintilla_syntax_highlighting.setChecked(config.get_config("scintilla_syntax_highlighting"))
		self.ui.checkbox_scintilla_whitespace_visible.setChecked(config.get_config("scintilla_whitespace_visible"))		
		self.ui.font_scintilla_font_family.setCurrentFont(QtGui.QFont(config.get_config("scintilla_font_family")))
		self.ui.spinbox_scintilla_font_size.setValue(config.get_config("scintilla_font_size"))
				
		# Disable some of the controls, if they depend on other controls
		if self.main_window.autosave_interval <= 0:
			self.ui.spinbox_autosave_interval.setDisabled(True)	
				
		if not self.main_window.opensesamerun:
			self.ui.checkbox_auto_opensesamerun_exec.setDisabled(True)
			self.ui.edit_opensesamerun_exec.setDisabled(True)
			self.ui.label_opensesamerun_exec.setDisabled(True)
					
		if self.main_window.opensesamerun_exec == "":
			self.ui.edit_opensesamerun_exec.setDisabled(True)
			self.ui.label_opensesamerun_exec.setDisabled(True)
			
		i = 0
		if self.main_window.style == "":
			self.ui.combobox_style.addItem("[Default]")
			self.ui.combobox_style.setCurrentIndex(i)
			i += 1
		for style in QtGui.QStyleFactory.keys():
			self.ui.combobox_style.addItem(style)
			if self.main_window.style == str(style):
				self.ui.combobox_style.setCurrentIndex(i)
			i += 1

		# Set the plugin status			
		for plugin in plugins.list_plugins(filter_disabled=False):
			self.checkbox_plugins[plugin].setChecked(not plugins.plugin_disabled(plugin))
			
		self.lock = False			
			
	def apply(self):
	
		"""Apply the controls"""
		
		if self.lock:
			return
		self.lock = True
		
		if self.main_window.experiment.debug:
			print "preferences_widget.apply(): applying controls"		
		
		self.main_window.immediate_rename = self.ui.checkbox_immediately_rename.isChecked()
		self.main_window.show_startup_tip = self.ui.checkbox_show_random_tips.isChecked()		
		self.main_window.experiment.auto_response = self.ui.checkbox_autoresponse.isChecked()
		self.main_window.ui.action_enable_auto_response.setChecked(self.ui.checkbox_autoresponse.isChecked())
		
		if self.ui.checkbox_toolbar_text.isChecked():
			self.main_window.ui.toolbar_main.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
		else:
			self.main_window.ui.toolbar_main.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
			
		if self.ui.checkbox_enable_autosave.isChecked():
			self.main_window.autosave_interval = 60000 * self.ui.spinbox_autosave_interval.value()
		else:
			self.main_window.autosave_interval = 0
		self.main_window.autosave_max_age = self.ui.spinbox_autosave_max_age.value()			
		self.main_window.start_autosave_timer()
			
		self.main_window.auto_check_update = self.ui.checkbox_auto_update_check.isChecked()
		self.main_window.opensesamerun = self.ui.checkbox_opensesamerun.isChecked()
		
		self.ui.edit_opensesamerun_exec.setEnabled(self.ui.checkbox_opensesamerun.isChecked() and not self.ui.checkbox_auto_opensesamerun_exec.isChecked())
		self.ui.label_opensesamerun_exec.setEnabled(self.ui.checkbox_opensesamerun.isChecked() and not self.ui.checkbox_auto_opensesamerun_exec.isChecked())
		
		if self.ui.checkbox_auto_opensesamerun_exec.isChecked():
			self.main_window.opensesamerun_exec = ""
			self.ui.edit_opensesamerun_exec.setText("")
		else:
			if self.ui.edit_opensesamerun_exec.text() == "":
				if os.name == "nt":
					self.ui.edit_opensesamerun_exec.setText("opensesamerun.exe")
				else:
					self.ui.edit_opensesamerun_exec.setText("opensesamerun")
			self.main_window.opensesamerun_exec = str(self.ui.edit_opensesamerun_exec.text())
		
		config.set_config("new_experiment_dialog", self.ui.checkbox_new_experiment_dialog.isChecked())			
		config.set_config("scintilla_auto_indent", self.ui.checkbox_scintilla_auto_indent.isChecked())
		config.set_config("scintilla_brace_match", self.ui.checkbox_scintilla_brace_match.isChecked())
		config.set_config("scintilla_custom_font", self.ui.checkbox_scintilla_custom_font.isChecked())
		config.set_config("scintilla_eol_visible", self.ui.checkbox_scintilla_eol_visible.isChecked())
		config.set_config("scintilla_folding", self.ui.checkbox_scintilla_folding.isChecked())
		config.set_config("scintilla_indentation_guides", self.ui.checkbox_scintilla_indentation_guides.isChecked())
		config.set_config("scintilla_line_numbers", self.ui.checkbox_scintilla_line_numbers.isChecked())
		config.set_config("scintilla_right_margin", self.ui.checkbox_scintilla_right_margin.isChecked())
		config.set_config("scintilla_syntax_highlighting", self.ui.checkbox_scintilla_syntax_highlighting.isChecked())
		config.set_config("scintilla_whitespace_visible", self.ui.checkbox_scintilla_whitespace_visible.isChecked())		
		config.set_config("scintilla_font_family", str(self.ui.font_scintilla_font_family.currentFont().family()))
		config.set_config("scintilla_font_size", self.ui.spinbox_scintilla_font_size.value())								
		
		# Create a semicolon-separated list of disabled plugins
		l = []
		for plugin in plugins.list_plugins(filter_disabled=False):
			if not self.checkbox_plugins[plugin].isChecked():
				l.append(plugin)
		config.set_config("disabled_plugins", ";".join(l))		
				
		self.main_window.style = self.ui.combobox_style.currentText()
		self.main_window.set_style()									
		self.main_window.save_state()
		
		self.lock = False
