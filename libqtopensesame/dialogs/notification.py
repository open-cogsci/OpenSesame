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

from PyQt4 import QtCore, QtGui
from libqtopensesame.dialogs.base_dialog import base_dialog

class notification(base_dialog):

	"""
	desc:
		The notification dialog shows a simple notification.
	"""

	def __init__(self, main_window, msg, title=None, icon=None):

		"""
		desc:
			Constructor.

		arguments:
			main_window:	The main window object.
			msg:			A notification message.

		keywords:
			title:			A custom dialog title.
			icon:			A custom dialog icon.
		"""

		super(notification, self).__init__(main_window,
			ui=u'dialogs.notification_dialog')
		self.ui.textedit_notification.setHtml(msg)
		if title != None:
			self.ui.label_title.setText(title)
		if icon != None:
			self.ui.label_notification.setPixmap(self.theme.qpixmap(icon))
		self.adjustSize()
