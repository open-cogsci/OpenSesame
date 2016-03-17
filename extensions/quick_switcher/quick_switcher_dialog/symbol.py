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
from libqtopensesame.widgets.base_widget import base_widget

class quick_open_element_symbol(base_widget):

	"""
	desc:
		A symbol element for the quick switcher.
	"""

	def __init__(self, item, phase, symbol):

		"""
		desc:
			Constructor.

		arguments:
			item:
				desc:	An inline_script item.
				type:	inline_script
			phase:
				desc:	The phase, i.e. 'Run' or 'Prepare'.
				type:	unicode
			symbol:
				desc:	A symbol tuple as returned by QProgEdit.
				type:	tuple
		"""

		super(quick_open_element_symbol, self).__init__(item.main_window)
		self.item = item
		self.phase = phase
		self.lineNo, self._type, self.name, self.argspec = symbol
		self.icon = self.theme.qlabel(u'text-x-script')
		self.label = QtWidgets.QLabel(u'%s <b>%s</b><br /><i>In: %s [%s:%d]</i>' % (
			self._type, self.name, self.item.name, self.phase, self.lineNo))
		self.layout = QtWidgets.QHBoxLayout(self)
		self.layout.addWidget(self.icon)
		self.layout.addWidget(self.label)
		self.layout.addStretch()
		self.setLayout(self.layout)

	def match(self, query):

		"""
		returns:
			desc:	True if the symbol matches the query, False otherwise.
			type:	bool
		"""

		_item_type = self.item.item_type.lower()
		_item_name = self.item.name.lower()
		_name = self.name.lower()
		_type = self._type.lower()
		_phase = self.phase.lower()
		for term in query.lower().split():
			if term not in _item_type and term not in _item_name and \
				term not in _type and term not in _phase and term not in _name:
				return False
		return True

	def activate(self):

		"""
		desc:
			Opens the inline_script tab, switches to the correct phase and sets
			the cursor at the symbol line.
		"""

		self.item.open_tab()
		tab = self.item.qprogedit.tab(self.phase)
		tab.focusTab()
		tab.setCursorPosition(self.lineNo-1, 0)
