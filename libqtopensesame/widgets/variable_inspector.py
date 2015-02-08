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

from libopensesame import debug
from libqtopensesame.widgets.base_widget import base_widget
from PyQt4 import QtCore, QtGui

class variable_inspector(base_widget):

	def __init__(self, main_window):

		"""
		desc:
			Constructor

		arguments:
			main_window:	A qtopensesame object.
		"""

		super(variable_inspector, self).__init__(main_window,
			ui=u'widgets.variable_inspector')
		self.unsorted = True
		self.ui.edit_variable_filter.textChanged.connect(self.refresh)
		self.ui.button_help_variables.clicked.connect(
			self.main_window.ui.tabwidget.open_variables_help)

	def refresh(self):

		"""
		desc:
			Refresh the variable-inspector table.
		"""

		if self.unsorted:
			self.ui.table_variables.sortItems(0, QtCore.Qt.AscendingOrder)
			self.unsorted = False
		scrollpos = self.ui.table_variables.verticalScrollBar().sliderPosition()
		col = self.ui.table_variables.currentColumn()
		row = self.ui.table_variables.currentRow()
		filt = str(self.ui.edit_variable_filter.text())
		self.ui.table_variables.setSortingEnabled(False)
		i = 0
		for var, val, item in self.experiment.var_list(filt):
			self.ui.table_variables.insertRow(i)
			val = self.experiment.unistr(val)
			self.ui.table_variables.setItem(i, 0,
				sortable(var, u'%s_%s_%s' % (var,val,item)))
			self.ui.table_variables.setItem(i, 1, sortable(val,
				u'%s_%s_%s' % (val,var,item)))
			self.ui.table_variables.setItem(i, 2, sortable(item,
				u'%s_%s_%s' % (item,var,val)))
			i += 1
		self.ui.table_variables.setRowCount(i)
		self.ui.table_variables.setSortingEnabled(True)
		self.ui.table_variables.setCurrentCell(row, col)
		self.ui.table_variables.verticalScrollBar().setSliderPosition(scrollpos)

	def set_focus(self):

		"""
		desc:
			Sets the focus on the filter widget.
		"""

		self.ui.edit_variable_filter.setFocus()

class sortable(QtGui.QTableWidgetItem):

	"""
	desc:
		A sortable QTableWidgetItem.
	"""

	def __init__(self, text, sort_key):

		"""
		desc:
			Constructor.

		arguments:
			text:		The cell text.
			sort_key:	The key to use for sorting.
		"""

		QtGui.QTableWidgetItem.__init__(self, text,
			QtGui.QTableWidgetItem.UserType)
		self.sort_key = sort_key

	def __lt__(self, other):

		"""
		desc:
			Sort operator (less than).

		arguments:
			other:	Another sortable object.

		returns:
			A boolean indicating whether self is less than other.
		"""

		return self.sort_key < other.sort_key
