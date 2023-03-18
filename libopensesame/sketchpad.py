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
from libopensesame import sketchpad_elements
from libopensesame.item import Item
from libopensesame.exceptions import InvalidSketchpadElementScript, \
    InvalidValue
from libopensesame.base_response_item import BaseResponseItem
from libopensesame.keyboard_response import KeyboardResponseMixin
from libopensesame.mouse_response import MouseResponseMixin
from openexp.canvas import Canvas


class Sketchpad(BaseResponseItem, KeyboardResponseMixin, MouseResponseMixin):

    description = 'Displays stimuli'
    is_oneshot_coroutine = True

    def reset(self):
        self.var.duration = 'keypress'
        self.elements = []

    def element_module(self):
        r"""Determines the module to be used for the element classes. The
        runtime and GUI use different modules.

        Returns
        -------
        module
            A module containing sketchpad-element classes
        """
        return sketchpad_elements

    def from_string(self, string):
        self.var.clear()
        self.comments = []
        self.reset()
        if string is None:
            return
        for line in string.split('\n'):
            if self.parse_variable(line):
                continue
            cmd, arglist, kwdict = self.syntax.parse_cmd(line)
            if cmd != 'draw':
                continue
            if len(arglist) == 0:
                raise InvalidSketchpadElementScript(
                    f'Incomplete draw command: {line}')
            element_type = arglist[0]
            if not hasattr(self.element_module(), element_type):
                raise InvalidSketchpadElementScript(
                    f'Unknown sketchpad element: {element_type}')
            element_class = getattr(self.element_module(), element_type)
            element = element_class(self, line)
            self.elements.append(element)
        self.elements.sort(
            key=lambda element:
            -element.z_index
            if isinstance(element.z_index, int)
            else 0
        )

    def process_response(self, response_args):
        """See base_response_item."""
        if self.var.duration == 'mouseclick':
            MouseResponseMixin.process_response(self, response_args)
            return
        super().process_response(response_args)

    def prepare_response_func(self):
        """See base_response_item."""
        if isinstance(self.var.duration, (int, float)):
            self._flush = lambda: None
            return self._prepare_sleep_func(self.var.duration)
        if self.var.duration == 'keypress':
            self._flush = lambda: self._keyboard.flush()
            return KeyboardResponseMixin.prepare_response_func(self)
        if self.var.duration == 'mouseclick':
            self._flush = lambda: self._mouse.flush()
            return MouseResponseMixin.prepare_response_func(self)
        raise InvalidValue(f'Invalid duration: {self.var.duration}')

    def _elements(self):
        r"""Creates a list of sketchpad elements that are shown, sorted by
        z-index.
        """
        elements = [e for e in self.elements if e.is_shown()]
        try:
            elements.sort(key=lambda e: -int(self.syntax.eval_text(e.z_index)))
        except ValueError as e:
            raise InvalidValuei('Invalid z_index for sketchpad element')
        return elements

    def prepare(self):
        super().prepare()
        self.canvas = Canvas(self.experiment, color=self.var.foreground,
                             background_color=self.var.background)
        with self.canvas:
            for element in self._elements():
                temp_name = element.draw()
                if element.element_name is not None:
                    self.canvas.rename_element(temp_name, element.element_name)

    def run(self):
        self._t0 = self.set_item_onset(self.canvas.show())
        self._flush()
        super().run()

    def coroutine(self):
        yield
        self.set_item_onset(self.canvas.show())

    def to_string(self):
        s = super().to_string()
        for element in self.elements:
            s += '\t%s\n' % element.to_string()
        return s

    def var_info(self):
        if self.var.get('duration', _eval=False, default='') in \
                ['keypress', 'mouseclick']:
            return super().var_info()
        return Item.var_info(self)


# Alias for backwards compatibility
sketchpad = Sketchpad
