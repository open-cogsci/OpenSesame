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

from libopensesame.exceptions import osexception
from libopensesame import item, generic_response, debug
import openexp.sampler

class sampler(item.item, generic_response.generic_response):

	"""Sound playback item"""

	description = u'Plays a sound file in .wav or .ogg format'

	def __init__(self, name, experiment, string = None):

		"""
		Constructor.

		Arguments:
		name 		--	The name of the item.
		experiment 	--	The experiment.

		Keyword arguments:
		string		-- 	The item definition string. (default=None)
		"""

		self.sample = u''
		self.pan = 0
		self.pitch = 1
		self.fade_in = 0
		self.volume = 1.0
		self.stop_after = 0
		self.duration = u'sound'
		self.block = False
		item.item.__init__(self, name, experiment, string)

	def prepare_duration_sound(self):

		"""Sets the duration function for 'sound' duration."""

		self.block = True
		self._duration_func = self.dummy

	def prepare(self):

		"""Prepares for playback."""

		item.item.prepare(self)
		if self.sample.strip() == u'':
			raise osexception( \
				u'No sample has been specified in sampler "%s"' % self.name)
		sample = self.experiment.get_file(self.eval_text(self.sample))
		if debug.enabled:
			self.sampler = openexp.sampler.sampler(self.experiment, sample)
		else:
			try:
				self.sampler = openexp.sampler.sampler(self.experiment, sample)
			except Exception as e:
				raise osexception( \
					u'Failed to load sample in sampler "%s": %s' % (self.name, \
					e))

		pan = self.get(u'pan')
		if pan == -20:
			pan = u'left'
		elif pan == 20:
			pan = u'right'

		self.sampler.pan(pan)
		self.sampler.volume(self.get(u'volume'))
		self.sampler.pitch(self.get(u'pitch'))
		self.sampler.fade_in(self.get(u'fade_in'))
		self.sampler.stop_after(self.get(u'stop_after'))
		generic_response.generic_response.prepare(self)

	def run(self):

		"""Plays the sample."""

		self.set_item_onset(self.time())
		self.set_sri()
		self.sampler.play(self.block)
		self.process_response()

	def var_info(self):

		"""
		Give a list of dictionaries with variable descriptions

		Returns:
		A list of (name, description) tuples
		"""		

		return item.item.var_info(self) + \
			generic_response.generic_response.var_info(self)
