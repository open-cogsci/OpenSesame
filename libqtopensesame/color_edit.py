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

class color_edit(QtGui.QWidget):

	"""A QWidget with a QLineEdit and a QPushButton that pops up a colorpicker"""

	def __init__(self, experiment, parent=None):
	
		"""
		Constructor
		
		Arguments:
		experiment -- the experiment
		
		Keywords arguments:
		parent -- the parent QWidget (default=None)		
		"""
	
		QtGui.QWidget.__init__(self, parent)		
		self.experiment = experiment
		self.edit = QtGui.QLineEdit()
		self.edit.editingFinished.connect(self.apply)
		self.button = QtGui.QPushButton()
		self.button.setIcon(self.experiment.icon("colorpicker"))
		self.button.setIconSize(QtCore.QSize(16,16))		
		self.button.clicked.connect(self.colorpicker)
		layout = QtGui.QHBoxLayout()				
		layout.setContentsMargins(0,0,0,0)
		layout.addWidget(self.edit)
		layout.addWidget(self.button)
		self.setLayout(layout)						

	def colorpicker(self):
	
		"""Pick a color with the colorpicker dialog"""
	
		color = self.experiment.colorpicker(self.experiment.sanitize(self.text()))
		if color == None:
			return
		self.setText(color)
		self.apply()

	def text(self):
	
		"""
		Return the text (emulate QLineEdit behavior)
		
		Returns:
		A QString
		"""
	
		return self.edit.text()
		
	def setText(self, s):
	
		"""
		Set the text (emulate QLineEdit behavior)
		
		Arguments:
		s -- the text
		"""
	
		self.edit.setText(s)
		
	def apply(self):
	
		"""Emit a 'set_color' signal to indicate that a color has been picker"""		
		
		self.emit(QtCore.SIGNAL("set_color"))
