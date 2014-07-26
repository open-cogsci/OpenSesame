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
from libqtopensesame.misc import drag_and_drop
from libqtopensesame.misc.base_subcomponent import base_subcomponent
from libqtopensesame.widgets import draggables, item_context_menu
from libopensesame import debug

class tree_overview(base_subcomponent, QtGui.QTreeWidget):

	"""
	desc:
		The overview area.
	"""

	def __init__(self, parent):

		"""
		desc:
			Constructor.

		arguments:
			parent:
				desc:	The parent widget.
				type:	QWidget
		"""

		super(tree_overview, self).__init__(parent)

	def mousePressEvent(self, e):

		"""
		desc:
			Initiates a drag event after a mouse press.

		arguments:
			e:
				desc:	A mouse event.
				type:	QMouseEvent
		"""

		super(tree_overview, self).mousePressEvent(e)
		if e.buttons() != QtCore.Qt.LeftButton:
			return
		# Get item and open tab.
		target_treeitem = self.itemAt(e.pos())
		self.main_window.open_item(target_treeitem)
		# Ignore drops on non-droppable tree items.
		if not self.droppable_treeitem(target_treeitem):
			e.ignore()
			return
		# Get the target item
		target_item_name = unicode(target_treeitem.text(0))
		data = {
			u'type'				: u'item-clone',
			u'item-name'		: target_item_name,
			u'QTreeWidgetItem'	: `target_treeitem`,
			}
		drag_and_drop.send(self, data)

	def droppable_treeitem(self, treeitem):

		"""
		desc:
			Determines if a tree item is able to accept drops.

		arguments:
			treeitem:
				desc:	A tree item.
				type:	QTreeWidgetItem

		returns:
			desc:	A bool indicating if the tree item is droppable.
			type:	bool
		"""

		# Do not accept drops on nothing or drops on top-level tree-items, which
		# are the experiment and unused items bin.
		if treeitem == None or treeitem.parent() == None:
			return False
		return True

	def drop_event_item_clone(self, data, e):

		"""
		desc:
			Handles drop events for item moves.

		arguments:
			data:
				desc:	A drop-data dictionary.
				type:	dict:
			e:
				desc:	A drop event.
				type:	QDropEvent
		"""

		target_treeitem = self.itemAt(e.pos())
		if not self.droppable_treeitem(target_treeitem):
			e.ignore()
			return
		print data
		target_item_name = unicode(target_treeitem.text(0))
		# Don't accept drops on the same item
		if `target_treeitem` == data[u'QTreeWidgetItem']:
			e.ignore()
			return
		# Check for recursion, i.e. check if the source item name is also in
		# the parent hierarchy.
		parent_treeitem = target_treeitem.parent()
		while parent_treeitem.parent() != None:
			if unicode(parent_treeitem.text(0)) == data[u'item-name']:
				e.ignore()
				return
			parent_treeitem = parent_treeitem.parent()
		self.drop_event_item_create(data, e)

	def drop_event_item_create(self, data, e):

		"""
		desc:
			Handles drop events for item creation.

		arguments:
			data:
				desc:	A drop-data dictionary.
				type:	dict:
			e:
				desc:	A drop event.
				type:	QDropEvent
		"""

		# Ignore drops on non-droppable tree items.
		target_treeitem = self.itemAt(e.pos())
		if not self.droppable_treeitem(target_treeitem):
			e.ignore()
			return
		# Get the target item
		target_item_name = unicode(target_treeitem.text(0))
		target_item = self.experiment.items[target_item_name]
		# If a drop has been made on a loop, tell the loop to accept a new item.
		if target_item.item_type == u'loop':
			if data[u'type'] == u'item-create':
				target_item.set_new_item(data[u'item-type'])
			else:
				target_item.set_existing_item(data[u'item-name'])
		# If a drop has been made on a sequence, append the item to the
		# sequence.
		elif target_item.item_type == u'sequence':
			if data[u'type'] == u'item-create':
				target_item.insert_new_item(data[u'item-type'])
			else:
				target_item.insert_existing_item(data[u'item-name'])
		else:
			parent_treeitem = target_treeitem.parent()
			parent_item_name = unicode(parent_treeitem.text(0))
			parent_item = self.experiment.items[parent_item_name]
			# If a drop has been made on an item that has a loop as parent,
			# tell the parent loop to accept a new item.
			if parent_item.item_type == u'loop':
				if data[u'type'] == u'item-create':
					parent_item.set_new_item(data[u'item-type'])
				else:
					parent_item.set_existing_item(data[u'item-name'])
			# If a drop has been made on an item that has a sequence as parent,
			# tell the parent sequence to accept a new item after the position
			# of the drop target.
			elif parent_item.item_type == u'sequence':
				index = parent_treeitem.indexOfChild(target_treeitem)
				if data[u'type'] == u'item-create':
					parent_item.insert_new_item(data[u'item-type'], index=index)
				else:
					parent_item.insert_existing_item(data[u'item-name'],
						index=index)
		e.accept()

	def dropEvent(self, e):

		"""
		desc:
			Handles drop events for file opening and item creation.

		arguments:
			e:
				desc:	A drop event.
				type:	QDropEvent
		"""

		data = drag_and_drop.receive(e)
		if data[u'type'] == u'item-create':
			self.drop_event_item_create(data, e)
		elif data[u'type'] == u'item-clone':
			self.drop_event_item_clone(data, e)
		elif data[u'type'] == u'url-local':
			self.main_window.open_file(path=data[u'url'])
		else:
			e.ignore()

	def dragEnterEvent(self, e):

		"""
		desc:
			Handles drag-enter events to see if the item tree can handle
			incoming drops.

		arguments:
			e:
				desc:	A drag-enter event.
				type:	QDragEnterEvent
		"""

		data = drag_and_drop.receive(e)
		if data[u'type'] in (u'item-create', u'item-clone', u'url-local'):
			e.accept()
		else:
			e.ignore()

	def dragMoveEvent(self, e):

		"""
		desc:
			Handles drag-move events to see if the item tree can handle
			incoming drops.

		arguments:
			e:
				desc:	A drag-move event.
				type:	QDragMoveEvent
		"""

		data = drag_and_drop.receive(e)
		if data[u'type'] == u'url-local':
			e.accept()
		elif data[u'type'] in (u'item-create', u'item-clone'):
			if not self.droppable_treeitem(self.itemAt(e.pos())):
				e.ignore()
			else:
				e.accept()
		else:
			e.ignore()

	def context_menu(self, item, pos=None):

		"""
		Present a context menu for an item.

		Arguments:
		item -- a QTreeWidgetItem

		Keyword arguments:
		A position for the top-left of the menu (default=None)
		"""

		target_item = item
		item_name = unicode(target_item.text(0))
		parent_item = target_item.parent()
		if parent_item != None:
			parent_name = unicode(parent_item.text(0))
		else:
			parent_name = None
		index = None
		if parent_name in self.main_window.experiment.items:
			parent_type = \
				self.main_window.experiment.items[parent_name].item_type

			# If the parent is a sequence, get the position of the item in the
			# sequence, because the name by itself is ambiguous since the name
			# may occur multiple times in one sequence
			if parent_type == u'sequence':
				index = 0
				for index in range(parent_item.childCount()):
					child = parent_item.child(index)
					if child == target_item:
						break
					index += 1

		if item_name not in self.main_window.experiment.items:
			return
		item = self.main_window.experiment.items[item_name]
		m = item_context_menu.item_context_menu("Item", self, item, \
			parent_name, index)

		if pos == None:
			m.popup(self.mapToGlobal(self.pos()))
		else:
			m.popup(pos)

	def contextMenuEvent(self, e):

		"""
		Show a context menu at the cursor position

		Arguments:
		e -- the content menu event
		"""

		item = self.itemAt(e.pos())
		self.context_menu(item, e.globalPos())


	def keyPressEvent(self, e):

		"""
		Capture key presses to auto-activate selected items

		Arguments:
		e -- a QKeyEvent
		"""

		QtGui.QTreeWidget.keyPressEvent(self, e)
		if e.key() in [QtCore.Qt.Key_Up, QtCore.Qt.Key_Down, \
			QtCore.Qt.Key_PageUp, QtCore.Qt.Key_PageDown, QtCore.Qt.Key_Home, \
			QtCore.Qt.Key_End, QtCore.Qt.Key_Return]:
			self.main_window.open_item(self.currentItem())
		elif e.key() == QtCore.Qt.Key_Space:
			self.context_menu(self.currentItem())

	def recursive_children(self, item):

		"""
		Get a list of unused items from the itemtree

		Returns:
		A list of items (strings) that are children of the parent item
		"""

		children = []
		for i in range(item.childCount()):
			child = item.child(i)
			children.append(unicode(child.text(0)))
			children += self.recursive_children(child)
		return children

	def unused_items(self):

		"""
		Get a list of unused items

		Returns:
		A list of unused items (names as strings)
		"""

		return self.main_window.ui.itemtree.recursive_children( \
			self.main_window.ui.itemtree.topLevelItem( \
				self.main_window.ui.itemtree.topLevelItemCount()-1))

