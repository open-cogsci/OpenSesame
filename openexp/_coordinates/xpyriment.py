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
from libopensesame.exceptions import osexception
from openexp._coordinates.coordinates import Coordinates


class Xpyriment(Coordinates):

	"""
	desc:
		For function specifications and docstrings, see
		`openexp._coordinates.coordinates`.
	"""

	def __init__(self):

		Coordinates.__init__(self)
		self._xwcenter = self.experiment.expyriment.screen.window_size[0]/2
		self._ywcenter = self.experiment.expyriment.screen.window_size[1]/2

	def to_xy(self, x, y=None):

		if isinstance(x, tuple):
			x, y = x
		x, y = self.none_to_center(x, y)
		if self._canvas_dev:
			# For expyriment, 0,0 is the display center and positive y
			# coordinates are up.
			if self.uniform_coordinates:
				return x, -y
			return x - self._xcenter, self._ycenter - y
		if self._mouse_dev:
			# The mouse is centered on the top-left, but we need to take into
			# account that the display is padded in fullscreen mode.
			if self.uniform_coordinates:
				return x + self._xwcenter, y + self._ywcenter
			return x + self._xwcenter - self._xcenter, \
				y + self._ywcenter - self._ycenter

	def from_xy(self, x, y=None):

		if isinstance(x, tuple):
			x, y = x
		if not self._mouse_dev:
			raise osexception(u'Only mouse supported')
		if self.uniform_coordinates:
			return x - self._xwcenter, y - self._ywcenter
		return x - self._xwcenter + self._xcenter, \
			y - self._ywcenter + self._ycenter


# Non PEP-8 alias for backwards compatibility
xpyriment = Xpyriment
