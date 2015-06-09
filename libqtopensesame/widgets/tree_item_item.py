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
from libqtopensesame.misc import _
from libqtopensesame.widgets.tree_base_item import tree_base_item

class tree_item_item(tree_base_item):

	"""
	desc:
		Corresponds to an item widget in the overview area.
	"""

	def __init__(self, item, extra_info=None, parent_item=None, index=None):

		"""
		desc:
			Constructor.

		arguments:
			item:
				desc:	An item.
				type:	qtitem

		keywords:
			extra_info:
				desc:	Extra info that is shown in the second column. Not shown
						in overview mode.
				type:	[NoneType, unicode]
		"""

		super(tree_item_item, self).__init__()
		self.setup(item.main_window)
		self.item = item
		tooltip = _(u"Type: %s\nDescription: %s") % (item.item_type,
			item.description)
		self.setText(0, item.name)
		if extra_info != None:
			self.setText(1, extra_info)
		self.setFlags(QtCore.Qt.ItemIsEditable | self.flags())
		self.setIcon(0, self.experiment.icon(item.item_icon()))
		self.name = item.name
		self._droppable = True
		self._draggable = True
		self._lock = False
		self.setToolTip(0, tooltip)

	@property
	def open_tab(self):
		return self.item.open_tab

	@property
	def close_tab(self):
		return self.item.close_tab

	def has_append_menu(self):

		return self.item.item_type == u'sequence'
	
	def ancestry(self):

		"""
		desc:
			Gets the full ancestry of a tree item, i.e. a sequence of items that
			are above the item in the hierarchy. The index of the item in the
			parent is indicated by a ':'. The index is 0 in the case of most
			items, but is mostly necessary for indicating the position in
			sequence items.

			For example:

				fixdot:2.trial_sequence:0.block_loop:0.experiment:0

		arguments:
			treeitem:
				desc:	The tree item that contains the item.
				type:	QTreeWidgetItem

		returns:
			desc:	A (item name, ancestry) tuple. For example:

						(u'trial_sequence',
						u'trial_sequence:0.block_loop:0.experiment:0')

			type:	tuple
		"""

		treeitem = self
		item_name = unicode(treeitem.text(0))
		l = []
		while True:
			if treeitem.parent() != None:
				index = treeitem.parent().indexOfChild(treeitem)
			else:
				index = 0
			l.append(unicode(treeitem.text(0))+u':'+unicode(index))
			treeitem = treeitem.parent()
			if treeitem == None or not treeitem.droppable:
				break
		return item_name, u'.'.join(l)

	def show_context_menu(self, pos):

		"""
		desc:
			Pops up the item context menu.

		arguments:
			pos:
				desc:	The cursor position.
				type:	QPoint
		"""

		from libqtopensesame.widgets.item_context_menu import item_context_menu
		menu = item_context_menu(self.main_window, self)
		menu.popup(pos)

	def rename(self, from_name, to_name):

		"""
		desc:
			Renames an item.

		arguments:
			from_name:
				desc:	The old item name.
				type:	unicode
			to_name:
				desc:	The new item name.
				type:	unicode
		"""

		super(tree_item_item, self).rename(from_name, to_name)
		if unicode(self.text(0)) == from_name:
			self.setText(0, to_name)
			self.name = to_name

	def start_rename(self):

		"""
		desc:
			Goes into edit mode for the item's name.
		"""

		self.treeWidget().editItem(self, 0)

	def start_edit_runif(self):

		"""
		desc:
			Goes into edit mode for the item's run-if statement. This is only
			applicable to sequences, i.e. not if the treewidget is in overview
			mode.
		"""

		if not self.treeWidget().overview_mode:
			self.treeWidget().editItem(self, 1)

	def set_icon(self, name, icon):

		"""See tree_base_item."""

		super(tree_item_item, self).set_icon(name, icon)
		if unicode(self.text(0)) == name:
			self.setIcon(0, self.theme.qicon(icon))

	def drop_hint(self):

		if self.treeWidget().overview_mode or self.parent() == None:
			if self.item.item_type == u'loop':
				return _(u'Set as item to run for %s') % self.name
			if self.item.item_type == u'sequence':
				return _(u'Insert into %s') % self.name
		return _(u'Drop below %s') % self.name

	def is_deletable(self):

		"""
		returns:
			desc:	True if the item for this treeitem can be deleted, False
					otherwise.
			type:	bool
		"""

		return hasattr(self.parent(), u'item')

	def is_cloneable(self):

		"""
		returns:
			desc:	True if the item for this treeitem can be cloned, False
					otherwise. An item can be cloned if it is in a sequence.
			type:	bool
		"""

		if not hasattr(self.parent(), u'item'):
			return False
		if not getattr(self.parent(), u'item').item_type == u'sequence':
			return False
		return True

	def delete(self):

		"""
		desc:
			Deletes the item, if possible.
		"""

		if not self.is_deletable():
			return
		index = self.parent().indexOfChild(self)
		parent_item = self.parent().item
		parent_item.remove_child_item(self.item.name, index)
		parent_item.update()
		self.experiment.build_item_tree()

	def permanently_delete(self):

		"""
		desc:
			Permanently deletes the item, if possible.
		"""

		if not self.is_deletable():
			return
		if QtGui.QMessageBox.question(self.treeWidget(),
			_(u'Permanently delete item'),
			_(u'Are you sure you want to permanently delete <b>%s</b>? All linked copies of <b>%s</b> will be deleted. You will not be able to undo this.') \
			% (self.name, self.name),
			buttons=(QtGui.QMessageBox.Yes|QtGui.QMessageBox.No),
			defaultButton=QtGui.QMessageBox.No) \
			!= QtGui.QMessageBox.Yes:
			return
		del self.item_store[self.name]
		self.close_tab()
		self.experiment.build_item_tree()

	def copy(self):

		"""
		desc:
			Copy the item to the clipboard in json text format.
		"""

		import json

		data = {
			u'type'				: u'item-new',
			u'item-name'		: self.item.name,
			u'item-type'		: self.item.item_type,
			u'ancestry'			: u'',
			u'script'			: self.item.to_string()
			}
		text = json.dumps(data).decode('utf-8')
		QtGui.QApplication.clipboard().setText(text)

	def clipboard_data(self):

		"""
		desc:
			Gets an item data dictionary from the clipboard.

		returns:
			desc:	A data dictionary or None if no valid data was found.
			type:	[dict, NoneType]
		"""

		import json
		from libqtopensesame.misc import drag_and_drop

		text = unicode(QtGui.QApplication.clipboard().text())
		try:
			data = json.loads(text)
		except:
			return None
		if drag_and_drop.matches(data, [u'item-new']):
			return data
		return None

	def paste(self):

		"""
		desc:
			Pastes clipboard data onto the current item, if possible.
		"""

		data = self.clipboard_data()
		if data != None:
			self.treeWidget().drop_event_item_new(data, target_treeitem=self)

	def create_linked_copy(self):

		if not self.is_cloneable():
			return
		index = self.parent().indexOfChild(self)
		parent_item = self.parent().item
		parent_item.insert_child_item(self.item.name, index+1)
		parent_item.update()
		self.experiment.build_item_tree(select=self.item.name)

	def create_unlinked_copy(self):

		if not self.is_cloneable():
			return
		index = self.parent().indexOfChild(self)
		item = self.item_store.unlinked_copy(self.item)
		parent_item = self.parent().item
		parent_item.insert_child_item(item.name, index+1)
		parent_item.update()
		self.experiment.build_item_tree(select=item.name)
