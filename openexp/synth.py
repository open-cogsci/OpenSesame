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

class synth:

	"""
	This is a dummy class, which morphes into the appropriate backend. For a list of
	functions, see openexp._synth.legacy
	"""

	def __init__(self, experiment, osc = "sine", freq = 440, length = 100, attack = 0, decay = 5):
	
		if experiment.debug:
			print "synth.__init__(): morphing into openexp._synth.%s" % experiment.synth_backend				
			exec("import openexp._synth.%s" % experiment.synth_backend)
			self.__class__ = eval("openexp._synth.%s.%s" % (experiment.synth_backend, experiment.synth_backend))					
		else:
			try:
				exec("import openexp._synth.%s" % experiment.synth_backend)
				self.__class__ = eval("openexp._synth.%s.%s" % (experiment.synth_backend, experiment.synth_backend))
			except Exception as e:
				raise openexp.exceptions.canvas_error("Failed to import 'openexp._synth.%s' as synth backend.<br /><br />Error: %s" % (experiment.backend, e))	
											
		exec("openexp._synth.%s.%s.__init__(self, experiment, osc, freq, length, attack, decay)" % (experiment.synth_backend, experiment.synth_backend))
				

		

