#-*- coding:utf-8 -*-

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
from libqtopensesame.sketchpad_elements._arrow import arrow
from libqtopensesame.sketchpad_elements._circle import circle
from libqtopensesame.sketchpad_elements._ellipse import ellipse
from libqtopensesame.sketchpad_elements._fixdot import fixdot
from libqtopensesame.sketchpad_elements._gabor import gabor
from libqtopensesame.sketchpad_elements._image import image
from libqtopensesame.sketchpad_elements._line import line
from libqtopensesame.sketchpad_elements._noise import noise
from libqtopensesame.sketchpad_elements._textline import textline
from libqtopensesame.sketchpad_elements._rect import rect
elements = [textline, image, fixdot, line, arrow, rect, circle, ellipse, gabor,
	noise]
