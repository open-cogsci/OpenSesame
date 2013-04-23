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

from PyQt4 import QtCore, QtGui
from libopensesame import debug

class color_edit(QtGui.QWidget):

	"""A colorpicker QWidget with a QLineEdit and a QPushButton."""

	def __init__(self, parent=None):
	
		"""
		Constructor.
		
		Arguments:
		experiment	--	The experiment object.
		
		Keywords arguments:
		parent		--	The parent QWidget. (default=None)
		"""
	
		QtGui.QWidget.__init__(self, parent)		
		self.edit = QtGui.QLineEdit()
		self.edit.editingFinished.connect(self.apply)
		self.editingFinished = self.edit.editingFinished
		self.button = QtGui.QPushButton()
		self.button.setIconSize(QtCore.QSize(16,16))		
		self.button.clicked.connect(self.colorpicker)
		layout = QtGui.QHBoxLayout()				
		layout.setContentsMargins(0,0,0,0)
		layout.addWidget(self.edit)
		layout.addWidget(self.button)
		self.setLayout(layout)						

	def colorpicker(self):
	
		"""Picks a color with the colorpicker dialog."""
	
		color = self.experiment.colorpicker(self.experiment.sanitize( \
			self.text()))
		if color == None:
			return
		self.setText(color)
		self.apply()		

	def text(self):
	
		"""
		Returns the text (emulate QLineEdit behavior).
		
		Returns:
		A QString.
		"""
	
		return self.edit.text()
		
	def setText(self, s):
	
		"""
		Sets the text (emulate QLineEdit behavior).
		
		Arguments:
		s	--	The text.
		"""
	
		self.edit.setText(s)
		
	def apply(self):
	
		"""Emit a 'set_color' signal to indicate that a color has been picker"""		
		
		self.emit(QtCore.SIGNAL(u'set_color'))
		
	def initialize(self, experiment, color=None):
	
		"""
		Initializes the widget.
		
		Arguments:
		experiment	--	The experiment object.
		
		Keyword arguments:
		color		--	A color to start with or None for experiment foreground
						default. (default=None)
		"""
		
		debug.msg(u'color = %s' % color)
		self.experiment = experiment
		if color == None:
			color = self.experiment.get(u'foreground', _eval=False)
		self.setText(color)
		self.button.setIcon(self.experiment.icon(u'colorpicker'))
		
