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


class Polygon(Element):

	def __init__(self, canvas, vertices, **properties):

		properties = properties.copy()
		properties.update({ 'vertices' : vertices })
		self._shapely_polygon = None
		Element.__init__(self, canvas, **properties)

	@property
	def rect(self):

		left = min(x for x,y in self.vertices)
		right = max(x for x,y in self.vertices)
		top = min(y for x,y in self.vertices)
		bottom = max(y for x,y in self.vertices)
		return left, top, right-left, bottom-top

	def __contains__(self, xy):

		# Shapely is used to determine whether a point falls exactly within the
		# polygon. If shapely isn't available, we fall back to a simple bounding
		# box. The shapely polygon is stored for performance.
		try:
			from shapely.geometry import Polygon as ShapelyPolygon, Point
		except ImportError:
			return Element.__contains__(self, xy)
		if self._shapely_polygon is None:
			self._shapely_polygon = ShapelyPolygon(self.vertices)
		return self._shapely_polygon.contains(Point(*xy))

	def _on_attribute_change(self, **kwargs):

		# When a change occurs the shapely polygon (if any) needs to be
		# redetermined in __contains__
		self._shapely_polygon = None
		Element._on_attribute_change(self, **kwargs)
