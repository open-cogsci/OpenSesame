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
from libopensesame import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
import random


class advanced_delay(item.item):

	description = u'Waits for a specified duration'

	def reset(self):

		"""
		desc:
			Initialize plug-in.
		"""

		self.var.duration = 1000
		self.var.jitter = 0
		self.var.jitter_mode = u'Uniform'

	def prepare(self):

		"""
		desc:
			The preparation phase of the plug-in.
		"""

		item.item.prepare(self)
		# Sanity check on the duration value, which should be a positive numeric
		# value.
		if type(self.var.duration) not in (int, float) or self.var.duration < 0:
			raise osexception(
				u'Duration should be a positive numeric value in advanced_delay %s' \
				% self.name)
		if self.var.jitter_mode == u'Uniform':
			self._duration = random.uniform(self.var.duration-self.var.jitter/2,
				self.var.duration+self.var.jitter/2)
		elif self.var.jitter_mode == u'Std. Dev.':
			self._duration = random.gauss(self.var.duration, self.var.jitter)
		else:
			raise osexception(
				u'Unknown jitter mode in advanced_delay %s' % self.name)
		# Don't allow negative durations.
		if self._duration < 0:
			self._duration = 0
		self._duration = int(self._duration)
		self.experiment.var.set(u'delay_%s' % self.name, self._duration)

	def run(self):

		"""
		desc:
			The run phase of the plug-in.
		"""

		self.set_item_onset(self.time())
		self.sleep(self._duration)

	def var_info(self):

		"""
		Gives a list of dictionaries with variable descriptions.

		Returns:
		A list of (name, description) tuples.
		"""

		return item.item.var_info(self) + [(u'delay_%s' % self.name, \
			u'[Determined at runtime]')]

class qtadvanced_delay(advanced_delay, qtautoplugin):

	"""Automatic plug-in GUI."""

	def __init__(self, name, experiment, script=None):

		advanced_delay.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)
