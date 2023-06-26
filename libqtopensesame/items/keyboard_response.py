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
from libopensesame.keyboard_response import KeyboardResponse as \
    KeyboardResponseRuntime
from libqtopensesame.validators import TimeoutValidator
from libqtopensesame.items.qtplugin import QtPlugin
from openexp.keyboard import Keyboard
from qtpy import QtCore, QtWidgets
from libqtopensesame.misc.translate import translation_context
_ = translation_context('keyboard_response', category='item')


class KeyboardResponse(KeyboardResponseRuntime, QtPlugin):
    """keyboard_response item GUI"""
    
    description = _('Collects keyboard responses')
    help_url = 'manual/response/keyboard'
    lazy_init = True

    def __init__(self, name, experiment, string=None):
        KeyboardResponseRuntime.__init__(self, name, experiment, string)
        QtPlugin.__init__(self)

    def init_edit_widget(self):
        super().init_edit_widget(stretch=True)
        # Use auto-controls for most stuff
        self.add_line_edit_control(
            var='correct_response',
            label=_('Correct response'),
            info=_('Leave empty to use "correct_response"'))
        self.add_line_edit_control(
            var='allowed_responses',
            label=_('Allowed responses'),
            info=_('Separated by semicolons, e.g. "z;/"'))
        self.add_line_edit_control(
            var='timeout',
            label=_('Timeout'),
            info=_('In milliseconds or "infinite"'),
            validator=TimeoutValidator(self))
        self.add_combobox_control(
            var='event_type',
            label=_('Event type'),
            options=['keypress', 'keyrelease'])
        self.add_checkbox_control('flush', _('Flush pending key events'))
        # List available keys
        button_list_keys = QtWidgets.QPushButton(
            self.theme.qicon('help-about'),
            _('List available keys'))
        button_list_keys.setIconSize(QtCore.QSize(16, 16))
        button_list_keys.clicked.connect(self.list_keys)
        self.add_control('', button_list_keys)

    def list_keys(self):
        """Show a dialog with available key names"""
        my_keyboard = Keyboard(self.experiment)
        keylist = filter(lambda key: key.strip(), my_keyboard.valid_keys())
        md = '# ' + _('Key names') + '\n\n' \
            + _('The following key names are valid:') + '\n\n- ' \
            + '\n- '.join(['`%s`' % key for key in keylist])
        self.tabwidget.open_markdown(md, icon='os-keyboard_response',
                                     title=_('Key names'))


# Alias for backwards compatibility
keyboard_response = KeyboardResponse
