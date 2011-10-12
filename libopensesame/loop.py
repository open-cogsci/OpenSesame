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
import openexp.keyboard
from random import *
from math import *

class loop(item.item):

	"""A loop item runs a single other item multiple times, while varying independent variables"""

	def __init__(self, name, experiment, string = None):

		"""
		Constructor

		Arguments:
		name -- the name of the item
		experiment -- an instance of libopensesame.experiment

		Keyword arguments:
		string -- a string with the item definition (default = None)
		"""

		self.cycles = 1
		self.repeat = 1
		self.matrix = {}
		self.order = "random"
		self.description = "Repeatedly runs another item"
		self.item_type = "loop"
		self.item = ""
		item.item.__init__(self, name, experiment, string)

	def from_string(self, string):

		"""
		Create a loop from a definition in a string

		Arguments:
		string -- the definition of the loop
		"""

		for i in string.split("\n"):

			self.parse_variable(i)

			# Extract the item to run
			i = shlex.split(i.strip())
			if len(i) > 0:
				if i[0] == "run" and len(i) > 1:
					self.item = i[1]

				if i[0] == "setcycle" and len(i) > 3:

					cycle = int(i[1])
					var = i[2]
					val = i[3]
					try:
						if int(val) == float(val):
							val = int(val)
						else:
							val = float(val)
					except:
						pass

					if cycle not in self.matrix:
						self.matrix[cycle] = {}
					self.matrix[cycle][var] = val

	def run(self):

		"""
		Run the loop

		Returns:
		True on success, False on failure
		"""

		# First generate a list
		l = []

		j = 0

		# Walk through all complete repeats
		whole_repeats = int(self.repeat)
		for j in range(whole_repeats):
			for i in range(self.cycles):
				l.append( (j, i) )

		# Add the leftover repeats
		partial_repeats = self.repeat - whole_repeats
		if partial_repeats > 0:
			all_cycles = range(self.cycles)
			_sample = sample(all_cycles, int(len(all_cycles) * partial_repeats))
			for i in _sample:
				l.append( (j, i) )

		# Randomize the list if necessary
		if self.order == "random":
			shuffle(l)

		# Create a keyboard to flush responses between cycles
		self._keyboard = openexp.keyboard.keyboard(self.experiment)

		# Walk through the list
		for j, i in l:
			if self.item in self.experiment.items:

				# Set the variables from the matrix
				if i in self.matrix:
					for var in self.matrix[i]:
						val = self.matrix[i][var]

						# By starting with an "=" sign, users can incorporate a Python
						# statement, for example to call functions from the random or
						# math module
						if type(val) == str and len(val) > 2 and val[0] == "=":
							code = "%s" % self.eval_text(val[1:], soft_ignore = True, quote_str = True)
							if self.experiment.debug:
								print "loop.run(): evaluating '%s'" % code
							try:
								val = eval(code)
							except Exception as e:
								raise exceptions.runtime_error("Failed to evaluate '%s' in loop item '%s': %s" % (code, self.name, e))

						self.experiment.set(var, val)

				if eval("self.experiment.items[\"%s\"].prepare()" % self.item):
					exec("self.experiment.items[\"%s\"].run()" % self.item)
				else:
					raise exceptions.runtime_error("Failed to prepare item '%s', which is called by loop item '%s'" % (self.item, self.name))

			else:
				raise exceptions.runtime_error("Could not find item '%s', which is called by loop item '%s'" % (self.item, self.name))

		return True

	def to_string(self):

		"""
		Create a string with the definition of the loop

		Returns:
		A string with the definition
		"""

		s = item.item.to_string(self, "loop")
		for i in self.matrix:
			for var in self.matrix[i]:
				s += "\tsetcycle %d %s \"%s\"\n" % (i, var, self.matrix[i][var])
		s += "\trun %s\n" % self.item
		return s

	def var_info(self):

		"""
		Describe the variables specific to the loop

		Returns:
		A list of (variable name, description) tuples
		"""

		l = item.item.var_info(self)
		var_list = {}
		for i in self.matrix:
			for var in self.matrix[i]:
				if var not in var_list:
					var_list[var] = []
				var_list[var].append(str(self.matrix[i][var]))
		for var in var_list:
			l.append( (var, "[" + ", ".join(var_list[var]) + "]"))
		return l

