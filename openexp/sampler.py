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

def sampler(experiment, **kwdict):

	"""
	desc:
		A factory that returns a back-end specific sampler object.

	arguments:
		experiment:
			desc:	The experiment object.
			type:	experiment

	keyword-dict:
		kwdict:		See sampler.__init__() for a description of available
					keywords.
	"""

	backend = experiment.get(u'sampler_backend')
	debug.msg(u'morphing into %s' % backend)
	mod = __import__('openexp._sampler.%s' % backend, fromlist=['dummy'])
	cls = getattr(mod, backend)
	return cls(experiment, **kwdict)

def init_sound(experiment):

	"""
	desc:
		Calls the back-end specific init_sound function.

	arguments:
		experiment:		The experiment object.
		type:			experiment
	"""

	backend = experiment.sampler_backend		
	debug.msg('morphing into %s' % backend)
	mod = __import__('openexp._sampler.%s' % backend, fromlist=['dummy'])			
	mod.init_sound(experiment)
		
def close_sound(experiment):

	"""
	desc:
		Calls the back-end specific close_sound function.

	arguments:
		experiment:		The experiment object.
		type:			experiment
	"""

	backend = experiment.sampler_backend		
	debug.msg('morphing into %s' % backend)
	mod = __import__('openexp._sampler.%s' % backend, fromlist=['dummy'])			
	mod.close_sound(experiment)
