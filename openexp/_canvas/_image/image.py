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


class Image(Element):

	def __init__(self, canvas, fname, center=True, x=None, y=None, scale=None,
		rotation=None):

		x, y = canvas.none_to_center(x, y)
		Element.__init__(self, canvas, fname=fname, center=center, x=x, y=y,
			scale=scale, rotation=rotation)

	@property
	def rect(self):

		from PIL import Image

		im = Image.open(self.fname)
		w1, h1 = im.size
		if self.rotation is not None and self.rotation != 0:
			im = im.rotate(self.rotation, expand=True)
		w2, h2 = im.size
		dx = (w2-w1)/2
		dy = (h2-h1)/2
		if self.scale is not None:
			w2 *= self.scale
			h2 *= self.scale
			dx *= self.scale
			dy *= self.scale
		x, y = self.none_to_center(self.x, self.y)
		if self.center:
			return x-w2//2, y-h2//2, w2, h2
		return x-dx, y-dy, w2, h2
