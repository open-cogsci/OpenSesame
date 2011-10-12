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
from libqtopensesame import item_context_menu

drop_target = None

class draggable_handle(QtGui.QLabel):

	"""The draggable handles for re-ordering the list"""

	def __init__(self, parent=None):
	
		"""
		Constructor
		
		Keywords arguments:
		parent -- the parent widget
		"""

		QtGui.QLabel.__init__(self)
		self.setPixmap(QtGui.QPixmap(parent._list.sequence.experiment.resource("handle.png")))
		self.setAcceptDrops(True)
		self.setCursor(QtCore.Qt.OpenHandCursor)
		self.container = parent
		self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		self.setToolTip("Drag this item to re-order")
		
	def valid_drag(self, mime_data):
	
		"""
		Checks if mime data corresponds to a valid drag operation
		
		Arguments:
		mime_data -- the mime data
		
		Returns:
		True or False		
		"""
	
		if mime_data.hasText():
			l = mime_data.text().split(" ")
			if len(l) == 2 and l[0] in ["__osdrag__", "__osnew__"]:
				return True
		return False
		
		
	def index_from_mime_data(self, mime_data):
	
		"""
		Extract the item index from a mime data
		
		Returns:
		An item index or -1 if the mime data was invalid
		"""
	
		if mime_data.hasText():
			l = mime_data.text().split(" ")
			if len(l) == 2 and l[0] == "__osdrag__":
				try:
					return int(l[1])
				except:
					pass
		return -1
					
	def dragEnterEvent(self, e):
	
		"""
		Handle incoming drags
		
		Arguments:
		e -- a QDragEvent		
		"""
		
		if self.valid_drag(e.mimeData()):
			e.accept()						
		else:
			e.ignore()

	def dropEvent(self, e):
	
		"""
		Handle incoming drops
		
		Arguments:
		e -- a QDragEvent		
		"""	
		
		global drop_target
			
		if self.valid_drag(e.mimeData()):		
			from_index = self.index_from_mime_data(e.mimeData())
			if from_index >= 0:		
				e.accept()
				self.container._list.sequence.move(from_index, self.container.index)
			else:
				drop_target = self.container._list.sequence.name, self.container.index, False
				e.setDropAction(QtCore.Qt.CopyAction)
				e.accept()
		else:
			e.ignore()
		
	def mouseMoveEvent(self, e):
	
		"""
		Start drags
		
		Arguments:
		e -- a QMouseEvent
		"""	
	
		mime_data = QtCore.QMimeData()
		mime_data.setText("__osdrag__ %d" % self.container.index)		
		drag = QtGui.QDrag(self)
		drag.setMimeData(mime_data)
		drag.setHotSpot(e.pos() - self.rect().topLeft())
		dropAction = drag.start(QtCore.Qt.MoveAction)
		
class run_if_edit(QtGui.QLineEdit):

	"""Item 'run if' edit"""

	def __init__(self, parent):
	
		"""
		Constructor
		
		Arguments:
		parent -- the parent container
		"""	
	
		QtGui.QLineEdit.__init__(self, parent.item[1])
		self.container = parent	
		self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)		
		self.editingFinished.connect(self.change)
		self.setToolTip("Run this item only under the following conditions")
		
	def change(self):
	
		"""Apply changes"""
	
		self.container._list.sequence.set_run_if(self.container.index, self.text())
		
class open_button(QtGui.QPushButton):
	
	"""A button containing the item icon and name"""

	def __init__(self, item, parent):
	
		"""
		Constructor
		
		Arguments:
		item -- the item tuple (name, run_if)
		parent -- the parent container
		"""				
	
		item_type = parent._list.sequence.experiment.items[item[0]].item_type
		icon = parent._list.sequence.experiment.icon(item_type)
		QtGui.QPushButton.__init__(self, icon, item[0], parent)
		self.setObjectName("sequence_open_button")
		self.container = parent
		self.item = item
		self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		self.setFlat(True)
		self.setIconSize(QtCore.QSize(32,16))
		self.clicked.connect(self.open_item_tab)
		self.setToolTip("Click to edit this item")
		
	def open_item_tab(self):
	
		"""Open the item's tab"""
		
		self.container._list.sequence.experiment.items[self.item[0]].open_tab()
		
	def mousePressEvent(self, e):
	
		"""
		Open the tab on a left click and show the context menu on a right click
		
		Arguments:
		e -- a QMouseEvent
		"""
		
		if e.button() == QtCore.Qt.LeftButton:
			QtGui.QPushButton.mousePressEvent(self, e)
		elif e.button() == QtCore.Qt.RightButton:
			item = self.container._list.sequence.experiment.items[self.item[0]]
			m = item_context_menu.item_context_menu("Item", self, item,
				self.container._list.sequence.name, self.container.index)
			m.popup(e.globalPos())
									
class draggable_widget_container(QtGui.QFrame):

	"""A container for a single item"""

	def __init__(self, parent, item, index):
	
		"""
		Constructor
		
		Arguments:
		parent -- the parent draggable_list
		item -- the item tuple (name, run_if)
		index -- the index of the item in the sequence
		"""
	
		QtGui.QFrame.__init__(self, parent)
		self.setObjectName("sequence_container")
		self.item = item
		self.setFrameStyle(QtGui.QFrame.Panel)
		self._list = parent
		self.handle = draggable_handle(self)		
		self.run_if_edit = run_if_edit(self)		
		self.index = index
		self._layout = QtGui.QHBoxLayout()		
		self._layout.addWidget(self.handle)
		self._layout.addWidget(open_button(item, self))
		self._layout.addStretch()
		self._layout.addWidget(QtGui.QLabel("<small><i>Run if</i></small>"))
		self._layout.addWidget(self.run_if_edit)
		self.setLayout(self._layout)	
		self._layout.setContentsMargins(4, 4, 4, 4)
		self.setMinimumSize(100,32)
		self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, \
			QtGui.QSizePolicy.Fixed)

class draggable_list(QtGui.QWidget):

	"""The main draggable list"""

	def __init__(self, sequence):
	
		"""
		Constructor
		
		Arguments:
		sequence -- the parent sequence item
		"""
	
		QtGui.QWidget.__init__(self)
		self.items = []
		self.sequence = sequence
		self._layout = QtGui.QVBoxLayout()				
		self._layout.setContentsMargins(4, 4, 4, 16)
		self._layout.setSpacing(0)
		self.setLayout(self._layout)
		self.widgets = []
		self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, \
			QtGui.QSizePolicy.MinimumExpanding)
				
	def refresh(self):
	
		"""Refresh the view"""
		
		for widget in self.widgets:
			self._layout.removeWidget(widget)
			widget.hide()
			del widget
		self.widgets = []
		
		for i in range(len(self.sequence.items)):
			item_name = self.sequence.items[i][0]
			if  item_name not in self.sequence.experiment.items:
				self.sequence.experiment.notify("Unkown item '%s' in sequence '%s'. You can fix this using the script editor." \
					% (item_name, self.sequence.name))
			else:				
				widget = draggable_widget_container(self, self.sequence.items[i], i)
				self.widgets.append(widget)
				self._layout.addWidget(widget)
				
		spacer = QtGui.QWidget()
		self.widgets.append(spacer)
		self._layout.addWidget(spacer)
		

