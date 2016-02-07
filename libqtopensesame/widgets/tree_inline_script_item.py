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
from libqtopensesame.widgets.tree_item_item import tree_item_item
from libqtopensesame.widgets.tree_inline_script_phase_item import \
	tree_inline_script_phase_item
from libqtopensesame.widgets.tree_inline_script_symbol_item import \
	tree_inline_script_symbol_item
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'tree_inline_script_item', category=u'core')

class tree_inline_script_item(tree_item_item):

	"""
	desc:
		Corresponds to an inline-script widget in the overview area.
	"""

	def __init__(self, item, extra_info=None, parent_item=None, index=None,
		symbols=True):

		"""
		desc:
			Constructor. For arguments, see [tree_item_item].
		"""

		super(tree_inline_script_item, self).__init__(item,
			extra_info=extra_info, parent_item=parent_item, index=index)
		self.symbols = symbols
		if symbols:
			prepare_tree_widget = tree_inline_script_phase_item(item,
				u'prepare')
			run_tree_widget = tree_inline_script_phase_item(item, u'run')
			self.addChild(prepare_tree_widget)
			self.addChild(run_tree_widget)
			self.item.qprogedit.tab(0).setSymbolTree(prepare_tree_widget,
				tree_inline_script_symbol_item)
			self.item.qprogedit.tab(1).setSymbolTree(run_tree_widget,
				tree_inline_script_symbol_item)
		else:
			self.item.qprogedit.tab(0).setSymbolTree(None)
			self.item.qprogedit.tab(1).setSymbolTree(None)

	def expand(self):

		"""
		desc:
			Override so that we do not recursively expand and show all symbols.
		"""

		pass
