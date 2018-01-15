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
from openexp._canvas._element.group import Group
from openexp.canvas_elements import Line, Ellipse


class FixDot(Group):

	def __init__(self, canvas, x=None, y=None, style=u'default', **properties):

		if x is None:
			x = 0 if canvas.uniform_coordinates else canvas._width/2
		if y is None:
			y = 0 if canvas.uniform_coordinates else canvas._height/2
		h = 2
		if u'large' in style:
			s = 16
		elif u'medium' in style or style == u'default':
			s = 8
		elif u'small' in style:
			s = 4
		else:
			raise osexception(u'Unknown style: %s' % self.style)
		if u'open' in style or style == u'default':
			elements = [
				Ellipse(x-s, y-s, 2*s, 2*s, fill=True, **properties) \
					.construct(canvas),
				Ellipse(x-h, y-h, 2*h, 2*h, fill=True,
					color=canvas.background_color.colorspec,
					**{key : val for key, val in properties.items() \
					if key != u'color'}).construct(canvas)
				]
		elif u'filled' in style:
			elements = [Ellipse(
				x-s, y-s, 2*s, 2*s, fill=True, **properties)\
				.construct(canvas)]
		elif u'cross' in style:
			elements = [
				Line(x, y-s, x, y+s, **properties).construct(canvas),
				Line(x-s, y, x+s, y, **properties).construct(canvas)
				]
		else:
			raise osexception(u'Unknown style: %s' % self.style)
		properties = properties.copy()
		properties.update({ 'x' : x, 'y' : y, u'style' : style })
		Group.__init__(self, canvas, elements, **properties)
