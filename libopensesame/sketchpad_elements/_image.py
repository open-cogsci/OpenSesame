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


class Image(BaseElement):

    """
    desc:
            An image element for the sketchpad.
    """

    def __init__(self, sketchpad, string):
        """
        desc:
                Constructor.

        arguments:
                sketchpad:		A sketchpad object.
                string:			A definition string.
        """

        defaults = [
            (u'x', None),
            (u'y', None),
            (u'file', None),
            (u'scale', 1),
            (u'rotation', 0),
            (u'center', 1),
        ]
        super().__init__(sketchpad, string, defaults=defaults)

    def draw(self):
        """
        desc:
                Draws the element to the canvas of the sketchpad.
        """

        properties = self.eval_properties()
        try:
            _file = self.pool[properties[u'file']]
        except:
            _file = u''
        return self.canvas.image(_file,
                                 center=properties[u'center'] == 1,
                                 x=properties[u'x'],
                                 y=properties[u'y'],
                                 scale=properties[u'scale'],
                                 rotation=properties[u'rotation']
                                 )

    def to_string(self):
        """See base_element."""

        # For backwards compatibility we don't include the rotation keyword if
        # it is left on 0 (i.e. no rotation). This is necessary for sketchpads
        # to be parse-able in 3.1.X.
        return self.syntax.create_cmd(u'draw', [self._type],
            {
                var: val for var, val in self.properties.items()
                if var not in (u'name', u'rotation') or val
            }
        )


# Alias for backwards compatibility
image = Image
