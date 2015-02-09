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
import tempfile
import pygame
import os

 # A list of temporary files that should be cleaned up.
temp_files = []

def canvas(experiment, *arglist, **kwdict):

	"""
	desc:
		A factory that returns a back-end specific canvas object.

	arguments:
		experiment:
			desc:	The experiment object.
			type:	experiment

	argument-list:
		arglist:	See canvas.__init__().

	keyword-dict:
		kwdict:		See canvas.__init__().
	"""

	backend = experiment.get(u'canvas_backend')
	debug.msg(u'morphing into %s' % backend)
	mod = __import__('openexp._canvas.%s' % backend, fromlist=['dummy'])
	cls = getattr(mod, backend)
	return cls(experiment, *arglist, **kwdict)

def init_display(experiment):

	"""
	desc:
		Calls the back-end specific init_display function.

	arguments:
		experiment:		The experiment object.
		type:			experiment
	"""

	backend = experiment.get(u'canvas_backend')
	debug.msg('morphing into %s' % backend)
	mod = __import__('openexp._canvas.%s' % backend, fromlist=['dummy'])
	mod.init_display(experiment)

def close_display(experiment):

	"""
	desc:
		Calls the back-end specific close_display function.

	arguments:
		experiment:		The experiment object.
		type:			experiment
	"""

	backend = experiment.get(u'canvas_backend')
	debug.msg('morphing into %s' % backend)
	mod = __import__('openexp._canvas.%s' % backend, fromlist=['dummy'])
	mod.close_display(experiment)

def clean_up(verbose=False):

	"""
	desc:
		Cleans up temporary pool folders.

	keywords:
		verbose:
			desc:	Indicates if debugging output should be provided.
			type:	bool
	"""

	global temp_files
	if verbose:
		print(u"canvas.clean_up()")
	for path in temp_files:
		if verbose:
			print(u"canvas.clean_up(): removing '%s'" % path)
		try:
			os.remove(path)
		except Exception as e:
			if verbose:
				print(u"canvas.clean_up(): failed to remove '%s': %s" \
					% (path, e))

def gabor_file(*arglist, **kwdict):

	"""
	desc:
		Creates a temporary file containing a Gabor patch.

	argument-list:
		arglist:	See canvas.gabor() for a description of arguments.

	keyword-dict:
		kwdict:		See canvas.gabor() for a description of keywords.

	returns:
		A path to the image file.
	"""

	global temp_files
	from openexp._canvas import canvas
	surface = canvas._gabor(*arglist, **kwdict)
	tmp = tempfile.mkstemp(suffix='.png')[1]
	pygame.image.save(surface, tmp)
	temp_files.append(tmp)
	return tmp

def noise_file(*arglist, **kwdict):

	"""
	desc:
		Creates a temporary file containing a noise patch.

	argument-list:
		arglist:	See canvas.noise_path() for a description of arguments.

	keyword-dict:
		kwdict:		See canvas.noise_path() for a description of keywords.

	returns:
		A path to the image file.
	"""

	global temp_files
	from openexp._canvas import canvas
	surface = canvas._noise_patch(*arglist, **kwdict)
	tmp = tempfile.mkstemp(suffix='.png')[1]
	pygame.image.save(surface, tmp)
	temp_files.append(tmp)
	return tmp
