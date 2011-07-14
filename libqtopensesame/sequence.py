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

		elif cmd == "delete":
			self.sequence.experiment.main_window.close_item_tab(self.sequence.items[row][0])
			self.sequence.items.remove(self.sequence.items[row])
		elif cmd == "up" and row > 0:
			tmp = self.sequence.items[row - 1]
			self.sequence.items[row - 1] = self.sequence.items[row]
			self.sequence.items[row] = tmp
		elif cmd == "down" and row < len(self.sequence.items) - 1:
			tmp = self.sequence.items[row + 1]
			self.sequence.items[row + 1] = self.sequence.items[row]
			self.sequence.items[row] = tmp
		elif cmd == "top":
			tmp = self.sequence.items[row]
			self.sequence.items.remove(tmp)
			self.sequence.items = [tmp] + self.sequence.items
		elif cmd == "bottom":
			tmp = self.sequence.items[row]
			self.sequence.items.remove(tmp)
			self.sequence.items.append(tmp)
		elif cmd == "rename":

			old_name = self.sequence.items[row][0]
			new_name, ok = QtGui.QInputDialog.getText(self.sequence.experiment.main_window.ui.centralwidget, "Rename", "Please enter a new name", text = old_name)
			new_name = str(new_name)
			if ok and new_name != old_name:
				if new_name in self.sequence.experiment.items:
					self.sequence.experiment.notify("An item named '%s' already exists!" % new_name)
				else:
					self.sequence.experiment.rename(old_name, new_name)

		self.sequence.experiment.main_window.refresh(self.sequence.name)

class items_combobox(QtGui.QComboBox):

	"""Used to select items in the item list"""

	def __init__(self, item, items, sequence, select, exclude, parent = None, tooltip = None):

		"""
		Constructor

		Arguments:
		item -- the index of the item in the sequence
		items -- a list of available items
		sequence -- a sequence item
		select -- the currently selected item
		exclude -- a list of items that should be excluded

		Keyword arguments:
		parent -- a parent widget (default = None)
		tooltip -- a tooptip (default = None)
		"""

		QtGui.QComboBox.__init__(self, parent)
		self.sequence = sequence
		self.item = item

		self.addItem("Select item")
		if tooltip != None:
			self.setToolTip(tooltip)

		i = 1
		for item in items:
			if item not in exclude:
				self.addItem(item)
				self.setItemIcon(i, self.sequence.experiment.icon(self.sequence.experiment.items[item].item_type))
				if self.sequence.experiment.items[item].name == select:
					self.setCurrentIndex(i)
				i += 1

		QtCore.QObject.connect(self, QtCore.SIGNAL("currentIndexChanged(int)"), self.action)

	def action(self, dummy = None):

		"""
		Handles a changed selection

		Keyword arguments:
		dummy -- a dummy parameter that is passed by the signal handler (default = None)
		"""

		cur = str(self.currentText())
		if cur == "Select item":
			self.sequence.items[self.item] = "undefined", "always"
		else:
			self.sequence.items[self.item] = str(self.currentText()), self.sequence.items[self.item][1]
		self.sequence.experiment.build_item_tree()
		self.sequence.script_widget()

class items_linedit(QtGui.QLineEdit):

	"""Used for the 'Run if' conditions in the item list"""

	def __init__(self, item, sequence, text, parent = None, tooltip = None):

		"""
		Constructor

		Arguments:
		item -- the index of the item in the sequence
		sequence -- the sequence
		text -- the current 'Run if' condition

		Keyword arguments:
		parent -- a parent item (default = None)
		tooltip -- a tooltip (default = None)
		"""

		QtGui.QLineEdit.__init__(self, text, parent)
		self.item = item
		self.sequence = sequence
		QtCore.QObject.connect(self, QtCore.SIGNAL("editingFinished()"), self.action)
		if tooltip != None:
			self.setToolTip(tooltip)

	def action(self, dummy = None):

		"""
		Handles a text change

		Keyword arguments:
		dummy -- a dummy parameter passed by the signal handler (default = None)
		"""

		cond = self.sequence.experiment.sanitize(str(self.text()).strip())
		if cond == "":
			cond = "always"
		self.setText(cond)
		self.sequence.items[self.item] = self.sequence.items[self.item][0], str(self.text())
		self.sequence.script_widget()

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

		self._widget = QtGui.QFrame()
		self._widget.setFrameStyle(QtGui.QFrame.StyledPanel)
		self._grid = QtGui.QGridLayout(self._widget)
		self._widget.setLayout(self._grid)

		self.edit_vbox.addWidget(self._widget)

		self.combobox_item_type = self.experiment.item_type_combobox()
		self.combobox_items = QtGui.QComboBox()

		grid = QtGui.QGridLayout()
		grid.setMargin(0)

		grid.addWidget(QtGui.QLabel("Append existing item"), 0, 0)
		grid.addWidget(self.combobox_items, 0, 1)
		grid.addWidget(self.action_button("add", "Append existing item to sequence", ("add", "existing")), 0, 2)

		grid.addWidget(QtGui.QLabel("Append new item"), 1, 0)
		grid.addWidget(self.combobox_item_type, 1, 1)
		grid.addWidget(self.action_button("add", "Create and append  new item to sequence", ("add", "new")), 1, 2)

		grid.setColumnStretch(3, 10)

		grid_widget = QtGui.QFrame()
		grid_widget.setLayout(grid)

		self.edit_vbox.addWidget(grid_widget)
		self.edit_vbox.addStretch()

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
		self.experiment.clear_widget(self._widget)

		if len(self.items) == 0:
			self._grid.addWidget(QtGui.QLabel("<b>The sequence is empty!</b><br />You can add items to the sequence using the buttons below."), 0, 0)

		else:
			self._grid.addWidget(QtGui.QLabel("#"), 0, 0)
			self._grid.addWidget(QtGui.QLabel("Item"), 0, 1)
			self._grid.addWidget(QtGui.QLabel("Run if ... "), 0, 2)

			row = 1
			for item, cond in self.items:

				self.items_combobox = items_combobox(row-1, self.experiment.items, self, item, self.parents(), tooltip = "Select item")
				self._grid.addWidget(QtGui.QLabel("%d" % row), row, 0)
				self._grid.addWidget(self.items_combobox, row, 1)
				self._grid.addWidget(items_linedit(row-1, self, cond, tooltip = "A simple conditional statement, e.g., 'correct = 1'"), row, 2)
				self._grid.addWidget(self.action_button("top", "", ("top", row-1), tooltip = "Move item to top"), row, 3)
				self._grid.addWidget(self.action_button("up", "", ("up", row-1), tooltip = "Move item one position up"), row, 4)
				self._grid.addWidget(self.action_button("down", "", ("down", row-1), tooltip = "Move item one position down"), row, 5)
				self._grid.addWidget(self.action_button("bottom", "", ("bottom", row-1), tooltip = "Move item to bottom"), row, 6)
				self._grid.addWidget(self.action_button("rename", "", ("rename", row-1), tooltip = "Rename item"), row, 7)
				self._grid.addWidget(self.action_button("delete", "", ("delete", row-1), tooltip = "Remove item from sequence"), row, 8)
				row += 1

		self._active = True

		return self._edit_widget

	def delete(self, index):

		"""
		Delete an item from the sequence

		Arguments:
		index -- the index of the item to be deleted
		"""

		if self.debug:
			print "sequence.delete(): deleting %s (%d) from sequence %s" % (self.items[index], index, self.name)
		del self.items[index]
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

