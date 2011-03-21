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
from openexp import canvas
import shlex
import re

class inline_script(item.item):

	def __init__(self, name, experiment, string = None):
	
		"""
		Initialize the inline_script
		"""

		self.description = "Executes Python code"
		self.item_type = "inline_script"		
		
		self._prepare = ""
		self._run = ""
		self._var_info = None
		
		item.item.__init__(self, name, experiment, string)		
		
	def copy_sketchpad(self, item_name):
	
		"""
		A convenience function which copies the canvas from a sketchpad
		"""
		
		c = self.offline_canvas()
		c.copy(self.experiment.items[item_name].canvas)
		return c
		
	def offline_canvas(self):
	
		"""
		A convenience function to create a new offline canvas
		"""
	
		return canvas.canvas(self.experiment, self.get("background"), self.get("foreground"))
		
	def prepare(self):
	
		"""
		Execute the prepare script
		"""	
		
		item.item.prepare(self)		
		
		try:
			exec(self._prepare)
		except Exception as e:
			
			raise exceptions.inline_error(self.name, "prepare", e)
				
		return True
		
	def run(self):
	
		"""
		Execute the run script
		"""		
		try:
			exec(self._run)
		except Exception as e:		
			raise exceptions.inline_error(self.name, "run", e)
		
		return True		
		
	def var_info(self):
	
		"""
		Give a list of dictionaries with variable descriptions
		"""
		
		# Don't parse the script if it isn't necessary, since
		# regular expressions are a bit slow
		if self._var_info != None:
			return self._var_info
		
		l = item.item.var_info(self)

		m = re.findall("self.experiment.set\(\"(\w+)\"(\s*),(\s*)(\"*)([^\"\)]*)(\"*)", self._prepare + self._run)
		for var, s1, s2, q1, val, q2 in m:
			if q1 != "\"":
				val = "<i>Set to [%s]</i>" % val
			l.append( (var, val) )		
		self._var_info = l
		
		return l			
