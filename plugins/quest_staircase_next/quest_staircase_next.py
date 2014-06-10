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

from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin

class quest_staircase_next(item):

	description = \
		u'Updates the Quest test value based on a response'

	def __init__(self, name, experiment, script=None):

		"""
		Constructor.

		Arguments:
		name		--	The name of the plug-in.
		experiment	--	The experiment object.

		Keyword arguments:
		script		--	A definition script. (default=None)
		"""

		self.response_var = u'correct'
		item.__init__(self, name, experiment, script)

	def run(self):

		"""Run phase for plug-in."""

		self.experiment.quest.update(self.get(u'quest_test_value'),
			self.get(self.get(u'response_var')))
		self.experiment.quest_set_next_test_value()

class qtquest_staircase_next(quest_staircase_next, qtautoplugin):

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

		quest_staircase_next.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)
