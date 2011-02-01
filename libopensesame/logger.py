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

from libopensesame import item, exceptions
import shlex

class logger(item.item):

	def __init__(self, name, experiment, string = None):
	
		"""
		Initialize the logger
		"""

		self.logvars = []
		self.log_started = False
		self.description = "Logs experimental data"		
		self.item_type = "logger"
		self.use_quotes = "yes"
		self.auto_log = "yes"
		item.item.__init__(self, name, experiment, string)				
		
	def run(self):
	
		"""
		Do the actual logging
		"""
					
		if not self.log_started:
			self.log_started = True
						
			# If auto logging is enabled, collect all variables
			if self.get("auto_log") == "yes":
				self.logvars = []
				for logvar, val, item in self.experiment.var_list():
					if self.has(logvar):
						self.logvars.append(logvar)			
						if self.experiment.debug:
							print "logger.run(): auto-logging '%s'" % logvar			
							
			# Sort the logvars to ascertain a consistent ordering
			self.logvars = sorted(self.logvars)
													
			# Draw the first line with variables
			self.log(",".join(self.logvars))
									
		l = []
		for var in self.logvars:
			try:
				l.append(str(self.get(var)))
			except exceptions.runtime_error as e:
				raise exceptions.runtime_error("Logger '%s' tries to log the variable '%s', but this variable is not available. Please deselect '%s' in logger '%s'." % (self.name, var, var, self.name))
		if self.get("use_quotes") == "yes":
			self.log("\"" + ("\",\"".join(l)) + "\"")
		else:				
			self.log(",".join(l))
		
	def from_string(self, string):
	
		"""
		Read the logger from a string
		"""
	
		self.logvars = []
		for line in string.split("\n"):		
			self.parse_variable(line)		
			l = shlex.split(line)
			if len(l) > 1 and l[0] == "log":
				self.logvars.append(l[1])
				
	def to_string(self):
	
		"""
		Encode the logger back into a string
		"""
	
		s = item.item.to_string(self, "logger")
		for logvar in self.logvars:
			s += "\t" + "log \"%s\"\n" % logvar
		return s
