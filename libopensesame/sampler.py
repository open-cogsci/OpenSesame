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
from openexp.sampler import sampler as openexp_sampler
from libopensesame.item import item
from libopensesame.base_response_item import base_response_item
from libopensesame.keyboard_response import keyboard_response_mixin
from libopensesame.mouse_response import mouse_response_mixin


class sampler(base_response_item, keyboard_response_mixin,
	mouse_response_mixin):

	"""
	desc:
		An item for sound-file playback.
	"""

	description = u'Plays a sound file in .wav or .ogg format'
	is_oneshot_coroutine = True

	def reset(self):

		"""See item."""

		self.var.sample = u''
		self.var.pan = 0
		self.var.pitch = 1
		self.var.fade_in = 0
		self.var.stop_after = 0
		self.var.volume = 1.0
		self.var.duration = u'sound'

	def process_response(self, response_args):

		"""See base_response_item."""

		if self.var.duration == u'mouseclick':
			mouse_response_mixin.process_response(self, response_args)
			return
		base_response_item.process_response(self, response_args)

	def prepare_response_func(self):

		"""See base_response_item."""

		if isinstance(self.var.duration, (int, float)):
			return self._prepare_sleep_func(self.var.duration)
		if self.var.duration == u'keypress':
			return keyboard_response_mixin.prepare_response_func(self)
		if self.var.duration == u'mouseclick':
			return mouse_response_mixin.prepare_response_func(self)
		if self.var.duration == u'sound':
			return lambda: None
		raise osexception(u'Invalid duration: %s' % self.var.duration)

	def prepare(self):

		"""See item."""

		base_response_item.prepare(self)
		if safe_decode(self.var.sample).strip() == u'':
			raise osexception(
				u'No sample has been specified in sampler "%s"' % self.name)
		sample = self.experiment.pool[self.var.sample]
		try:
			self.sampler = openexp_sampler(self.experiment, sample)
		except Exception as e:
			raise osexception(u'Failed to load sample: %s' % sample,
				exception=e)
		pan = self.var.pan
		if pan == -20:
			pan = u'left'
		elif pan == 20:
			pan = u'right'
		self.sampler.pan = pan
		self.sampler.volume = self.var.volume
		self.sampler.pitch = self.var.pitch
		self.sampler.fade_in = self.var.fade_in
		self.sampler.duration = self.var.stop_after
		self.sampler.block = self.var.duration == u'sound'

	def run(self):

		"""See item."""

		self._t0 = self.set_item_onset()
		self.sampler.play()
		base_response_item.run(self)

	def coroutine(self):

		"""See coroutines plug-in."""

		self.sampler.block = False
		yield
		self.set_item_onset()
		self.sampler.play()

	def var_info(self):

		"""See item."""

		if self.var.get(u'duration', _eval=False, default=u'') in \
			[u'keypress', u'mouseclick']:
			return base_response_item.var_info(self)
		return item.var_info(self)
