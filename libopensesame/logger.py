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
from libopensesame import item, debug

class logger(item.item):

	"""The logger item logs variables to a plain text .csv file"""

	description = u'Logs experimental data'

	def reset(self):

		"""See item."""

		self.logvars = []
		self.var.auto_log = u'yes'

	def run(self):

		"""Log the selected variables"""

		self.set_item_onset()
		if self.var.auto_log:
			self.experiment.log.write_vars()
		else:
			self.experiment.log.write_vars(self.logvars)

	def from_string(self, string):

		"""
		Parse the logger from a definition string

		Arguments:
		string -- definition string
		"""

		self.variables = {}
		self.comments = []
		self.reset()
		if string is None:
			return
		for line in string.split(u'\n'):
			self.parse_variable(line)
			l = self.syntax.split(line)
			if len(l) > 1 and l[0] == u'log':
				self.logvars.append(l[1])

	def to_string(self):

		"""
		Encode the logger back into a definition string

		Returns:
		A definition string
		"""

		s = item.item.to_string(self, u'logger')
		for logvar in self.logvars:
			s += u'\tlog "%s"\n' % logvar
		return s
