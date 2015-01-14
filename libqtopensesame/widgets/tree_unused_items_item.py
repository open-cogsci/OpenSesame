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

from PyQt4 import QtCore, QtGui
from libqtopensesame.misc import _
from libqtopensesame.widgets.tree_base_item import tree_base_item
from libqtopensesame.misc import drag_and_drop

class tree_unused_items_item(tree_base_item):

	"""
	desc:
		Corresponds to the unused-items widget in the overview area.
	"""

	def __init__(self, main_window):

		"""
		desc:
			Constructor.

		arguments:
			main_window:
				desc:	The main-window object.
				type:	qtopensesame
		"""

		super(tree_unused_items_item, self).__init__()
		self.setup(main_window)
		self.setText(0, _(u'Unused items'))
		self.setIcon(0, self.theme.qicon(u'unused'))
		self.setToolTip(0, _(u'Unused items'))
		self._droppable = True
		self._draggable = False
		self.name = u'__unused__'
		for item_name in self.experiment.items.unused():
			self.experiment.items[item_name].build_item_tree(self, max_depth=1)

	def droppable(self, data):

		return drag_and_drop.matches(data, [u'item-existing'])

	def drop_hint(self):

		return _(u'Move to unused items')

	def open_tab(self):

		self.main_window.tabwidget.open_unused()

	def ancestry(self):

		return u'__unused__', u'__unused__:0'
