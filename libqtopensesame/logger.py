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

import libopensesame.logger
import libqtopensesame.qtitem
from PyQt4 import QtCore, QtGui

class logger(libopensesame.logger.logger, libqtopensesame.qtitem.qtitem):

	"""GUI controls for the logger item"""

	def __init__(self, name, experiment, string = None):

		"""
		Constructor

		Arguments:
		name -- the name of the item
		experiment -- the experiment

		Keyword arguments:
		string -- the definition string for the item (default = None)
		"""

		libopensesame.logger.logger.__init__(self, name, experiment, string)
		libqtopensesame.qtitem.qtitem.__init__(self)

	def init_edit_widget(self):

		"""Construct the edit_widget that contains the controls"""

		self.lock = True # Lock to prevent recursion

		libqtopensesame.qtitem.qtitem.init_edit_widget(self, False)
		self.edit_grid_widget.hide()

		# The loop table with corresponding buttons
		self.logvar_table = QtGui.QTableWidget(255, 3)
		self.logvar_table.horizontalHeader().setStretchLastSection(True)
		self.logvar_table.verticalHeader().setVisible(False)

		self.logvar_table.setGridStyle(QtCore.Qt.NoPen)
		self.logvar_table.setAlternatingRowColors(True)
		self.logvar_table.setColumnWidth(0, 24)
		self.logvar_table.setColumnWidth(1, 300)

		vbox = QtGui.QVBoxLayout()
		vbox.setContentsMargins(0, 0, 0, 0)

		button_add = QtGui.QPushButton(self.experiment.icon("add"), "Add custom variable")
		button_add.clicked.connect(self.add_custom)
		button_add.setToolTip("Add an arbitrary variable by name")

		button_suggest = QtGui.QPushButton(self.experiment.icon("apply"), "Smart select")
		button_suggest.clicked.connect(self.suggest_variables)
		button_suggest.setToolTip("Automatically select (likely) relevant variables")

		button_select_all = QtGui.QPushButton(self.experiment.icon("apply"), "Select all")
		button_select_all.clicked.connect(self.select_all)
		button_select_all.setToolTip("Select all variables")

		button_deselect_all = QtGui.QPushButton(self.experiment.icon("clear"), "Deselect all")
		button_deselect_all.clicked.connect(self.deselect_all)
		button_deselect_all.setToolTip("Deselect all variables")

		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(button_select_all)
		hbox.addWidget(button_deselect_all)
		hbox.addStretch()
		hbox.addWidget(button_suggest)
		hbox.addWidget(button_add)
		hbox.setMargin(0)

		self.logvar_buttons = QtGui.QWidget()
		self.logvar_buttons.setLayout(hbox)

		self.checkbox_ignore_missing = QtGui.QCheckBox("Use 'NA' for variables that have not been set")
		self.checkbox_ignore_missing.stateChanged.connect(self.apply_edit_changes)

		self.checkbox_auto_log = QtGui.QCheckBox("Automatically detect and log all variables")
		self.checkbox_auto_log.stateChanged.connect(self.apply_edit_changes)

		vbox.addWidget(self.checkbox_ignore_missing)
		vbox.addWidget(self.checkbox_auto_log)
		vbox.addWidget(self.logvar_buttons)
		vbox.addWidget(self.logvar_table)

		widget = QtGui.QWidget()
		widget.setLayout(vbox)

		self.edit_vbox.addWidget(widget)
		self.lock = False # Unlock

	def edit_widget(self):

		"""
		Update the edit_widget to reflect changes in the item

		Returns:
		The edit widget
		"""

		self.lock = True
		libqtopensesame.qtitem.qtitem.edit_widget(self)

		if self.get("auto_log") == "yes":
			self.checkbox_auto_log.setChecked(True)
			self.logvar_buttons.setDisabled(True)
			self.logvar_table.setDisabled(True)
		else:
			self.checkbox_auto_log.setChecked(False)
			self.logvar_buttons.setEnabled(True)
			self.logvar_table.setEnabled(True)

		self.checkbox_ignore_missing.setChecked(self.get("ignore_missing") == "yes")

		self.logvar_table.setRowCount(0)

		self.logvar_table.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem(""))
		self.logvar_table.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem("Variable"))
		self.logvar_table.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem("Source item(s)"))

		# Fill the table
		row = 0
		var_rows = {}
		all_vars = []
		for var, val, item in self.experiment.var_list():

			# Only add a new row if the variable isn't already in the table
			if var not in all_vars:

				all_vars.append(var)
				var_rows[var] = row
				checkbox = QtGui.QCheckBox()
				checkbox.var = var
				checkbox.stateChanged.connect(self.apply_edit_changes)
				if var in self.logvars:
					checkbox.setChecked(True)

				self.logvar_table.insertRow(row)
				self.logvar_table.setCellWidget(row, 0, checkbox)
				self.logvar_table.setCellWidget(row, 1, QtGui.QLabel(var))
				self.logvar_table.setCellWidget(row, 2, QtGui.QLabel(item))
				row += 1

			# .. otherwise change the source item(s) column
			else:

				label = self.logvar_table.cellWidget(var_rows[var], 2)
				label.setText(label.text() + "; " + item)

		for var in self.logvars:
			if var not in all_vars:
				checkbox = QtGui.QCheckBox()
				checkbox.var = var
				checkbox.stateChanged.connect(self.apply_edit_changes)
				checkbox.setChecked(True)
				self.logvar_table.insertRow(row)
				self.logvar_table.setCellWidget(row, 0, checkbox)
				self.logvar_table.setCellWidget(row, 1, QtGui.QLabel(var))
				self.logvar_table.setCellWidget(row, 2, QtGui.QLabel("custom"))
				row += 1

		self.lock = False
		return self._edit_widget

	def apply_edit_changes(self, dummy = None):

		"""
		Update the item to match the edit_widget

		Keyword arguments:
		dummy -- a dummy argument passed by the signal handler (default = None)
		"""

		if not libqtopensesame.qtitem.qtitem.apply_edit_changes(self, False) or self.lock:
			return

		if self.checkbox_auto_log.isChecked():
			self.set("auto_log", "yes")
			self.logvar_buttons.setDisabled(True)
			self.logvar_table.setDisabled(True)
		else:
			self.set("auto_log", "no")
			self.logvar_buttons.setDisabled(False)
			self.logvar_table.setDisabled(False)

		if self.checkbox_ignore_missing.isChecked():
			self.set("ignore_missing", "yes")
		else:
			self.set("ignore_missing", "no")

		self.logvars = []
		for row in range(self.logvar_table.rowCount()):
			checkbox = self.logvar_table.cellWidget(row, 0)

			if checkbox != None:
				if checkbox.isChecked():
					self.logvars.append(checkbox.var)

		self.experiment.main_window.refresh(self.name, refresh_edit = False)

	def suggest_variables(self):

		"""Smart select all variables that should probably be logged"""

		i = 0
		for item in self.experiment.items:
			if self.experiment.items[item].item_type in ("loop", "keyboard_response", "mouse_response"):
				for var, val in self.experiment.items[item].var_info():
					if var not in self.logvars and var != "time_%s" % item and var != "count_%s" % item:
						self.logvars.append(var)
			if self.experiment.items[item].item_type == "sequence":
				for var, val in self.experiment.items[item].var_info():
					if var not in self.logvars and var == "count_%s" % item:
						self.logvars.append(var)

		self.edit_widget()
		self.experiment.main_window.refresh(self.name)

	def select_all(self):

		"""Select all variables"""

		for var, val, item in self.experiment.var_list():
			if var not in self.logvars:
				self.logvars.append(var)

		self.edit_widget()
		self.experiment.main_window.refresh(self.name)

	def deselect_all(self):

		"""Deselect all variables"""

		self.logvars = []
		self.edit_widget()
		self.experiment.main_window.refresh(self.name)

	def add_custom(self):

		"""Select a custom variable by name that is not recognized"""

		var, ok = QtGui.QInputDialog.getText( \
			self.experiment.main_window.ui.centralwidget, \
			"Add custom variable", "Which variable do you wish to log?")
		if ok:
			var = self.experiment.sanitize(var, strict=True, allow_vars=False)
			if var == "":
				self.experiment.notify( \
					"The variable name you entered was not valid. A variable name may consist of characters, numbers and underscores.")
				return
			if var not in self.logvars:
				self.logvars.append(var)
				self.edit_widget()
				self.experiment.main_window.refresh(self.name)
				
	def rename_var(self, item, from_name, to_name):
	
		"""
		A notification that a variable has been renamed
		
		Arguments:
		item -- the item doing the renaming		
		from_name -- the old variable name
		to_name -- the new variable name
		"""
	
		if from_name in self.logvars:
			if self.experiment.debug:
				print "logger.rename_var(): '%s' has been renamed to '%s'" % (from_name, to_name)				
			resp = QtGui.QMessageBox.question(self.experiment.main_window, "Use new name in logger?",
				"Do you want to use the new name in the logger item '%s' as well?" % self.name,
				QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
			if resp == QtGui.QMessageBox.No:
				return				
			self.logvars.remove(from_name)
			self.logvars.append(to_name)
			self.edit_widget()

