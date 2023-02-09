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
from libopensesame.mouse_response import MouseResponse


class TouchResponse(MouseResponse):

    def reset(self):

        self.var._ncol = 2
        self.var._nrow = 1
        super().reset()

    def process_response(self, response_args):
        response, pos, t1 = response_args
        if pos is not None:
            x, y = pos
            if self.experiment.var.uniform_coordinates == u'yes':
                _x = x+self.experiment.var.width/2
                _y = y+self.experiment.var.height/2
            else:
                _x, _y = x, y
            col = _x // (self.experiment.var.width / self.var._ncol)
            row = _y // (self.experiment.var.height / self.var._nrow)
            response = row * self.var._ncol + col + 1
        super().process_response((response, pos, t1))
