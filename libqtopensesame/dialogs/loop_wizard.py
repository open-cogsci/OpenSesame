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

from libqtopensesame.misc.config import cfg
from libqtopensesame.dialogs.base_dialog import base_dialog

class loop_wizard(base_dialog):

	"""
	desc:
		The loop-wizard dialog
	"""

	def __init__(self, main_window, msg=None):

		"""
		desc:
			Constructor.

		arguments:
			main_window:	The main window object.
			msg:			A text message.
		"""

		super(loop_wizard, self).__init__(main_window,
			ui=u'dialogs.loop_wizard_dialog')
		icons = {}
		icons[u"cut"] = self.experiment.icon(u"cut")
		icons[u"copy"] = self.experiment.icon(u"copy")
		icons[u"paste"] = self.experiment.icon(u"paste")
		icons[u"clear"] = self.experiment.icon(u"clear")
		self.ui.table_example.build_context_menu(icons)
		self.ui.table_wizard.build_context_menu(icons)
		self.ui.table_example.hide()
		self.ui.table_wizard.setRowCount(255)
		self.ui.table_wizard.setColumnCount(255)
		self.ui.table_wizard.set_contents(cfg.loop_wizard)

	def column_count(self):

		"""
		returns:
			The number of used columns in the table.
		"""

		return self.ui.table_wizard.columnCount()

	def row_count(self):

		"""
		returns:
			The number of used rows in the table.
		"""

		return self.ui.table_wizard.rowCount()

	def get_item(self, row, column):

		"""
		desc:
			Gets an item from the table.

		arguments:
			row:	A row number.
			column:	A column number.

		returns:
			An item.
		"""

		return self.ui.table_wizard.item(row, column)

	def exec_(self):

		"""
		desc:
			Executes the dialog.

		returns:
			The dialog return status.
		"""

		ret_val = super(loop_wizard, self).exec_()
		cfg.loop_wizard = self.ui.table_wizard.get_contents()
		return ret_val
