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

import libopensesame.sketchpad
from libqtopensesame.items import qtplugin, feedpad
from libqtopensesame.widgets import sketchpad_widget
from libqtopensesame.dialogs import sketchpad_dialog
from PyQt4 import QtCore, QtGui

class sketchpad(libopensesame.sketchpad.sketchpad, feedpad.feedpad, \
	qtplugin.qtplugin):

	"""The GUI controls for the sketchpad"""

	def __init__(self, name, experiment, string=None):

		"""
		Constructor

		Arguments:
		name -- the name of the item
		experiment -- an instance of libopensesame.experiment

		Keyword arguments:
		string -- a string with the item definition (default = None)
		"""

		libopensesame.sketchpad.sketchpad.__init__(self, name, experiment, \
			string)
		qtplugin.qtplugin.__init__(self)

	def apply_edit_changes(self):

		"""Apply changes to the controls"""
		
		if not qtplugin.qtplugin.apply_edit_changes(self, False) or self.lock:
			return False
		self.experiment.main_window.refresh(self.name)
		return True			

	def edit_widget(self):

		"""Update the controls based on the items settings"""
		
		self.lock = True
		qtplugin.qtplugin.edit_widget(self)
		self.lock = False
		self.tools_widget.refresh()
		return self._edit_widget		

	def init_edit_widget(self):

		"""Construct the edit widget that contains the controls"""

		qtplugin.qtplugin.init_edit_widget(self, False)		
		self.add_line_edit_control('duration', 'Duration',
			tooltip='A numeric value (duration in milliseconds), "keypress", or "mouseclick"' \
			)
		self.popout_button = QtGui.QPushButton(self.experiment.icon(self.item_type), "Open editor in new window")
		self.popout_button.setIconSize(QtCore.QSize(16,16))
		self.popout_button.setToolTip("Open the sketchpad editor in a new window")
		QtCore.QObject.connect(self.popout_button, QtCore.SIGNAL("clicked()"), self.popout)
		self.add_control('', self.popout_button, 
			'Open the sketchpad editor in a new window')
		self.tools_widget = sketchpad_widget.sketchpad_widget(self)
		self.edit_vbox.addWidget(self.tools_widget)

