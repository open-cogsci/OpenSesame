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
import copy
from functools import partial
from openexp.color import color


class Element(object):

	read_only = False

	def __init__(self, canvas, **properties):

		self._canvas = canvas
		if u'visible' not in properties:
			properties[u'visible'] = True
		if u'color' in properties:
			properties[u'color'] = color(self.experiment, properties[u'color'])
		self._properties = properties
		for prop in self.property_names:
			self._create_property(prop)
		if canvas.auto_prepare and self.visible:
			self.prepare()

	def __add__(self, element):

		from openexp._canvas._element.group import Group
		return Group(self.canvas, [self, element])

	def copy(self, canvas):

		e = copy.deepcopy(self)
		e._canvas = canvas
		return e

	def prepare(self):

		pass

	def show(self):

		pass

	def _on_attribute_change(self, **kwargs):

		pass

	@property
	def experiment(self):

		return self._canvas.experiment

	@property
	def to_xy(self):

		return self._canvas.to_xy

	@property
	def none_to_center(self):

		return self._canvas.none_to_center

	@property
	def uniform_coordinates(self):

		return self._canvas.uniform_coordinates

	@property
	def property_names(self):

		return set(self._properties.keys()) \
			| set(self._canvas.configurables.keys())

	def _create_property(self, key):

		setattr(self.__class__, key, property(
			partial(self._getter, key),
			partial(self._setter, key),
			self._deller, u''))

	@staticmethod
	def _getter(key, self):

		try:
			return self._properties[key]
		except KeyError:
			return self._canvas.__cfg__[key]

	@staticmethod
	def _setter(key, self, val):

		if key == u'color':
			val = color(self.experiment, val)
		self._properties[key] = val
		self._on_attribute_change(**{key: val})

	@staticmethod
	def _deller(self, key):

		pass
