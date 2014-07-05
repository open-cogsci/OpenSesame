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

from libqtopensesame.misc.base_component import base_component
from PyQt4 import QtCore, QtGui

class base_dialog(QtGui.QDialog, base_component):

	"""
	desc:
		A base class for dialogs.
	"""

	def __init__(self, main_window, ui=None, frameless=False):

		"""
		desc:
			Constructor.

		arguments:
			main_window:	A qtopensesame object.

		keywords:
			ui:
							An id for a user-interface file, for example
							'dialogs.quick_open_item'.
			frameless:		Indicates whether the dialog should have a frame.
		"""

		window_flags = QtCore.Qt.Dialog
		if frameless:
			window_flags = window_flags | QtCore.Qt.FramelessWindowHint
		super(base_dialog, self).__init__(main_window, flags=window_flags)
		self.setup(main_window, ui=ui)

