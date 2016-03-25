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

from qtpy import QtCore, QtWidgets
from libqtopensesame.misc.base_subcomponent import base_subcomponent

class line_edit_filter(base_subcomponent, QtWidgets.QLineEdit):

	"""
	desc:
		An action element for the quick switcher. We need to re-implement this
		so that we can capture key-down presses that switch to the list.
	"""

	def __init__(self, dialog):

		"""
		desc:
			Constructor.

		arguments:
			dialog:
				desc:	The parent dialog.
				type:	quick_switcher
		"""

		super(line_edit_filter, self).__init__(dialog)
		self.dialog = dialog
		self.setup(dialog)

	def keyPressEvent(self, e):

		"""
		desc:
			Process key down presses to switch to the list.

		arguments:
			e:
				type:	QKeyEvent
		"""

		if e.key() == QtCore.Qt.Key_Down:
			e.accept()
			self.dialog.focus_list()
			return
		super(line_edit_filter, self).keyPressEvent(e)
