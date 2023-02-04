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


class Gabor(BaseElement):

    """
    desc:
            A gabor-patch element for the sketchpad.
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
            (u'x',		None),
            (u'y',		None),
            (u'orient',	0),
            (u'freq',	.1),
            (u'env',	u'gaussian'),
            (u'size', 	96),
            (u'stdev',	12),
            (u'phase',	0),
            (u'color1',	u'white'),
            (u'color2', u'black'),
            (u'bgmode',	u'avg')
        ]
        super().__init__(sketchpad, string, defaults=defaults)

    def draw(self):
        """
        desc:
                Draws the element to the canvas of the sketchpad.
        """

        properties = self.eval_properties()
        return self.canvas.gabor(properties[u'x'], properties[u'y'],
                                 properties[u'orient'], properties[u'freq'],
                                 env=properties[u'env'], size=properties[u'size'],
                                 stdev=properties[u'stdev'], phase=properties[u'phase'],
                                 col1=properties[u'color1'], col2=properties[u'color2'],
                                 bgmode=properties[u'bgmode'])


# Alias for backwards compatibility
gabor = Gabor
