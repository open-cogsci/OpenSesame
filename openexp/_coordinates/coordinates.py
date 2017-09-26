#-*- coding:utf-8 -*-

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
from openexp._canvas.canvas import Canvas
from openexp._mouse.mouse import Mouse
from libopensesame.exceptions import osexception


class Coordinates(object):

	"""
	desc:
		A base class for classes that need to perform coordinate conversions.
	"""

	def __init__(self):

		"""
		desc:
			Constructor.
		"""

		self.uniform_coordinates = \
			self.experiment.var.uniform_coordinates==u'yes'
		self._width = self.experiment.var.width
		self._height = self.experiment.var.height
		self._xcenter = self._width/2
		self._ycenter = self._height/2
		if self.uniform_coordinates:
			self._bottom = self._ycenter
			self._top = -self._ycenter
			self._left = -self._xcenter
			self._right = self._xcenter
		else:
			self._top = self._left = 0
			self._bottom = self._height
			self._right = self._width
		self._mouse_dev = isinstance(self, Mouse)
		self._canvas_dev = isinstance(self, Canvas)
		if not self._mouse_dev and not self._canvas_dev:
			raise osexception(
				u'coordinates class should be coparent with canvas or mouse class')

	def none_to_center(self, x, y):

		"""
		desc:
			Interpretes None coordinates as the display center.

		arguments:
			x:
				desc:	An X coordinate.
				type:	[int, float, NoneType]
			y:
				desc:	A Y coordinate.
				type:	[int, float, NoneType]

		returns:
			desc:	An (x, y) coordinate tuple.
			type:	tuple
		"""

		if x is None:
			if not self.uniform_coordinates:
				x = self._xcenter
			else:
				x = 0
		if y is None:
			if not self.uniform_coordinates:
				y = self._ycenter
			else:
				y = 0
		return x, y

	def to_xy(self, x, y=None):

		"""
		desc:
			Converts coordinates from the OpenSesame reference frame to the
			back-end specific reference frame. `None` values are taken as the
			display center.

		arguments:
			x:
				desc:	An x coordinate, or an (x,y) tuple.
				type:	[float, int, NoneType, tuple]

		keywords:
			y:
				desc:	A y coordinate. Only applicable if x was not a tuple.
				type:	[float, int, NoneType]

		returns:
			desc:	An (x, y) coordinate tuple in the back-end specific
					reference frame.
			type:	tuple
		"""

		raise NotImplementedError()

	def from_xy(self, x, y=None):

		"""
		desc:
			Converts coordinates from the back-end specific reference frame to
			the OpenSesame reference frame.

		arguments:
			x:
				desc:	An x coordinate, or an (x,y) tuple.
				type:	[float, int, tuple]

		keywords:
			y:
				desc:	A y coordinate. Only applicable if x was not a tuple.
				type:	[float, int, NoneType]

		returns:
			desc:	An (x, y) coordinate tuple in the OpenSesame reference
					frame.
			type:	tuple
		"""

		raise NotImplementedError()


# Non PEP-8 alias for backwards compatibility
coordinates = Coordinates
