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
import os
from libopensesame.item import item
from libopensesame.generic_response import generic_response
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.canvas import canvas

class fixation_dot(item, generic_response):

	"""A simple fixation-dot plug-in."""

	description = \
		u'Presents a central fixation dot with a choice of various styles'

	def reset(self):

		"""
		desc:
			Initialize the plug-in.
		"""

		self.var.style = u'default'
		self.var.duration = 1000
		self.var.penwidth = 3
		self.var.x = 0
		self.var.y = 0

	def prepare(self):

		"""
		desc:
			Prepare a canvas with a fixation dot.
		"""

		# Call parent functions.
		item.prepare(self)
		generic_response.prepare(self)
		# Create a canvas.
		self.c = canvas(self.experiment, background_color=self.var.background,
			color=self.var.foreground, penwidth=self.var.penwidth)
		self.c.color = self.var.foreground
		self.c.background_color = self.var.background
		# Set the coordinates.
		self._x = self.var.x
		self._y = self.var.y
		if self.var.uniform_coordinates != u'yes':
			self._x += self.c.width/2
			self._y += self.c.height/2
		# For backwards compatibility, we support a few special fixdot styles
		if self.var.style == u'filled':
			self.c.ellipse(self._x - 10, self._y - 10, 20, 20, fill=True)
		elif self.var.style == u'filled-small':
			self.c.ellipse(self._x - 5, self._y - 5, 10, 10, fill=True)
		elif self.var.style == u'empty':
			self.c.ellipse(self._x - 10, self._y - 10, 20, 20, fill=False)
		elif self.var.style == u'empty-small':
			self.c.ellipse(self._x - 5, self._y - 5, 10, 10, fill=False)
		elif self.var.style == u'cross':
			self.c.line(self._x - 10, self._y, self._x + 10, self._y)
			self.c.line(self._x, self._y - 10, self._x, self._y + 10)
		elif self.var.style == u'cross-small':
			self.c.line(self._x - 5, self._y, self._x + 5, self._y)
			self.c.line(self._x, self._y - 5, self._x, self._y + 5)
		# But the new way is to use the style keyword
		else:
			self.c.fixdot(self._x, self._y, style=self.var.style)

	def run(self):

		"""
		desc:
			Show the canvas and wait for a specified duration.
		"""

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

	def __init__(self, name, experiment, script=None):

		fixation_dot.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)
