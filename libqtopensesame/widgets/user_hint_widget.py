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

from PyQt4 import QtGui
from libqtopensesame.misc.base_subcomponent import base_subcomponent

class user_hint_widget(QtGui.QFrame, base_subcomponent):

	"""
	desc:
		Provides informative hints to the user.
	"""

	def __init__(self, main_window, item):

		"""
		desc:
			Constructor.

		arguments:
			main_window:	A qtopensesame object.
			item:			A qtitem.
		"""

		super(user_hint_widget, self).__init__(main_window)
		self.setup(main_window, ui=u'widgets.user_hint_widget')
		self.item = item
		self.clear()
		self.ui.button_edit_script.clicked.connect(self.item.show_script)
		self.hide()

	def disable(self, disabled=True):

		"""
		desc:
			Disables the widget.

		keywords:
			disabled:
				desc:	Indicates whether the widget should be disabled.
				type:	bool
		"""

		self.ui.button_edit_script.setDisabled(disabled)

	def add_user_hint(self, hint):

		"""
		desc:
			Adds a user hint.

		arguments:
			hint:		A user-hint text.
		"""

		self.hints.append(hint)

	def clear(self):

		"""
		desc:
			Clears all user hints.
		"""

		self.hints = []
		self.hide()

	def refresh(self):

		"""
		desc:
			Updates the widget with the current user hints.
		"""

		if len(self.hints) == 0:
			self.hide()
			return
		s = u'\n'.join(self.hints)
		self.ui.label_user_hint.setText(s)
		self.show()
