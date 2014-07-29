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
		self.setIcon(0, self.experiment.icon(item.item_type))
		self.name = item.name
		self._droppable = True
		self._draggable = True
		self._lock = False
		self.setToolTip(0, tooltip)

	def open_tab(self):

		self.item.open_tab()

	def rename(self, to_name):

		"""
		desc:
			Renames the item that belongs to this tree item, and refreshes the
			ui accordingly.

		arguments:
			to_name:
				desc:	The new name of the item.
				type:	unicode
		"""

		if self._lock:
			return
		self._lock = True
		if self.experiment.items.rename(self.name, to_name):
			self.name = to_name
			self.setText(0, self.name)
		self._lock = False

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

		from libqtopensesame.widgets.item_context_menu import item_context_menu
		menu = item_context_menu(u'Item', self, self.item)
		menu.popup(pos)

	def rename(self, from_name, to_name):

		super(tree_item_item, self).rename(from_name, to_name)
		if unicode(self.text(0)) == from_name:
			self.setText(0, to_name)

