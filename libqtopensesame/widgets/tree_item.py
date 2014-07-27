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
from libqtopensesame.misc.base_subcomponent import base_subcomponent

class tree_item(base_subcomponent, QtGui.QTreeWidgetItem):

	"""
	desc:
		Corresponds to an item widget in the overview area.
	"""

	__droppable__ = True

	def __init__(self, item):

		"""
		desc:
			Constructor.

		arguments:
			item:
				desc:	An item.
				type:	qtitem
		"""

		super(tree_item, self).__init__()
		self.setup(item.main_window)
		self.item = item
		tooltip = _(u"Type: %s\nDescription: %s") % (item.item_type,
			item.description)
		self.setText(0, item.name)
		self.setIcon(0, self.experiment.icon(item.item_type))
		self.name = item.name
		self.setToolTip(0, tooltip)

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
			if not hasattr(treeitem.parent(), u'__droppable__'):
				break
			treeitem = treeitem.parent()
		return item_name, u'.'.join(l)

	def expand(self):

		"""
		desc:
			Expands this item and all items under it.
		"""

		self.setExpanded(True)
		for i in range(self.childCount()):
			self.child(i).expand()
