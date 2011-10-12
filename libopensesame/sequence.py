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
import openexp.keyboard
import shlex

class sequence(item.item):

	"""The sequence item"""

	def __init__(self, name, experiment, string=None):
	
		"""
		Constructor
		
		Arguments:
		name -- the item name
		experiment the opensesame experiment
		
		Keywords arguments:
		string -- a definition string (default=None)
		"""
	
		self.items = []		
		self.item_type = "sequence"		
		self.description = "Runs a number of items in sequence"		
		self.flush_keyboard = "yes"
		item.item.__init__(self, name, experiment, string)
				
	def run(self):
	
		"""
		Run the sequence
		
		Returns:
		True on success, False on failure
		"""
	
		# Optionally flush the responses to catch escape presses
		if self._keyboard != None:
			self._keyboard.flush()		
		for item, cond in self._items:		
			if eval(cond):	
				self.experiment.items[item].run()
		return True							
		
	def parse_run(self, i):
	
		"""
		Parse a run line from the definition script
		
		Arguments:
		i -- a list of words, corresponding to a single script line
		
		Returns:
		A (item_name, conditional) tuple
		"""
	
		name = i[1]
		cond = "always"
		if len(i) > 2:
			cond = i[2]	
		return i[1], cond 
		
	def from_string(self, string):
	
		"""
		Parses a definition string
		
		Arguments:
		string -- a definition string
		"""
	
		for i in string.split("\n"):
			self.parse_variable(i)
			i = shlex.split(i.strip())
			if len(i) > 0:
				if i[0] == "run" and len(i) > 1:				
					self.items.append(self.parse_run(i))			
		
	def prepare(self):
	
		"""
		Prepare the sequence
		
		Returns:
		True on success, False on failure
		"""
		
		item.item.prepare(self)
		
		if self.get("flush_keyboard") == "yes":		
			# Create a keyboard to flush responses at the start of the run phase
			self._keyboard = openexp.keyboard.keyboard(self.experiment)
		else:
			self._keyboard = None
		
		self._items = []
		for _item, cond in self.items:
			if _item not in self.experiment.items:			
				raise exceptions.runtime_error( \
					"Could not find item '%s', which is called by sequence item '%s'" \
					% (_item, self.name))
			if not self.experiment.items[_item].prepare():			
				raise exceptions.runtime_error( \
					"Failed to prepare item '%s', which is called by sequence item '%s'" \
					% (_item, self.name))
				
			self._items.append( (_item, self.compile_cond(cond)) )
															
		return True
			
	def to_string(self):
	
		"""
		Encode the sequence as a definition string
		
		Returns:
		A definition string
		"""
	
		s = item.item.to_string(self, "sequence")
		for _item, cond in self.items:
			s += "\trun %s \"%s\"\n" % (_item, cond)
		return s			
		
