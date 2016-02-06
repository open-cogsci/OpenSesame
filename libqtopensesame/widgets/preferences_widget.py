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

from libopensesame import debug
from libopensesame.exceptions import osexception
from libqtopensesame.widgets.base_widget import base_widget
from libqtopensesame.misc import config, theme
from qtpy import QtCore, QtWidgets
import os

class preferences_widget(base_widget):

	"""
	desc:
		The widget for the preferences tab.
	"""

	def __init__(self, main_window):

		"""
		desc:
			Constructor.

		arguments:
			main_window:	A qtopensesame object.
		"""

		super(preferences_widget, self).__init__(main_window,
			ui=u'widgets.preferences_widget')
		self.tab_name = u'__preferences__'
		self.lock = False
		# Connect the controls
		self.ui.checkbox_autoresponse.toggled.connect(self.apply)
		self.ui.checkbox_toolbar_text.toggled.connect(self.apply)
		self.ui.checkbox_small_toolbar.toggled.connect(self.apply)
		self.ui.combobox_runner.currentIndexChanged.connect(self.apply)
		self.ui.combobox_style.currentIndexChanged.connect(self.apply)
		self.ui.combobox_theme.currentIndexChanged.connect(self.apply)
		self.set_controls()
		for ext in self.extensions:
			try:
				w = ext.settings_widget()
			except Exception as e:
				if not isinstance(e, osexception):
					e = osexception(msg=u'Extension error', exception=e)
				self.notify(
					u'Extension %s failed to return settings widget (see debug window for stack trace)' \
					% ext.name())
				self.console.write(e)
				continue
			if w is not None:
				self.ui.layout_preferences.addWidget(w)
		self.ui.container_widget.adjustSize()

	def set_controls(self):

		"""
		desc:
			Updates the controls.
		"""

		if self.lock:
			return
		self.lock = True
		self.ui.checkbox_autoresponse.setChecked(
			self.experiment.auto_response)
		self.ui.checkbox_toolbar_text.setChecked(
			self.main_window.ui.toolbar_main.toolButtonStyle() == \
			QtCore.Qt.ToolButtonTextUnderIcon)
		self.ui.checkbox_small_toolbar.setChecked(
			config.get_config(u"toolbar_size") == 16)
		self.ui.combobox_runner.setCurrentIndex(
			self.ui.combobox_runner.findText(config.get_config(u'runner'),
			flags=QtCore.Qt.MatchContains))
		# Set the style combobox
		i = 0
		if config.get_config(u'style') == u'':
			self.ui.combobox_style.addItem(u"[Default]")
			self.ui.combobox_style.setCurrentIndex(i)
			i += 1
		for style in QtWidgets.QStyleFactory.keys():
			self.ui.combobox_style.addItem(style)
			if config.get_config(u'style') == str(style):
				self.ui.combobox_style.setCurrentIndex(i)
			i += 1
		# Set the theme combobox
		i = 0
		for _theme in theme.available_themes:
			self.ui.combobox_theme.addItem(_theme)
			if config.get_config(u'theme') == _theme:
				self.ui.combobox_theme.setCurrentIndex(i)
			i += 1
		self.lock = False

	def apply(self):

		"""Apply the controls"""

		if self.lock:
			return
		self.lock = True
		self.experiment.auto_response = \
			self.ui.checkbox_autoresponse.isChecked()
		self.main_window.ui.action_enable_auto_response.setChecked(
			self.ui.checkbox_autoresponse.isChecked())

		if self.ui.checkbox_toolbar_text.isChecked():
			self.main_window.ui.toolbar_main.setToolButtonStyle(
				QtCore.Qt.ToolButtonTextUnderIcon)
		else:
			self.main_window.ui.toolbar_main.setToolButtonStyle(
				QtCore.Qt.ToolButtonIconOnly)

		old_size = config.get_config(u'toolbar_size')
		if self.ui.checkbox_small_toolbar.isChecked():
			new_size = 16
		else:
			new_size = 32
		if old_size != new_size:
			config.set_config(u"toolbar_size", new_size)
			self.theme.set_toolbar_size(config.get_config("toolbar_size"))

		from libqtopensesame import runners
		for runner in runners.runner_list:
			if runner in self.ui.combobox_runner.currentText():
				config.set_config(u'runner', runner)

		config.set_config(u'theme',
			str(self.ui.combobox_theme.currentText()))

		config.set_config(u'style',
			str(self.ui.combobox_style.currentText()))
		self.main_window.save_state()

		self.lock = False
