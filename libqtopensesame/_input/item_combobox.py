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
from qtpy import QtWidgets
from libqtopensesame.misc.base_subcomponent import base_subcomponent
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'item_combobox', category=u'core')


class item_combobox(QtWidgets.QComboBox, base_subcomponent):

	"""
	desc:
		A combobox to select existing items.
	"""

	def __init__(self, main_window, filter_fnc=None):

		QtWidgets.QComboBox.__init__(self, main_window)
		self.setup(main_window)
		self.filter_fnc = filter_fnc
		self.refresh()

	@property
	def filter_fnc(self):

		return self._filter_fnc

	@filter_fnc.setter
	def filter_fnc(self, filter_fnc):

		if filter_fnc is None:
			self._filter_fnc = lambda item: True
		else:
			self._filter_fnc = filter_fnc

	@property
	def selected_item(self):

		return self.currentText()

	def currentText(self):

		if self.currentIndex() == 0:
			return u''
		return QtWidgets.QComboBox.currentText(self)

	def findText(self, item):

		if not item:
			return 0
		return QtWidgets.QComboBox.findText(self, safe_decode(item))

	@property
	def items(self):

		return filter(self._filter_fnc, self.item_store)

	def select(self, item_name):

		i = self.findText(item_name)
		if i < 0:
			self.setCurrentIndex(0)
			return False
		self.setCurrentIndex(i)
		return True

	def refresh(self):

		prev_selected = self.selected_item
		while self.count():
			self.removeItem(0)
		self.addItem(_(u'No item selected'))
		self.setItemIcon(0, self.theme.qicon(u'go-down'))
		for i, item_name in enumerate(self.items):
			self.addItem(item_name)
			self.setItemIcon(i+1,
				self.theme.qicon(self.item_store[item_name].item_icon()))
		self.select(prev_selected)
