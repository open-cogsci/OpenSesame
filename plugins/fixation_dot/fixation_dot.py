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

import os
from PyQt4 import QtGui, QtCore
from libopensesame.item import item
from libopensesame.generic_response import generic_response
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.canvas import canvas

class fixation_dot(item, generic_response):

	"""A simple fixation-dot plug-in."""

	description = \
		u'Presents a central fixation dot with a choice of various styles'

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
		self.style = u'default'
		self.duration = 1000
		self.penwidth = 3
		self.x = 0
		self.y = 0
		# Call the parent constructor.
		item.__init__(self, name, experiment, script)

	def prepare(self):

		"""Prepare a canvas with a fixation dot."""

		# Call parent functions.
		item.prepare(self)
		generic_response.prepare(self)
		# Create a canvas.
		self.c = canvas(self.experiment, self.get(u'background'), \
			self.get(u'foreground'))
		# Set the coordinates.
		self._x = self.get(u'x') + self.c.xcenter()
		self._y = self.get(u'y') + self.c.ycenter()
		# Draw the fixation dot.
		self.c.set_penwidth(self.get(u'penwidth'))
		if self.style == u'default':
			self.c.fixdot(self._x, self._y)
		elif self.style == u'filled':
			self.c.ellipse(self._x - 10, self._y - 10, 20, 20, True)
		elif self.style == u'filled-small':
			self.c.ellipse(self._x - 5, self._y - 5, 10, 10, True)
		elif self.style == u'empty':
			self.c.ellipse(self._x - 10, self._y - 10, 20, 20, False)
		elif self.style == u'empty-small':
			self.c.ellipse(self._x - 5, self._y - 5, 10, 10, False)
		elif self.style == u'cross':
			self.c.line(self._x - 10, self._y, self._x + 10, self._y)
			self.c.line(self._x, self._y - 10, self._x, self._y + 10)
		elif self.style == u'cross-small':
			self.c.line(self._x - 5, self._y, self._x + 5, self._y)
			self.c.line(self._x, self._y - 5, self._x, self._y + 5)

	def run(self):

		"""Show the canvas and wait for a specified duration."""

		self.set_item_onset(self.c.show())
		self.set_sri()
		self.process_response()
		
	def var_info(self):
		
		"""
		Gives a list of dictionaries with variable descriptions.

		Returns:
		A list of (name, description) tuples.
		"""		

		return item.var_info(self) + generic_response.var_info(self)

class qtfixation_dot(fixation_dot, qtautoplugin):

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

		fixation_dot.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)
