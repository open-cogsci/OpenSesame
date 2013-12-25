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
from libopensesame import item, debug
from libqtopensesame.items.qtautoplugin import qtautoplugin
from PyQt4 import QtGui, QtCore
import os.path
import random

class advanced_delay(item.item):
	
	description = u'Waits for a specified duration'

	def __init__(self, name, experiment, script=None):

		"""
		Constructor.
		
		Arguments:
		name		--	The name of the plug-in.
		experiment	--	The experiment object.
		
		Keyword arguments:
		script		--	A definition script. (default=None)
		"""

		self.duration = 1000
		self.jitter = 0
		item.item.__init__(self, name, experiment, script)

	def prepare(self):

		"""The preparation phase of the plug-in."""

		item.item.prepare(self)

		try:
			if self.get(u"jitter_mode") == u"Uniform":
				self._duration = int(self.get(u"duration") + \
					random.uniform(0, self.get(u"jitter")) - \
					self.get(u"jitter")*0.5)
			elif self.get(u"jitter_mode") == u"Std. Dev.":
				self._duration = int(self.get(u"duration") + \
					random.gauss(0, self.get(u"jitter")))
			else:
				raise osexception( \
					u'Unknown jitter mode in advanced_delay %s' % self.name)
		except:
			raise osexception( \
				u"Invalid duration and/ or jitter in advanced_delay '%s'" % \
				self.name)

		if self._duration < 0:
			self._duration = 0

		self.experiment.set(u"delay_%s" % self.name, self._duration)
		debug.msg(u"delay for %s ms" % self._duration)

	def run(self):

		"""The run phase of the plug-in."""

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
	
	def __init__(self, name, experiment, script=None):

		advanced_delay.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)

