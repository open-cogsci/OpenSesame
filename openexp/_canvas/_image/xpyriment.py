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
from libopensesame.exceptions import osexception
from openexp._canvas._image.image import Image
from openexp._canvas._element.xpyriment import XpyrimentElement
from expyriment.stimuli import Picture


class Xpyriment(XpyrimentElement, Image):

	def prepare(self):

		self._stim = Picture(filename=safe_decode(self.fname))
		if self.rotation is not None and self.rotation != 0:
			w1, h1 = self._stim.surface_size
			self._stim.rotate(-self.rotation)
			w2, h2 = self._stim.surface_size
			dx = (w2-w1)/2
			dy = (h2-h1)/2
		else:
			dx = dy = 0
		if self.scale is not None:
			self._stim.scale((self.scale, self.scale))
			dx *= self.scale
			dy *= self.scale
		x, y = self.to_xy(self.x, self.y)
		if not self.center:
			w, h = self._stim.surface_size
			x += w//2-dx
			y -= h//2-dy
		self._stim.reposition((x, y))
