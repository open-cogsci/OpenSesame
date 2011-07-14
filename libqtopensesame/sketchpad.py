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

import libopensesame.sketchpad
import libqtopensesame.qtitem
import libqtopensesame.feedpad
import libqtopensesame.sketchpad_widget
import libqtopensesame.sketchpad_dialog
from PyQt4 import QtCore, QtGui

class sketchpad(libopensesame.sketchpad.sketchpad, libqtopensesame.feedpad.feedpad, libqtopensesame.qtitem.qtitem):

	"""The GUI controls for the sketchpad"""

	def __init__(self, name, experiment, string = None):

		"""
		Constructor

		Arguments:
		name -- the name of the item
		experiment -- an instance of libopensesame.experiment

		Keyword arguments:
		string -- a string with the item definition (default = None)
		"""

		libopensesame.sketchpad.sketchpad.__init__(self, name, experiment, string)
		libqtopensesame.qtitem.qtitem.__init__(self)

	def apply_edit_changes(self):

		"""Apply changes to the controls"""

		if not libqtopensesame.qtitem.qtitem.apply_edit_changes(self, False):
			return

		dur = str(self.edit_duration.text()).strip()
		if dur.strip() != "":
			self.set("duration", dur)

		if self.checkbox_start_response_interval.isChecked():
			self.set("start_response_interval", "yes")
		else:
			self.set("start_response_interval", "no")

		self.experiment.main_window.refresh(self.name)

	def edit_widget(self):

		"""Update the controls based on the items settings"""

		libqtopensesame.qtitem.qtitem.edit_widget(self)

		if self.has("duration"):
			dur = self.get("duration")
		else:
			dur = ""
		self.edit_duration.setText(str(dur))
		self.checkbox_start_response_interval.setChecked(self.get("start_response_interval") == "yes")
		self.tools_widget.refresh()

		return self._edit_widget

	def init_edit_widget(self):

		"""Construct the edit widget that contains the controls"""

		libqtopensesame.qtitem.qtitem.init_edit_widget(self, False)

		row = 3
		self.edit_grid.addWidget(QtGui.QLabel("Duration"), row, 0)
		self.edit_duration = QtGui.QLineEdit()
		self.edit_duration.setToolTip("A numeric value (duration in milliseconds), 'keypress', 'mouseclick', or '[variable_name]'")
		QtCore.QObject.connect(self.edit_duration, QtCore.SIGNAL("editingFinished()"), self.apply_edit_changes)
		self.edit_grid.addWidget(self.edit_duration, row, 1)

		row += 1
		self.checkbox_start_response_interval = QtGui.QCheckBox("Start response interval")
		self.checkbox_start_response_interval.setToolTip("If checked, the response items will use the onset of the sketchpad to determine response time")
		self.edit_grid.addWidget(self.checkbox_start_response_interval, row, 0)
		QtCore.QObject.connect(self.checkbox_start_response_interval, QtCore.SIGNAL("stateChanged(int)"), self.apply_edit_changes)

		row += 1
		self.popout_button = QtGui.QPushButton(self.experiment.icon(self.item_type), "Open editor in new window")
		self.popout_button.setIconSize(QtCore.QSize(16,16))
		self.popout_button.setToolTip("Open the sketchpad editor in a new window")
		QtCore.QObject.connect(self.popout_button, QtCore.SIGNAL("clicked()"), self.popout)
		self.edit_grid.addWidget(self.popout_button, row, 0)

		self.tools_widget = libqtopensesame.sketchpad_widget.sketchpad_widget(self)
		self.edit_vbox.addWidget(self.tools_widget)

