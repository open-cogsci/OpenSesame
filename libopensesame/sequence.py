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
from libopensesame.exceptions import ItemDoesNotExist, \
    ConditionalExpressionError
from libopensesame.item import Item
import gc
from openexp.keyboard import Keyboard


class Sequence(Item):

    description = 'Runs a number of items in sequence'

    def reset(self):
        self.items = []
        self.var.flush_keyboard = 'yes'

    def run(self):
        self.set_item_onset()
        # Optionally flush the responses to catch escape presses
        if self._keyboard is not None:
            self._keyboard.flush()
        for _item, cond in self._items:
            self.python_workspace[u'self'] = self
            try:
                run = self.python_workspace._eval(cond)
            except Exception as e:
                raise ConditionalExpressionError(
                    'Error while evaluating run-if expression')
            if run:
                self.experiment.items.run(_item)
        if not gc.isenabled():
            gc.collect()

    def set_validator(self):
        self.validator = sequence

    def from_string(self, string):
        self.var.clear()
        self.comments = []
        self.reset()
        if string is None:
            return
        for s in string.split(u'\n'):
            self.parse_variable(s)
            cmd, arglist, kwdict = self.syntax.parse_cmd(s)
            if cmd != 'run' or not len(arglist):
                continue
            _item = arglist[0]
            if len(arglist) == 1:
                cond = 'True'
            else:
                cond = arglist[1]
            enabled = len(arglist) < 3 or arglist[2].lower() != 'disabled'
            self.items.append((_item, cond, enabled))

    def prepare(self):
        super().prepare()
        if self.var.flush_keyboard == 'yes':
            # Create a keyboard to flush responses at the start of the run
            # phase
            self._keyboard = Keyboard(self.experiment)
        else:
            self._keyboard = None
        self._items = []
        for _item, cond, enabled in self.items:
            if not enabled:
                continue
            if _item not in self.experiment.items:
                raise ItemDoesNotExist(_item)
            self.experiment.items.prepare(_item)
            self._items.append((_item, self.syntax.compile_cond(cond)))

    def to_string(self):
        s = super().to_string(self.item_type)
        for _item, cond, enabled in self.items:
            arglist = [_item, cond]
            if not enabled:
                arglist.append('disabled')
            s += '\t' + self.syntax.create_cmd('run', arglist) + '\n'
        return s


# Alias for backwards compatibility
sequence = Sequence
