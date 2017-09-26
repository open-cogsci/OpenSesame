#-*- coding:utf-8 -*-

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

from libopensesame.py3compat import *
from openexp import backend
import tempfile
try:
	import pygame
except ImportError:
	pass
import os

 # A list of temporary files that should be cleaned up.
temp_files = []


def Canvas(experiment, *arglist, **kwdict):

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

	cls = backend.get_backend_class(experiment, u'canvas')
	return cls(experiment, *arglist, **kwdict)


def init_display(experiment):

	"""
	desc:
		Calls the back-end specific init_display function.

	arguments:
		experiment:		The experiment object.
		type:			experiment
	"""

	cls = backend.get_backend_class(experiment, u'canvas')
	cls.init_display(experiment)


def close_display(experiment):

	"""
	desc:
		Calls the back-end specific close_display function.

	arguments:
		experiment:		The experiment object.
		type:			experiment
	"""

	cls = backend.get_backend_class(experiment, u'canvas')
	cls.close_display(experiment)


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

	from openexp._canvas import canvas as _canvas
	surface = _canvas._gabor(*arglist, **kwdict)
	fd, fname = tempfile.mkstemp(suffix=u'.png')
	pygame.image.save(surface, fname)
	temp_files.append(fname)
	os.close(fd)
	return fname


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

	from openexp._canvas import canvas as _canvas
	surface = _canvas._noise_patch(*arglist, **kwdict)
	fd, fname = tempfile.mkstemp(suffix=u'.png')
	pygame.image.save(surface, fname)
	temp_files.append(fname)
	os.close(fd)
	return fname


# Non PEP-8 alias for backwards compatibility
canvas = Canvas
