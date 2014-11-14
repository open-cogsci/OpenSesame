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

class tree_general_item(tree_base_item):

	"""
	desc:
		Corresponds to the general widget in the overview area.
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

		super(tree_general_item, self).__init__()
		self.setup(main_window)
		self.setText(0, self.experiment.title)
		self.setIcon(0, self.theme.qicon(u'os-experiment'))
		self.setToolTip(0, _(u'General options'))
		self._droppable = False
		self._draggable = False
		self.name = u'__general__'
		if self.experiment.start in self.experiment.items:
			self.experiment.items[self.experiment.start].build_item_tree(self)
			self.child(0).set_draggable(False)
		self.expand()

	def open_tab(self):

		self.main_window.tabwidget.open_general()
