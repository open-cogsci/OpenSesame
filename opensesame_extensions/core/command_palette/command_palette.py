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
from pyqt_code_editor.widgets import QuickOpenDialog
from libqtopensesame.misc.translate import translation_context
_ = translation_context('command_palette', category='extension')


class QuickCommandPaletteDialog(QuickOpenDialog):
    def __init__(self, parent, items):
        super().__init__(parent, items, title=_("Command palette"))

    def on_item_selected(self, item_dict: dict):
        print(item_dict)
        item_dict['action']()


class CommandPalette(BaseExtension):

    def activate(self):

        QuickCommandPaletteDialog(
            self.main_window,
            self._actions(self.main_window.menuBar())).exec()

    def _actions(self, menu):

        actions = []
        for action in menu.actions():
            if action.menu() is not None:
                actions += self._actions(action.menu())
                continue
            if action.text():
                actions.append({'name': action.text().replace(u'&', ''),
                                'action': action.trigger})
        return actions

    def _trigger(self, action):

        action.trigger()

    def event_command_palette_activate(self):

        self.activate()
