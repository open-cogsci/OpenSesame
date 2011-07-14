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
import libqtopensesame.sketchpad_widget

class sketchpad_dialog(QtGui.QDialog):

	"""
	This dialog is the pop-out version of the sketchpad_widget
	"""

	def __init__(self, parent, sketchpad):
	
		QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCloseButtonHint)
		self.sketchpad = sketchpad
		self.tools_widget = libqtopensesame.sketchpad_widget.sketchpad_widget(self.sketchpad, parent = self, embed = False)					
		
		self.close_button = QtGui.QPushButton(self.sketchpad.experiment.icon("close"), "Close")
		self.close_button.setIconSize(QtCore.QSize(16,16))
		QtCore.QObject.connect(self.close_button, QtCore.SIGNAL("clicked()"), self.accept)	
		
		self.hbox = QtGui.QHBoxLayout()
		self.hbox.addStretch()
		self.hbox.addWidget(self.close_button)
		self.hbox.setContentsMargins(0, 0, 0, 0)
		
		self.hbox_widget = QtGui.QWidget()
		self.hbox_widget.setLayout(self.hbox)
		
		self.vbox = QtGui.QVBoxLayout()
		self.vbox.addWidget(self.tools_widget)
		self.vbox.addWidget(self.hbox_widget)			
		
		self.setLayout(self.vbox)
