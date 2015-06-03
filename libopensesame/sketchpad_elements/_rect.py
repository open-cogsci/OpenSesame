#-*- coding:utf-8 -*-

"""
This file is part of openexp.

openexp is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

openexp is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with openexp.  If not, see <http://www.gnu.org/licenses/>.
"""

from libopensesame.sketchpad_elements._base_element import base_element

class rect(base_element):

	"""
	desc:
		A rectangle element for the sketchpad.
	"""

	def __init__(self, sketchpad, string):

		"""
		desc:
			Constructor.

		arguments:
			sketchpad:		A sketchpad object.
			string:			A definition string.
		"""

		defaults = [
			(u'x'		, None),
			(u'y'		, None),
			(u'w'		, None),
			(u'h'		, None),
			(u'fill'	, 0),
			(u'color'	, sketchpad.get(u'foreground')),
			(u'penwidth', 1),
			]
		super(rect, self).__init__(sketchpad, string, defaults=defaults)

	def draw(self):

		"""
		desc:
			Draws the element to the canvas of the sketchpad.
		"""

		properties = self.eval_properties()
		return self.canvas.rect(properties[u'x'], properties[u'y'],
			properties[u'w'], properties[u'h'],
			fill=properties[u'fill'],
			color=properties[u'color'],
			penwidth=properties[u'penwidth'])
