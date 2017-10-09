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

		Element.__init__(self, canvas, fname=fname, center=center, x=x, y=y,
			scale=scale, rotation=rotation)

	@property
	def rect(self):

		from PIL import Image

		im = Image.open(fname)
		w, h = im.size
		if self.center:
			return self.x-w//2, self.y-h//2, w, h
		return self.x, self.y, w, h
