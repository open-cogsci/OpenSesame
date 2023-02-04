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
from libopensesame.oslogging import oslogger
from libqtopensesame.extensions import base_extension


class restore_ui_elements(base_extension):

    """
    desc:
            Restores key UI elements when they have been accidentally hidden.
    """

    @base_extension.as_thread(1000)
    def event_startup(self):

        if (
                self.main_window.toolbar_items.isVisible() and
                (self.menubar.isVisible() or self.toolbar.isVisible()) and
                self.main_window.dock_overview.isVisible()
        ):
            return
        oslogger.debug('some key ui elements are hidden')
        from libqtopensesame._input.confirmation import confirmation
        if not confirmation(
                self.main_window,
                _('Some important elements of the user interface have been hidden. Do you want to show them again?'),
                title=_('Restore user interface'),
                default='yes'
        ).show():
            return
        oslogger.debug('showing key ui elements')
        self.main_window.toolbar_items.setVisible(True)
        self.menubar.setVisible(True)
        self.toolbar.setVisible(True)
        self.main_window.dock_overview.setVisible(True)
