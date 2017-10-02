# coding=utf-8

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
import math
from openexp._canvas._polygon.polygon import Polygon


class Arrow(Polygon):

	def __init__(self, canvas, sx, sy, ex, ey, body_length=0.8, body_width=.5,
		head_width=30, **properties):

		Polygon.__init__(self, canvas,
			self._shape(sx, sy, ex, ey, body_length, body_width, head_width),
			**properties)

	@staticmethod
	def _shape(sx, sy, ex, ey, body_length, body_width, head_width):

		"""
		returns:
			Returns a list of (x, y) tuples that specify an arrow shape.
		"""

		# length
		d = math.sqrt((ey-sy)**2 + (sx-ex)**2)
		# direction
		angle = math.atan2(ey-sy, ex-sx)
		_head_width = (1-body_width)/2.0
		body_width = body_width/2.0
		# calculate coordinates
		p4 = (ex, ey)
		p1 = (sx +body_width * head_width * math.cos(angle - math.pi/2),
			sy + body_width * head_width * math.sin(angle - math.pi/2))
		p2 = (p1[0] + body_length*math.cos(angle) * d,
			p1[1] + body_length * math.sin(angle) * d)
		p3 = (p2[0]+_head_width * head_width * math.cos(angle-math.pi/2),
			p2[1] + _head_width * head_width * math.sin(angle-math.pi/2))
		p7 = (sx + body_width * head_width*math.cos(angle + math.pi/2),
			sy + body_width * head_width*math.sin(angle + math.pi/2))
		p6 = (p7[0] + body_length * math.cos(angle) * d,
			p7[1] + body_length * math.sin(angle) * d)
		p5 = (p6[0]+_head_width * head_width * math.cos(angle+math.pi/2),
			p6[1]+_head_width * head_width * math.sin(angle+math.pi/2))
		return [p1, p2, p3, p4, p5, p6, p7]
