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
from openexp import backend


class ElementFactory(object):

	def __init__(self, *args, **kwargs):

		self._args = args
		self._kwargs = kwargs

	def construct(self, canvas):

		bck = backend.backend_guess(canvas.experiment, u'canvas')
		mod = __import__('openexp._canvas._%s.%s' % (self.mod, bck),
			fromlist=['dummy'])
		cls = getattr(mod, bck.capitalize())
		return cls(canvas, *self._args, **self._kwargs)


class Line(ElementFactory): mod = 'line'
class Rect(ElementFactory): mod = 'rect'
class Ellipse(ElementFactory): mod = 'ellipse'
class Circle(ElementFactory): mod = 'circle'
class FixDot(ElementFactory): mod = 'fixdot'
class Polygon(ElementFactory): mod = 'polygon'
class Image(ElementFactory): mod = 'image'
class Gabor(ElementFactory): mod = 'gabor'
class NoisePatch(ElementFactory): mod = 'noise_patch'
class RichText(ElementFactory): mod = 'richtext'
class Arrow(ElementFactory): mod = 'arrow'
Text = RichText
