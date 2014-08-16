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
		self.setIcon(0, self.theme.qicon(u'os-symbol'))
		self._droppable = False
		self._draggable = False
		self.expand()

	def open_tab(self):

		"""
		desc:
			Open the inline-script tab.
		"""

		self.inline_script.open_tab()
		if self.phase == u'prepare':
			self.inline_script.qprogedit.selectTab(0)
		else:
			self.inline_script.qprogedit.selectTab(1)
