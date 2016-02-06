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

from qtpy import QtWidgets
from libqtopensesame.misc.base_subcomponent import base_subcomponent

class user_hint_widget(QtWidgets.QFrame, base_subcomponent):

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
		self.ui.button_hide.clicked.connect(self.dismiss)
		self.hints = []
		self.dismissed_hints = []
		self.clear()

	def disable(self, disabled=True):

		"""
		desc:
			Disables the widget.

		keywords:
			disabled:
				desc:	Indicates whether the widget should be disabled.
				type:	bool
		"""

		self.ui.button_hide.setDisabled(disabled)

	def add(self, hint):

		"""
		desc:
			Adds a user hint.

		arguments:
			hint:
				desc:	A user-hint message, or a list of messages.
				type:	[list, unicode]
		"""

		if not isinstance(hint, list):
			hint = [hint]
		for _hint in hint:
			if _hint in self.dismissed_hints:
				continue
			if _hint in self.hints:
				continue
			self.hints.append(_hint)

	def dismiss(self):

		"""
		desc:
			Dismiss all current user hints.
		"""

		self.dismissed_hints += self.hints
		self.clear()

	def clear(self):

		"""
		desc:
			Clears all user hints.
		"""

		self.hints = []
		self.refresh()

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
