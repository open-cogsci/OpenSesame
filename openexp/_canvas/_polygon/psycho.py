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
from openexp._canvas._element.psycho import PsychoElement
from psychopy import visual


class Psycho(PsychoElement, Polygon):

	def prepare(self):

		self._stim = visual.ShapeStim(
			self.win,
			lineWidth=self.penwidth,
			vertices=[self.to_xy(x, y) for x, y in self.vertices],
			lineColor=self.color.backend_color,
			closeShape=True,
			fillColor=self.color.backend_color if self.fill else None,
			interpolate=False
		)
