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
from libopensesame.exceptions import osexception
from libopensesame.base_response_item import base_response_item
from openexp._canvas.canvas import Canvas
from openexp.mouse import mouse


class mouse_response_mixin(object):

	"""
	desc:
		A mixin class that should be inherited along with base_response_item
		by all classes that want to collect mouse responses.
	"""

	_resp_codes = {
		u'none' : None,
		u'timeout' : None,
		u'left_button' : 1,
		u'middle_button' : 2,
		u'right_button' : 3,
		u'left' : 1,
		u'middle' : 2,
		u'right' : 3,
		u'scroll_up' : 4,
		u'scroll_down': 5
	}

	def button_code(self, response):

		if response is None or isinstance(response, int):
			return response
		try:
			return int(response)
		except:
			return self._resp_codes[response.lower()]

	def prepare_response_func(self):

		"""See base_response_item."""

		if self._allowed_responses is None:
			buttonlist = None
		else:
			buttonlist = [self.button_code(r) for r in self._allowed_responses]
		self._mouse = mouse(
			self.experiment,
			timeout=self._timeout,
			buttonlist=buttonlist
		)
		return self._mouse.get_click

	def process_response(self, response_args):

		"""See base_response_item."""

		response, pos, t1 = response_args
		if pos is None:
			self.experiment.var.cursor_x = u'NA'
			self.experiment.var.cursor_y = u'NA'
		else:
			self.experiment.var.cursor_x, self.experiment.var.cursor_y = pos
		if self.var.linked_sketchpad:
			if self.var.linked_sketchpad not in self.experiment.items:
				raise osexception(
					u'Item does not exist: %s'
					% self.var.linked_sketchpad
				)
			item = self.experiment.items[self.var.linked_sketchpad]
			if (
				not hasattr(item, u'canvas')
				or not isinstance(item.canvas, Canvas)
			):
				raise osexception(
					u'Item does not have a canvas: %s'
					% self.var.linked_sketchpad
				)
			self.experiment.var.cursor_roi = u';'.join(
				item.canvas.elements_at(*pos)
			)
		else:
			self.experiment.var.cursor_roi = u'undefined'
		base_response_item.process_response(self, (response, t1) )


class mouse_response(mouse_response_mixin, base_response_item):

	"""
	desc:
		An item for collecting mouse responses.
	"""

	description = u'Collects mouse responses'
	process_feedback = True

	def reset(self):

		"""See item."""

		self.var.flush = u'yes'
		self.var.show_cursor = u'yes'
		self.var.timeout = u'infinite'
		self.var.duration = u'mouseclick'
		self.var.linked_sketchpad = u''
		self.var.unset(u'allowed_responses')
		self.var.unset(u'correct_response')

	def validate_response(self, response):

		"""See base_response_item."""

		try:
			self.button_code(response)
		except:
			return False
		return True

	def response_matches(self, test, ref):

		"""See base_response_item."""

		return any(self.button_code(test) == self.button_code(r) for r in ref)

	def prepare(self):

		"""See item."""

		base_response_item.prepare(self)
		self._flush = self.var.flush == u'yes'

	def run(self):

		"""See item."""

		if self._flush:
			self._mouse.flush()
		# Show cursor if necessary
		if self.var.show_cursor == u'yes':
			self._mouse.visible = True
		base_response_item.run(self)
		self._mouse.visible = False

	def coroutine(self):

		"""See coroutines plug-in."""

		self._mouse.timeout = 0
		alive = True
		yield
		self._t0 = self.set_item_onset()
		if self._flush:
			self._mouse.flush()
		while alive:
			button, pos, time = self._mouse.get_click()
			if button is not None:
				break
			alive = yield
		self.process_response((button, pos, time))

	def var_info(self):

		"""See item."""

		return base_response_item.var_info(self) + [
			(u'cursor_x', u'[Depends on response]'),
			(u'cursor_y', u'[Depends on response]'),
			(u'cursor_roi', u'[Depends on response]')
		]
