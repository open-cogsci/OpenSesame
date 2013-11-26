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

from libopensesame import debug
from libqtopensesame.ui import preferences_widget_ui
from libqtopensesame.misc import config, theme
from libopensesame import plugins
from PyQt4 import QtCore, QtGui
import os

class preferences_widget(QtGui.QWidget):

	"""The widget displayed in the preferences tab."""

	def __init__(self, parent):

		"""
		Constructor.

		Arguments:
		parent	--	The parent widget.
		"""

		QtGui.QWidget.__init__(self, parent)
		self.tab_name = u'__preferences__'
		self.main_window = parent
		# Setup the GUI
		self.ui = preferences_widget_ui.Ui_preferences_widget()
		self.ui.setupUi(self)
		self.main_window.theme.apply_theme(self)
		self.lock = False
		# Connect the controls
		self.ui.checkbox_immediately_rename.toggled.connect(self.apply)
		self.ui.checkbox_autoresponse.toggled.connect(self.apply)
		self.ui.checkbox_toolbar_text.toggled.connect(self.apply)
		self.ui.checkbox_small_toolbar.toggled.connect(self.apply)
		self.ui.checkbox_enable_autosave.toggled.connect(self.apply)
		self.ui.spinbox_autosave_interval.valueChanged.connect(self.apply)
		self.ui.spinbox_autosave_max_age.valueChanged.connect(self.apply)
		self.ui.checkbox_auto_update_check.toggled.connect(self.apply)
		self.ui.combobox_runner.currentIndexChanged.connect(self.apply)
		self.ui.button_browse_autosave.clicked.connect( \
			self.main_window.open_autosave_folder)
		self.ui.button_update_check.clicked.connect( \
			self.main_window.check_update)
		self.ui.combobox_style.currentIndexChanged.connect(self.apply)
		self.ui.combobox_theme.currentIndexChanged.connect(self.apply)
		# Construct the plugin section
		self.checkbox_plugins = {}
		self.ui.edit_plugin_folders.setText(u'; '.join(plugins.plugin_folders( \
			only_existing=False)))
		for plugin in sorted(plugins.list_plugins(filter_disabled=False)):
			self.checkbox_plugins[plugin] = QtGui.QCheckBox(plugin)
			self.checkbox_plugins[plugin].toggled.connect(self.apply)
			self.ui.layout_plugin_list.addWidget(self.checkbox_plugins[plugin])
		self.set_controls()

	def set_controls(self):

		"""Updates the controls."""

		if self.lock:
			return
		self.lock = True
		debug.msg()

		self.ui.checkbox_immediately_rename.setChecked( \
			config.get_config(u'immediate_rename'))
		self.ui.checkbox_autoresponse.setChecked( \
			self.main_window.experiment.auto_response)
		self.ui.checkbox_toolbar_text.setChecked( \
			self.main_window.ui.toolbar_main.toolButtonStyle() == \
			QtCore.Qt.ToolButtonTextUnderIcon)
		self.ui.checkbox_small_toolbar.setChecked( \
			config.get_config(u"toolbar_size") == 16)		
		self.ui.checkbox_enable_autosave.setChecked( \
			config.get_config(u'autosave_interval') > 0)
		self.ui.spinbox_autosave_interval.setValue( \
			config.get_config(u'autosave_interval') / 60000) # Show in minutes
		self.ui.spinbox_autosave_max_age.setValue( \
			config.get_config(u'autosave_max_age'))
		self.ui.checkbox_auto_update_check.setChecked(config.get_config( \
			u'auto_update_check'))		
		self.ui.combobox_runner.setCurrentIndex( \
			self.ui.combobox_runner.findText(config.get_config(u'runner'), \
			flags=QtCore.Qt.MatchContains))		
		# Disable some of the controls, if they depend on other controls
		if config.get_config(u'autosave_interval') <= 0:
			self.ui.spinbox_autosave_interval.setDisabled(True)
		# Set the style combobox
		i = 0
		if config.get_config(u'style') == u'':
			self.ui.combobox_style.addItem(u"[Default]")
			self.ui.combobox_style.setCurrentIndex(i)
			i += 1
		for style in QtGui.QStyleFactory.keys():
			self.ui.combobox_style.addItem(style)
			if config.get_config(u'style') == unicode(style):
				self.ui.combobox_style.setCurrentIndex(i)
			i += 1
		# Set the theme combobox
		i = 0
		for _theme in theme.available_themes:
			self.ui.combobox_theme.addItem(_theme)
			if config.get_config(u'theme') == _theme:
				self.ui.combobox_theme.setCurrentIndex(i)
			i += 1
		# Set the plugin status
		for plugin in plugins.list_plugins(filter_disabled=False):
			self.checkbox_plugins[plugin].setChecked(not \
				plugins.plugin_disabled(plugin))
		self.lock = False

	def apply(self):

		"""Apply the controls"""

		if self.lock:
			return
		self.lock = True
		debug.msg()

		config.set_config(u'immediate_rename', \
			self.ui.checkbox_immediately_rename.isChecked())
		self.main_window.experiment.auto_response = \
			self.ui.checkbox_autoresponse.isChecked()
		self.main_window.ui.action_enable_auto_response.setChecked( \
			self.ui.checkbox_autoresponse.isChecked())

		if self.ui.checkbox_toolbar_text.isChecked():
			self.main_window.ui.toolbar_main.setToolButtonStyle( \
				QtCore.Qt.ToolButtonTextUnderIcon)
		else:
			self.main_window.ui.toolbar_main.setToolButtonStyle( \
				QtCore.Qt.ToolButtonIconOnly)
		
		old_size = config.get_config(u'toolbar_size')
		if self.ui.checkbox_small_toolbar.isChecked():
			new_size = 16
		else:
			new_size = 32
		if old_size != new_size:
			config.set_config(u"toolbar_size", new_size)
			self.main_window.theme.set_toolbar_size(config.get_config( \
				"toolbar_size"))		

		if self.ui.checkbox_enable_autosave.isChecked():
			config.set_config(u'autosave_interval', 60000 * \
				self.ui.spinbox_autosave_interval.value())
		else:
			config.set_config(u'autosave_interval', 0)	
		config.set_config(u'autosave_max_age', \
			self.ui.spinbox_autosave_max_age.value())
		self.main_window.start_autosave_timer()

		config.set_config(u'auto_update_check', \
			self.ui.checkbox_auto_update_check.isChecked())
		
		from libqtopensesame import runners
		for runner in runners.runner_list:
			if runner in self.ui.combobox_runner.currentText():
				config.set_config(u'runner', runner)

		config.set_config(u'theme', unicode( \
			self.ui.combobox_theme.currentText()))

		# Create a semicolon-separated list of disabled plugins
		l = []
		for plugin in plugins.list_plugins(filter_disabled=False):
			if not self.checkbox_plugins[plugin].isChecked():
				l.append(plugin)
		config.set_config(u"disabled_plugins", ";".join(l))

		config.set_config(u'style', unicode( \
			self.ui.combobox_style.currentText()))
		self.main_window.save_state()

		self.lock = False
