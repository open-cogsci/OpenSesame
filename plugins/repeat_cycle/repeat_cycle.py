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
from libopensesame import item
from libqtopensesame.items.qtautoplugin import qtautoplugin

class repeat_cycle(item.item):

	"""
	desc:
		A plug-in to repeat a loop's cycle by setting the `repeat_cycle`
		experimental variable to 1.
	"""


	description = u"Optionally repeat a cycle from a loop"

	def reset(self):

		"""
		desc:
			Initialize the plug-in.
		"""

		self.var.condition = u'never'

	def prepare(self):

		"""
		desc:
			Prepare the item.
		"""

		item.item.prepare(self)
		self._condition = self.syntax.compile_cond(self.var.get(u'condition',
			_eval=False))
		return True

	def run(self):

		"""
		desc:
			Run the item.
		"""

		if self.python_workspace._eval(self._condition):
			self.experiment.var.repeat_cycle = 1
		return True

class qtrepeat_cycle(repeat_cycle, qtautoplugin):

	def __init__(self, name, experiment, script=None):

		# Call parent constructors.
		repeat_cycle.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)
