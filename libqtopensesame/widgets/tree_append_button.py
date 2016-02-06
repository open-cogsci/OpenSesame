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
from libqtopensesame.misc.base_subcomponent import base_subcomponent
from libqtopensesame.widgets.tree_append_menu import tree_append_menu
from qtpy import QtWidgets

class tree_append_button(base_subcomponent, QtWidgets.QPushButton):

	"""
	desc:
		An append item menu that appears below the tree structure of sequence
		items.
	"""

	def setup(self, main_window):

		super(tree_append_button, self).setup(main_window)
		self.setIcon(self.main_window.theme.qicon(u'list-add'))
		self.tree_overview = self.parent()
		self.append_menu = tree_append_menu(self.tree_overview)
		self.setMenu(self.append_menu)
		self.setFlat(True)
		self.adjustSize()

	def set_position(self):

		"""
		desc:
			Places the button right below the last item.
		"""

		last_item = self.tree_overview.topLevelItem(0)
		while self.tree_overview.itemBelow(last_item) is not None:
			last_item = self.tree_overview.itemBelow(last_item)
		index = self.tree_overview.indexFromItem(last_item)
		rect = self.tree_overview.visualRect(index)
		rect.moveTop(rect.top() + 1.75*rect.height())
		rect.moveLeft(4)
		geom = self.geometry()
		geom.moveTopLeft(rect.bottomLeft())
		self.setGeometry(geom)
