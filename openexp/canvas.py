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

import openexp.exceptions
import tempfile
import pygame
import os

temp_files = [] # Contains a list of temporary files that should be cleaned up

class canvas:

	"""A 'magic' class that morphs into the approriate backend from openexp._canvas"""
	
	def __init__(self, experiment, bgcolor = None, fgcolor = None):
	
		"""Constructor"""
	
		if experiment.debug:
			print "canvas.__init__(): morphing into openexp._canvas.%s" % experiment.canvas_backend		
			exec("import openexp._canvas.%s" % experiment.canvas_backend)
			self.__class__ = eval("openexp._canvas.%s.%s" % (experiment.canvas_backend, experiment.canvas_backend))				
		else:
			try:
				exec("import openexp._canvas.%s" % experiment.canvas_backend)
				self.__class__ = eval("openexp._canvas.%s.%s" % (experiment.canvas_backend, experiment.canvas_backend))				
			except Exception as e:
				raise openexp.exceptions.canvas_error("Failed to import 'openexp._canvas.%s' as video backend.<br /><br />Error: %s" % (experiment.canvas_backend, e))													

		exec("openexp._canvas.%s.%s.__init__(self, experiment, bgcolor, fgcolor)" % (experiment.canvas_backend, experiment.canvas_backend))				
		
def init_display(experiment):

	"""Call the back-end specific init_display function"""

	if experiment.debug:
		exec("import openexp._canvas.%s" % experiment.canvas_backend)
		exec("openexp._canvas.%s.init_display(experiment)" % experiment.canvas_backend)
	else:
		try:
			exec("import openexp._canvas.%s" % experiment.canvas_backend)
			exec("openexp._canvas.%s.init_display(experiment)" % experiment.canvas_backend)
		except Exception as e:
			raise openexp.exceptions.canvas_error("Failed to call openexp._canvas.%s.init_display()<br /><br />Error: %s" % (experiment.canvas_backend, e))				
		
def close_display(experiment):

	"""Call the back-end specific close_display function"""
	
	if experiment.debug:
		exec("import openexp._canvas.%s" % experiment.canvas_backend)
		exec("openexp._canvas.%s.close_display(experiment)" % experiment.canvas_backend)
	else:
		try:
			exec("import openexp._canvas.%s" % experiment.canvas_backend)
			exec("openexp._canvas.%s.close_display(experiment)" % experiment.canvas_backend)
		except Exception as e:
			raise openexp.exceptions.canvas_error("Failed to call openexp._canvas.%s.close_display()<br /><br />Error: %s" % (experiment.canvas_backend, e))						
		
def clean_up(verbose = False):
	
	"""
	Cleans up the temporary pool folders
	
	Keyword arguments:
	verbose -- a boolean indicating if debugging output should be provided (default = False)
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
					
