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

import math
from libqtopensesame.sketchpad_elements._base_element import base_element
from libopensesame.sketchpad_elements import circle as circle_runtime

pos_start = None

class circle(base_element, circle_runtime):

	@staticmethod
	def click(sketchpad, pos):

		global pos_start
		if pos_start == None:
			pos_start = pos
			return None
		r = math.sqrt((pos[0]-pos_start[0])**2 + (pos[1]-pos_start[1])**2)
		properties = {
				u'x':		pos_start[0],
				u'y':		pos_start[1],
				u'r':		r,
				u'color': 	sketchpad.current_color(),
				u'penwidth'	: sketchpad.current_penwidth(),
				u'fill'		: sketchpad.current_fill(),
				u'show_if'	: sketchpad.current_show_if()
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
