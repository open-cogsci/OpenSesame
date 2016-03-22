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

class quick_open_element_item(base_widget):

	"""
	desc:
		An item element for the quick switcher.
	"""

	def __init__(self, item):

		"""
		desc:
			Constructor.

		arguments:
			item:
				desc:	An item.
				type:	qtitem
		"""

		super(quick_open_element_item, self).__init__(item.main_window)
		self.item = item
		self.icon = self.theme.qlabel(self.item.item_icon())
		self.label = QtWidgets.QLabel(u'item <b>%s</b><br /><i>Type: %s</i>' \
			% (self.item.name, self.item.item_type))
		self.layout = QtWidgets.QHBoxLayout(self)
		self.layout.addWidget(self.icon)
		self.layout.addWidget(self.label)
		self.layout.addStretch()
		self.setLayout(self.layout)

	def match(self, query):

		"""
		returns:
			desc:	True if the item matches the query, False otherwise.
			type:	bool
		"""

		_type = self.item.item_type.lower()
		_name = self.item.name.lower()
		for term in query.lower().split():
			if term not in _type and term not in _name:
				return False
		return True

	def activate(self):

		"""
		desc:
			Opens the item tab.
		"""

		self.item.open_tab()
