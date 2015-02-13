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
from libopensesame.sequence import sequence as sequence_runtime
from libqtopensesame.widgets.tree_item_item import tree_item_item
from libqtopensesame.widgets.tree_overview import tree_overview
from libqtopensesame.items.qtplugin import qtplugin
from libqtopensesame.items.qtstructure_item import qtstructure_item

class sequence(qtstructure_item, qtplugin, sequence_runtime):

	"""
	desc:
		GUI controls for the sequence item.
	"""

	def __init__(self, name, experiment, string=None):

		"""
		desc:
			Constructor.

		arguments:
			name:		The item name.
			experiment:	The experiment object.

		keywords:
			string:		A definition string.
		"""

		sequence_runtime.__init__(self, name, experiment, string)
		qtplugin.__init__(self)
		self.last_removed_child = None, None

	def init_edit_widget(self):

		"""See qtitem."""

		super(sequence, self).init_edit_widget(False)
		self.treewidget = tree_overview(self.main_window, overview_mode=False)
		self.treewidget.setup(self.main_window)
		self.treewidget.structure_change.connect(self.update)
		self.treewidget.text_change.connect(self.update_script)
		self.set_focus_widget(self.treewidget)
		self.edit_vbox.addWidget(self.treewidget)
		self.add_checkbox_control(u'flush_keyboard',
			u'Flush pending key presses at sequence start',
			u'Flush pending key presses at sequence start')

	def edit_widget(self):

		"""See qtitem."""

		super(sequence, self).edit_widget()
		self.treewidget.clear()
		self.toplevel_treeitem = self.build_item_tree(max_depth=2)
		self.treewidget.addTopLevelItem(self.toplevel_treeitem)
		self.toplevel_treeitem.setExpanded(True)
		self.treewidget.resizeColumnToContents(0)

	def rename(self, from_name, to_name):

		"""See qtitem."""

		qtplugin.rename(self, from_name, to_name)
		new_items = []
		for item, cond in self.items:
			if item == from_name:
				new_items.append( (to_name, cond) )
			else:
				new_items.append( (item, cond) )
		self.items = new_items
		self.treewidget.rename(from_name, to_name)

	def delete(self, item_name, item_parent=None, index=None):

		"""See qtitem."""

		if item_parent == None or (item_parent == self.name and index == None):
			redo = True
			while redo:
				redo = False
				for i in range(len(self.items)):
					if self.items[i][0] == item_name:
						self.items = self.items[:i]+self.items[i+1:]
						redo = True
						break
		elif item_parent == self.name and index != None:
			if self.items[index][0] == item_name:
				self.items = self.items[:index]+self.items[index+1:]

	def build_item_tree(self, toplevel=None, items=[], max_depth=-1,
		extra_info=None):

		"""See qtitem."""

		widget = tree_item_item(self, extra_info=extra_info)
		items.append(self.name)
		if max_depth < 0 or max_depth > 1:
			for item, cond in self.items:
				if item in self.experiment.items:
					self.experiment.items[item].build_item_tree(widget, items,
						max_depth=max_depth-1, extra_info=cond)
		if toplevel != None:
			toplevel.addChild(widget)
		else:
			widget.set_draggable(False)
		return widget

	def set_run_if(self, index, cond=u'always'):

		"""
		desc:
			Sets the run-if statement for an item at a specific index.

		arguments:
			index:
				desc:	The index of the item to change the run-if statement of.
				type:	int

		keywords:
			cond:
				desc:	The run-if statement.
				type:	unicode
		"""

		self.items[index] = self.items[index][0], cond

	def children(self):

		"""See qtitem."""

		_children = []
		for item, cond in self.items:
			if item not in self.experiment.items:
				continue
			_children += [item] + self.experiment.items[item].children()
		return _children

	def is_child_item(self, item):

		"""See qtitem."""

		for i, cond in self.items:
			if i == item or (i in self.experiment.items and \
				self.experiment.items[i].is_child_item(item)):
				return True
		return False

	def insert_child_item(self, item_name, index=0):

		"""See qtitem."""

		if item_name == self.last_removed_child[0]:
			# If this item was just removed, re-add it and preserve its run-if
			# statement.
			self.items.insert(index, self.last_removed_child)
		else:
			self.items.insert(index, (item_name, u'always'))
		self.main_window.set_unsaved(True)

	def remove_child_item(self, item_name, index=0):

		"""See qtitem."""

		if index < 0:
			items = []
			for item, cond in self.items:
				if item != item_name:
					items.append( (item, cond) )
			self.items = items
		elif len(self.items) > index and self.items[index][0] == item_name:
			# We remember the last removed child item, because we will re-use
			# it's run-if statement if it is re-added.
			self.last_removed_child = self.items[index]
			del self.items[index]
		self.main_window.set_unsaved(True)
