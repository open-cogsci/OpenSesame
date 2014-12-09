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
from libopensesame import sampler, item, generic_response
import openexp.synth

class synth(sampler.sampler, item.item):

	"""Plays a synthesized sound"""

	description = u'A basic sound synthesizer'

	def reset(self):

		"""See item."""

		self.item_type = u'synth'
		self.freq = 440
		self.length = 100
		self.osc = u'sine'
		self.pan = 0
		self.attack = 0
		self.decay = 5
		self.volume = 1.0
		self.duration = u'sound'
		self.block = False

	def prepare(self):

		"""Prepares for playback."""

		item.item.prepare(self)
		try:
			self.sampler = openexp.synth.synth(self.experiment, \
				self.get(u'osc'), self.get(u'freq'), self.get(u'length'), \
				self.get(u'attack'), self.get(u'decay'))
		except Exception as e:
			raise osexception( \
				u"Failed to generate sound in synth '%s': %s" % (self.name, e))
		pan = self.get(u'pan')
		if pan == -20:
			pan = u'left'
		elif pan == 20:
			pan = u'right'
		self.sampler.pan(pan)
		self.sampler.volume(self.get(u'volume'))
		generic_response.generic_response.prepare(self)
