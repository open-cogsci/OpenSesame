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

temp_files = []

class canvas:
	
	def __init__(self, experiment, bgcolor = "black", fgcolor = "white"):
	
		try:
			exec("from openexp.video import %s" % experiment.video_backend)
			self.__class__ = eval("%s.%s" % (experiment.video_backend, experiment.video_backend))
		except Exception as e:
			raise openexp.exceptions.canvas_error("Failed to import 'openexp.video.%s' as video backend.<br /><br />Error: %s" % (experiment.video_backend, e))		
											
		exec("openexp.video.%s.%s.__init__(self, experiment, bgcolor, fgcolor)" % (experiment.video_backend, experiment.video_backend))	
			
	def color(self, color):
		pass
				
	def flip(self, x = True, y = False):
		pass		
		
	def copy(self, canvas):
		pass
		
	def xcenter(self):
		pass	
		
	def ycenter(self):
		pass
		
	def show(self):
		pass
		
	def clear(self, color = None):
		pass
		
	def set_penwidth(self, penwidth):
		pass
		
	def set_fgcolor(self, color):
		pass
		
	def set_bgcolor(self, color):
		pass
		
	def set_font(self, style, size):
		pass
		
	def fixdot(self, x = None, y = None, color = None):
		pass	
		
	def circle(self, x, y, r, fill = False, color = None):
		pass

	def line(self, sx, sy, ex, ey, color = None):
		pass
		
	def arrow(self, sx, sy, ex, ey, arrow_size = 5, color = None):
		pass	
		
	def rect(self, x, y, w, h, fill = False, color = None):
		pass
			
	def ellipse(self, x, y, w, h, fill = False, color = None):
		pass		
			
	def text_size(self, text):
		pass
		
	def text(self, text, center = True, x = None, y = None, color = None):
		pass
		
	def textline(self, text, line, color = None):
		pass
		
	def image(self, fname, center = True, x = None, y = None, scale = None):
		pass
							
	def gabor(self, x, y, orient, freq, env = "gaussian", size = 96, stdev = 12, phase = 0, col1 = "white", col2 = "black", bgmode = "avg"):
		pass
		
	def noise_patch(self, x, y, env = "gaussian", size = 96, stdev = 12, col1 = "white", col2 = "black", bgmode = "avg"):
		pass
		
def init_display(experiment):

	"""
	Call the init_display function from the back-end
	"""

	try:
		exec("from openexp.video import %s" % experiment.video_backend)
		exec("openexp.video.%s.init_display(experiment)" % experiment.video_backend)
	except Exception as e:
		raise openexp.exceptions.canvas_error("Failed to call openexp.video.%s.init_display()<br /><br />Error: %s" % (experiment.video_backend, e))				
		
def close_display(experiment):

	"""
	Call the close_display function from the back-end
	"""

	try:
		exec("from openexp.video import %s" % experiment.video_backend)
		exec("openexp.video.%s.close_display(experiment)" % experiment.video_backend)
	except Exception as e:
		raise openexp.exceptions.canvas_error("Failed to call openexp.video.%s.close_display()<br /><br />Error: %s" % (experiment.video_backend, e))						
		
def clean_up(verbose = False):
	
	"""
	Cleans up the temporary pool folders
	"""
	
	global temp_files
	
	if verbose:
		print "canvas.clean_up()"
	
	for path in temp_files:
		if verbose:
			print "canvas.clean_up(): removing '%s'" % path
		try:
			os.remove(path)
		except:
			if verbose:
				print "canvas.clean_up(): failed to remove '%s'" % path
				
