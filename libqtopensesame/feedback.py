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
import libqtopensesame.sketchpad_widget
from PyQt4 import QtCore, QtGui

class feedback(libopensesame.feedback.feedback, libqtopensesame.qtitem.qtitem):

	def __init__(self, name, experiment, string = None):
	
		"""
		Initialize the experiment		
		"""
		
		libopensesame.feedback.feedback.__init__(self, name, experiment, string)
		libqtopensesame.qtitem.qtitem.__init__(self)
		
	def apply_edit_changes(self):
	
		"""
		Apply changes to the edit widget
		"""
		
		libqtopensesame.qtitem.qtitem.apply_edit_changes(self)
		
		dur = str(self.edit_duration.text()).strip()
		if dur.strip() != "":
			self.set("duration", dur)
			
		self.experiment.main_window.refresh(self.name)		
				
	def popout(self):
	
		"""
		Opens a new window for the editor
		"""
		
		a = libqtopensesame.sketchpad_dialog.sketchpad_dialog(self.experiment.ui.centralwidget, self);
		a.exec_()
		self.apply_edit_changes()	
		
	def static_items(self):
		
		"""
		Returns all items that do not contain variables
		in their definitions, except for text items, which
		are always returned.
		"""
		
		l = []
		for item in self.items:
		
			static = True
			for var in item:
				if var != "text" and type(item[var]) == str and item[var].find("[") >= 0:
					static = False
			if static:
				l.append(item)
		return l			

	def init_edit_widget(self):
	
		"""
		Build the edit widget
		"""
		
		libqtopensesame.qtitem.qtitem.init_edit_widget(self, False)
		
		row = 0
		
		self.edit_grid.addWidget(QtGui.QLabel("Duration"), row, 0)
		self.edit_duration = QtGui.QLineEdit()
		QtCore.QObject.connect(self.edit_duration, QtCore.SIGNAL("editingFinished()"), self.apply_edit_changes)
		self.edit_grid.addWidget(self.edit_duration, row, 1)

		row += 1
		self.popout_button = QtGui.QPushButton(self.experiment.icon(self.item_type), "Open editor in new window")
		self.popout_button.setIconSize(QtCore.QSize(16, 16))
		QtCore.QObject.connect(self.popout_button, QtCore.SIGNAL("clicked()"), self.popout)		
		self.edit_grid.addWidget(self.popout_button, row, 0)				
		
		self.tools_widget = libqtopensesame.sketchpad_widget.sketchpad_widget(self)		
		self.edit_vbox.addWidget(self.tools_widget)		
									
	def edit_widget(self):
	
		"""
		Refresh and return the edit widget
		"""

		libqtopensesame.qtitem.qtitem.edit_widget(self)

		if self.has("duration"):
			dur = self.get("duration")
		else:
			dur = ""		
		self.edit_duration.setText(str(dur))	
		self.tools_widget.refresh()			
								
		return self._edit_widget
		
	def item_tree_info(self):
	
		"""
		Returns an info string for the item tree widget
		
		Returns:
		An info string
		"""
		
		if type(self.duration) == int:
			return "%s ms" % self.duration
		return "%s" % self.duration				
