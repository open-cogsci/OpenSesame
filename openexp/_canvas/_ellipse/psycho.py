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
from openexp._canvas._ellipse.ellipse import Ellipse
from openexp._canvas._element.psycho import PsychoElement
from psychopy import visual
from PIL import Image, ImageDraw
import numpy as np


class Psycho(PsychoElement, Ellipse):

	def prepare(self):

		p = int(self.penwidth)
		w = int(self.w)
		h = int(self.h)
		x = int(self.x)
		y = int(self.y)
		if self.fill:
			# A filled ellipse ignores the penwidth and fills up exactly the
			# specified size
			im = Image.new('L', (w, h), 0)
			dr = ImageDraw.Draw(im)
			dr.ellipse((0, 0, w-1, h-1), fill=1)
		elif p == 1:
			# An unfilled ellipses with a pendwidth of 1 also fills up exactly
			# the specified size
			im = Image.new('L', (w, h), 0)
			dr = ImageDraw.Draw(im)
			dr.ellipse((0,0,w-1,h-1), outline=1)
		else:
			# An unfilled ellipse with a positive larger than 1 fills up
			# slightly more than the specified size, because half the penwidth
			# extends beyond the size on each side.
			im = Image.new('L', (w+p, h+p), 0)
			dr = ImageDraw.Draw(im)
			dr.ellipse((0,0,w+p-1, h+p-1), fill=1)
			dr.ellipse((p, p, w-1, h-1), fill=0)
		# Transform the image into a mask, and remap the colors to PsychoPy
		# format (-1 = transparent, 1 = opaque)
		mask = np.array(im, dtype=int)
		mask[mask == 0] = -1
		self._stim = visual.GratingStim(win=self.win, mask=mask,
			pos=self.to_xy(x+w/2, y+h/2), size=im.size,
			color=self.color.backend_color, tex=None)
