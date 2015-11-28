#-*- coding:utf-8 -*-

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

from libopensesame.sketchpad_elements._base_element import base_element

class image(base_element):

	"""
	desc:
		An image element for the sketchpad.
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
			(u'file'	, None),
			(u'scale'	, 1),
			(u'center'	, 1),
			]
		super(image, self).__init__(sketchpad, string, defaults=defaults)

	def draw(self):

		"""
		desc:
			Draws the element to the canvas of the sketchpad.
		"""

		properties = self.eval_properties()
		try:
			_file = self.pool[properties[u'file']]
		except:
			_file = u''
		return self.canvas.image(_file, center=properties[u'center']==1,
			x=properties[u'x'], y=properties[u'y'], scale=properties[u'scale'])
