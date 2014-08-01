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

class quick_open_item(base_dialog):

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

		super(quick_open_item, self).__init__(main_window,
			ui=u'dialogs.quick_open_item',
			flags=QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint)
		self.ui.filter_line_edit.textChanged.connect(self.populate_list)
		self.ui.filter_line_edit.returnPressed.connect(self.select_item)
		self.ui.items_list_widget.itemActivated.connect(self.select_item)
		self.items = []
		for item_name in sorted(self.experiment.items):
			item_type = self.experiment.items[item_name].item_type
			item_icon = self.experiment.icon(item_type)
			self.items.append( (item_name, item_type, item_icon) )
		self.populate_list()

	def populate_list(self):

		"""
		desc:
			Populates the item list based on the filter text.
		"""

		self.ui.items_list_widget.clear()
		filter_text = unicode(self.ui.filter_line_edit.text()).lower()
		for item_name, item_type, item_icon in self.items:
			if filter_text in item_name.lower() \
				or filter_text in item_type.lower():
				self.ui.items_list_widget.addItem(QtGui.QListWidgetItem(
					item_icon, item_name))

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
			if len(self.ui.items_list_widget) > 0:
				 list_widget_item = self.ui.items_list_widget.item(0)
			else:
				self.accept()
		if list_widget_item == None:
			return
		item_name = unicode(list_widget_item.text())
		self.experiment.items[item_name].open_tab()
		self.accept()

