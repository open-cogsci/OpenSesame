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

from libqtopensesame.sketchpad_elements._base_element import base_element
from libopensesame.sketchpad_elements import line as line_runtime

pos_start = None

class line(base_element, line_runtime):

	@staticmethod
	def click(sketchpad, pos):

		global pos_start
		if pos_start == None:
			pos_start = pos
			return None
		properties = {
				u'x1':		pos_start[0],
				u'y1':		pos_start[1],
				u'x2':		pos[0],
				u'y2':		pos[1],
				u'color': 	sketchpad.current_color(),
				u'penwidth'	: sketchpad.current_penwidth(),
				u'show_if'	: sketchpad.current_show_if()
			}
		e = line(sketchpad, properties=properties)
		pos_start = None
		return e

	@staticmethod
	def requires_color():
		return True

	@staticmethod
	def requires_penwidth():
		return True
