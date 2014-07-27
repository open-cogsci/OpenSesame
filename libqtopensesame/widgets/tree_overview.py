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
from libqtopensesame.widgets import item_context_menu
from libqtopensesame.widgets.tree_item import tree_item
from libopensesame import debug

class tree_overview(base_subcomponent, QtGui.QTreeWidget):

	"""
	desc:
		The overview area.
	"""

	def __init__(self, main_window, overview_mode=True):

		super(tree_overview, self).__init__(main_window)
		self.overview_mode = overview_mode
		self.setAcceptDrops(True)
		if self.overview_mode:
			self.setHeaderHidden(True)
		else:
			self.setHeaderHidden(False)

	def mousePressEvent(self, e):

		"""
		desc:
			Initiates a drag event after a mouse press, these are used to
			implement item moving, shallow copying, and deep copying.

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
		if self.overview_mode:
			self.main_window.open_item(target_treeitem)
		# Ignore drops on non-droppable tree items.
		if not self.droppable_treeitem(target_treeitem):
			e.ignore()
			return
		# Get the target item
		target_item_name, target_item_ancestry = target_treeitem.ancestry()
		if (QtCore.Qt.ControlModifier & e.modifiers()) and \
			(QtCore.Qt.ShiftModifier & e.modifiers()):
			target_item = self.experiment.items[target_item_name]
			data = {
				u'type'				: u'item-new',
				u'item-name'		: target_item.name,
				u'item-type'		: target_item.item_type,
				u'ancestry'			: target_item_ancestry,
				u'script'			: target_item.to_string()
				}
		else:
			data = {
				u'type'				: u'item-existing',
				u'item-name'		: target_item_name,
				u'ancestry'			: target_item_ancestry,
				}
		drag_and_drop.send(self, data)

	def parent_from_ancestry(self, ancestry):

		"""
		desc:
			Gets the parent item, and the index of the item in the parent, based
			on an item's ancestry, as returned by ancestry_from_treeitem.

		arguments:
			ancestry:
				desc:	An ancestry string.
				type:	unicode

		returns:
			desc:	A (parent item name, index) tuple.
			type:	tuple
		"""

		l = ancestry.split(u'.')
		if len(l) == 1:
			return None, None
		parent_item_name = l[1].split(u':')[0]
		index = int(l[0].split(u':')[1])
		return parent_item_name, index

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
		if treeitem == None or not hasattr(treeitem, u'__droppable__'):
			return False
		return True

	def drop_event_item_move(self, data, e):

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

		if not drag_and_drop.matches(data, [u'item-existing']):
			e.ignore()
			return
		target_treeitem = self.itemAt(e.pos())
		if not self.droppable_treeitem(target_treeitem):
			debug.msg(u'Drop ignored: target not droppable')
			e.ignore()
			return
		target_item_name, target_item_ancestry = target_treeitem.ancestry()
		if target_item_ancestry.endswith(data[u'ancestry']):
			debug.msg(u'Drop ignored: recursion prevented')
			e.ignore()
			return
		parent_item_name, index = self.parent_from_ancestry(data[u'ancestry'])
		if parent_item_name == None:
			debug.msg(u'Drop ignored: no parent')
			e.ignore()
			return
		if not QtCore.Qt.ControlModifier & e.keyboardModifiers():
			self.experiment.items[parent_item_name].remove_child_item(
				data[u'item-name'], index)
		self.drop_event_item_new(data, e)

	def drop_event_item_new(self, data, e):

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

		if not drag_and_drop.matches(data, [u'item-existing', u'item-new']):
			e.ignore()
			return
		# Ignore drops on non-droppable tree items.
		target_treeitem = self.itemAt(e.pos())
		if not self.droppable_treeitem(target_treeitem):
			e.ignore()
			return
		# Get the target item
		target_item_name = unicode(target_treeitem.text(0))
		target_item = self.experiment.items[target_item_name]
		# Get the item to be inserted. If the drop type is item-new, we need
		# to create a new item, otherwise we get an existin item.
		if data[u'type'] == u'item-new':
			item = self.experiment.items.new(data[u'item-type'],
				data[u'item-name'], data[u'script'])
		else:
			item = self.experiment.items[data[u'item-name']]
		# If a drop has been made on a loop or sequence, we can insert the new
		# item directly. We only do this in overview mode, because it is
		# confusing otherwise.
		if self.overview_mode and \
			target_item.item_type in [u'loop', u'sequence']:
			target_item.insert_child_item(item.name)
		# If the item has ni parent, also drop on it directly. This is the case
		# in sequence views of the overview area.
		elif target_treeitem.parent() == None:
			target_item.insert_child_item(item.name)
		# Otherwise, we find the parent of the target item, and insert the new
		# item at the correct position.
		else:
			parent_treeitem = target_treeitem.parent()
			parent_item_name = unicode(parent_treeitem.text(0))
			parent_item = self.experiment.items[parent_item_name]
			index = parent_treeitem.indexOfChild(target_treeitem)
			parent_item.insert_child_item(item.name, index)
		e.accept()
		self.main_window.refresh()

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
		if data[u'type'] == u'item-new':
			self.drop_event_item_new(data, e)
		elif data[u'type'] == u'item-existing':
			self.drop_event_item_move(data, e)
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
		if drag_and_drop.matches(data, [u'item-new', u'item-existing',
			u'url-local']):
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
		if drag_and_drop.matches(data, [u'url-local']):
			e.accept()
		elif drag_and_drop.matches(data, [u'item-new', u'item-existing']):
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
