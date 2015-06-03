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

from libqtopensesame.widgets import good_looking_table
from libqtopensesame.misc import _
from PyQt4 import QtCore, QtGui

class loop_table(good_looking_table.good_looking_table):

	"""The looptable extends the QtTableWidget to allow copying and pasting"""

	def __init__(self, loop, rows, columns, parent=None):

		"""
		Constructor

		Arguments:
		loop -- the loop item
		rows -- the nr of rows
		columns -- the nr of columns

		Keyword arguments:
		parent -- parent QWidget (default=None)
		"""

		self.pos = None
		self.loop = loop
		self.lock = False

		icons = {}
		icons["cut"] = self.loop.experiment.icon("cut")
		icons["copy"] = self.loop.experiment.icon("copy")
		icons["paste"] = self.loop.experiment.icon("paste")
		icons["clear"] = self.loop.experiment.icon("clear")

		if not isinstance(rows, int):
			self.loop.user_hint_widget.add(
				_(u'Invalid or variably defined number of cycles: %s' % rows))
			self.loop.user_hint_widget.refresh()
			rows = 0
		good_looking_table.good_looking_table.__init__(self,
			rows, columns, icons, parent)
		self.cellChanged.connect(self.apply_changes)

	def paste(self):

		"""Paste data from the clipboard into the table"""

		self.lock = True
		good_looking_table.good_looking_table.paste(self)
		self.lock = False
		self.apply_changes()

	def _clear(self):

		"""Clear the table"""

		self.lock = True
		good_looking_table.good_looking_table._clear(self)
		self.lock = False
		self.apply_changes()

	def apply_changes(self):

		"""
		Apply changes to the table and make sure that the cursor is restored to
		its previous position
		"""

		if self.lock:
			return
		self.loop.apply_edit_changes()

	def set_text(self, cycle, col, text):

		"""
		desc:
			Sets text in the loop table in a way that doesn't trigger a
			cellChanged signal.

		arguments:
			cycle:
				desc:	The row.
				type:	int
			col:
				desc:	The column.
				type:	int
			text:
				desc:	The text.
				type:	unicode
		"""

		self.blockSignals(True)
		self.setItem(cycle, col, QtGui.QTableWidgetItem(text))
		self.blockSignals(False)
