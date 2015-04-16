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

class base_line_arrow(base_element):

	"""
	desc:
		A base class for line and arrow elements.

		See base_element for docstrings and function descriptions.
	"""

	pos_start = None
	preview = None

	def set_pos(self, x=0, y=0):

		dx = self.properties[u'x2'] - self.properties[u'x1']
		dy = self.properties[u'y2'] - self.properties[u'y1']
		self.properties[u'x1'] = x
		self.properties[u'y1'] = y
		self.properties[u'x2'] = x+dx
		self.properties[u'y2'] = y+dy

	@classmethod
	def mouse_press(cls, sketchpad, pos):

		if cls.pos_start is not None:
			return
		cls.pos_start = pos
		cls.preview = sketchpad.canvas.line(pos[0], pos[1], pos[0], pos[1],
			color=cfg.sketchpad_preview_color,
			penwidth=cfg.sketchpad_preview_penwidth)

	@classmethod
	def mouse_move(cls, sketchpad, pos):

		if cls.pos_start is None:
			return
		cls.preview.setLine(cls.pos_start[0], cls.pos_start[1], pos[0], pos[1])

	@classmethod
	def reset(cls):

		cls.pos_start = None

	@staticmethod
	def requires_color():
		return True

	@staticmethod
	def requires_penwidth():
		return True
