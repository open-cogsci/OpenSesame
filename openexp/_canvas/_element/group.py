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


class Group(Element):

	def __init__(self, canvas, elements=[], **properties):

		if not all(isinstance(e, Element) for e in elements):
			raise TypeError('A group can only contain canvas elements')
		self._elements = elements
		Element.__init__(self, canvas, **properties)

	def prepare(self):

		for element in self._elements:
			element.prepare()

	def show(self):

		for element in self._elements:
			element.show()

	def __len__(self):

		return len(self._elements)

	def __add__(self, element):

		return Group(self.canvas, self._elements + [element])

	@staticmethod
	def _setter(key, self, val):

		raise TypeError(u'Properties of element groups cannot be changed')
