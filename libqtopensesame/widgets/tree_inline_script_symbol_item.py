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
from QProgEdit import QSymbolTreeWidgetItem
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'tree_inline_script_symbol_item', category=u'core')

class tree_inline_script_symbol_item(tree_base_item, QSymbolTreeWidgetItem):

	"""
	desc:
		Corresponds to a symbol from an inline script (i.e. a function or class)
	"""

	def __init__(self, editor, lineNo, _type, name, argSpec):

		"""
		desc:
			Constructor.
		"""

		tree_base_item.__init__(self)
		QSymbolTreeWidgetItem.__init__(self, editor, lineNo, _type, name,
			argSpec)
		self.arg_list = [editor, lineNo, _type, name, argSpec]
		self._droppable = False
		self._draggable = False

	@property
	def inline_script(self):
		return self.parent().inline_script

	def open_tab(self):

		"""
		desc:
			Open the inline-script tab and reveal the symbol.
		"""

		self.inline_script.open_tab(select_in_tree=False)
		self.activate()

	def clone(self):

		"""
		returns:
			desc:	A deep copy of this object.
			type:	tree_inline_script_symbol_item
		"""

		return tree_inline_script_symbol_item(*self.arg_list)
