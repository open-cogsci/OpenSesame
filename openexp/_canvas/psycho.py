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

import math
import openexp._canvas.legacy
import openexp.exceptions
from psychopy import visual, core
import pygame
from PIL import Image, ImageFont, ImageDraw

class psycho(openexp._canvas.legacy.legacy):

	"""
	This is a canvas backend which uses PsychoPy (with Pyglet). This canvas is extremely
	inefficient, but these can be dealt with by clever use of the prepare function.
	"""
	
	def __init__(self, experiment, bgcolor = "black", fgcolor = "white"):
		
		"""
		Initializes the canvas. The specified colors should be used as a 
		default for subsequent drawing operations.
		
		Arguments:
		experiment -- an instance of libopensesame.experiment.experiment
		
		Keyword arguments:
		bgcolor -- a human-readable background color (default = "black")
		fgcolor -- a human-readable foreground color (default = "white")
		"""
		
		self.experiment = experiment
		self.set_fgcolor(fgcolor)
		self.set_bgcolor(bgcolor)
		self.penwidth = 1
		self.antialias = True
				
		self.surface = pygame.Surface( (self.experiment.width, self.experiment.height) )		
		self.stim = None
		self.set_font(self.experiment.font_family, self.experiment.font_size)
		self.clear()		
		self.stim_list = []
		
	def set_font(self, style, size):
	
		"""
		Sets the font for subsequent drawing operations.
		
		Arguments:
		style -- A font located in the resources folder (without the .ttf extension)
		size -- A font size in pixels		
		"""
		
		self.font_style = style
		self.font_size = size		
		
	def text_size(self, text):
	
		"""
		Determines the size of a text string in pixels.
		
		Arguments:
		text -- The text string
		
		Returns:
		A (width, height) tuple containing the dimensions of the text string
		"""
		
		# TODO
		raise openexp.exceptions.canvas_error("openexp._canvas.psycho.text_size(): not implemented!")
		
	def text(self, text, center = True, x = None, y = None, color = None):
		
		"""
		Draws text.
		
		Arguments:
		text -- The text string
		
		Keyword arguments:
		center -- A boolean indicating whether the coordinates reflect the center (True)
				  or top-left (default = True)
		x -- The X coordinate. None = center. (default = None)
		y -- The Y coordinate. None = center. (default = None)
		color -- A custom human readable foreground color. This does not affect the
				 default foreground color as set by set_fdcolor(). (Default = None)		
		"""
		
		if center:
			halign = "center"
			valign = "center"
		else:
			halign = "left"
			valign = "top"
			
		if color == None:
			color = self.fgcolor
		else:
			color = self.color(color)
								
		pos = x - self.xcenter(), self.ycenter() - y						
		
		col = '#%02x%02x%02x' % (self.fgcolor.r, self.fgcolor.g, self.fgcolor.b)
		stim = visual.TextStim(win = self.experiment.window, text = text, alignHoriz = halign, height = self.font_size, alignVert = valign, pos = pos, color = col, opacity = 1)
		self.stim_list.append(stim)
		
	def textline(self, text, line, color = None):
		
		"""
		A convenience function that draws a line of text based on a 
		line number. The text strings are centered on the X-axis and
		vertically spaced with 1.5 the line height as determined by
		text_size().
		
		Arguments:
		text -- The text string
		line -- A line number, where 0 is the center and > 0 is below the center.
		color -- A custom human readable foreground color. This does not affect the
				 default foreground color as set by set_fdcolor(). (Default = None)		
		"""
		
		# TODO
		raise openexp.exceptions.canvas_error("openexp._canvas.psycho.textline(): not implemented!")
						
	def prepare(self):
	
		"""
		The pygame surface needs to be converted to a PIL image, which subsequently
		needs to be converted to a PsychoPy stim. This is very inefficient, so we
		tuck it away in the prepare phase
		"""
		
		t = self.experiment.clock.getTime()
		pg_img = pygame.image.tostring(self.surface, "RGB")
		pil_img = Image.fromstring("RGB", (self.experiment.width, self.experiment.height), pg_img)
		self.stim = visual.SimpleImageStim(win = self.experiment.window, image = pil_img)	
		if self.experiment.debug:
			print "psycho.prepare(): canvas preparation took %d ms" % (1000 * (self.experiment.clock.getTime() - t))
		
	def show(self):
		
		"""
		Puts the canvas onto the screen.
		
		Returns:
		A timestamp containing the time at which the canvas actually appeared
		on the screen (or a best guess).
		"""
			
		t1 = self.experiment.clock.getTime()
		if self.stim == None:
			self.prepare()
		self.stim.draw()
		for s in self.stim_list:
			s.draw()						
		self.experiment.window.flip(clearBuffer = True)		
		t2 = self.experiment.clock.getTime()		
		if self.experiment.debug:
			print "psycho.show(): show took %d ms" % (1000 * (t2 - t1))
		return 1000.0 * t2
		
	def clear(self, color = None):
		
		"""
		Clears the canvas with the current background color.
		
		Keyword arguments:
		color -- A custom background color to be used. This does not affect the
				 default background color as set by set_bgcolor().
				 (Default = None)
		"""
		
		openexp._canvas.legacy.legacy.clear(self, color)
		self.stim_list = []
		self.stim = None

"""
Static methods
"""

# Store the experiment as a singleton, to be used in the _time() function
_experiment = None

def init_display(experiment):

	"""
	Initialize the display before the experiment begins.
		
	Arguments:
	experiment -- An instance of libopensesame.experiment.experiment. The following properties are
				  of particular importance: experimnent.fullscreen (bool), experiment.width (int) and
				  experiment.height (int). The experiment also contains default font settings as
				  experriment.font_family (str) and experiment.font_size (int).
	"""
	
	global _experiment
	_experiment = experiment	
	
	if experiment.has("psychopy_monitor"):
		monitor = experiment.get("psychopy_monitor")
	else:
		monitor = "testMonitor"
		
	if experiment.has("psychopy_wintype"):
		wintype = experiment.get("psychopy_wintype")
	else:
		wintype = "pyglet"
			
	experiment.window = visual.Window( [experiment.width, experiment.height], fullscr = experiment.fullscreen, monitor = monitor, units = "pix", winType = wintype)
	experiment.clock = core.Clock()	
	experiment._time_func = _time	
				
def close_display(experiment):

	"""
	Close the display after the experiment is finished.
	
	Arguments:
	experiment -- An instance of libopensesame.experiment.experiment	
	"""
	
	experiment.window.close()	
	
def _time():

	"""
	Returns a psychopy timestamp converted to milliseconds. This function is not
	to be called directly, but is used by openexp.experiment.time()
	"""

	global _experiment
	return 1000.0 * _experiment.clock.getTime()
	
	
