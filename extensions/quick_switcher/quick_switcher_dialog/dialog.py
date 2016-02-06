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
from libopensesame import plugins
from libqtopensesame.dialogs.base_dialog import base_dialog
from quick_switcher_dialog.item import quick_open_element_item
from quick_switcher_dialog.symbol import quick_open_element_symbol
from quick_switcher_dialog.action import quick_open_element_action

class quick_switcher(base_dialog):

	"""
	desc:
		The quick-open-item dialog allows the user to select an item directly
		using the keyboard.
	"""

	def __init__(self, main_window):

		"""
		desc:
			Constructor.

		arguments:
			main_window:	The main window object.
		"""

		super(quick_switcher, self).__init__(main_window,
			ui=u'extensions.quick_switcher.quick_switcher',
			flags=QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint)
		self.ui.filter_line_edit.textChanged.connect(self.filter_list)
		self.ui.filter_line_edit.returnPressed.connect(self.select_item)
		self.ui.items_list_widget.itemActivated.connect(self.select_item)
		self.items = []
		for item_name in self.experiment.items:
			item = self.experiment.items[item_name]
			list_widget_item = QtWidgets.QListWidgetItem()
			element = quick_open_element_item(item)
			list_widget_item.setSizeHint(element.minimumSizeHint())
			self.ui.items_list_widget.addItem(list_widget_item)
			self.ui.items_list_widget.setItemWidget(list_widget_item, element)
			if item.item_type == u'inline_script':
				item.edit_widget()
				for phase in (u'Run', u'Prepare'):
					for symbol in item.qprogedit.tab(phase).symbols():
						list_widget_item = QtWidgets.QListWidgetItem()
						element = quick_open_element_symbol(item, phase, symbol)
						list_widget_item.setSizeHint(element.minimumSizeHint())
						self.ui.items_list_widget.addItem(list_widget_item)
						self.ui.items_list_widget.setItemWidget(
							list_widget_item, element)
		for element in self.action_elements(
			self.main_window.menubar.actions()):
			list_widget_item = QtWidgets.QListWidgetItem()
			list_widget_item.setSizeHint(element.minimumSizeHint())
			self.ui.items_list_widget.addItem(list_widget_item)
			self.ui.items_list_widget.setItemWidget(list_widget_item,
				element)

	def action_elements(self, actions, path_to_action=[]):

		"""
		desc:
			Builds a list of action elements.

		arguments:
			actions:
				desc:	A list of actions.
				type:	list

		keywords:
			path_to_action:
				desc:	A list of parent action texts.
				type:	list

		returns:
			type:	quick_open_element_action
		"""

		l = []
		for action in actions:
			text = str(action.text())
			# Skip separators
			if text == u'':
				continue
			_path_to_action = path_to_action + [text]
			menu = action.menu()
			if menu is None:
				l.append(quick_open_element_action(self, action,
					_path_to_action))
			else:
				l += self.action_elements(action.menu().actions(),
					_path_to_action)
		return l

	def exec_(self):

		"""
		desc:
			Focus the filter input and activate the dialog.
		"""

		self.ui.label_quick_switcher_wait.hide()
		self.ui.items_list_widget.show()
		self.ui.items_list_widget.setCurrentRow(0)
		self.ui.filter_line_edit.clear()
		self.ui.filter_line_edit.setFocus()
		super(quick_switcher, self).exec_()

	def show_wait(self):

		self.ui.label_quick_switcher_wait.show()
		self.ui.items_list_widget.hide()
		QtWidgets.QApplication.processEvents()

	def filter_list(self):

		"""
		desc:
			Populates the item list based on the filter text.
		"""

		query = str(self.ui.filter_line_edit.text()).lower()
		for i in range(self.ui.items_list_widget.count()):
			list_widget_item = self.ui.items_list_widget.item(i)
			element = self.ui.items_list_widget.itemWidget(list_widget_item)
			match = element.match(query)
			if match and list_widget_item.isHidden():
				list_widget_item.setHidden(False)
			elif not match and not list_widget_item.isHidden():
				list_widget_item.setHidden(True)
		i = self.first_index()
		if i is not None:
			self.ui.items_list_widget.setCurrentRow(i)

	def first_item(self):

		"""
		desc:
			Gets the first visible item.

		returns:
			desc:	The first visible item, or None if there are no items.
			type:	[QListWidgetItem, None]
		"""

		for i in range(self.ui.items_list_widget.count()):
			list_widget_item = self.ui.items_list_widget.item(i)
			if not list_widget_item.isHidden():
				return list_widget_item
		return None

	def first_index(self):

		"""
		desc:
			Gets the index of the first visible item.

		returns:
			desc:	The first visible index, or None if there are no items.
			type:	[int, None]
		"""

		for i in range(self.ui.items_list_widget.count()):
			list_widget_item = self.ui.items_list_widget.item(i)
			if not list_widget_item.isHidden():
				return i
		return None

	def select_item(self, list_widget_item=None):

		"""
		desc:
			Selects an item and closes the dialog.

		keywords:
			list_item_widget:
				The selected QListWidgetItem or None to select the top item from
				the list.
		"""

		if list_widget_item is None:
			list_widget_item = self.first_item()
		if list_widget_item is None or list_widget_item.isHidden():
			self.accept()
			return
		element = self.ui.items_list_widget.itemWidget(list_widget_item)
		element.activate()
		self.accept()

	def focus_list(self):

		"""
		desc:
			Sets focus on the item list.
		"""

		self.ui.items_list_widget.setFocus()

