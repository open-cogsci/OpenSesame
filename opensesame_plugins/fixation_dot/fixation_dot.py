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
from libopensesame.base_response_item import base_response_item
from libopensesame.sketchpad import sketchpad
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.canvas import canvas


class fixation_dot(sketchpad):

    r"""A simple fixation-dot plug-in."""
    description = \
        u'Presents a central fixation dot with a choice of various styles'

    def reset(self):
        """See item."""
        self.var.style = u'default'
        self.var.duration = 1000
        self.var.penwidth = 3
        self.var.x = 0
        self.var.y = 0

    def prepare(self):
        """See item."""
        base_response_item.prepare(self)
        # Create a canvas.
        self.canvas = canvas(self.experiment,
                             background_color=self.var.background, color=self.var.foreground,
                             penwidth=self.var.penwidth)
        # Set the coordinates.
        self._x = self.var.x
        self._y = self.var.y
        if self.var.uniform_coordinates != u'yes':
            self._x += self.canvas.width/2
            self._y += self.canvas.height/2
        # For backwards compatibility, we support a few special fixdot styles
        if self.var.style == u'filled':
            self.canvas.ellipse(self._x - 10, self._y - 10, 20, 20, fill=True)
        elif self.var.style == u'filled-small':
            self.canvas.ellipse(self._x - 5, self._y - 5, 10, 10, fill=True)
        elif self.var.style == u'empty':
            self.canvas.ellipse(self._x - 10, self._y - 10, 20, 20, fill=False)
        elif self.var.style == u'empty-small':
            self.canvas.ellipse(self._x - 5, self._y - 5, 10, 10, fill=False)
        elif self.var.style == u'cross':
            self.canvas.line(self._x - 10, self._y, self._x + 10, self._y)
            self.canvas.line(self._x, self._y - 10, self._x, self._y + 10)
        elif self.var.style == u'cross-small':
            self.canvas.line(self._x - 5, self._y, self._x + 5, self._y)
            self.canvas.line(self._x, self._y - 5, self._x, self._y + 5)
        # But the new way is to use the style keyword
        else:
            self.canvas.fixdot(self._x, self._y, style=self.var.style)

    # We don't use the fancy sketchpad from and to string functions.

    def from_string(self, string):
        base_response_item.from_string(self, string)

    def to_string(self):
        return base_response_item.to_string(self)


class qtfixation_dot(fixation_dot, qtautoplugin):

    def __init__(self, name, experiment, script=None):

        fixation_dot.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)
