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
from libopensesame.sketchpad_elements._base_element import BaseElement


class Fixdot(BaseElement):

    r"""A fixation-dot element for the sketchpad."""
    def __init__(self, sketchpad, string):
        r"""Constructor.

        Parameters
        ----------
        sketchpad
            A sketchpad object.
        string
            A definition string.
        """
        defaults = [
            (u'x', None),
            (u'y', None),
            (u'color', sketchpad.var.get(u'foreground')),
            (u'style', u'default'),
        ]
        super().__init__(sketchpad, string, defaults=defaults)

    def draw(self):
        r"""Draws the element to the canvas of the sketchpad."""
        properties = self.eval_properties()
        return self.canvas.fixdot(properties[u'x'], properties[u'y'],
                                  style=properties[u'style'],
                                  color=properties[u'color'])

# Alias for backwards compatibility
fixdot = Fixdot
