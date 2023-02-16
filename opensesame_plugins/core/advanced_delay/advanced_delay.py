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
from libopensesame.exceptions import osexception
from libopensesame.item import Item
import random


class AdvancedDelay(Item):

    def reset(self):
        self.var.duration = 1000
        self.var.jitter = 0
        self.var.jitter_mode = u'Uniform'

    def prepare(self):
        super().prepare()
        if not isinstance(self.var.duration, (int, float)) \
                or self.var.duration < 0:
            raise osexception('Duration should be a positive numeric value')
        if self.var.jitter_mode == u'Uniform':
            self._duration = random.uniform(
                self.var.duration-self.var.jitter / 2,
                self.var.duration+self.var.jitter / 2)
        elif self.var.jitter_mode == u'Std. Dev.':
            self._duration = random.gauss(self.var.duration, self.var.jitter)
        else:
            raise osexception(f'Unknown jitter mode: {self.var.jitter_mode}')
        if self._duration < 0:
            self._duration = 0
        self._duration = int(self._duration)
        self.experiment.var.set(f'delay_{self.name}', self._duration)

    def run(self):
        self.set_item_onset(self.clock.time())
        self.clock.sleep(self._duration)

    def var_info(self):
        return super().var_info() + \
            [(f'delay_{self.name}', '[Determined at runtime]')]
