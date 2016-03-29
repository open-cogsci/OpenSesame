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
from libqtopensesame.misc.base_subcomponent import base_subcomponent
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'tree_base_item', category=u'core')

class tree_base_item(base_subcomponent, QtWidgets.QTreeWidgetItem):

	"""
	desc:
		A base class that corresponds to any widget in the overview area.
	"""

	def start_edit(self, col):

		self.treeWidget().editItem(self, col)

	def ancestry(self):

		return None

	def path(self):

		if self.parent() is None:
			return self.text(0)
		return self.parent().path() + u'.' + self.text(0)

	def children(self):

		l = []
		for i in range(self.childCount()):
			child = self.child(i)
			l += [child] + child.children()
		return l

	def show_context_menu(self, pos):

		pass

	def paste(self):

		pass

	def copy(self):

		pass

	def create_linked_copy(self):

		pass

	def create_unlinked_copy(self):

		pass

	def copy_linked(self):

		pass

	def copy_unlinked(self):

		pass

	def delete(self):

		pass

	def permanently_delete(self):

		pass

	def open_tab(self):

		pass

	def drop_hint(self):

		return None

	def droppable(self, data):

		return self._droppable

	def set_droppable(self, droppable):

		self._droppabe = droppable

	def draggable(self):

		return self._draggable

	def set_draggable(self, draggable):

		self._draggable = draggable

	def has_append_menu(self):

		return False

	def expand(self):

		"""
		desc:
			Expands this item and all items under it.
		"""

		self.setExpanded(True)
		for i in range(self.childCount()):
			self.child(i).expand()

	def collapse(self):

		"""
		desc:
			Collapses this item and all items under it.
		"""

		self.setExpanded(False)
		for i in range(self.childCount()):
			self.child(i).collapse()

	def rename(self, from_name, to_name):

		"""
		desc:
			Renames an item.

		arguments:
			from_name:
				desc:	The old name.
				type:	unicode
			to_name:
				desc:	The new name.
				type:	unicode
		"""

		for i in range(self.childCount()):
			self.child(i).rename(from_name, to_name)

	def set_icon(self, name, icon):

		"""
		desc:
			Changes an item's icon.

		arguments:
			name:
				desc:	The item name.
				type:	unicode
			icon:
				desc:	The icon name.
				type:	unicode
		"""

		for i in range(self.childCount()):
			self.child(i).set_icon(name, icon)
