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
import openexp.mouse
from libopensesame.mouse_response import mouse_response
from libqtopensesame.items.qtautoplugin import qtautoplugin


class touch_response(mouse_response):

	"""A simple fixation-dot plug-in."""

	description = \
		u'A grid-based response item, convenient for touch screens'

	def reset(self):

		self.var._ncol = 2
		self.var._nrow = 1
		mouse_response.reset(self)

	def process_response(self, response_args):

		"""See base_response_item."""

		response, pos, t1 = response_args
		if pos is not None:
			x, y = pos
			if self.experiment.var.uniform_coordinates == u'yes':
				_x = x+self.experiment.var.width/2
				_y = y+self.experiment.var.height/2
			else:
				_x, _y = x, y
			col = _x // (self.experiment.var.width / self.var._ncol)
			row = _y // (self.experiment.var.height / self.var._nrow)
			response = row * self.var._ncol + col + 1
		mouse_response.process_response(self, (response, pos, t1) )


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
