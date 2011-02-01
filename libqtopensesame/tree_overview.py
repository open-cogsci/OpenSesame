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

class tree_overview(QtGui.QTreeWidget):

	"""
	This class implements the drag-and-droppable
	overview tree.
	"""

	def __init__(self, parent):
	
		"""
		Constructor
		"""
	
		QtGui.QTreeWidget.__init__(self, parent)
		
	def dragEnterEvent(self, e):
		
		"""
		Accept an incoming drag event
		"""
	
		if e.mimeData().hasText():	
			e.setDropAction(QtCore.Qt.CopyAction)
			e.accept()
		else:
			e.ignore()

	def dragMoveEvent(self, e):
	
		"""
		Highlight the appropriate item
		while a drop is being moved.
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
		"""
	
		if e.mimeData().hasText():	
			e.setDropAction(QtCore.Qt.CopyAction)
			
			item = self.itemAt(e.pos())
			if item != None:
				item.setSelected(True)
				self.drop_target = item
				e.accept()
			else:
				e.ignore()
		else:
			e.ignore()
			
	def contextMenuEvent(self, e):
	
		"""
		Show the context menu
		"""
		
		# Get the target item
		target_item = self.itemAt(e.pos())
		item_name = str(target_item.text(0))
		if item_name not in self.main_window.experiment.items:
			return
		item_type = self.main_window.experiment.items[item_name].item_type
		
		# Get the parent item
		parent_type = None
		parent_item = target_item.parent()
		parent_name = str(parent_item.text(0))
		if parent_name in self.main_window.experiment.items:
			parent_type = self.main_window.experiment.items[parent_name].item_type
			
			# If the parent is a sequence, get the position of the item in the
			# sequence, because the name by itself is ambiguous since the name
			# may occur multiple times in one sequence
			if parent_type == "sequence":
				for index in range(parent_item.childCount()):
					child = parent_item.child(index)
					if child == target_item:
						break
					index += 1
					
		# The menu text
		open_text = "Open %s" % item_name
		edit_text = "Edit script"
		rename_text = "Rename"
		delete_text = "Delete"		
		help_text = "%s help" % item_type.capitalize()

		# Build and show the context menu		
		menu = QtGui.QMenu()
		menu.addAction(self.main_window.experiment.icon(item_type), open_text)
		menu.addAction(self.main_window.experiment.icon("script"), edit_text)
		menu.addSeparator()
		menu.addAction(self.main_window.experiment.icon("rename"), rename_text)
		if parent_type == "sequence":
			menu.addAction(self.main_window.experiment.icon("delete"), delete_text)		
		menu.addSeparator()		
		menu.addAction(self.main_window.experiment.icon("help"), help_text)			
		action = menu.exec_(e.globalPos())
		
		# If no action was selected, just return
		if action == None:
			return
					
		# Otherwise handle the action
		action = str(action.text())		
		if action == open_text:
			self.main_window.experiment.items[item_name].open_edit_tab()
		elif action == edit_text:
			self.main_window.experiment.items[item_name].open_script_tab()
		elif action == rename_text:
			self.rename(item_name)
		elif action == help_text:
			self.main_window.experiment.items[item_name].open_help_tab()
		elif action == delete_text:
			self.main_window.experiment.items[parent_name].delete(index)
			
	def rename(self, old_name):
	
		"""
		Rename an item
		"""
	
		new_name, ok = QtGui.QInputDialog.getText(self.main_window.ui.centralwidget, "Rename", "Please enter a new name", text = old_name)
		new_name = str(new_name)
		if ok and new_name != old_name:
			if new_name in self.main_window.experiment.items:
				self.main_window.experiment.notify("An item named '%s' already exists!" % new_name)					
			else:			
				self.main_window.experiment.rename(old_name, new_name)

