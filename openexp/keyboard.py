"""
This file is part of openexp.

openexp is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

openexp is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with openexp.  If not, see <http://www.gnu.org/licenses/>.
"""

class keyboard:

	"""
	Based on the keyboard_backend variable in the experiment, this class
	morphs into the appropriate keyboard backend class.
	"""

	def __init__(self, experiment, keylist = None, timeout = None):
	
		if experiment.debug:
			print "keyboard.__init__(): morphing into openexp._keyboard.%s" % experiment.keyboard_backend				
			exec("import openexp._keyboard.%s" % experiment.keyboard_backend)
			self.__class__ = eval("openexp._keyboard.%s.%s" % (experiment.keyboard_backend, experiment.keyboard_backend))					
		else:
			try:
				exec("import openexp._keyboard.%s" % experiment.keyboard_backend)
				self.__class__ = eval("openexp._keyboard.%s.%s" % (experiment.keyboard_backend, experiment.keyboard_backend))
			except Exception as e:
				raise openexp.exceptions.canvas_error("Failed to import 'openexp._keyboard.%s' as keyboard backend.<br /><br />Error: %s" % (experiment.backend, e))		
															
		exec("openexp._keyboard.%s.%s.__init__(self, experiment, keylist, timeout)" % (experiment.keyboard_backend, experiment.keyboard_backend))
		

