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

from libopensesame import item, exceptions, debug

class logger(item.item):

	"""The logger item logs variables to a plain text .csv file"""

	description = u'Logs experimental data'

	def __init__(self, name, experiment, string=None):

		"""
		Constructor.
		
		Arguments:
		name		--	The name of the item.
		experiment 	--	The experiment.

		Keyword arguments:
		string		--	An item definition string (default=None).
		"""

		self.logvars = []
		self.log_started = False
		self.use_quotes = u'yes'
		self.auto_log = u'yes'
		self.ignore_missing = u'yes' # This means that missing variables should
									# be ignored in the sense that they are
									# assigned the value 'NA'. They are included
									# in the logfile.
		item.item.__init__(self, name, experiment, string)

	def run(self):

		"""Log the selected variables"""

		if not self.log_started:
			self.log_started = True
			# If auto logging is enabled, collect all variables
			if self.get(u'auto_log') == u'yes':
				self.logvars = []
				for logvar, val, item in self.experiment.var_list():
					if (self.has(logvar) or self.get(u'ignore_missing') == \
						u'yes') and logvar not in self.logvars:
						self.logvars.append(logvar)
						debug.msg(u'auto-logging "%s"' % logvar)
			# Sort the logvars to ascertain a consistent ordering
			self.logvars.sort()
			# Draw the first line with variables
			self.log(u','.join(self.logvars))

		l = []
		for var in self.logvars:
			try:
				val = self.unistr(self.get(var))
			except exceptions.runtime_error as e:
				if self.get(u'ignore_missing') == u'yes':
					val = u'NA'
				else:
					raise exceptions.runtime_error( \
						u"Logger '%s' tries to log the variable '%s', but this variable is not available. Please deselect '%s' in logger '%s' or enable the 'Use NA for variables that have not been set' option." \
						% (self.name, var, var, self.name))
			l.append(val)

		if self.get(u'use_quotes') == u'yes':
			self.log(u'"' + (u'","'.join(l)) + u'"')
		else:
			self.log(u",".join(l))

	def from_string(self, string):

		"""
		Parse the logger from a definition string
		
		Arguments:
		string -- definition string
		"""

		self.logvars = []
		for line in string.split(u'\n'):
			self.parse_variable(line)
			l = self.split(line)
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

