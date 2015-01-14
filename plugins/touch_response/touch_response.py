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

import openexp.mouse
from libopensesame.mouse_response import mouse_response
from libqtopensesame.items.qtautoplugin import qtautoplugin

class touch_response(mouse_response):

	"""A simple fixation-dot plug-in."""

	description = \
		u'A grid-based response item, convenient for touch screens'

	def __init__(self, name, experiment, script=None):

		"""
		Constructor.

		Arguments:
		name		--	The name of the plug-in.
		experiment	--	The experiment object.

		Keyword arguments:
		script		--	A definition script. (default=None)
		"""

		# Set default values.
		self._ncol = 2
		self._nrow = 1
		mouse_response.__init__(self, name, experiment, script)

	def process_response_mouseclick(self, retval):

		"""Processes a mouseclick response."""

		self.experiment.start_response_interval = self.sri
		button, pos, self.experiment.end_response_interval = retval
		if pos != None:
			x, y = pos
			col = x // (self.experiment.width / self._ncol)
			row = y // (self.experiment.height / self._nrow)
			cell = row * self._ncol + col + 1
			self.experiment.set(u'cursor_x', x)
			self.experiment.set(u'cursor_y', y)
			self.experiment.set(u'response', cell)
		else:
			self.experiment.set(u'cursor_x', u'NA')
			self.experiment.set(u'cursor_y', u'NA')
			self.experiment.set(u'response', None)

class qttouch_response(touch_response, qtautoplugin):

	"""The GUI part of the plug-in. Controls are defined in info.json."""

	def __init__(self, name, experiment, script=None):

		"""
		Constructor.

		Arguments:
		name		--	The name of the plug-in.
		experiment	--	The experiment object.

		Keyword arguments:
		script		--	A definition script. (default=None)
		"""

		touch_response.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)
