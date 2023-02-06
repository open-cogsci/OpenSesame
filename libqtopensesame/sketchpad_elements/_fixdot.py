# -*- coding:utf-8 -*-

"""
This file is part of openexp.

openexp is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

openexp is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with openexp.  If not, see <http://www.gnu.org/licenses/>.
"""
from libopensesame.py3compat import *
from libqtopensesame.sketchpad_elements._base_element import BaseElement
from libopensesame.sketchpad_elements import Fixdot as FixdotRuntime


class Fixdot(BaseElement, FixdotRuntime):

    r"""A fixdot element.
    See base_element for docstrings and function
    descriptions.
    """
    @classmethod
    def mouse_press(cls, sketchpad, pos):

        properties = {
            u'x':		pos[0],
            u'y':		pos[1],
            u'color': 	sketchpad.current_color(),
            u'show_if': sketchpad.current_show_if()
        }
        e = Fixdot(sketchpad, properties=properties)
        return e

    @staticmethod
    def requires_color():
        return True


# Alias for backwards compatibility
fixdot = Fixdot
