#-*- coding:utf-8 -*-

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

from libopensesame import debug

class sampler:

	"""
	This is a dummy class, which morphes into the appropriate backend. For a list of
	functions, see openexp._sampler.legacy
	"""

	def __init__(self, experiment, src):

		backend = experiment.sampler_backend		
		debug.msg('morphing into %s' % backend)
		mod = __import__('openexp._sampler.%s' % backend, fromlist=['dummy'])			
		cls = getattr(mod, backend)
		self.__class__ = cls
		cls.__init__(self, experiment, src)
		

def init_sound(experiment):

	"""Call the back-end specific init_sound function"""

	backend = experiment.sampler_backend		
	debug.msg('morphing into %s' % backend)
	mod = __import__('openexp._sampler.%s' % backend, fromlist=['dummy'])			
	mod.init_sound(experiment)
		
def close_sound(experiment):

	"""Call the back-end specific close_sound function"""

	backend = experiment.sampler_backend		
	debug.msg('morphing into %s' % backend)
	mod = __import__('openexp._sampler.%s' % backend, fromlist=['dummy'])			
	mod.close_sound(experiment)
