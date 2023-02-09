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
import time
import platform
from libopensesame.py3compat import *
from libqtopensesame.extensions import BaseExtension
from qtpy.QtCore import PYQT_VERSION_STR


__author__ = u"Daniel Schreij"
__license__ = u"GPLv3"


class Notifications(BaseExtension):

    def event_startup(self):

        self.old_notifications = {}
        self.expiration_time = 60  # a minute
        self._suspend = False
        self.notification_area = QNotifications.QNotificationArea(
            self.tabwidget,
            useGlobalCSS=True
        )
        self.notification_area.move(0, 15)
        self.notification_area.setEntryEffect(u'fadeIn', 200)
        self.notification_area.setExitEffect(u'fadeOut', 200)
        # Filthly hack to make this work with Qt4 on the Mac
        # Otherwise the notifications are not shown on top.
        if platform.system() == "Darwin" and PYQT_VERSION_STR < '5':
            self.notification_area.setParent(self.main_window)
            self.notification_area.setParent(self.tabwidget)

    def event_notify(
            self,
            message,
            category='primary',
            timeout=5000,
            always_show=False,
            buttontext=None
    ):
        """ Show a notification 'message' in the style 'notification type' for
        'timeout' milliseconds (where 0 milliseconds displays the notification
        indefinitely, until the user removes it)."""
        if self._suspend:
            return
        current_time = time.time()
        # See if notification has been shown before. If it is within
        # self.expiration_time, don't show it again.
        if not always_show:
            if (message, category, timeout, buttontext) in self.old_notifications:
                prev_time = self.old_notifications[(
                    message,
                    category,
                    timeout,
                    buttontext
                )]
                if current_time - prev_time < self.expiration_time:
                    return
            # Add notification to old notifications list.
            self.old_notifications[(
                message,
                category,
                timeout,
                buttontext
            )] = current_time
        try:
            self.notification_area.display(
                message, category, timeout, timeout != 0, buttontext
            )
        except TypeError:
            # Older versions of QNotifications did not support the autohide
            # option
            self.notification_area.display(
                message, category, timeout, buttontext
            )

    def event_notify_suspend(self):

        self._suspend = True

    def event_notify_resume(self):

        self._suspend = False
