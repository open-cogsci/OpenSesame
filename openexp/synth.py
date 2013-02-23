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

class synth:

	"""
	This is a dummy class, which morphes into the appropriate backend. For a list of
	functions, see openexp._synth.legacy
	"""

	def __init__(self, experiment, osc="sine", freq=440, length=100, attack=0, decay=5):
	
		backend = experiment.synth_backend		
		debug.msg('morphing into %s' % backend)
		mod = __import__('openexp._sampler.%s' % backend, fromlist=['dummy'])			
		cls = getattr(mod, backend)
		self.__class__ = cls
		cls.__init__(self, experiment, osc, freq, length, attack, decay)
		

