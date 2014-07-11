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

from libopensesame import debug, sketchpad_elements
from libopensesame.exceptions import osexception
from libopensesame.item import item
from libopensesame.generic_response import generic_response
from openexp.canvas import canvas

class sketchpad(item, generic_response):

	"""
	desc:
		The runtime part of the sketchpad item.
	"""

	description = u'Displays stimuli'

	def __init__(self, name, experiment, string=None):

		"""
		desc:
			Constructor.

		arguments:
			name:			The name of the item.
			experiment:		The experiment object.

		keywords:
			string:			The item definition string or None to initialize
							from scratch.
		"""

		self.duration = u'keypress'
		self.elements = []
		super(sketchpad, self).__init__(name, experiment, string=string)

	def from_string(self, string):

		"""
		desc:
			Parses a definition string.

		arguments:
			string:		A definition string.
		"""

		for line in string.split(u'\n'):
			if not self.parse_variable(line):
				l = self.split(line)
				if len(l) > 0:
					if l[0] == u'draw':
						if len(l) == 1:
							raise osexception(
								u'Incomplete draw command: \'%s\'' % line)
						element_type = l[1]
						if not hasattr(sketchpad_elements, element_type):
							raise osexception(
								u'Unknown sketchpad element: \'%s\'' \
								% element_type)
						element_class = getattr(sketchpad_elements,
							element_type)
						element = element_class(self, line)
						self.elements.append(element)
		self.elements.sort(key=lambda element: -element.z_index)
		print self.to_string()

	def prepare(self):

		"""
		desc:
			Prepares the canvas.
		"""

		super(sketchpad, self).prepare()
		generic_response.prepare(self)
		self.canvas = canvas(self.experiment,
			fgcolor=self.get(u'foreground'),
			bgcolor=self.get(u'background'), auto_prepare=False)
		for element in self.elements:
			element.draw()
		self.canvas.prepare()

	def run(self):

		"""
		desc:
			Shows the canvas and implements the duration.
		"""

		self.set_item_onset(self.canvas.show())
		self.set_sri(False)
		self.process_response()

	def to_string(self):

		"""
		desc:
			Generates a string representation for the sketchpad.

		returns:
			A string representation.
		"""

		s = super(sketchpad, self).to_string()
		for element in self.elements:
			s += u'\t%s\n' % element.to_string()
		return s

	def var_info(self):

		"""
		desc:
			Returns a list of dictionaries with variable descriptions.

		returns:
			A list of (name, description) tuples.
		"""

		l = item.item.var_info(self)
		if self.get(u'duration', _eval=False) in [u'keypress', u'mouseclick']:
			l += generic_response.var_info(self)
		return l
