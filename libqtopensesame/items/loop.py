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

import copy
from libopensesame.loop import loop as loop_runtime
from libqtopensesame.items.qtitem import qtitem
from libqtopensesame.items.qtstructure_item import qtstructure_item
from libqtopensesame.misc import _
from libqtopensesame.misc.config import cfg
from libqtopensesame.widgets import loop_table
from libqtopensesame.widgets.loop_widget import loop_widget
from libqtopensesame.widgets.tree_item_item import tree_item_item
from libqtopensesame.validators import cond_validator
from libopensesame import debug
from PyQt4 import QtCore, QtGui

class loop(qtstructure_item, qtitem, loop_runtime):

	"""The GUI for the loop item"""

	def __init__(self, name, experiment, string=None):

		"""
		Constructor.

		Arguments:
		name		--	Name of the item.
		experiment	-- 	The experiment object.

		Keyword arguments:
		string		--	The definition string. (default=None)
		"""

		self.lock_cycles = False
		loop_runtime.__init__(self, name, experiment, string)
		qtitem.__init__(self)

	def rename(self, from_name, to_name):

		"""
		Handles an item rename.

		Arguments:
		from_name	--	The old name of the item to be renamed.
		to_name		--	The new name of the item to be renamed.
		"""

		qtitem.rename(self, from_name, to_name)
		if self.item == from_name:
			self.item = to_name

	def delete(self, item_name, item_parent=None, index=None):

		"""
		Deletes an item.

		Arguments:
		item_name		--	The name of the item to be deleted.

		Keywords arguments:
		item_parent		--	The parent item. (default=None)
		index			--	The index of the item in the parent. (default=None)
		"""

		if self.item == item_name and item_parent == self.name:
			self.item = u""

	def add_cyclevar(self):

		"""Presents a dialog and add a variable,"""

		var_name, ok = QtGui.QInputDialog.getText(self.loop_table, \
			_(u'New variable'), \
			_(u'Enter a variable name, optionally followed by a default value (i.e., \"varname defaultvalue\")'))

		if ok:
			l = self.cyclevar_list()
			var_name = str(var_name)

			# Split by space, because a name may be followed by a default value
			_l = var_name.split()
			if len(_l) > 1:
				default = _l[1]
				var_name = _l[0]
			else:
				default = ""

			# Check for valid variable names
			var_name = self.experiment.sanitize(var_name, strict=True, \
				allow_vars=False)
			if var_name == u"":
				self.experiment.notify( \
					u"Variable names must consist of alphanumeric characters and underscores, and must not be empty")
				return

			# Check if the variable already exists
			if l is not None and var_name in l:
				self.experiment.notify( \
					_(u"A variable with the name '%s' already exists") \
						% var_name)
				return

			for i in range(self.cycles):
				if i not in self.matrix:
					self.matrix[i] = {}
				self.matrix[i][var_name] = default

			self.refresh_loop_table()
			self.apply_edit_changes()

	def cyclevar_list(self):

		"""
		Returns a list of variables.

		Returns:
		A list of variable names
		"""

		var_list = []
		for i in self.matrix:
			for var in self.matrix[i]:
				if var not in var_list:
					var_list.append(var)
		if len(var_list) == 0:
			return None
		return var_list


	def rename_var(self, item, from_name, to_name):

		"""
		Processes a notification that a variable has been renamed.

		Arguments:
		item		--	The item doing the renaming.
		from_name	--	The old variable name.
		to_name		--	The new variable name.
		"""

		# Only accept renames from this item
		if item != self.name:
			return
		for i in self.matrix:
			if from_name in self.matrix[i]:
				val = self.matrix[i][from_name]
				del self.matrix[i][from_name]
				self.matrix[i][to_name] = val

	def rename_cyclevar(self):

		"""Presents a dialog and rename a variable."""

		var_list = self.cyclevar_list()
		if var_list is None:
			return

		old_var, ok = QtGui.QInputDialog.getItem( \
			self.experiment.ui.centralwidget, _(u"Rename variable"), \
			_(u"Which variable do you want to rename?"), var_list, \
			editable=False)
		if ok:
			_new_var, ok = QtGui.QInputDialog.getText(self.loop_table, \
				_(u'New variable'), _(u'Enter a new variable name'), text=old_var)
			if ok and _new_var != old_var:
				old_var = str(old_var)
				new_var = self.experiment.sanitize(_new_var, strict=True, \
					allow_vars=False)
				if _new_var != new_var or new_var == "":
					self.experiment.notify( \
						_(u"Please use only letters, numbers and underscores"))
					return
				if new_var in var_list:
					self.experiment.notify( \
						_(u"A variable with the name '%s' already exists") % \
						new_var)
					return
			self.rename_var(self.name, old_var, new_var)
			self.refresh_loop_table()
			self.apply_edit_changes()

	def remove_cyclevar(self):

		"""Presents a dialog and remove a variable."""

		var_list = self.cyclevar_list()
		if var_list is None:
			return

		var, ok = QtGui.QInputDialog.getItem(self.experiment.ui.centralwidget, \
			_(u"Remove variable"), _(u"Which variable do you want to remove?"), \
			var_list)
		if ok:
			var = str(var)
			for i in self.matrix:
				if var in self.matrix[i]:
					del self.matrix[i][var]

			self.refresh_loop_table()
			self.apply_edit_changes()

	def cyclevar_count(self):

		"""
		Counts the number of variables in the loop,

		Returns:
		The number of variables in the loop.
		"""

		l = []
		c = 0
		for cycle in self.matrix:
			for var in self.matrix[cycle]:
				if var not in l:
					l.append(var)
					c += 1
		return c

	def cycle_count(self):

		"""
		Counts the number of cycles, which is the maximum of the table length
		and the 'cycles' variables.

		Returns:
		The number of cycles.
		"""

		if type(self.cycles) != int:
			return 0
		return max(self.cycles, len(self.matrix))

	def set_cycle_count(self, cycles, confirm=True):

		"""
		Sets the nr of cycles and truncates data if necessary.

		Arguments:
		cycles		--	The number of cycles.

		Keyword arguments:
		confirm		--	Indicates whether confirmation is required before data
						is removed from the table. (default=True)
		"""

		if self.lock_cycles:
			return
		self.lock_cycles = True
		debug.msg(u"cycles = %s" % cycles)
		# Ask for confirmation before reducing the number of cycles.
		if len(self.matrix) > cycles and confirm:
			resp = QtGui.QMessageBox.question(self.experiment.ui.centralwidget,
				_(u"Remove cycles?"),
				_(u"By reducing the number of cycles, data will be lost from the table. Do you wish to continue?"),
				QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
			if resp == QtGui.QMessageBox.No:
				self.loop_widget.ui.spin_cycles.setValue(self.cycles)
				self.lock_cycles = False
				return
		for i in self.matrix.keys():
			if i >= cycles:
				del self.matrix[i]
		self.lock_cycles = False
		self.set(u"cycles", cycles)

	def call_count(self):

		"""
		Returns the number of times that the target item is called in total,
		which depends on the repeat and cycles.

		Returns:
		The number of calls or 0 if the number of calls could not be determined.
		"""

		try:
			if self.order == u"sequential" and self.offset != u"yes":
				return int(self.cycles * self.repeat - self.skip)
			return int(self.cycles * self.repeat)
		except:
			return 0

	def refresh_summary(self):

		"""Refreshes the cycle count summary."""

		if self.item not in self.experiment.items:
			s = _(u"<font color='red'>No item to run specified</font>")
		else:
			cc = self.call_count()
			if self.order == u'sequential' and self.offset != u'yes':
				s = _(u"<b>%s</b> will be called <b>%s</b> x <b>%s</b> - <b>%s</b> = <b>%s</b> times in <b>%s</b> order") \
					% (self.item, self.cycles, self.repeat, self.skip, cc, \
					self.order)
			else:
				s = _(u"<b>%s</b> will be called <b>%s</b> x <b>%s</b> = <b>%s</b> times in <b>%s</b> order") \
					% (self.item, self.cycles, self.repeat, cc, self.order)
			if self.order == u"sequential" and self.skip > 0:
				s += _(u" starting at cycle <b>%s</b>") % self.skip
				if self.offset == u"yes" and self.skip >= cc:
					s += _(u" <font color='red'><b>(too many cycles skipped)</b></font>")
			if cc < 1:
				s += _(u" <font color='red'><b>(zero, negative, or unknown length)</b></font>")
		self.loop_widget.ui.label_summary.setText(u"<small>%s</small>" % s)

	def refresh_loop_table(self, lock=True):

		"""
		Rebuilds the loop table.

		Keyword arguments:
		lock	--	A boolean indicating whether the item should be locked to
					prevent recursion. (default=True)
		"""

		if lock:
			self.lock = True

		# Don't crash if the cycle variable is variable, simply provide an
		# error message (due to the sanity check) and disable the loop table.
		if type(self.cycles) != int:
			self.loop_table.setEnabled(False)
			self.lock = False
			return
		self.loop_table.setEnabled(True)

		# Don't clear and resize the table if this is not necessary, because
		# this makes the cursor jump
		if self.loop_table.rowCount() != self.cycles or \
			self.loop_table.columnCount() != self.cyclevar_count():
			self.loop_table.clear()
			self.loop_table.setRowCount(self.cycles)
			self.loop_table.setColumnCount(self.cyclevar_count())

		# Determine the order in which the columns are displayed
		column_order = []
		if self.cyclevar_list() is not None:
			if self.has(u"column_order"):
				for var in self.unistr(self.get(u"column_order")).split(u";"):
					if var in self.cyclevar_list():
						column_order.append(var)
			for var in self.cyclevar_list():
				if var not in column_order:
					column_order.append(var)

		# Create the column headers
		i = 0
		for var in column_order:
			self.loop_table.setHorizontalHeaderItem(i, \
				QtGui.QTableWidgetItem(var))
			i += 1

		# Fill the table
		var_columns = {}
		new_column = 0
		for cycle in self.matrix:
			for var in self.matrix[cycle]:
				col = column_order.index(var)
				self.loop_table.set_text(cycle, col,
					self.experiment.unistr(self.matrix[cycle][var]))

		# Store the number of cycles and the column order
		self.set(u"cycles", max(self.get(u"cycles"), self.cycle_count()))
		self.set(u"column_order", u";".join(column_order))

		if lock:
			self.lock = False

	def wizard_process(self, d, l=[]):

		"""
		Rebuilds the loop table based on a dictionary of variables and levels.

		Arguments:
		d	--	A dictionary of variables and levels.

		Keyword arguments:
		l	--	A list of variables and values. (default=[])
		"""

		if len(d) == 0:
			for var, val in l:
				if self.i not in self.matrix:
					self.matrix[self.i] = {}
				self.matrix[self.i][var] = val
			self.i += 1
			return
		var = list(d.keys())[0]
		for val in d[var]:
			_d = copy.copy(d)
			del _d[var]
			self.wizard_process(_d, l + [(var, val)])

	def wizard(self):

		"""Presents the variable wizard dialog."""

		from libqtopensesame.dialogs.loop_wizard import loop_wizard
		d = loop_wizard(self.experiment.main_window)
		if d.exec_() == QtGui.QDialog.Accepted:
			#cfg.loop_wizard = a.ui.table_wizard.get_contents()
			debug.msg(u"filling loop table")
			# First read the table into a dictionary of variables
			var_dict = {}
			for col in range(d.column_count()):
				var = None
				for row in range(d.row_count()):
					item = d.get_item(row, col)
					if item is None:
						break
					s = str(item.text())
					if s == u'':
						break
					if row == 0:
						var = self.experiment.sanitize(s, True)
						var_dict[var] = []
					elif var is not None:
						var_dict[var].append(s)

			# If the variable wizard was not parsed correctly, provide a
			# notification and do nothin
			if len(var_dict) == 0:
				self.experiment.notify(
					_(u'You provided an empty or invalid variable definition. For an example of a valid variable definition, open the variable wizard and select "Show example".'))
				return

			# Then fill the loop table
			self.i = 0
			self.matrix = {}
			self.wizard_process(var_dict)
			self.set_cycle_count(len(self.matrix))
			self.lock = True
			self.loop_widget.ui.spin_cycles.setValue(self.cycle_count())
			self.lock = False
			self.refresh_loop_table()
			self.refresh_summary()
			self.apply_edit_changes()

	def init_edit_widget(self):

		"""Builds the loop controls."""

		super(loop, self).init_edit_widget(stretch=False)
		self.loop_widget = loop_widget(self.experiment.main_window)
		self.loop_widget.ui.widget_advanced.hide()
		self.edit_vbox.addWidget(self.loop_widget)
		self.auto_add_widget(self.loop_widget.ui.spin_cycles)
		self.auto_add_widget(self.loop_widget.ui.spin_repeat, u"repeat")
		self.auto_add_widget(self.loop_widget.ui.spin_skip, u"skip")
		self.auto_add_widget(self.loop_widget.ui.combobox_order, u"order")
		self.auto_add_widget(self.loop_widget.ui.checkbox_offset, u"offset")
		self.auto_add_widget(self.loop_widget.ui.combobox_item, u"item")
		self.auto_add_widget(self.loop_widget.ui.edit_break_if, u"break_if")
		self.loop_widget.ui.edit_break_if.setValidator(cond_validator(self,
			default=u'never'))
		self.loop_widget.ui.button_add_cyclevar.clicked.connect(
			self.add_cyclevar)
		self.loop_widget.ui.button_rename_cyclevar.clicked.connect(
			self.rename_cyclevar)
		self.loop_widget.ui.button_remove_cyclevar.clicked.connect(
			self.remove_cyclevar)
		self.loop_widget.ui.button_wizard.clicked.connect(self.wizard)
		self.loop_widget.ui.button_apply_weights.clicked.connect(
			self.apply_weights)
		self.loop_widget.ui.combobox_order.setItemIcon(0,
			self.experiment.icon(u"random"))
		self.loop_widget.ui.combobox_order.setItemIcon(1,
			self.experiment.icon(u"sequential"))
		self.loop_table = loop_table.loop_table(self, self.cycles,
			self.cyclevar_count())
		self.edit_vbox.addWidget(self.loop_table)

	def update_widget_state(self):

		"""
		desc:
			Enables or disables widgets, based on the settings.
		"""

		self.refresh_summary()
		if self.get(u"order") == u"random":
			self.loop_widget.ui.label_skip.setDisabled(True)
			self.loop_widget.ui.spin_skip.setDisabled(True)
			self.loop_widget.ui.checkbox_offset.setDisabled(True)
		else:
			self.loop_widget.ui.label_skip.setDisabled(False)
			self.loop_widget.ui.spin_skip.setDisabled(False)
			self.loop_widget.ui.checkbox_offset.setDisabled(
				type(self.skip) != int or self.skip < 1)
		break_if = self.get(u'break_if', _eval=False)
		if break_if not in [u'never', u''] or \
			self.get(u'offset', _eval=False) == u'yes' or \
			self.get(u'skip', _eval=False) != 0:
			self.loop_widget.ui.checkbox_advanced.setChecked(True)
			self.loop_widget.ui.widget_advanced.show()

	def edit_widget(self):

		"""Set the loop controls from the variables"""

		# Update the item combobox
		self.experiment.item_combobox(self.item, self.parents(),
			self.loop_widget.ui.combobox_item)
		super(loop, self).edit_widget()
		self.refresh_loop_table(lock=False)
		self.loop_widget.ui.spin_cycles.setValue(self.cycle_count())
		# Update advanced settings
		break_if = self.get(u'break_if', _eval=False)
		self.loop_widget.ui.edit_break_if.setText(break_if)
		self.update_widget_state()

	def apply_weights(self):

		"""Repeat certain cycles based on the value in a particular column"""

		var_list = self.cyclevar_list()
		if var_list is None:
			return

		weight_var, ok = QtGui.QInputDialog.getItem(
			self.experiment.ui.centralwidget, _(u"Apply weight"),
			_(u"Which variable contains the weights?"), var_list,
			editable=False)
		if not ok:
			return

		self.matrix = {}
		_row = 0
		for row in range(self.loop_table.rowCount()):
			self.matrix[_row] = {}
			weight = 1
			for col in range(self.loop_table.columnCount()):
				var = str(self.loop_table.horizontalHeaderItem(col).text())
				cell = self.loop_table.item(row, col)
				if cell is None:
					val = u''
				else:
					val = str(self.loop_table.item(row, col).text())
				if var == weight_var:
					try:
						weight = int(val)
					except:
						weight = 1
				self.matrix[_row][var] = val
			if weight <= 0:
				del self.matrix[_row]
			else:
				_row += 1
				while weight > 1:
					weight -= 1
					if _row-1 in self.matrix:
						self.matrix[_row] = self.matrix[_row-1]
					_row += 1
		self.set_cycle_count(_row)
		self.update()

	def apply_edit_changes(self, dummy=None):

		"""
		Sets the variables from the controls.

		Keyword arguments:
		dummy	-- A dummy argument passed by the signal handler. (default=None)
		"""

		# Set item to run
		item = str(self.loop_widget.ui.combobox_item.currentText())
		self.set(u'item', item)
		# Validate and set the break-if statement
		break_if = self.clean_cond(self.loop_widget.ui.edit_break_if.text(),
			default=u'never')
		self.loop_widget.ui.edit_break_if.setText(break_if)
		self.set(u'break_if', break_if)
		# Walk through the loop table and apply all changes
		self.matrix = {}
		for row in range(self.loop_table.rowCount()):
			self.matrix[row] = {}
			for col in range(self.loop_table.columnCount()):
				var = str(self.loop_table.horizontalHeaderItem(col).text())
				cell = self.loop_table.item(row, col)
				if cell is None:
					val = u''
				else:
					val = str(self.loop_table.item(row, col).text())
				if not self.sanitize_check(val):
					val = self.sanitize(val)
				self.matrix[row][var] = val
		row = self.loop_table.currentRow()
		column = self.loop_table.currentColumn()
		self.set_cycle_count(self.loop_widget.ui.spin_cycles.value())
		self.refresh_loop_table()
		self.loop_table.setCurrentCell(row, column)
		super(loop, self).apply_edit_changes()
		self.experiment.build_item_tree()
		self.update_widget_state()

	def build_item_tree(self, toplevel=None, items=[], max_depth=-1,
		extra_info=None):

		"""See qtitem."""

		items.append(self.name)
		widget = tree_item_item(self, extra_info=extra_info)
		if toplevel is not None:
			toplevel.addChild(widget)
		if (max_depth < 0 or max_depth > 1) \
			and self.item in self.experiment.items:
			self.experiment.items[self.item].build_item_tree(widget, items,
				max_depth=max_depth-1)
		return items

	def is_child_item(self, item):

		"""See qtitem."""

		return self.item == item or (self.item in self.experiment.items and \
			self.experiment.items[self.item].is_child_item(item))

	def insert_child_item(self, item_name, index=0):

		"""See qtitem."""

		self.item = item_name
		self.update()
		self.main_window.set_unsaved(True)

	def remove_child_item(self, item_name, index=0):

		"""See qtitem."""

		if item_name == self.item:
			self.item = u''
		self.update()
		self.main_window.set_unsaved(True)
