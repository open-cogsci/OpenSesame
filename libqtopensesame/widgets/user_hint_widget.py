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

from libqtopensesame.ui import user_hint_widget_ui
from PyQt4 import QtGui

class user_hint_widget(QtGui.QFrame):

	"""Provides various informative hints to the user"""

	def __init__(self, parent, item):

		"""
		Constructor.

		Arguments:
		parent		--	The parent QWidget.
		item		--	The item to provide a header for.
		"""

		QtGui.QWidget.__init__(self)	
		self.main_window = parent
		self.item = item
		self.ui = user_hint_widget_ui.Ui_user_hint_widget()
		self.ui.setupUi(self)
		self.ui.button_edit_script.clicked.connect(self.item.open_script_tab)
		self.main_window.theme.apply_theme(self)
		self.hide()
		
	def add_user_hint(self, hint):
		
		"""
		Adds a user hint.
		
		Arguments:
		hint		--	A text with the user hint.
		"""
		
		self.hints.append(hint)

	def clear(self):
		
		"""Clears all user hints."""
		
		self.hints = []
		self.hide()
		
	def refresh(self):
		
		"""Updates the widget with the current user hints."""
		
		if len(self.hints) == 0:
			self.hide()
			return		
		s = '\n'.join(self.hints)
		self.ui.label_user_hint.setText(s)
		self.show()