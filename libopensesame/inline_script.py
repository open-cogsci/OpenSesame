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

	"""Allows users to use Python code in their experiments"""

	def __init__(self, name, experiment, string = None):
	
		"""<DOC>
		Constructor. You will generally not create an
		inline_script item yourself, but use OpenSesame to create a body
		for the prepare() and run() functions.

		Arguments:
		name -- the name of the item
		experiment -- the experiment
		
		Keyword arguments:
		string -- an item definition string (default = None)			
		</DOC>"""

		self.description = "Executes Python code"
		self.item_type = "inline_script"			
		self._prepare = ""
		self._run = ""
		self._var_info = None	
		item.item.__init__(self, name, experiment, string)		
		
	def copy_sketchpad(self, sketchpad_name):
	
		"""<DOC>
		Create a canvas that is a copy from the canvas of a sketchpad item

		Arguments:
		sketchpad_name -- the name of the sketchpad

		Returns:
		An openexp canvas
		</DOC>"""
		
		c = self.offline_canvas()
		c.copy(self.experiment.items[sketchpad_name].canvas)
		return c
		
	def offline_canvas(self):
	
		"""<DOC>
		Create an empty canvas

		Returns:
		An openexp canvas
		</DOC>"""
	
		return canvas.canvas(self.experiment, self.get("background"), self.get("foreground"))
		
	def prepare(self):
	
		"""<DOC>
		Execute the prepare script. The code that you enter in the 'prepare'
		tab of an inline_script item in the GUI is used as a body for this
		function.
		</DOC>"""	
		
		item.item.prepare(self)
				
		try:
			self.cprepare = compile(self._prepare, "<string>", "exec")
		except Exception as e:
			raise exceptions.inline_error(self.name, "prepare", e)
			
		try:
			self.crun = compile(self._run, "<string>", "exec")
		except Exception as e:
			raise exceptions.inline_error(self.name, "run", e)			
		
		try:
			exec(self.cprepare)
		except Exception as e:			
			raise exceptions.inline_error(self.name, "prepare", e)
				
		return True
		
	def run(self):
	
		"""<DOC>
		Execute the run script. The code that you enter in the 'run'
		tab of an inline_script item in the GUI is used as a body for this
		function.
		</DOC>"""
		
		try:
			exec(self.crun)
		except Exception as e:		
			raise exceptions.inline_error(self.name, "run", e)
		
		return True		
		
	def var_info(self):
	
		"""
		Give a list of dictionaries with variable descriptions

		Returns:
		A list of (variable, description) tuples
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
