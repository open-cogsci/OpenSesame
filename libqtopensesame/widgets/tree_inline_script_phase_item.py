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

from libopensesame.py3compat import *
from qtpy import QtCore, QtWidgets
from libqtopensesame.widgets.tree_base_item import tree_base_item

class tree_inline_script_phase_item(tree_base_item):

	"""
	desc:
		Corresponds to the tree item for a run or prepare phase.
	"""

	def __init__(self, inline_script, phase):

		"""
		desc:
			Constructor.
		"""

		super(tree_inline_script_phase_item, self).__init__()
		self.setup(inline_script.main_window)
		self.inline_script = inline_script
		self.phase = phase
		self.setText(0, phase)
		self.setIcon(0, self.theme.qicon(u'text-x-script'))
		self._droppable = False
		self._draggable = False
		self.expand()

	def open_tab(self):

		"""
		desc:
			Open the inline-script tab.
		"""

		self.inline_script.open_tab(select_in_tree=False)
		if self.phase == u'prepare':
			self.inline_script.qprogedit.selectTab(0)
		else:
			self.inline_script.qprogedit.selectTab(1)

	def clear(self):

		"""
		desc:
			Clears the symbols.
		"""

		tree_base_item.takeChildren(self)

	def add_symbol(self, symbol):

		"""
		desc:
			Adds a symbol.

		arguments:
			symbol:		A symbol
			type:		tree_inline_script_symbol_item
		"""

		tree_base_item.addChild(self, symbol)

	def clones(self):

		"""
		desc:
			Returns a list of all clones of this phase in the tree. This is
			necessary, because different QTreeWidgetItems correspond to
			shallow copies of the same item.

		returns:
			desc:	A list of clones.
			type:	list
		"""

		treewidget = self.treeWidget()
		if treewidget is None:
			return [self]
		l = treewidget.findItems(self.inline_script.name,
			QtCore.Qt.MatchFixedString|QtCore.Qt.MatchRecursive, 0)
		_clones = []
		for treeitem in l:
			if not hasattr(treeitem, u'symbols') or not treeitem.symbols:
				continue
			if self.phase == u'prepare':
				_clones.append(treeitem.child(0))
			else:
				_clones.append(treeitem.child(1))
		return _clones

	def takeChildren(self):

		"""
		desc:
			Implements QTreeWidgetItems.takeChildren for all clones of this
			object.
		"""

		for c in self.clones():
			c.clear()

	def addChild(self, child):

		"""
		desc:
			Implements QTreeWidgetItems.addChild for all clones of this
			object.

		arguments:
			child:	A child object.
			type:	QTreeWidgetItem
		"""

		for c in self.clones():
			c.add_symbol(child.clone())
