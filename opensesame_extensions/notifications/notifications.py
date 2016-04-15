# -*- coding: utf-8 -*-
"""
@author: Daniel Schreij

This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

This module is distributed under the Apache v2.0 License.
You should have received a copy of the Apache v2.0 License
along with this module. If not, see <http://www.apache.org/licenses/>.
"""

import QNotifications
from libopensesame.py3compat import *
from libqtopensesame.extensions import base_extension

__author__ = u"Daniel Schreij"
__license__ = u"GPLv3"

class notifications(base_extension):

	def event_startup(self):

		self.old_notifications = []
		self.notification_area = QNotifications.QNotificationArea(
			self.tabwidget, useGlobalCSS=True)
		self.notification_area.setEntryEffect(u'fadeIn', 200)
		self.notification_area.setExitEffect(u'fadeOut', 200)

	def event_notify(self, message, category='primary', timeout=5000):
		""" Show a notification 'message' in the style 'notification type' for
		'timeout' milliseconds (where 0 milliseconds displays the notification
		indefinitely, until the user removes it)."""

		if (message, category, timeout) in self.old_notifications:
			return
		self.old_notifications.append( (message, category, timeout) )
		self.notification_area.display(message, category, timeout)
