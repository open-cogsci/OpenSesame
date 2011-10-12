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
import libqtopensesame.qtitem
import libqtopensesame.draggables
from PyQt4 import QtCore, QtGui
import sip

class action_button(QtGui.QPushButton):

	"""Used for the up/ down/ remove buttons in the sequence item list"""

	def __init__(self, sequence, icon, string, parent = None, tooltip = None):

		"""
		Constructor

		Arguments:
		sequence -- a sequence item
		icon -- the icon to be used
		string -- the text for the button

		Keyword arguments:
		parent -- a parent widget (default = None)
		tooltip -- a tooltip (default = None)
		"""

		QtGui.QPushButton.__init__(self, icon, "", parent)
		self.setToolTip(string)
		self.sequence = sequence
		self.setIconSize(QtCore.QSize(16, 16))
		QtCore.QObject.connect(self, QtCore.SIGNAL("clicked()"), self.action)
		if tooltip != None:
			self.setToolTip(tooltip)

	def action(self):

		"""Handles a button click"""

		cmd, row = self.data
		if cmd == "add":
			if row == "existing":
				item = str(self.sequence.combobox_items.currentText())
				self.sequence.items.append( (item, "always") )

			elif row == "new":

				item_type = str(self.sequence.combobox_item_type.currentText())

				# The separator has been selected
				if item_type == "":
					return

				# The sequence and loop are a bit different, because they need
				# an extra dialog when they are created
				if item_type in ("sequence", "loop"):
					item = eval("self.sequence.experiment.main_window.add_%s(False, \"%s\")" % (item_type, self.sequence.name))
				else:
					item = self.sequence.experiment.main_window.add_item(item_type, False)

				# If the item has been created, add it to the sequence
				# and select it.
				if item != None:
					self.sequence.items.append( (item, "always") )
					self.sequence.experiment.main_window.refresh(self.sequence.name)
					self.sequence.experiment.main_window.select_item(self.sequence.name)
				return

		self.sequence.experiment.main_window.refresh(self.sequence.name)

class sequence(libopensesame.sequence.sequence, libqtopensesame.qtitem.qtitem):

	"""GUI controls for the sequence item"""

	def __init__(self, name, experiment, string = None):

		"""
		Constructor

		Arguments:
		name -- the name of the item
		experiment -- an instance of libopensesame.experiment

		Keyword arguments:
		string -- a string with the item definition (default = None)
		"""

		self._active = True
		libopensesame.sequence.sequence.__init__(self, name, experiment, string)
		libqtopensesame.qtitem.qtitem.__init__(self)

	def action_button(self, icon, label, data, tooltip = None):

		"""
		Creates a simple pushbutton with a specific function

		Arguments:
		icon -- the icon
		label -- the label
		data -- a (function, parameter) tuple, such as ("add", "existing")

		Keyword arguments:
		tooltip -- a tooltip (default = None)

		Returns:
		An action_button
		"""

		b = action_button(self, self.experiment.icon(icon), label, tooltip = tooltip)
		b.data = data
		return b

	def init_edit_widget(self):

		"""Construct the edit_widget that contains the controls"""

		libqtopensesame.qtitem.qtitem.init_edit_widget(self, False)
		
		# Flush keyboard checkbox
		self.checkbox_flush_keyboard = QtGui.QCheckBox( \
			"Flush pending key presses at sequence start")
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
		l.addWidget(self.experiment.label_image("info"))
		l.addWidget(QtGui.QLabel("The sequence is empty"))
		l.addStretch()
		
		self.button_existing = self.action_button("add", \
			"Append existing item to sequence", ("add", "existing"))
		self.button_new = self.action_button("add", \
			"Create and append  new item to sequence", ("add", "new"))
		
		grid = QtGui.QGridLayout()
		grid.setMargin(0)
		grid.addWidget(QtGui.QLabel("Append existing item"), 0, 0)
		grid.addWidget(self.combobox_items, 0, 1)
		grid.addWidget(self.button_existing, 0, 2)
		grid.addWidget(QtGui.QLabel("Append new item"), 1, 0)
		grid.addWidget(self.combobox_item_type, 1, 1)
		grid.addWidget(self.button_new, 1, 2)
		grid.setColumnStretch(3, 10)
		
		self.draggable_list = libqtopensesame.draggables.draggable_list(self)
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
		Update the edit_widget to reflect changes in the item

		Returns:
		The edit widget
		"""

		if not self._active:
			return self._edit_widget
		self._active = False

		libqtopensesame.qtitem.qtitem.edit_widget(self)
		self.experiment.item_combobox(None, self.parents(), self.combobox_items)
		if self.combobox_items.count() == 0:
			self.combobox_items.setDisabled(True)
			self.button_existing.setDisabled(True)
		else:
			self.combobox_items.setDisabled(False)
			self.button_existing.setDisabled(False)
			
		self.checkbox_flush_keyboard.setChecked( \
			self.get("flush_keyboard") == "yes")
		
		self.draggable_list.refresh()
		self.frame_empty.setVisible(len(self.items) == 0)
		self._active = True

		return self._edit_widget
		
	def apply_edit_changes(self):
	
		"""Apply controls"""
						
		libqtopensesame.qtitem.qtitem.apply_edit_changes(self)		
		if self.checkbox_flush_keyboard.isChecked():
			self.set("flush_keyboard", "yes")
		else:
			self.set("flush_keyboard", "no")		
				
	def move(self, from_index, to_index):
	
		"""
		Swaps to items from the sequence
		
		Arguments:
		from_index -- the old index
		to_index -- the new index
		"""

		self.items.insert(to_index, self.items.pop(from_index))
		self.experiment.main_window.refresh(self.name)		
		
	def set_run_if(self, index, s):
	
		"""
		Change the 'run if' statement of an item
		
		Arguments:
		index -- the index of the item
		s -- the new run if statement
		"""
	
		s = self.experiment.sanitize(s)
		if s == "":
			s = "always"
		if s != self.items[index][1]:
			self.items[index] = self.items[index][0], s
			self.experiment.main_window.refresh(self.name)		

	def rename(self, from_name, to_name):

		"""
		Rename an item

		Arguments:
		from_name -- the original name
		to_name -- the new name
		"""

		libqtopensesame.qtitem.qtitem.rename(self, from_name, to_name)
		new_items = []
		for item, cond in self.items:
			if item == from_name:
				new_items.append( (to_name, cond) )
			else:
				new_items.append( (item, cond) )
		self.items = new_items		
		
	def delete(self, item_name, item_parent=None, index=None):	
	
		"""
		Delete an item
		
		Arguments:
		item_name -- the name of the item to be deleted
		
		Keywords arguments:
		item_parent -- the parent item (default=None)
		index -- the index of the item in the parent (default=None)
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
		Construct the item tree

		Arguments:
		toplevel -- the toplevel widget
		items -- a list of items that have already been added to the item tree (to avoid recursion)

		Returns:
		The updated list of added items
		"""

		widget = self.item_tree_widget(toplevel)
		toplevel.addChild(widget)

		for item, cond in self.items:
			if item in self.experiment.items and self.experiment.items[item] not in items:
				items.append(self.experiment.items[item])
		for item, cond in self.items:
			if item in self.experiment.items:
				self.experiment.items[item].build_item_tree(widget, items)

		widget.setExpanded(True)
		return items

	def is_offspring(self, item):

		"""
		Checks if the item is offspring of the current item

		Arguments:
		item -- the item to be checked

		Returns:
		True if the item is offspring of the current item, False otherwise
		"""

		for i, cond in self.items:
			if i == item or (i in self.experiment.items and self.experiment.items[i].is_offspring(item)):
				return True
		return False

	def item_tree_info(self):

		"""
		Returns an info string for the item tree widget

		Returns:
		An info string
		"""

		return "%s items" % len(self.items)

