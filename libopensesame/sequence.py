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

from libopensesame.exceptions import osexception
from libopensesame import item
import openexp.keyboard

class sequence(item.item):

	"""The sequence item"""

	description = u'Runs a number of items in sequence'

	def __init__(self, name, experiment, string=None):
	
		"""
		Constructor.

		Arguments:
		name 		--	The name of the item.
		experiment 	--	The experiment.

		Keyword arguments:
		string		-- 	The item definition string. (default=None)
		"""
	
		self.items = []		
		self.flush_keyboard = u'yes'
		item.item.__init__(self, name, experiment, string)
				
	def run(self):
	
		"""Runs the sequence."""
	
		# Optionally flush the responses to catch escape presses
		if self._keyboard != None:
			self._keyboard.flush()		
		for item, cond in self._items:		
			if eval(cond):	
				self.experiment.items[item].run()
		
	def parse_run(self, i):
	
		"""
		Parses a run line from the definition script.
		
		Arguments:
		i 		-- 	A list of words, corresponding to a single script line.
		
		Returns:
		An (item_name, conditional) tuple.
		"""
	
		name = i[1]
		cond = u'always'
		if len(i) > 2:
			cond = i[2]	
		return i[1], cond 
		
	def from_string(self, string):
	
		"""
		Parses a definition string.
		
		Arguments:
		string 	--	A definition string.
		"""
	
		for i in string.split(u'\n'):
			self.parse_variable(i)
			i = self.split(i.strip())
			if len(i) > 0:
				if i[0] == u'run' and len(i) > 1:
					self.items.append(self.parse_run(i))			
		
	def prepare(self):
	
		"""Prepares the sequence."""
		
		item.item.prepare(self)
		if self.get(u'flush_keyboard') == u'yes':
			# Create a keyboard to flush responses at the start of the run phase
			self._keyboard = openexp.keyboard.keyboard(self.experiment)
		else:
			self._keyboard = None
		self._items = []
		for _item, cond in self.items:
			if _item not in self.experiment.items:			
				raise osexception( \
					u"Could not find item '%s', which is called by sequence item '%s'" \
					% (_item, self.name))
			self.experiment.items[_item].prepare()				
			self._items.append( (_item, self.compile_cond(cond)) )
			
	def to_string(self):
	
		"""
		Encodes the sequence as a definition string.
		
		Returns:
		A definition string.
		"""
	
		s = item.item.to_string(self, self.item_type)
		for _item, cond in self.items:
			s += u'\trun %s "%s"\n' % (_item, cond)
		return s
		
