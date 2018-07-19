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


class Line(Element):

	CONTAINS_MAX_DIST = 10

	def __init__(self, canvas, sx, sy, ex, ey, **properties):

		properties = properties.copy()
		properties.update({'sx' : sx, 'sy' : sy, 'ex' : ex, 'ey' : ey})
		self._shapely_line = None
		Element.__init__(self, canvas, **properties)

	@property
	def rect(self):

		return self._rect(self.sx, self.sy, self.ex-self.sx, self.ey-self.sy)

	def __contains__(self, xy):

		# Shapely is used to determine whether a point is close enough to the
		# line to be counted as 'inside' it. If shapely isn't available, we fall
		# back to a simple bounding box. The shapely LineString is stored for
		# performance.
		try:
			from shapely.geometry import LineString, Point
		except ImportError:
			return Element.__contains__(self, xy)
		if self._shapely_line is None:
			self._shapely_line = LineString([
				(self.sx, self.sy),
				(self.ex, self.ey)
			])
		return Point(*xy).distance(self._shapely_line) < self.CONTAINS_MAX_DIST

	def _on_attribute_change(self, **kwargs):

		# When a change occurs the shapely line (if any) needs to be
		# redetermined in __contains__
		self._shapely_line = None
		Element._on_attribute_change(self, **kwargs)
