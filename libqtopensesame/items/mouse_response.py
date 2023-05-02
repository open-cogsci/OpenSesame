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
from libopensesame.mouse_response import MouseResponse as MouseResponseRuntime
from libqtopensesame.items.qtplugin import QtPlugin
from libqtopensesame.validators import TimeoutValidator
from libqtopensesame.misc.translate import translation_context
from libqtopensesame._input.item_combobox import ItemComboBox
from libqtopensesame.items.feedpad import Feedpad
_ = translation_context(u'mouse_response', category=u'item')


class MouseResponse(MouseResponseRuntime, QtPlugin):

    """mouse_response item GUI"""
    description = _(u'Collects mouse responses')
    help_url = u'manual/response/mouse'
    lazy_init = True

    def __init__(self, name, experiment, string=None):
        r"""Constructor

        Parameters
        ----------
        name
            The item name.
        experiment
            The experiment object.
        string, optional
            The item definition string, or None for default initialization.
        """
        MouseResponseRuntime.__init__(self, name, experiment, string)
        QtPlugin.__init__(self)

    def init_edit_widget(self):
        r"""Initialize controls."""
        super().init_edit_widget(stretch=True)
        self.add_line_edit_control(
            var=u'correct_response',
            label=_(u'Correct response'),
            info=_(u'Leave empty to use "correct_response"')
        )
        self.add_line_edit_control(
            var=u'allowed_responses',
            label=_(u'Allowed responses'),
            info=_(u'Separated by semicolons, e.g. "left_button;right_button"')
        )
        self.add_line_edit_control(
            var=u'timeout',
            label=_(u'Timeout'),
            tooltip=_(u'In milliseconds or "infinite"'),
            validator=TimeoutValidator(self)
        )
        self._combobox_sketchpad = ItemComboBox(
            self.main_window,
            filter_fnc=lambda item: isinstance(
                self.experiment.items[item],
                Feedpad
            )
        )
        self._combobox_sketchpad.activated.connect(self.apply_edit_changes)
        self.auto_combobox[u'linked_sketchpad'] = self._combobox_sketchpad
        self.add_control(
            label=_(u'Linked sketchpad'),
            widget=self._combobox_sketchpad,
            info=_('Elements define regions of interest')
        )
        self.add_combobox_control(
            var=u'event_type',
            label=_(u'Event type'),
            options=[
                u'mouseclick',
                u'mouserelease'
            ]
        )
        self.add_checkbox_control(
            var=u'show_cursor',
            label=_(u'Visible mouse cursor')
        )
        self.add_checkbox_control(
            var=u'flush',
            label=_(u'Flush pending mouse clicks')
        )

    def edit_widget(self):
        self._combobox_sketchpad.refresh()
        QtPlugin.edit_widget(self)

    def rename(self, from_name, to_name):
        QtPlugin.rename(self, from_name, to_name)
        if self.var.linked_sketchpad == from_name:
            self.var.linked_sketchpad = to_name

    def delete(self, item_name, item_parent=None, index=None):
        if self.var.linked_sketchpad == item_name:
            self.var.linked_sketchpad = u''


# Alias for backwards compatibility
mouse_response = MouseResponse
