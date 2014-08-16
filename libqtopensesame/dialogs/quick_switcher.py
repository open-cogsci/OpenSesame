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
from libqtopensesame.dialogs.base_dialog import base_dialog
from libqtopensesame.widgets.quick_open_element_item import \
	quick_open_element_item
from libqtopensesame.widgets.quick_open_element_symbol import \
	quick_open_element_symbol

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
			ui=u'dialogs.quick_switcher',
			flags=QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint)
		self.ui.filter_line_edit.textChanged.connect(self.filter_list)
		self.ui.filter_line_edit.returnPressed.connect(self.select_item)
		self.ui.items_list_widget.itemActivated.connect(self.select_item)
		self.items = []
		for item_name in self.experiment.items:
			item = self.experiment.items[item_name]
			list_widget_item = QtGui.QListWidgetItem()
			element = quick_open_element_item(item)
			list_widget_item.setSizeHint(element.minimumSizeHint())
			self.ui.items_list_widget.addItem(list_widget_item)
			self.ui.items_list_widget.setItemWidget(list_widget_item, element)
			if item.item_type == u'inline_script':
				item.edit_widget()
				for phase in (u'Run', u'Prepare'):
					for symbol in item.qprogedit.tab(phase).symbols():
						list_widget_item = QtGui.QListWidgetItem()
						element = quick_open_element_symbol(item, phase, symbol)
						list_widget_item.setSizeHint(element.minimumSizeHint())
						self.ui.items_list_widget.addItem(list_widget_item)
						self.ui.items_list_widget.setItemWidget(
							list_widget_item, element)

	def filter_list(self):

		"""
		desc:
			Populates the item list based on the filter text.
		"""

		query = unicode(self.ui.filter_line_edit.text()).lower()
		for i in range(self.ui.items_list_widget.count()):
			list_widget_item = self.ui.items_list_widget.item(i)
			element = self.ui.items_list_widget.itemWidget(list_widget_item)
			match = element.match(query)
			if match and list_widget_item.isHidden():
				list_widget_item.setHidden(False)
			elif not match and not list_widget_item.isHidden():
				list_widget_item.setHidden(True)

	def select_item(self, list_widget_item=None):

		"""
		desc:
			Selects an item and closes the dialog.

		keywords:
			list_item_widget:
				The selected QListWidgetItem or None to select the top item from
				the list.
		"""

		if list_widget_item == None:
			for i in range(self.ui.items_list_widget.count()):
				list_widget_item = self.ui.items_list_widget.item(i)
				if not list_widget_item.isHidden():
					break
		if list_widget_item == None or list_widget_item.isHidden():
			self.accept()
			return
		element = self.ui.items_list_widget.itemWidget(list_widget_item)
		element.activate()
		self.accept()

