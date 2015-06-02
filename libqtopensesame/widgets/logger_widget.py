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
from PyQt4 import QtGui
from libqtopensesame.misc import _
from libqtopensesame.widgets.base_widget import base_widget

class logger_widget(base_widget):

	"""
	desc:
		The logger widget.
	"""

	def __init__(self, logger):

		"""
		desc:
			Constructor.

		arguments:
			sketchpad:
				desc:	A logger object.
				type:	logger
		"""

		super(logger_widget, self).__init__(logger.main_window,
			ui=u'widgets.logger')
		self.logger = logger
		self.checkboxes = []
		self.ui.button_select_all.clicked.connect(self.select_all)
		self.ui.button_deselect_all.clicked.connect(self.deselect_all)
		self.ui.button_smart_select.clicked.connect(self.smart_select)
		self.ui.button_add_custom_variable.clicked.connect(
			self.add_custom_variable)

	def select_all(self):

		"""
		desc:
			Selects all known variables.
		"""

		self.logger.logvars = [t[0] for t in self.experiment.var_list()]
		self.logger.update()

	def deselect_all(self):

		"""
		desc:
			Deselects all currently selected variables.
		"""

		self.logger.logvars = []
		self.logger.update()

	def smart_select(self):

		"""
		desc:
			Selects variables that are likely relevant to the user. Those are
			all variables from loop, keyboard_response, and mouse_response
			items, except for the time_* and count_* variables. In addition,
			all count_* variables from sequence items are selected.
		"""

		for item_name in self.experiment.items:
			if item_name in self.experiment.items.unused():
				continue
			item = self.experiment.items[item_name]
			if item.item_type in (u"loop", u"keyboard_response",
				u"mouse_response"):
				for var, val in item.var_info():
					if var not in self.logger.logvars and \
						var != u"time_%s" % item and var != u"count_%s" % item:
						self.logger.logvars.append(var)
			if item.item_type == u"sequence":
				for var, val in item.var_info():
					if var not in self.logger.logvars and \
						var == u"count_%s" % item:
						self.logger.logvars.append(var)
		self.logger.update()
		self.logger.user_hint_widget.add(_(u'A smart selection of variables '
			u'has been made. Are you sure that all relevant variables are now '
			u'selected?'))
		self.logger.user_hint_widget.refresh()

	def add_custom_variable(self):

		"""
		desc:
			Provides a simple dialog for the user to add a custom variable.
		"""

		name = self.text_input(_(u'Add custom variable'),
			message=_(u'Which variable do you wish to log?'))
		if self.experiment.syntax.sanitize(name, strict=True,
			allow_vars=False) != name:
			self.notify(_(u'"%s" is not a valid variable name!' % name))
			return
		self.logger.logvars.append(name)
		self.logger.update()

	def update(self):

		"""
		desc:
			Fills the table with variables, makes a selection, and disables/
			enables the table.
		"""

		# Fill the table
		row = 0
		var_rows = {}
		all_vars = []
		self.checkboxes = []
		self.table_var.clear()
		for var, val, item in self.experiment.var_list():
			# Only add a new row if the variable isn't already in the table
			if var not in all_vars:
				all_vars.append(var)
				var_rows[var] = row
				checkbox = QtGui.QCheckBox()
				checkbox.var = var
				checkbox.clicked.connect(self.logger.apply_edit_changes)
				self.checkboxes.append(checkbox)
				if var in self.logger.logvars:
					checkbox.setChecked(True)
				self.table_var.insertRow(row)
				self.table_var.setCellWidget(row, 0, checkbox)
				self.table_var.setCellWidget(row, 1, QtGui.QLabel(var))
				self.table_var.setCellWidget(row, 2, QtGui.QLabel(item))
				row += 1
			# .. otherwise change the source item(s) column
			else:
				label = self.table_var.cellWidget(var_rows[var], 2)
				label.setText(label.text() + "; " + item)
		for var in self.logger.logvars:
			if var not in all_vars:
				checkbox = QtGui.QCheckBox()
				checkbox.var = var
				checkbox.clicked.connect(self.logger.apply_edit_changes)
				checkbox.setChecked(True)
				self.checkboxes.append(checkbox)
				self.table_var.insertRow(row)
				self.table_var.setCellWidget(row, 0, checkbox)
				self.table_var.setCellWidget(row, 1, QtGui.QLabel(var))
				self.table_var.setCellWidget(row, 2, QtGui.QLabel("custom"))
				row += 1
		if self.logger.var.get(u'auto_log', _eval=False) == u'yes':
			auto = True
		else:
			auto = False
		self.table_var.setDisabled(auto)
		self.button_select_all.setDisabled(auto)
		self.button_deselect_all.setDisabled(auto)
		self.button_smart_select.setDisabled(auto)
		self.button_add_custom_variable.setDisabled(auto)

	def var_selection(self):

		"""
		returns:
			desc:	A list of selected variable names.
			type:	list
		"""

		l = []
		for checkbox in self.checkboxes:
			if checkbox.isChecked():
				l.append(str(checkbox.var))
		return l
