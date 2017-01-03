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
from libqtopensesame.dialogs.base_dialog import base_dialog
from quick_switcher_dialog.item import quick_open_element_item
from quick_switcher_dialog.symbol import quick_open_element_symbol
from quick_switcher_dialog.action import quick_open_element_action
from quick_switcher_dialog.sortable_list_widget import sortable_list_widget


NAVIGATION_KEYS = [
	QtCore.Qt.Key_Home,
	QtCore.Qt.Key_End,
	QtCore.Qt.Key_Up,
	QtCore.Qt.Key_Down,
	QtCore.Qt.Key_PageUp,
	QtCore.Qt.Key_Return,
	QtCore.Qt.Key_Enter,
	QtCore.Qt.Key_PageDown
	]

NUMBER_KEYS = range(QtCore.Qt.Key_1, QtCore.Qt.Key_9)
	

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
		self._element_size = None
		self._sortkey = 0
		self._item_elements = {}
		self.ui.filter_line_edit.textChanged.connect(self.filter_list)
		self.ui.filter_line_edit.returnPressed.connect(self.select_item)
		self.ui.items_list_widget.itemActivated.connect(self.select_item)
		# Monkeypatch key processing, so that we can smoothly control the list
		# and filter widget at the same time.
		self.ui.filter_line_edit._keyPressEvent = \
			self.ui.filter_line_edit.keyPressEvent
		self.ui.filter_line_edit.keyPressEvent = self.on_keypress
		self.ui.items_list_widget._keyPressEvent = \
			self.ui.items_list_widget.keyPressEvent
		self.ui.items_list_widget.keyPressEvent = self.on_keypress
		# Populate dialog with action elements
		for element in self.action_elements(self.main_window.menubar.actions()):
			list_widget_item = sortable_list_widget(self.sortkey)
			list_widget_item.setSizeHint(self.element_size(element))
			self.ui.items_list_widget.addItem(list_widget_item)
			self.ui.items_list_widget.setItemWidget(list_widget_item,
				element)
		# Populate dialog with item elements
		for item_name in self.experiment.items:
			self.add_item(item_name)
				
	@property
	def sortkey(self):
		
		"""
		desc:
			An automatically incrementing sort key.
		"""
		
		self._sortkey += 1
		return self._sortkey
				
	def element_size(self, element):
		
		"""
		desc:
			Determines the size of a list element. Uses previously determined
			size if available, to improve performance.
			
		arguments:
			element:
				desc:	The element to determine the size for.
				type:	QListWidgetItem
				
		returns:
			type:	QSize
		"""
		
		if self._element_size is None:
			self._element_size = QtCore.QSize(
				self.ui.items_list_widget.size().width(),
				element.minimumSizeHint().height())
		return self._element_size
				
	def add_item(self, item_name):
		
		"""
		desc:
			Adds one or more elements to the quick switcher for an item.
			
		arguments:
			item_name:	The name of an item.
		"""
		
		item = self.experiment.items[item_name]
		list_widget_item = sortable_list_widget(self.sortkey)
		self._item_elements[item_name] = [list_widget_item]
		element = quick_open_element_item(item)
		list_widget_item.setSizeHint(self.element_size(element))
		self.ui.items_list_widget.addItem(list_widget_item)
		self.ui.items_list_widget.setItemWidget(list_widget_item, element)
		if item.item_type == u'inline_script':
			# Call edit widget to make sure that QProgEdit has content and thus
			# can extract symbols. But don't do this for the currently visible
			# item, because that causes the cursor to jump to the top.
			if self.tabwidget.current_item() != item_name:
				item.edit_widget()
			for phase in (u'Run', u'Prepare'):
				for symbol in item.qprogedit.tab(phase).symbols():
					list_widget_item = sortable_list_widget(self.sortkey)
					self._item_elements[item_name].append(list_widget_item)
					element = quick_open_element_symbol(item, phase, symbol)
					list_widget_item.setSizeHint(self.element_size(element))
					self.ui.items_list_widget.addItem(list_widget_item)
					self.ui.items_list_widget.setItemWidget(
						list_widget_item, element)
						
	def delete_item(self, item_name):
		
		"""
		desc:
			Removes elements corresponding to an item from the quick switcher.
			
		arguments:
			item_name:	The name of the item.
		"""
		
		if item_name not in self._item_elements:
			return
		for list_widget_item in self._item_elements.pop(item_name):
			row = self.ui.items_list_widget.row(list_widget_item)
			self.ui.items_list_widget.takeItem(row)
		
	def rename_item(self, from_name, to_name):
		
		"""
		desc:
			Modifies the quick switcher for an item rename.
			
		arguments:
			from_name:	The old item name.
			to_name:	The new item name.
		"""
		
		self.delete_item(from_name)
		self.add_item(to_name)
		
	def refresh_item(self, item_name):
		
		"""
		desc:
			Refresh an item in the quick switcher.
			
		arguments:
			item_name:	The name of an item.
		"""
		
		self.delete_item(item_name)
		self.add_item(item_name)
		
	def bump_item(self, item_name):
		
		"""
		desc:
			Puts an item at the top of the quick switcher.
		
		arguments:
			item_name:	The name of an item.
		"""

		if item_name not in self._item_elements:
			return
		for list_widget_item in self._item_elements[item_name]:
			list_widget_item.sortkey = self.sortkey

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
		
	def on_keypress(self, e):
		
		"""
		desc:
			Overrides the keyPressEvent() of the items list and filter edit,
			manages the focus, and dispatches the events to the correct widget.
			
		arguments:
			e:
				type:	QKeyEvent
		"""
		
		if e.key() in NUMBER_KEYS:
			row = e.key() - QtCore.Qt.Key_1
			list_widget_item = self.ui.items_list_widget.item(row)
			self.ui.items_list_widget.itemWidget(list_widget_item).activate()
			self.accept()
			return
		if e.key() in NAVIGATION_KEYS:
			self.ui.items_list_widget.setFocus()
			self.ui.items_list_widget._keyPressEvent(e)
			return
		self.ui.filter_line_edit.setFocus()
		self.ui.filter_line_edit._keyPressEvent(e)
