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

class arrow(base_element):

	"""
	desc:
		An arrow element for the sketchpad.
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
			(u'x1'				, None),
			(u'y1'				, None),
			(u'x2'				, None),
			(u'y2'				, None),
			(u'proportion'		, 0.8),
			(u'arrow_width'		, 30),
			(u'arrowhead_width'	, 0.5),
			(u'color'			, sketchpad.get(u'foreground')),
			(u'penwidth'		, 1),
			(u'fill'			, True),
			]
		super(arrow, self).__init__(sketchpad, string, defaults=defaults)

	def draw(self):

		"""
		desc:
			Draws the element to the canvas of the sketchpad.
		"""

		properties = self.eval_properties()
		return self.canvas.arrow(properties[u'x1'], properties[u'y1'],
			properties[u'x2'], properties[u'y2'],
			color=properties[u'color'],
			penwidth=properties[u'penwidth'],
			arrowhead_width=properties[u'arrowhead_width'],
			proportion=properties[u'proportion'],
			arrow_width=properties[u'arrow_width'],
			fill=properties[u'fill'])

