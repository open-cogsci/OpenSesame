# coding=utf-8

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
from libqtopensesame.extensions import BaseExtension


class CommandPalette(BaseExtension):

    def activate(self):

        self.extension_manager.fire(
            u'quick_select',
            haystack=self._actions(self.main_window.menuBar()),
            placeholder_text=_(u'Search actions …')
        )

    def _actions(self, menu):

        actions = []
        for action in menu.actions():
            if action.menu() is not None:
                actions += self._actions(action.menu())
                continue
            if action.text():
                actions.append((
                    action.text().replace(u'&', ''),
                    action,
                    self._trigger)
                )
        return actions

    def _trigger(self, action):

        action.trigger()

    def event_command_palette_activate(self):

        self.activate()
