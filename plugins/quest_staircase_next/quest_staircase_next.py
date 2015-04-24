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

from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin

class quest_staircase_next(item):

	"""
	desc:
		Process a response and adjust staircase level.
	"""

	description = u'Updates the Quest test value based on a response'

	def reset(self):

		"""
		desc:
			Initialize default variables.
		"""

		self.var.response_var = u'correct'

	def run(self):

		"""
		desc:
			Run phase for plug-in.
		"""

		resp = self.var.get(self.var.response_var)
		try:
			resp = float(resp)
		except:
			# Don't process non-float responses
			return
		self.experiment.quest.update(self.var.quest_test_value, resp)
		self.experiment.quest_set_next_test_value()

class qtquest_staircase_next(quest_staircase_next, qtautoplugin):

	"""
	desc:
		The GUI part of the plug-in. Controls are defined in info.json.
	"""

	def __init__(self, name, experiment, script=None):

		"""
		desc:
			Constructor.

		arguments:
			name:		The name of the plug-in.
			experiment:	The experiment object.

		keywords:
			script:		A definition script.
		"""

		quest_staircase_next.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)
