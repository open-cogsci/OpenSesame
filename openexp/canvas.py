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

temp_files = [] # Contains a list of temporary files that should be cleaned up

class canvas:

	"""A 'magic' class that morphs into the approriate backend from openexp._canvas"""
	
	def __init__(self, experiment, bgcolor=None, fgcolor=None, auto_prepare=True):
		
		backend = experiment.canvas_backend		
		debug.msg('morphing into %s' % backend)
		mod = __import__('openexp._canvas.%s' % backend, fromlist=['dummy'])			
		cls = getattr(mod, backend)
		self.__class__ = cls
		cls.__init__(self, experiment, bgcolor, fgcolor, auto_prepare)
			
def init_display(experiment):

	"""Call the back-end specific init_display function"""
	
	backend = experiment.canvas_backend		
	debug.msg('morphing into %s' % backend)
	mod = __import__('openexp._canvas.%s' % backend, fromlist=['dummy'])			
	mod.init_display(experiment)
		
def close_display(experiment):

	"""Call the back-end specific close_display function"""
		
	backend = experiment.canvas_backend		
	debug.msg('morphing into %s' % backend)
	mod = __import__('openexp._canvas.%s' % backend, fromlist=['dummy'])			
	mod.close_display(experiment)
		
def clean_up(verbose = False):
	
	"""
	Cleans up the temporary pool folders
	
	Keyword arguments:
	verbose		--	a boolean indicating if debugging output should be provided
					(default = False)
	"""
	
	global temp_files
	
	if verbose:
		print "canvas.clean_up()"
	
	for path in temp_files:
		if verbose:
			print "canvas.clean_up(): removing '%s'" % path
		try:
			os.remove(path)
		except Exception as e:
			if verbose:
				print "canvas.clean_up(): failed to remove '%s': %s" % (path, e)
						
def gabor_file(orient, freq, env = "gaussian", size = 96, stdev = 12, phase = 0, col1 = "white", col2 = "black", bgmode = "avg"):

	"""
	Creates a temporary file containing a Gabor patch.

	Keyword arguments:
	See canvas.noise_patch()
	
	Returns:
	A path to the image file
	"""
	
	global temp_files
	import openexp._canvas.legacy
	surface = openexp._canvas.legacy._gabor(orient, freq, env, size, stdev, phase, col1, col2, bgmode)
	
	tmp = tempfile.mkstemp(suffix = ".png")	[1]
	pygame.image.save(surface, tmp)
	temp_files.append(tmp)
	
	return tmp
	
def noise_file(env = "gaussian", size = 96, stdev = 12, col1 = "white", col2 = "black", bgmode = "avg"):

	"""
	Creates a temporary file containing a noise patch.
	
	Keyword arguments:
	See canvas.noise_patch()
	
	Returns:
	A path to the image file
	"""
	
	global temp_files	
	import openexp._canvas.legacy	
	surface = openexp._canvas.legacy._noise_patch(env, size, stdev, col1, col2, bgmode)
	
	tmp = tempfile.mkstemp(suffix = ".png")	[1]
	pygame.image.save(surface, tmp)
	temp_files.append(tmp)
	
	return tmp
					
