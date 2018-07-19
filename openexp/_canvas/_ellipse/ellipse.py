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
from openexp._canvas._element.element import Element


class Ellipse(Element):

	def __init__(self, canvas, x, y, w, h, **properties):

		properties = properties.copy()
		x, y, w, h = self._rect(x, y, w, h)
		properties.update({ 'x' : x, 'y' : y, 'w' : w, 'h' : h })
		Element.__init__(self, canvas, **properties)

	@property
	def rect(self):

		return self.x, self.y, self.w, self.h

	def __contains__(self, xy):

		# Source: https://math.stackexchange.com/questions/76457/
		# check-if-a-point-is-within-an-ellipse
		rx = self.w / 2
		ry = self.h / 2
		h = self.x + rx
		k = self.y + ry
		x, y = xy
		d = (x - h)**2 / rx**2 + (y - k)**2 / ry**2
		return d <= 1
