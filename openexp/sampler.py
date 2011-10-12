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

class sampler:

	"""
	This is a dummy class, which morphes into the appropriate backend. For a list of
	functions, see openexp._sampler.legacy
	"""

	def __init__(self, experiment, src):
	
		if experiment.debug:
			print "sampler.__init__(): morphing into openexp._sampler.%s" % experiment.sampler_backend				
			exec("import openexp._sampler.%s" % experiment.sampler_backend)
			self.__class__ = eval("openexp._sampler.%s.%s" % (experiment.sampler_backend, experiment.sampler_backend))					
		else:
			try:
				exec("import openexp._sampler.%s" % experiment.sampler_backend)
				self.__class__ = eval("openexp._sampler.%s.%s" % (experiment.sampler_backend, experiment.sampler_backend))
			except Exception as e:
				raise openexp.exceptions.sample_error("Failed to import 'openexp._sampler.%s' as sampler backend.<br /><br />Error: %s" % (experiment.sampler_backend, e))	
											
		exec("openexp._sampler.%s.%s.__init__(self, experiment, src)" % (experiment.sampler_backend, experiment.sampler_backend))				
		
def init_sound(experiment):

	"""Call the back-end specific init_sound function"""

	if experiment.debug:
		exec("import openexp._sampler.%s" % experiment.sampler_backend)
		exec("openexp._sampler.%s.init_sound(experiment)" % experiment.sampler_backend)
	else:
		try:
			exec("import openexp._sampler.%s" % experiment.sampler_backend)
			exec("openexp._sampler.%s.init_sound(experiment)" % experiment.sampler_backend)
		except Exception as e:
			raise openexp.exceptions.sample_error("Failed to call openexp._sampler.%s.init_sound()<br /><br />Error: %s" % (experiment.sampler_backend, e))				

def close_sound(experiment):

	"""Call the back-end specific close_sound function"""

	if experiment.debug:
		exec("import openexp._sampler.%s" % experiment.sampler_backend)
		exec("openexp._sampler.%s.close_sound(experiment)" % experiment.sampler_backend)
	else:
		try:
			exec("import openexp._sampler.%s" % experiment.sampler_backend)
			exec("openexp._sampler.%s.close_sound(experiment)" % experiment.sampler_backend)
		except Exception as e:
			raise openexp.exceptions.sample_error("Failed to call openexp._sampler.%s.close_sound()<br /><br />Error: %s" % (experiment.sampler_backend, e))				

