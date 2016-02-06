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
from libqtopensesame.dialogs.base_dialog import base_dialog
from libqtopensesame.misc.config import cfg

class update(base_dialog):

	"""
	desc:
		A simple text-input dialog.
	"""

	def __init__(self, main_window, msg=None):

		"""
		desc:
			Constructor.

		arguments:
			main_window:	The main window object.
			msg:			A text message.
		"""

		super(update, self).__init__(main_window, ui=u'dialogs.update_dialog')
		self.ui.textedit_notification.setHtml(msg)
		self.adjustSize()

	def exec_(self):

		"""
		desc:
			Executes the dialog.
		"""

		self.ui.checkbox_auto_check_update.setChecked(cfg.auto_update_check)
		super(update, self).exec_()
		cfg.auto_update_check = self.ui.checkbox_auto_check_update.isChecked()
		self.main_window.update_preferences_tab()
