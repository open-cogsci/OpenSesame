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

from PyQt4 import QtCore, QtGui
from libqtopensesame.misc import _
from libqtopensesame.misc.base_subcomponent import base_subcomponent

class tree_base_item(base_subcomponent, QtGui.QTreeWidgetItem):

	"""
	desc:
		A base class that corresponds to any widget in the overview area.
	"""

	def start_edit(self, col):

		self.treeWidget().editItem(self, col)

	def show_context_menu(self, pos):

		pass

	def droppable(self):

		return self._droppable

	def set_droppable(self, droppable):

		self._droppabe = droppable

	def draggable(self):

		return self._draggable

	def set_draggable(self, draggable):

		self._draggable = draggable

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
