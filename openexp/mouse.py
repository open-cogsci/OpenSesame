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

class mouse:

	"""
	Based on the mouse_backend variable in the experiment, this class
	morphs into the appropriate keyboard backend class.
	"""

	def __init__(self, experiment, buttonlist = None, timeout = None, visible = False):
	
		if experiment.debug:
			print "mouse.__init__(): morphing into openexp._mouse.%s" % experiment.mouse_backend				
			exec("import openexp._mouse.%s" % experiment.mouse_backend)
			self.__class__ = eval("openexp._mouse.%s.%s" % (experiment.mouse_backend, experiment.mouse_backend))					
		else:
			try:
				exec("import openexp._mouse.%s" % experiment.mouse_backend)
				self.__class__ = eval("openexp._mouse.%s.%s" % (experiment.mouse_backend, experiment.mouse_backend))
			except Exception as e:
				raise openexp.exceptions.canvas_error("Failed to import 'openexp._mouse.%s' as mouse backend.<br /><br />Error: %s" % (experiment.backend, e))		
											
		exec("openexp._mouse.%s.%s.__init__(self, experiment, buttonlist, timeout, visible)" % (experiment.mouse_backend, experiment.mouse_backend))
				

		
