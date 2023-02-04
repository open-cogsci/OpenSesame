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

import math
from libopensesame.py3compat import *
from libqtopensesame.misc.config import cfg
from libqtopensesame.sketchpad_elements._base_element import base_element
from libopensesame.sketchpad_elements import circle as circle_runtime


class circle(base_element, circle_runtime):

    pos_start = None
    preview = None

    @classmethod
    def mouse_press(cls, sketchpad, pos):

        if cls.pos_start is not None:
            return
        cls.pos_start = pos
        xc = sketchpad.canvas.xcenter()
        yc = sketchpad.canvas.ycenter()
        cls.preview = sketchpad.canvas.circle(pos[0], pos[1], 0,
                                              color=cfg.sketchpad_preview_color,
                                              penwidth=cfg.sketchpad_preview_penwidth)

    @classmethod
    def mouse_release(cls, sketchpad, pos):

        if cls.pos_start is None:
            cls.pos_start = pos
            return None
        if cls.radius(pos) < 1:
            cls.pos_start = None
            sketchpad.canvas.removeItem(cls.preview)
            return
        properties = {
            u'x':		cls.pos_start[0],
            u'y':		cls.pos_start[1],
            u'r':		cls.radius(pos),
            u'color': 	sketchpad.current_color(),
            u'penwidth': sketchpad.current_penwidth(),
            u'fill': sketchpad.current_fill(),
            u'show_if': sketchpad.current_show_if()
        }
        e = circle(sketchpad, properties=properties)
        cls.pos_start = None
        sketchpad.canvas.removeItem(cls.preview)
        return e

    @classmethod
    def mouse_move(cls, sketchpad, pos):

        if cls.pos_start is None or cls.preview is None:
            return
        xc = sketchpad.canvas.xcenter()
        yc = sketchpad.canvas.ycenter()
        r = cls.radius(pos)
        x = cls.pos_start[0]-r
        y = cls.pos_start[1]-r
        cls.preview.setRect(x, y, 2*r, 2*r)

    @classmethod
    def radius(cls, pos):

        return math.sqrt((pos[0]-cls.pos_start[0])**2 +
                         (pos[1]-cls.pos_start[1])**2)

    @classmethod
    def reset(cls):

        cls.pos_start = None

    @staticmethod
    def click(sketchpad, pos):

        global pos_start
        if pos_start is None:
            pos_start = pos
            return None
        r = cls.radius(pos)
        properties = {
            u'x':		pos_start[0],
            u'y':		pos_start[1],
            u'r':		r,
            u'color': 	sketchpad.current_color(),
            u'penwidth': sketchpad.current_penwidth(),
            u'fill': sketchpad.current_fill(),
            u'show_if': sketchpad.current_show_if()
        }
        e = circle(sketchpad, properties=properties)
        pos_start = None
        return e

    @staticmethod
    def requires_color():
        return True

    @staticmethod
    def requires_penwidth():
        return True

    @staticmethod
    def requires_fill():
        return True
