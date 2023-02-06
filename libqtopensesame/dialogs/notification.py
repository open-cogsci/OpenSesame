# -*- coding:utf-8 -*-

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
from libqtopensesame.dialogs.base_dialog import BaseDialog


class Notification(BaseDialog):

    r"""The notification dialog shows a simple notification."""
    def __init__(self, main_window, msg, title=None, icon=None):
        r"""Constructor.

        Parameters
        ----------
        main_window
            The main window object.
        msg
            A notification message.
        title, optional
            A custom dialog title.
        icon, optional
            A custom dialog icon.
        """
        super().__init__(main_window, ui=u'dialogs.notification_dialog')
        self.ui.textedit_notification.setHtml(msg)
        if title is not None:
            self.ui.label_title.setText(title)
        if icon is not None:
            self.ui.label_notification.setPixmap(self.theme.qpixmap(icon))
        self.adjustSize()


# Alias for backwards compatibility
notification = Notification
