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

import libopensesame.feedback
import libqtopensesame.qtitem
import libqtopensesame.feedpad
import libqtopensesame.sketchpad_widget
from PyQt4 import QtCore, QtGui

class feedback(libopensesame.feedback.feedback, libqtopensesame.feedpad.feedpad, libqtopensesame.qtitem.qtitem):

	"""The GUI for the feedback item"""

	def __init__(self, name, experiment, string = None):

		"""
		Constructor

		Arguments:
		name -- the name of the item
		experiment -- an instance of libopensesame.experiment

		Keyword arguments:
		string -- a string with the item definition (default = None)
		"""

		libopensesame.feedback.feedback.__init__(self, name, experiment, string)
		libqtopensesame.qtitem.qtitem.__init__(self)

	def apply_edit_changes(self):

		"""Apply changes to the controls"""

		libqtopensesame.qtitem.qtitem.apply_edit_changes(self)
		dur = self.experiment.sanitize(self.edit_duration.text(), strict=True)
		if dur.strip() != "":
			self.set("duration", dur)
		if self.checkbox_reset.isChecked():
			self.set("reset_variables", "yes")
		else:
			self.set("reset_variables", "no")
		self.experiment.main_window.refresh(self.name)

	def edit_widget(self):

		"""Update the controls based on the items settings"""

		libqtopensesame.qtitem.qtitem.edit_widget(self)
		self.edit_duration.setText(str(self.get_check("duration", "keypress")))
		self.checkbox_reset.setChecked(self.get_check("reset_variables", valid=["yes", "no"]) == "yes")
		self.tools_widget.refresh()
		return self._edit_widget

	def init_edit_widget(self):

		"""Construct the edit widget that contains the controls"""

		libqtopensesame.qtitem.qtitem.init_edit_widget(self, False)

		row = 0

		self.edit_grid.addWidget(QtGui.QLabel("Duration"), row, 0)
		self.edit_duration = QtGui.QLineEdit()
		QtCore.QObject.connect(self.edit_duration, QtCore.SIGNAL("editingFinished()"), self.apply_edit_changes)
		self.edit_grid.addWidget(self.edit_duration, row, 1)
		
		row += 1
		self.checkbox_reset = QtGui.QCheckBox("Reset feedback variables")
		self.checkbox_reset.toggled.connect(self.apply_edit_changes)
		self.edit_grid.addWidget(self.checkbox_reset, row, 0)

		row += 1
		self.popout_button = QtGui.QPushButton(self.experiment.icon(self.item_type), "Open editor in new window")
		self.popout_button.setIconSize(QtCore.QSize(16, 16))
		QtCore.QObject.connect(self.popout_button, QtCore.SIGNAL("clicked()"), self.popout)
		self.edit_grid.addWidget(self.popout_button, row, 0)

		self.tools_widget = libqtopensesame.sketchpad_widget.sketchpad_widget(self)
		self.edit_vbox.addWidget(self.tools_widget)

