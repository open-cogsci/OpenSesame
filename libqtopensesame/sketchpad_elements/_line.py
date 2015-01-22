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
from libqtopensesame.sketchpad_elements._base_line_arrow import base_line_arrow
from libopensesame.sketchpad_elements import line as line_runtime

class line(base_line_arrow, line_runtime):

	"""
	desc:
		A line element.

		See base_element for docstrings and function descriptions.
	"""

	@classmethod
	def mouse_release(cls, sketchpad, pos):

		if cls.pos_start is None:
			return
		dx = pos[0] - cls.pos_start[0]
		dy = pos[1] - cls.pos_start[1]
		if abs(dx) < 1 and abs(dy) < 1:
			cls.pos_start = None
			sketchpad.canvas.removeItem(cls.preview)
			return
		properties = {
				u'x1':		cls.pos_start[0],
				u'y1':		cls.pos_start[1],
				u'x2':		pos[0],
				u'y2':		pos[1],
				u'color': 	sketchpad.current_color(),
				u'penwidth'	: sketchpad.current_penwidth(),
				u'show_if'	: sketchpad.current_show_if()
			}
		e = line(sketchpad, properties=properties)
		cls.pos_start = None
		sketchpad.canvas.removeItem(cls.preview)
		return e
