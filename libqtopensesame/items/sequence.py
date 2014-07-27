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

import libopensesame.sequence
import libopensesame.plugins
from libqtopensesame.items import qtitem
from libqtopensesame.widgets import draggables
from libqtopensesame.misc import _
from PyQt4 import QtCore, QtGui
import sip

class action_button(QtGui.QPushButton):

	"""Used for the up/ down/ remove buttons in the sequence item list"""

	def __init__(self, sequence, icon, string, parent=None, tooltip=None):

		"""
		Constructor.

		Arguments:
		sequence	--	A sequence item.
		icon		--	The icon to be used.
		string		--	The text for the button.

		Keyword arguments:
		parent		--	A parent widget. (default=None)
		tooltip		--	A tooltip. (default=None)
		"""

		QtGui.QPushButton.__init__(self, icon, u'', parent)
		self.setToolTip(string)
		self.sequence = sequence
		self.setIconSize(QtCore.QSize(16, 16))
		self.clicked.connect(self.action)
		if tooltip != None:
			self.setToolTip(tooltip)

	def action(self):

		"""Handles a button click."""

		cmd, row = self.data
		if cmd == u"add":
			if row == u"existing":
				item = unicode(self.sequence.combobox_items.currentText())
				self.sequence.items.append( (item, u"always") )
			elif row == "new":
				item_type = unicode( \
					self.sequence.combobox_item_type.currentText())
				# The separator has been selected
				if item_type == "":
					return
				# The sequence and loop are a bit different, because they need
				# an extra dialog when they are created
				if item_type in (u"sequence", u"loop"):
					item = getattr(self.sequence.experiment.main_window, \
						u'add_%s' % item_type)(False, self.sequence.name)
				else:
					item = self.sequence.experiment.main_window.add_item( \
						item_type, False)
				# If the item has been created, add it to the sequence
				# and select it.
				if item != None:
					self.sequence.items.append( (item, u"always") )
					self.sequence.experiment.main_window.refresh( \
						self.sequence.name)
					self.sequence.experiment.main_window.select_item( \
						self.sequence.name)
				return
		self.sequence.experiment.main_window.refresh(self.sequence.name)

class sequence(libopensesame.sequence.sequence, qtitem.qtitem):

	"""GUI controls for the sequence item"""

	def __init__(self, name, experiment, string=None):

		"""
		Constructor.

		Arguments:
		name 		--	The item name.
		experiment	--	An instance of libopensesame.experiment.

		Keyword arguments:
		string		--	A string with the item definition. (default=None)
		"""

		self._active = True
		libopensesame.sequence.sequence.__init__(self, name, experiment, string)
		qtitem.qtitem.__init__(self)

	def action_button(self, icon, label, data, tooltip=None):

		"""
		Creates a simple pushbutton with a specific function.

		Arguments:
		icon	--	The icon.
		label	--	The label.
		data	--	A (function, parameter) tuple, such as ("add", "existing").

		Keyword arguments:
		tooltip --	A button tooltip. (default=None)

		Returns:
		An action_button instance.
		"""

		b = action_button(self, self.experiment.icon(icon), label, \
			tooltip=tooltip)
		b.data = data
		return b

	def init_edit_widget(self):

		"""Constructs the edit_widget that contains the controls."""

		qtitem.qtitem.init_edit_widget(self, False)
		# Flush keyboard checkbox
		self.checkbox_flush_keyboard = QtGui.QCheckBox( \
			_(u"Flush pending key presses at sequence start"))
		self.checkbox_flush_keyboard.toggled.connect(self.apply_edit_changes)
		form_layout = QtGui.QFormLayout()
		form_layout.setContentsMargins(0, 0, 0, 0)
		form_layout.addRow(self.checkbox_flush_keyboard)
		form_widget = QtGui.QWidget()
		form_widget.setLayout(form_layout)
		self.edit_vbox.addWidget(form_widget)
		self.combobox_item_type = self.experiment.item_type_combobox()
		self.combobox_items = QtGui.QComboBox()
		self.frame_empty = QtGui.QFrame()
		self.frame_empty.setFrameStyle(QtGui.QFrame.Panel)
		l = QtGui.QHBoxLayout()
		self.frame_empty.setLayout(l)
		l.addWidget(self.experiment.label_image(u"info"))
		l.addWidget(QtGui.QLabel(_(u"The %s is empty" % self.item_type)))
		l.addStretch()
		self.button_existing = self.action_button(u"button_select", \
			_(u"Append existing item to sequence"), (u"add",u"existing"))
		self.button_new = self.action_button(u"button_new", \
			_(u"Create and append  new item to sequence"), (u"add", u"new"))
		grid = QtGui.QGridLayout()
		grid.setMargin(0)
		grid.addWidget(QtGui.QLabel(_(u"Append existing item")), 0, 0)
		grid.addWidget(self.combobox_items, 0, 1)
		grid.addWidget(self.button_existing, 0, 2)
		grid.addWidget(QtGui.QLabel(_(u"Append new item")), 1, 0)
		grid.addWidget(self.combobox_item_type, 1, 1)
		grid.addWidget(self.button_new, 1, 2)
		grid.setColumnStretch(3, 10)
		self.draggable_list = draggables.draggable_list(self)
		scroll_area = QtGui.QScrollArea()
		scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
		scroll_area.setWidgetResizable(True)
		scroll_area.setWidget(self.draggable_list)
		self.edit_vbox.addWidget(self.frame_empty)
		self.edit_vbox.addWidget(scroll_area)
		grid_widget = QtGui.QFrame()
		grid_widget.setLayout(grid)
		self.edit_vbox.addWidget(grid_widget)
		return self._edit_widget

	def edit_widget(self):

		"""
		Updates the edit_widget to reflect changes in the item.

		Returns:
		The edit widget.
		"""

		if not self._active:
			return self._edit_widget
		self._active = False
		qtitem.qtitem.edit_widget(self)
		self.experiment.item_combobox(None, self.parents(), self.combobox_items)
		if self.combobox_items.count() == 0:
			self.combobox_items.setDisabled(True)
			self.button_existing.setDisabled(True)
		else:
			self.combobox_items.setDisabled(False)
			self.button_existing.setDisabled(False)
		self.checkbox_flush_keyboard.setChecked( \
			self.get(u"flush_keyboard") == u"yes")
		self.draggable_list.refresh()
		self.frame_empty.setVisible(len(self.items) == 0)
		self._active = True
		return self._edit_widget

	def apply_edit_changes(self):

		"""Applies the controls."""

		if not self._active:
			return
		qtitem.qtitem.apply_edit_changes(self)
		if self.checkbox_flush_keyboard.isChecked():
			self.set(u"flush_keyboard", u"yes")
		else:
			self.set(u"flush_keyboard", u"no")

	def move(self, from_index, to_index):

		"""
		Swaps two items from the sequence.

		Arguments:
		from_index	--	The old index.
		to_index	--	The new index.
		"""

		self.items.insert(to_index, self.items.pop(from_index))
		self.experiment.main_window.refresh(self.name)
		self.experiment.main_window.set_unsaved()

	def set_run_if(self, index, s):

		"""
		Change the 'run if' statement of an item.

		Arguments:
		index	--	The index of the item.
		s		--	The new run-if statement.
		"""

		s = self.clean_cond(s)
		if s != self.items[index][1]:
			self.items[index] = self.items[index][0], s
			self.experiment.main_window.refresh(self.name)
			self.experiment.main_window.set_unsaved()

	def rename(self, from_name, to_name):

		"""
		Renames an item.

		Arguments:
		from_name	--	The old name.
		to_name		--	The new name.
		"""

		qtitem.qtitem.rename(self, from_name, to_name)
		new_items = []
		for item, cond in self.items:
			if item == from_name:
				new_items.append( (to_name, cond) )
			else:
				new_items.append( (item, cond) )
		self.items = new_items

	def delete(self, item_name, item_parent=None, index=None):

		"""
		Deletes an item from the sequence.

		Arguments:
		item_name	--	The name of the item to be deleted.

		Keywords arguments:
		item_parent	--	The parent item. (default=None)
		index		--	The index of the item in the parent. (default=None)
		"""

		if item_parent == None or (item_parent == self.name and index == None):
			redo = True
			while redo:
				redo = False
				for i in range(len(self.items)):
					if self.items[i][0] == item_name:
						self.items = self.items[:i]+self.items[i+1:]
						redo = True
						break
		elif item_parent == self.name and index != None:
			if self.items[index][0] == item_name:
				self.items = self.items[:index]+self.items[index+1:]

	def build_item_tree(self, toplevel, items):

		"""
		Constructs the item tree.

		Arguments:
		toplevel	--	The toplevel widget.
		items		--	A list of items that have already been added to the item
						tree. (to avoid recursion)

		Returns:
		The updated list of added items.
		"""

		widget = self.item_tree_widget(toplevel)
		toplevel.addChild(widget)
		for item, cond in self.items:
			if item in self.experiment.items and self.experiment.items[item] \
				not in items:
				items.append(self.experiment.items[item])
		for item, cond in self.items:
			if item in self.experiment.items:
				self.experiment.items[item].build_item_tree(widget, items)
		widget.setExpanded(True)
		return items

	def is_child_item(self, item):

		for i, cond in self.items:
			if i == item or (i in self.experiment.items and \
				self.experiment.items[i].is_child_item(item)):
				return True
		return False

	def insert_child_item(self, item_name, index=0):

		self.items.insert(index, (item_name, u'always'))

	def remove_child_item(self, item_name, index=0):

		if self.items[index][0] == item_name:
			del self.items[index]
