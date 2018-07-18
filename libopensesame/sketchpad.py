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
from libopensesame import sketchpad_elements
from libopensesame.exceptions import osexception
from libopensesame.item import item
from libopensesame.base_response_item import base_response_item
from libopensesame.keyboard_response import keyboard_response_mixin
from libopensesame.mouse_response import mouse_response_mixin
from openexp.canvas import canvas

class sketchpad(base_response_item, keyboard_response_mixin,
	mouse_response_mixin):

	"""
	desc:
		The runtime part of the sketchpad item.
	"""

	description = u'Displays stimuli'
	is_oneshot_coroutine = True

	def reset(self):

		"""See item."""

		self.var.duration = u'keypress'
		self.elements = []

	def element_module(self):

		"""
		desc:
			Determines the module to be used for the element classes. The
			runtime and GUI use different modules.

		returns:
			desc:	A module containing sketchpad-element classes
			type:	module
		"""

		return sketchpad_elements

	def from_string(self, string):

		"""See item."""

		self.var.clear()
		self.comments = []
		self.reset()
		if string is None:
			return
		for line in string.split(u'\n'):
			if self.parse_variable(line):
				continue
			cmd, arglist, kwdict = self.syntax.parse_cmd(line)
			if cmd != u'draw':
				continue
			if len(arglist) == 0:
				raise osexception(u'Incomplete draw command: \'%s\'' % line)
			element_type = arglist[0]
			if not hasattr(self.element_module(), element_type):
				raise osexception(
					u'Unknown sketchpad element: \'%s\'' % element_type)
			element_class = getattr(self.element_module(), element_type)
			element = element_class(self, line)
			self.elements.append(element)
		self.elements.sort(
			key=lambda element:
				-element.z_index
				if isinstance(element.z_index, int)
				else 0
		)

	def process_response(self, response_args):

		"""See base_response_item."""

		if self.var.duration == u'mouseclick':
			mouse_response_mixin.process_response(self, response_args)
			return
		base_response_item.process_response(self, response_args)

	def prepare_response_func(self):

		"""See base_response_item."""

		if isinstance(self.var.duration, (int, float)):
			self._flush = lambda: None
			return self._prepare_sleep_func(self.var.duration)
		if self.var.duration == u'keypress':
			self._flush = lambda: self._keyboard.flush()
			return keyboard_response_mixin.prepare_response_func(self)
		if self.var.duration == u'mouseclick':
			self._flush = lambda: self._mouse.flush()
			return mouse_response_mixin.prepare_response_func(self)
		raise osexception(u'Invalid duration: %s' % self.var.duration)

	def _elements(self):

		"""
		desc:
			Creates a list of sketchpad elements that are shown, sorted by
			z-index.
		"""

		elements = [e for e in self.elements if e.is_shown()]
		try:
			elements.sort(key=lambda e: -int(self.syntax.eval_text(e.z_index)))
		except ValueError as e:
			raise osexception(
				u'Invalid z_index for sketchpad element',
				exception=e
			)
		return elements

	def prepare(self):

		"""See item."""

		base_response_item.prepare(self)
		self.canvas = canvas(
			self.experiment,
			color=self.var.foreground,
			background_color=self.var.background
		)
		with self.canvas:
			for element in self._elements():
				temp_name = element.draw()
				if element.element_name is not None:
					self.canvas.rename_element(
						temp_name, element.element_name
					)

	def run(self):

		"""See item."""

		self._t0 = self.set_item_onset(self.canvas.show())
		self._flush()
		base_response_item.run(self)

	def coroutine(self):

		"""See coroutines plug-in."""

		yield
		self.set_item_onset(self.canvas.show())

	def to_string(self):

		"""See item."""

		s = base_response_item.to_string(self)
		for element in self.elements:
			s += u'\t%s\n' % element.to_string()
		return s

	def var_info(self):

		"""See item."""

		if self.var.get(u'duration', _eval=False, default=u'') in \
			[u'keypress', u'mouseclick']:
			return base_response_item.var_info(self)
		return item.var_info(self)
