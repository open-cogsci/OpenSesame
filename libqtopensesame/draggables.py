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

import sip
from PyQt4 import QtGui, QtCore

class draggable_handle(QtGui.QPushButton):

	def __init__(self, item, parent=None):

		item_type = parent._list.sequence.experiment.items[item[0]].item_type
		QtGui.QPushButton.__init__(self, parent._list.sequence.experiment.icon("handle"), "", parent)        
		self.setAcceptDrops(True)
		self.setFlat(True)
		self.setCursor(QtCore.Qt.OpenHandCursor)
		self.container = parent
		self.setIconSize(QtCore.QSize(16,32))
		self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		
	def index_from_mime_data(self, mime_data):
	
		if mime_data.hasText():
			l = mime_data.text().split(" ")
			if len(l) == 2 and l[0] == "__osdrag__":
				try:
					return int(l[1])
				except:
					pass
		return -1
					
	def dragEnterEvent(self, e):
	
		if self.index_from_mime_data(e.mimeData()) >= 0:		
			e.accept()						
		else:
			e.ignore()

	def dropEvent(self, e):
	
		from_index = self.index_from_mime_data(e.mimeData())
		if from_index >= 0:
			e.accept()
			self.container._list.sequence.swap(from_index, self.container.index)
		else:
			e.ignore()
		
	def mouseMoveEvent(self, e):
	
		mime_data = QtCore.QMimeData()
		mime_data.setText("__osdrag__ %d" % self.container.index)		
		drag = QtGui.QDrag(self)
		drag.setMimeData(mime_data)
		drag.setHotSpot(e.pos() - self.rect().topLeft())
		dropAction = drag.start(QtCore.Qt.MoveAction)
		self.setDown(False)
		
class remove_button(QtGui.QPushButton):

	def __init__(self, parent):

		QtGui.QPushButton.__init__(self, parent._list.sequence.experiment.icon("delete"), "", parent)
		self.container = parent	
		self.setFlat(True)
		self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		self.clicked.connect(self.remove)
		
	def remove(self):
	
		self.container._list.sequence.delete(self.container.index)
		
class run_if_edit(QtGui.QLineEdit):

	def __init__(self, parent):
	
		QtGui.QLineEdit.__init__(self, parent.item[1])
		self.container = parent	
		self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)		
		self.editingFinished.connect(self.change)
		
	def change(self):
	
		self.container._list.sequence.set_run_if(self.container.index, self.text())
							
class draggable_widget_container(QtGui.QFrame):

	def __init__(self, parent, item, index):
	
		QtGui.QFrame.__init__(self, parent)
		self.item = item
		self.setFrameStyle(QtGui.QFrame.Panel)
		self._list = parent
		self.handle = draggable_handle(self.item, self)
		
		self.remove_button = remove_button(self)
		self.run_if_edit = run_if_edit(self)
		
		self.index = index
		self._layout = QtGui.QHBoxLayout()		
		self._layout.addWidget(self.handle)
		self._layout.addWidget(QtGui.QLabel(self.item[0]))
		self._layout.addWidget(self.run_if_edit)
		self._layout.addWidget(self.remove_button)
		self.setLayout(self._layout)	
		self._layout.setContentsMargins(2, 2, 2, 2)

class draggable_list(QtGui.QWidget):

	def __init__(self, sequence):
	
		QtGui.QWidget.__init__(self)
		self.items = []
		self.sequence = sequence
		self._layout = QtGui.QVBoxLayout()				
		self._layout.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self._layout)
		self.widgets = []	
				
	def refresh(self):
	
		for widget in self.widgets:
			self._layout.removeWidget(widget)
			widget.hide()
			del widget
		self.widgets = []
		
		for i in range(len(self.sequence.items)):
			widget = draggable_widget_container(self, self.sequence.items[i], i)
			self.widgets.append(widget)
			self._layout.addWidget(widget)
		

