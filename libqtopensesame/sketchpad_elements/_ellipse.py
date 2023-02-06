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
from libqtopensesame.misc.config import cfg
from libqtopensesame.sketchpad_elements._base_rect_ellipse import \
    BaseRectEllipse
from libopensesame.sketchpad_elements import Ellipse as EllipseRuntime


class Ellipse(BaseRectEllipse, EllipseRuntime):

    r"""An ellipse element.
    See base_element for docstrings and function
    descriptions.
    """
    @classmethod
    def mouse_press(cls, sketchpad, pos):

        if cls.pos_start is not None:
            return
        cls.pos_start = pos
        xc = sketchpad.canvas.xcenter()
        yc = sketchpad.canvas.ycenter()
        cls.preview = sketchpad.canvas.ellipse(pos[0]+xc, pos[1]+yc, 0, 0,
            color=cfg.sketchpad_preview_color,
            penwidth=cfg.sketchpad_preview_penwidth)


# Alias for backwards compatibility
ellipse = Ellipse
