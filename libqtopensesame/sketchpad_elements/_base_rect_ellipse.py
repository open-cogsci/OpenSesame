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
from libqtopensesame.misc.config import cfg
from libqtopensesame.sketchpad_elements._base_element import base_element

class base_rect_ellipse(base_element):

	pos_start = None
	preview = None

	@classmethod
	def mouse_release(cls, sketchpad, pos):

		if cls.pos_start is None:
			return
		w = pos[0]-cls.pos_start[0]
		h = pos[1]-cls.pos_start[1]
		# Don't draw line-like shapes
		if abs(w) < 1 or abs(h) < 1:
			cls.pos_start = None
			sketchpad.canvas.removeItem(cls.preview)
			return
		properties = {
				u'x':		cls.pos_start[0],
				u'y':		cls.pos_start[1],
				u'w':		w,
				u'h':		h,
				u'color': 	sketchpad.current_color(),
				u'penwidth'	: sketchpad.current_penwidth(),
				u'fill'		: sketchpad.current_fill(),
				u'show_if'	: sketchpad.current_show_if()
			}
		e = cls(sketchpad, properties=properties)
		cls.pos_start = None
		sketchpad.canvas.removeItem(cls.preview)
		return e

	@classmethod
	def mouse_move(cls, sketchpad, pos):

		if cls.pos_start is None or cls.preview is None:
			return
		x = cls.pos_start[0]
		y = cls.pos_start[1]
		w = pos[0]-cls.pos_start[0]
		h = pos[1]-cls.pos_start[1]
		if w < 0:
			x += w
			w *= -1
		if h < 0:
			y += h
			h *= -1
		cls.preview.setRect(x, y, w, h)

	@classmethod
	def reset(cls):

		cls.pos_start = None

	@staticmethod
	def requires_color():
		return True

	@staticmethod
	def requires_penwidth():
		return True

	@staticmethod
	def requires_fill():
		return True
