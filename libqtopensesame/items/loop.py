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

__author__ = "Sebastiaan Mathot"
__license__ = "GPLv3"

import copy
import libopensesame.loop
from libqtopensesame.items import qtitem
from libqtopensesame.misc import _
from libqtopensesame.ui import loop_wizard_dialog_ui, loop_widget_ui
from libqtopensesame.widgets import loop_table
from libopensesame import debug
from PyQt4 import QtCore, QtGui

class loop(libopensesame.loop.loop, qtitem.qtitem):

	"""The GUI for the loop item"""

	def __init__(self, name, experiment, string=None):

		"""
		Constructor

		Arguments:
		name -- name of the item
		experiment -- the experiment

		Keyword arguments:
		string -- definition string (default = None)
		"""

		libopensesame.loop.loop.__init__(self, name, experiment, string)
		qtitem.qtitem.__init__(self)
		self.sanity_criteria['repeat'] = {'type' : [int, float], \
			'msg' : 'Must be a numeric value'}
		self.sanity_criteria['cycles'] = {'type' : int, \
			'msg' : 'Must be a integer numeric value'}
		self.sanity_criteria['skip'] = {'type' : int, \
			'msg' : 'Must be a integer numeric value'}			

	def rename(self, from_name, to_name):

		"""
		Handle an item rename

		Arguments:
		from_name -- the old name of the item to be renamed
		to_name -- the new name of the item to be renamed
		"""

		qtitem.qtitem.rename(self, from_name, to_name)
		if self.item == from_name:
			self.item = to_name

	def delete(self, item_name, item_parent=None, index=None):

		"""
		Delete an item

		Arguments:
		item_name -- the name of the item to be deleted

		Keywords arguments:
		item_parent -- the parent item (default=None)
		index -- the index of the item in the parent (default=None)
		"""

		if self.item == item_name and item_parent == self.name:
			self.item = ""

	def add_cyclevar(self):

		"""Present a dialog and add a variable"""

		var_name, ok = QtGui.QInputDialog.getText(self.loop_table, \
			_('New variable'), \
			_('Enter a variable name, optionally followed by a default value (i.e., \"varname defaultvalue\")'))

		if ok:
			l = self.cyclevar_list()
			var_name = unicode(var_name)

			# Split by space, because a name may be followed by a default value
			_l = var_name.split()
			if len(_l) > 1:
				default = self.experiment.usanitize(_l[1])
				var_name = _l[0]
			else:
				default = ""

			# Check for valid variable names
			var_name = self.experiment.sanitize(var_name, strict=True, \
				allow_vars=False)
			if var_name == "":
				self.experiment.notify( \
					"Variable names must consist of alphanumeric characters and underscores, and must not be empty")
				return

			# Check if the variable already exists
			if l != None and var_name in l:
				self.experiment.notify( \
					_("A variable with the name '%s' already exists") \
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
		Return a list of variables

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
		A notification that a variable has been renamed

		Arguments:
		item -- the item doing the renaming
		from_name -- the old variable name
		to_name -- the new variable name
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

		"""Present a dialog and rename a variable"""

		var_list = self.cyclevar_list()
		if var_list == None:
			return

		old_var, ok = QtGui.QInputDialog.getItem( \
			self.experiment.ui.centralwidget, _("Rename variable"), \
			_("Which variable do you want to rename?"), var_list, \
			editable=False)
		if ok:
			_new_var, ok = QtGui.QInputDialog.getText(self.loop_table, \
				_('New variable'), _('Enter a new variable name'), text=old_var)
			if ok and _new_var != old_var:
				old_var = str(old_var)
				new_var = self.experiment.sanitize(_new_var, strict=True, \
					allow_vars=False)
				if _new_var != new_var or new_var == "":
					self.experiment.notify( \
						_("Please use only letters, numbers and underscores"))
					return
				if new_var in var_list:
					self.experiment.notify( \
						_("A variable with the name '%s' already exists") % \
						new_var)
					return
			for item in self.experiment.items.values():
				item.rename_var(self.name, old_var, new_var)
			self.refresh_loop_table()
			self.apply_edit_changes()

	def remove_cyclevar(self):

		"""Present a dialog and remove a variable"""

		var_list = self.cyclevar_list()
		if var_list == None:
			return

		var, ok = QtGui.QInputDialog.getItem(self.experiment.ui.centralwidget, \
			_("Remove variable"), _("Which variable do you want to remove?"), \
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
		Count the number of variables in the loop

		Returns:
		The number of variables
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
		Count the number of cycles, which is the maximum of the table length
		and the 'cycles' variables

		Returns:
		The number of cycles
		"""

		return max(self.get("cycles"), len(self.matrix))

	def set_cycle_count(self, cycles, confirm=True):

		"""
		Sets the nr of cycles and truncates data if necessary

		Arguments:
		cycles -- the number of cycles

		Keyword arguments:
		confirm -- indicates if confirmation is required before data is removed
				   from the table (default=True)
		"""

		debug.msg("cycles = %d" % cycles)
		cont = True
		while cont:
			cont = False
			for i in self.matrix:
				if i >= cycles:

					# Check if the cells that will be removed are not empty
					empty = True
					for var in self.matrix[i]:
						if self.matrix[i][var] != "":
							empty = False

					# Ask for confirmation (only the first time)
					if not empty and confirm:
						resp = QtGui.QMessageBox.question( \
							self.experiment.ui.centralwidget, \
							_("Remove cycles?"), \
							_("By reducing the number of cycles, data will be lost from the table. Do you wish to continue?"), \
							QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
						if resp == QtGui.QMessageBox.No:
							return
						confirm = False

					# Delete the cycle and restart the loop
					del self.matrix[i]
					cont = True
					break

		self.set("cycles", cycles)

	def call_count(self):

		"""
		The nr of times that the target item is called in total,
		which depends on the repeat and cycles

		Returns:
		The nr of calls
		"""
		
		try:
			if self.order == "sequential" and self.offset != "yes":
				return int(self.cycles * self.repeat - self.skip)
			return int(self.cycles * self.repeat)
		except:
			return 0

	def refresh_loop_table(self, lock = True):

		"""
		Rebuild the loop table

		Keyword arguments:
		lock -- a boolean indicating whether the item should be locked to
				prevent recursion (default = True)
		"""

		if lock:
			self.lock = True

		# Don't clear and resize the table if this is not necessary, because
		# this makes the cursor jump
		if self.loop_table.rowCount() != self.cycles or \
			self.loop_table.columnCount() != self.cyclevar_count():
			self.loop_table.clear()
			self.loop_table.setRowCount(self.cycles)
			self.loop_table.setColumnCount(self.cyclevar_count())

		# Determine the order in which the columns are displayed
		column_order = []
		if self.cyclevar_list() != None:
			if self.has("column_order"):
				for var in str(self.get("column_order")).split(";"):
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
				self.loop_table.setItem(cycle, col, \
					QtGui.QTableWidgetItem(self.unsanitize( \
						self.matrix[cycle][var])))

		# Store the number of cycles and the column order
		self.set("cycles", max(self.get("cycles"), self.cycle_count()))
		self.set("column_order", ";".join(column_order))

		if lock:
			self.lock = False

	def wizard_process(self, d, l=[]):

		"""
		Rebuilds the loop table based on a dictionary of variables and levels

		Arguments:
		d -- a dictionary of variables and levels

		Keyword arguments:
		l -- a list of variables and values (default = [])
		"""
		
		if len(d) == 0:
			for var, val in l:
				if self.i not in self.matrix:
					self.matrix[self.i] = {}
				self.matrix[self.i][var] = val
			self.i += 1
			return
		var = d.keys()[0]
		for val in d[var]:
			_d = copy.copy(d)
			del _d[var]
			self.wizard_process(_d, l + [(var, val)])

	def wizard(self):

		"""Present the variable wizard dialog"""

		icons = {}
		icons["cut"] = self.experiment.icon("cut")
		icons["copy"] = self.experiment.icon("copy")
		icons["paste"] = self.experiment.icon("paste")
		icons["clear"] = self.experiment.icon("clear")		

		# Set up the wizard dialog
		a = QtGui.QDialog(self.experiment.main_window.ui.centralwidget)
		a.ui = loop_wizard_dialog_ui.Ui_loop_widget()
		a.ui.setupUi(a)
		self.experiment.main_window.theme.apply_theme(a)
		a.ui.table_example.build_context_menu(icons)
		a.ui.table_wizard.build_context_menu(icons)
		a.ui.table_example.hide()
		a.ui.table_wizard.setRowCount(255)
		a.ui.table_wizard.setColumnCount(255)

		if a.exec_() == QtGui.QDialog.Accepted:		
			debug.msg("filling loop table")
			# First read the table into a dictionary of variables
			var_dict = {}
			for col in range(a.ui.table_wizard.columnCount()):
				var = None
				for row in range(a.ui.table_wizard.rowCount()):
					item = a.ui.table_wizard.item(row, col)
					if item == None:
						break
					s = item.text()
					if row == 0:
						var = self.experiment.sanitize(s, True)
						var_dict[var] = []
					elif var != None:
						var_dict[var].append(self.experiment.usanitize(s))
			# Then fill the loop table
			self.i = 0
			self.matrix = {}
			self.wizard_process(var_dict)
			self.set_cycle_count(len(self.matrix))
			self.lock = True		
			self.loop_widget.ui.spin_cycles.setValue(self.cycle_count())
			self.lock = False
			self.refresh_loop_table()

	def init_edit_widget(self):

		"""Build the loop controls"""

		self.lock = True

		qtitem.qtitem.init_edit_widget(self, False)
		self.loop_widget = QtGui.QWidget()
		self.loop_widget.ui = loop_widget_ui.Ui_loop_widget()
		self.loop_widget.ui.setupUi(self.loop_widget)		
		self.experiment.main_window.theme.apply_theme(self.loop_widget)
		self.loop_widget.ui.widget_advanced.hide()		
		
		self.edit_vbox.addWidget(self.loop_widget)
		
		self.auto_add_widget(self.loop_widget.ui.spin_cycles)		
		self.auto_add_widget(self.loop_widget.ui.spin_repeat, "repeat")
		self.auto_add_widget(self.loop_widget.ui.spin_skip, "skip")
		self.auto_add_widget(self.loop_widget.ui.combobox_item, "item")
		self.auto_add_widget(self.loop_widget.ui.combobox_order, "order")
		self.auto_add_widget(self.loop_widget.ui.checkbox_offset, "offset")
		self.auto_add_widget(self.loop_widget.ui.edit_break_if, "break_if")
		
		self.loop_widget.ui.button_add_cyclevar.clicked.connect( \
			self.add_cyclevar)
		self.loop_widget.ui.button_rename_cyclevar.clicked.connect( \
			self.rename_cyclevar)			
		self.loop_widget.ui.button_remove_cyclevar.clicked.connect( \
			self.remove_cyclevar)			
		self.loop_widget.ui.button_wizard.clicked.connect( \
			self.wizard)
		
		self.loop_widget.ui.combobox_order.setItemIcon(0, \
			self.experiment.icon("random"))
		self.loop_widget.ui.combobox_order.setItemIcon(1, \
			self.experiment.icon("sequential"))

		self.loop_table = loop_table.loop_table(self, self.cycles, \
			self.cyclevar_count())
		self.edit_vbox.addWidget(self.loop_table)
		
		self.lock = False				
		return self._edit_widget

	def edit_widget(self):

		"""Set the loop controls from the variables"""

		self.lock = True
		debug.msg()			
		# Update the item combobox
		self.experiment.item_combobox(self.item, self.parents(), \
			self.loop_widget.ui.combobox_item)
		qtitem.qtitem.edit_widget(self)
		self.refresh_loop_table(lock=False)		
		self.loop_widget.ui.spin_cycles.setValue(self.cycle_count())
		
		if self.get("order") == "random":
			self.loop_widget.ui.label_skip.setDisabled(True)
			self.loop_widget.ui.spin_skip.setDisabled(True)
			self.loop_widget.ui.checkbox_offset.setDisabled(True)
		else:
			self.loop_widget.ui.label_skip.setDisabled(False)
			self.loop_widget.ui.spin_skip.setDisabled(False)
			self.loop_widget.ui.checkbox_offset.setDisabled( \
				self.get("skip") < 1)
				
		# Update the summary
		cc = self.call_count()					
		if self.order == "sequential" and self.offset != "yes":
			s = _("<b>%s</b> will be called <b>%s</b> x <b>%s</b> - <b>%s</b> = <b>%s</b> times in <b>%s</b> order") \
				% (self.item, self.cycles, self.repeat, self.skip, cc, \
				self.order)
		else:			
			s = _("<b>%s</b> will be called <b>%s</b> x <b>%s</b> = <b>%s</b> times in <b>%s</b> order") \
				% (self.item, self.cycles, self.repeat, cc, self.order)	
		if self.order == "sequential" and self.skip > 0:
			s += _(" starting at cycle <b>%d</b>") % self.skip
			if self.offset == "yes" and self.skip >= cc:
				s += _(" <font color='red'><b>(too many cycles skipped)</b></font>")
		if cc < 1:
			s += _(" <font color='red'><b>(zero or negative length)</b></font>")
		self.loop_widget.ui.label_summary.setText("<small>%s</small>" % s)		
		self.lock = False
		return self._edit_widget

	def apply_edit_changes(self, dummy = None):

		"""
		Set the variables from the controls

		Keyword arguments:
		dummy -- a dummy argument passed by the signal handler (default = None)
		"""
		
		if self.lock or not qtitem.qtitem.apply_edit_changes(self, False):
			return
			
		self.lock = True

		self.matrix = {}
		for row in range(self.loop_table.rowCount()):
			self.matrix[row] = {}
			for col in range(self.loop_table.columnCount()):
				var = str(self.loop_table.horizontalHeaderItem(col).text())
				cell = self.loop_table.item(row, col)
				if cell == None:
					val = ""
				else:
					val = self.auto_type(self.experiment.usanitize( \
						self.loop_table.item(row, col).text()))
				self.matrix[row][var] = val

		row = self.loop_table.currentRow()
		column = self.loop_table.currentColumn()

		self.set_cycle_count(self.loop_widget.ui.spin_cycles.value())
		self.refresh_loop_table()
		self.experiment.main_window.refresh(self.name)
		self.loop_table.setCurrentCell(row, column)
		self.lock = False	

	def build_item_tree(self, toplevel, items):

		"""
		Construct an item tree

		Keyword arguments:
		toplevel -- the toplevel widget (default = None)
		items -- a list of items that have been added, to prevent recursion
				 (default=[])

		Returns:
		An updated list of items that have been added
		"""

		widget = self.item_tree_widget(toplevel)
		toplevel.addChild(widget)
		if self.item in self.experiment.items and self.item != None and \
			self.item.strip() != "":
			if self.experiment.items[self.item] not in items:
				items.append(self.experiment.items[self.item])
			self.experiment.items[self.item].build_item_tree(widget, items)
		widget.setExpanded(True)
		return items

	def is_offspring(self, item):

		"""
		Checks if the item is offspring of the current item

		Arguments:
		item -- the potential offspring

		Returns:
		True if the passed item is offspring, False otherwise
		"""

		return self.item == item or (self.item in self.experiment.items and \
			self.experiment.items[self.item].is_offspring(item))

