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
import re
from pyqode.core import api
from qtpy import QtWidgets
from libqtopensesame.misc.config import cfg
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'pyqode_manager', category=u'extension')


class ConvertIndentationMode(api.Mode):
    """Comments/uncomments a set of lines using Ctrl+/."""
    
    def __init__(self):
        super().__init__()
        self._action_tabs_to_spaces = QtWidgets.QAction(
            _('Convert tabs to spaces'),
            self.editor
        )
        self._action_spaces_to_tabs = QtWidgets.QAction(
            _('Convert spaces to tabs'),
            self.editor
        )

    def on_state_changed(self, state):
        """
        Called when the mode is activated/deactivated
        """
        if state:
            self._action_spaces_to_tabs.triggered.connect(self._spaces_to_tabs)
            self.editor.add_action(
                self._action_spaces_to_tabs,
                sub_menu='Python'
            )
            self._action_tabs_to_spaces.triggered.connect(self._tabs_to_spaces)
            self.editor.add_action(
                self._action_tabs_to_spaces,
                sub_menu='Python'
            )
        else:
            self.editor.remove_action(
                self._action_spaces_to_tabs,
                sub_menu='Python'
            )
            self._action_spaces_to_tabs.triggered.disconnect(
                self._spaces_to_tabs
            )
            self.editor.remove_action(
                self._action_tabs_to_spaces,
                sub_menu='Python'
            )
            self._action_tabs_to_spaces.triggered.disconnect(
                self._tabs_to_spaces
            )

    def _spaces_to_tabs(self):

        code = self.editor.toPlainText()
        while True:
            match = re.search(
                u'((?<=\n){indent}+)|(\A{indent}+)'.format(
                    indent=u' ' * cfg.pyqode_tab_length
                ),
                code
            )
            if not match:
                break
            space_indent = u'\t' * \
                (len(match.group()) // cfg.pyqode_tab_length)
            code = code[:match.start()] + space_indent + code[match.end():]
        self.editor.setPlainText(code)
        self.editor.document().setModified(True)

    def _tabs_to_spaces(self):

        code = self.editor.toPlainText()
        while True:
            match = re.search(u'((?<=\n)\t+)|(\A\t+)', code)
            if not match:
                break
            space_indent = u' ' * len(match.group()) * cfg.pyqode_tab_length
            code = code[:match.start()] + space_indent + code[match.end():]
        self.editor.setPlainText(code)
        self.editor.document().setModified(True)
