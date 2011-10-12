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
from libqtopensesame import draggables, item_context_menu


class tree_overview(QtGui.QTreeWidget):

	"""The drag-and-droppable overview tree"""

	def __init__(self, parent):
	
		"""
		Constructor
		
		Arguments:
		parent -- the parent item
		"""
	
		QtGui.QTreeWidget.__init__(self, parent)
		
	def dragEnterEvent(self, e):
		
		"""
		Accept an incoming drag event
		
		Arguments:
		e -- a QDragEvent
		"""
	
		if e.mimeData().hasText():	
			e.setDropAction(QtCore.Qt.CopyAction)
			e.accept()
		else:
			e.ignore()

	def dragMoveEvent(self, e):
	
		"""
		Highlight the appropriate item while a drop is being moved
		
		Arguments:
		e -- a QDragEvent		
		"""
	
		if e.mimeData().hasText():		
			e.setDropAction(QtCore.Qt.CopyAction)						
			for item in self.selectedItems():
				item.setSelected(False)			
			item = self.itemAt(e.pos())
			if item != None:
				item.setSelected(True)			
			e.accept()			
		else:		
			e.ignore()		

	def dropEvent(self, e):
	
		"""
		Accept a drop event
		
		Arguments:
		e -- a QDragEvent			
		"""
	
		if e.mimeData().hasText():	
			s = e.mimeData().text()
			e.setDropAction(QtCore.Qt.CopyAction)			
			item = self.itemAt(e.pos())
			
			if item == None:
				e.ignore()
				return			

			# Accept a drop on the toplevel item
			if item.parent() == None:
				draggables.drop_target = "__start__", None, True
				e.accept()
				return
				
			index = 0
			while True:			
				item_name = str(item.text(0))
				if item_name not in self.main_window.experiment.items:
					e.ignore()
					return
				item_type = self.main_window.experiment.items[item_name].item_type
				if item_type == "sequence":
					break
				index = item.parent().indexOfChild(item)
				item = item.parent()
			
			if item != None:
				item.setSelected(True)
				draggables.drop_target = item_name, index, True
				e.accept()
			else:
				e.ignore()
		else:
			e.ignore()
			
	def contextMenuEvent(self, e):
	
		"""
		Show a context menu
		
		Arguments:
		e -- the content menu event
		"""
	
		target_item = self.itemAt(e.pos())		
		item_name = str(target_item.text(0))
		parent_item = target_item.parent()
		if parent_item != None:
			parent_name = str(parent_item.text(0))		
		else:
			parent_name = None
		index = None
		if parent_name in self.main_window.experiment.items:
			parent_type = self.main_window.experiment.items[parent_name].item_type

			# If the parent is a sequence, get the position of the item in the
			# sequence, because the name by itself is ambiguous since the name
			# may occur multiple times in one sequence
			if parent_type == "sequence":
				index = 0
				for index in range(parent_item.childCount()):
					child = parent_item.child(index)
					if child == target_item:
						break
					index += 1
		
		if item_name not in self.main_window.experiment.items:
			return
		item = self.main_window.experiment.items[item_name]
		m = item_context_menu.item_context_menu("Item", self, item, parent_name, index)
		m.popup(e.globalPos())
								
