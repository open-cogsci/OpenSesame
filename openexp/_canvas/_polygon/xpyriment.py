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
from openexp._canvas._polygon.polygon import Polygon
from openexp._canvas._element.xpyriment import XpyrimentElement
from expyriment.stimuli import Shape
from expyriment.misc.geometry import points2vertices


class Xpyriment(XpyrimentElement, Polygon):

	def prepare(self):

		left = min(x for x, y in self.vertices)
		right = max(x for x, y in self.vertices)
		top = min(y for x, y in self.vertices)
		bottom = max(y for x, y in self.vertices)
		pos = left + (right-left)//2, top + (bottom-top)//2
		self._stim = Shape(
			line_width=0 if self.fill else self.penwidth,
			position=self.to_xy(pos),
			colour=self.color.backend_color,
			anti_aliasing=self.ANTI_ALIAS
		)
		self._stim.add_vertices(points2vertices(
			[self.to_xy(x, y) for x, y in self.vertices]
		))
		self._stim.preload()
