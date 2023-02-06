# -*- coding:utf-8 -*-

"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame. If not, see <http://www.gnu.org/licenses/>.
"""
from libopensesame.py3compat import *
from libopensesame import plugins
from libopensesame.base_response_item import base_response_item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.keyboard import keyboard


class joystick(base_response_item):

    r"""A plug-in for using a joystick/gamepad."""
    description = u'Collects input from a joystick or gamepad'
    process_feedback = True

    def reset(self):
        """See item."""
        self.var.timeout = u'infinite'
        self.var.allowed_responses = u''
        self.var._dummy = u'no'
        self.var._device = 0

    def validate_response(self, response):
        """See base_response_item."""
        try:
            response = int(response)
        except ValueError:
            return False
        return response >= 0 or response <= 255

    def _get_button_press(self):
        r"""Calls libjoystick.get_button_press() with the correct arguments."""
        return self.experiment.joystick.get_joybutton(
            joybuttonlist=self._allowed_responses,
            timeout=self._timeout
        )

    def prepare_response_func(self):
        """See base_response_item."""
        self._keyboard = keyboard(
            self.experiment,
            keylist=(
                self._allowed_responses if self._allowed_responses
                else list(range(0, 10))  # Only numeric keys
            ),
            timeout=self._timeout
        )
        if self.var._dummy == u'yes':
            return self._keyboard.get_key
        # Dynamically load a joystick instance
        if not hasattr(self.experiment, u'joystick'):
            _joystick = plugins.load_mod(__file__, u'libjoystick')
            self.experiment.joystick = _joystick.libjoystick(
                self.experiment,
                device=self._device
            )
            self.python_workspace[u'joystick'] = self.experiment.joystick
        if self._allowed_responses is not None:
            self._allowed_responses = [int(r) for r in self._allowed_responses]
        return self._get_button_press

    def response_matches(self, test, ref):
        """See base_response_item."""
        return safe_decode(test) in ref

    def coroutine(self):
        """See coroutines plug-in."""
        if self.var._dummy == u'yes':
            self._keyboard.timeout = 0
        else:
            self._timeout = 0
        alive = True
        yield
        self._t0 = self.set_item_onset()
        while alive:
            button, time = self._collect_response()
            if button is not None:
                break
            alive = yield
        self.process_response((button, time))


class qtjoystick(joystick, qtautoplugin):

    def __init__(self, name, experiment, script=None):

        # Call parent constructors.
        joystick.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)
