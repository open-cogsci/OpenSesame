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

import pygame
from pygame.locals import *
import random
import openexp.canvas
import openexp.exceptions
import math
import subprocess
import os
import os.path
import tempfile

class legacy:

	"""
	The legacy backend is the default backend which uses PyGame to handle all
	display operations.	
	
	This class serves as a template for creating OpenSesame video backends. Let's say
	you want to create a dummy backend. First, create dummy.py in the openexp.video
	folder. In dummy.py, create a dummy class, which is derived from openexp.canvas.canvas
	and which implements all the functions specified below.
	
	After you have done this, the new backend can be activated by adding "set video_backend dummy"
	to the general script. This will make OpenSesame use the dummy class instead of the default
	legacy backend.
		
	A few guidelines:
	-- Catch exceptions wherever possible and raise an openexp.exceptions.canvas_error
	   with a clear and descriptive error message.
	-- If you create a temporary file, add its path to the openexp.canvas.temp_files list.
	-- Do not deviate from the guidelines. All back-ends should be interchangeable and 
	   transparent to OpenSesame. You are free to add functionality to this class, to be 
	   used in inline scripts, but this should not break the basic functionality.
	-- Print debugging output only if experiment.debug == True and preferrably in the
	   following format: "template.__init__(): Debug message here".
	"""
	
	def __init__(self, experiment, bgcolor = None, fgcolor = None):
		
		"""<DOC>
		Initializes the canvas. The specified colors should be used as a 
		default for subsequent drawing operations.
		
		Arguments:
		experiment -- an instance of libopensesame.experiment.experiment
		
		Keyword arguments:
		bgcolor -- a human-readable background color or None to use experiment
				   default (default = None)
		fgcolor -- a human-readable foreground color or None to use experiment
				   default (default = None)
		</DOC>"""
		
		self.experiment = experiment

		if fgcolor == None:
			fgcolor = self.experiment.get("foreground")
		if bgcolor == None:
			bgcolor = self.experiment.get("background")

		self.set_fgcolor(fgcolor)
		self.set_bgcolor(bgcolor)
		self.penwidth = 1
		self.antialias = True
		
		self.surface = self.experiment.surface.copy()					
		self.font = self.experiment.font
		self.clear()
		
	def color(self, color):
	
		"""
		Transforms a "human readable" color into the format that
		is used by the back-end (e.g., a PyGame color).
		
		Arguments:
		color -- A color in one the following formats (by example):
			255, 255, 255 (rgb)
			255, 255, 255, 255 (rgba)
			#f57900 (case-insensitive html)
			100 (integer intensity value 0 .. 255, for gray-scale)
			0.1 (float intensity value 0 .. 1.0, for gray-scale)
		
		Returns:
		A color in the back-end format
		"""
	
		return _color(color)				
		
	def flip(self, x = True, y = False):
		
		"""<DOC>
		Flips the canvas along the x- and/ or y-axis. Note: This does not refresh the display,
		like e.g., pygame.display.flip(), which is handled by show().
		
		Keyword arguments:
		x -- A boolean indicating whether the canvas should be flipped horizontally (default = True)
		y -- A boolean indicating whether the canvas should be flipped vertically (default = False)
		</DOC>"""
		
		self.surface = pygame.transform.flip(self.surface, x, y)
				
	def copy(self, canvas):
	
		"""<DOC>
		Turn the current canvas into a copy of the passed canvas.
		
		Arguments:
		canvas -- The canvas to copy.
		</DOC>"""
		
		self.surface = canvas.surface.copy()
		
	def xcenter(self):
		
		"""<DOC>
		Returns:
		The center X coordinate in pixels.
		</DOC>"""
		
		return self.experiment.resolution[0] / 2
	
	def ycenter(self):
		
		"""<DOC>
		Returns:
		The center Y coordinate in pixels.
		</DOC>"""
		
		return self.experiment.resolution[1] / 2	
		
	def prepare(self):
	
		"""<DOC>
		Finishes up pending canvas operations (if any),
		so that a subsequent call to show() is extra fast.
		</DOC>"""
		
		pass
		
	def show(self):
		
		"""<DOC>
		Puts the canvas onto the screen.
		
		Returns:
		A timestamp containing the time at which the canvas actually appeared
		on the screen (or a best guess).
		</DOC>"""

		self.experiment.surface.blit(self.surface, (0, 0))		
		pygame.display.flip()
		return pygame.time.get_ticks()
		
	def clear(self, color = None):
		
		"""<DOC>
		Clears the canvas with the current background color.
		
		Keyword arguments:
		color -- A custom background color to be used. This does not affect the
				 default background color as set by set_bgcolor().
				 (Default = None)
		</DOC>"""
		
		if color != None:
			color = self.color(color)
		else:
			color = self.bgcolor
		
		self.surface.fill(color)
		
	def set_penwidth(self, penwidth):
		
		"""<DOC>
		Sets the pen width for subsequent drawing operations.
		
		Arguments:
		penwidth -- A pen width in pixels
		</DOC>"""
		
		self.penwidth = penwidth
		
	def set_fgcolor(self, color):
		
		"""<DOC>
		Sets the foreground color for subsequent drawing operations.
		
		Arguments:
		color -- A human readable color
		</DOC>"""
		
		self.fgcolor = self.color(color)		
		
	def set_bgcolor(self, color):
		
		"""<DOC>
		Sets the background color for subsequent drawing operations.
		
		Arguments:
		color -- A human readable color
		</DOC>"""

		self.bgcolor = self.color(color)	
		
	def set_font(self, style, size):
	
		"""<DOC>
		Sets the font for subsequent drawing operations.
		
		Arguments:
		style -- A font located in the resources folder (without the .ttf extension)
		size -- A font size in pixels		
		</DOC>"""
		
		self.font = pygame.font.Font(self.experiment.resource("%s.ttf" % style), size)
		
	def fixdot(self, x = None, y = None, color = None):
		
		"""<DOC>
		Draws a standard fixation dot, which is a big circle (r = 8px) with the
		foreground color and a smaller circle (r = 2px) of the background color.
		
		Keyword arguments:
		x -- The center X coordinate. None = center (default = None)
		y -- The center Y coordinate. None = center (default = None)
		color -- A custom human readable foreground color. This does not affect the
				 default foreground color as set by set_fgcolor(). (Default = None)
		</DOC>"""

		if color != None:
			color = self.color(color)
		else:
			color = self.fgcolor
		
		if x == None:
			x = self.xcenter()
			
		if y == None:
			y = self.ycenter()
					
		pygame.draw.circle(self.surface, color, (x, y), 8, 0)
		pygame.draw.circle(self.surface, self.bgcolor, (x, y), 2, 0)		
		
	def circle(self, x, y, r, fill = False, color = None):
		
		"""<DOC>
		Draws a circle.
		
		Arguments:
		x -- The center X coordinate
		y -- The center Y coordinate
		r -- The radius
		
		Keyword arguments:
		fill -- A boolean indicating whether the circle is outlined (False) or filled (True)
		color -- A custom human readable foreground color. This does not affect the
				 default foreground color as set by set_fgcolor(). (Default = None)
		</DOC>"""
						
		self.ellipse(x - r, y - r, 2 * r, 2 * r, fill = fill, color = color)

	def line(self, sx, sy, ex, ey, color = None):
		
		"""<DOC>
		Draws a line. Should accept parameters where sx > ex or sy > ey as well.
		
		Arguments:
		sx -- The left coordinate
		sy -- The top coordinate
		ex -- The right coordinate
		ey -- The bottom coordinate
		
		Keyword arguments:
		color -- A custom human readable foreground color. This does not affect the
				 default foreground color as set by set_fgcolor(). (Default = None)		
		</DOC>"""
		
		if color != None:
			color = self.color(color)
		else:
			color = self.fgcolor
				
		pygame.draw.line(self.surface, color, (sx, sy), (ex, ey), self.penwidth)
		
	def arrow(self, sx, sy, ex, ey, arrow_size = 5, color = None):
		
		"""<DOC>
		Draws an arrow. An arrow is a line, with an arrowhead at (ex, ey). The angle between
		the arrowhead lines and the arrow line is 45 degrees.
		
		Arguments:
		sx -- The left coordinate
		sy -- The top coordinate
		ex -- The right coordinate
		ey -- The bottom coordinate
		
		Keyword arguments:
		arrow_size -- The length of the arrowhead lines (default = 5)
		color -- A custom human readable foreground color. This does not affect the
				 default foreground color as set by set_fgcolor(). (Default = None)		
		</DOC>"""
		
		if color != None:
			color = self.color(color)
		else:
			color = self.fgcolor		
		
		pygame.draw.line(self.surface, color, (sx, sy), (ex, ey), self.penwidth)
		a = math.atan2(ey - sy, ex - sx)
		
		_sx = ex + arrow_size * math.cos(a + math.radians(135))
		_sy = ey + arrow_size * math.sin(a + math.radians(135))
		pygame.draw.line(self.surface, color, (_sx, _sy), (ex, ey), self.penwidth)		
		
		_sx = ex + arrow_size * math.cos(a + math.radians(225))
		_sy = ey + arrow_size * math.sin(a + math.radians(225))
		pygame.draw.line(self.surface, color, (_sx, _sy), (ex, ey), self.penwidth)		
		
	def rect(self, x, y, w, h, fill = False, color = None):
		
		"""<DOC>
		Draws a rectangle. Accepts parameters where w < 0 or h < 0 as well.
		
		Arguments:
		x -- The left X coordinate.
		y -- The top Y coordinate.
		w -- The width.
		h -- The height.
				
		Keyword arguments:
		fill -- A boolean indicating whether the rectangle is outlined (False) or filled (True)
		color -- A custom human readable foreground color. This does not affect the
				 default foreground color as set by set_fgcolor(). (Default = None)		
		</DOC>"""
		
		if color != None:
			color = self.color(color)
		else:
			color = self.fgcolor		
		
		if fill:
			pygame.draw.rect(self.surface, color, (x, y, w, h), 0)
		else:
			pygame.draw.rect(self.surface, color, (x, y, w, h), self.penwidth)
			
	def ellipse(self, x, y, w, h, fill = False, color = None):
		
		"""<DOC>
		Draws an ellipse. Accepts parameters where w < 0 or h < 0 as well.
		
		Arguments:
		x -- The left X coordinate.
		y -- The top Y coordinate.
		w -- The width.
		h -- The height.
				
		Keyword arguments:
		fill -- A boolean indicating whether the ellipse is outlined (False) or filled (True)
		color -- A custom human readable foreground color. This does not affect the
				 default foreground color as set by set_fgcolor(). (Default = None)		
		</DOC>"""
		
		if color != None:
			color = self.color(color)
		else:
			color = self.fgcolor
				
		x = int(x)
		y = int(y)
		w = int(w)
		h = int(h)
		
		if fill:
			pygame.draw.ellipse(self.surface, color, (x, y, w, h), 0)
		else:
			# Because the default way of drawing thick lines gives ugly results
			# for ellipses, we draw thick ellipses manually, by drawing an ellipse
			# with the background color inside of it
			i = self.penwidth / 2
			j = self.penwidth - i			
			pygame.draw.ellipse(self.surface, color, (x-i, y-i, w+2*i, h+2*i), 0)
			pygame.draw.ellipse(self.surface, self.bgcolor, (x+j, y+j, w-2*j, h-2*j), 0)			
			
	def text_size(self, text):
	
		"""<DOC>
		Determines the size of a text string in pixels.
		
		Arguments:
		text -- The text string
		
		Returns:
		A (width, height) tuple containing the dimensions of the text string
		</DOC>"""
		
		return self.font.size(text)				
		
	def text(self, text, center = True, x = None, y = None, color = None):
		
		"""<DOC>
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
		</DOC>"""
		
		if color != None:
			color = self.color(color)
		else:
			color = self.fgcolor		
			
		surface = self.font.render(text, self.antialias, color)
		size = self.font.size(text)
		
		if x == None:
			x = self.xcenter()
			
		if y == None:
			y = self.ycenter()
			
		if center:
			x -= size[0] / 2
			y -= size[1] / 2
			
		self.surface.blit(surface, (x, y))
		
	def textline(self, text, line, color = None):
		
		"""<DOC>
		A convenience function that draws a line of text based on a 
		line number. The text strings are centered on the X-axis and
		vertically spaced with 1.5 the line height as determined by
		text_size().
		
		Arguments:
		text -- The text string
		line -- A line number, where 0 is the center and > 0 is below the center.
		color -- A custom human readable foreground color. This does not affect the
				 default foreground color as set by set_fdcolor(). (Default = None)		
		</DOC>"""
		
		size = self.font.size(text)
		self.text(text, True, self.xcenter(), self.ycenter() + 1.5 * line * size[1], color = color)
		
	def image(self, fname, center = True, x = None, y = None, scale = None):
		
		"""<DOC>
		Draws an image from file. This function does not look in the file
		pool, but takes an absolute path.
		
		Arguments:
		fname -- The path of the file
		
		Keyword arguments:
		center -- A boolean indicating whether the given coordinates reflect the
				  center (True) or the top-left (False) of the image. (default = True)
		x -- The X coordinate. None = center. (default = None)
		y -- The Y coordinate. None = center. (default = None)
		scale -- The scaling factor of the image. 1.0 or None = no scaling, 2.0 = twice as large, etc. (default = None)
		</DOC>"""
		
		try:
			surface = pygame.image.load(fname)
		except pygame.error as e:
			raise openexp.exceptions.canvas_error("'%s' is not a supported image format" % fname)

		if scale != None:
			surface = pygame.transform.smoothscale(surface, (int(surface.get_width() * scale), int(surface.get_height() * scale)))

		size = surface.get_size()
		
		if x == None:
			x = self.xcenter()
			
		if y == None:
			y = self.ycenter()
			
		if center:
			x -= size[0] / 2
			y -= size[1] / 2
			
		self.surface.blit(surface, (x, y))
		
					
	def gabor(self, x, y, orient, freq, env = "gaussian", size = 96, stdev = 12, phase = 0, col1 = "white", col2 = "black", bgmode = "avg"):
	
		"""<DOC>
		Draws a Gabor patch. This function is derived from the online Gabor patch generator
		<http://www.cogsci.nl/software/online-gabor-patch-generator>	
		
		Arguments:
		x -- The center X coordinate
		y -- The center Y coordinate
		orient -- Orientation in degrees [0 .. 360]
		freq -- Frequency in cycles/px of the sinusoid
		
		Keyword arguments:	
		env -- Any of the following: "gaussian", "linear", "circular", "rectangle" (default = "gaussian")
		size -- Size in pixels (default = 96)
		stdev -- Standard deviation in pixels of the gaussian. Only applicable if env = "gaussian". (default = 12)
		phase -- Phase of the sinusoid [0.0 .. 1.0] (default = 0)
		col1: -- Human readable color for the tops (default = "white")
		col2 -- Human readable color for the troughs (default = "black")
		bgmode -- Specifies whether the background is the average of col1 and col2 (bgmode = "avg", a typical Gabor patch)
				  or equal to col2 ("col2"), useful for blending into the background. (default = "avg")
		</DOC>"""	
	
		surface = _gabor(orient, freq, env, size, stdev, phase, col1, col2, bgmode)
		self.surface.blit(surface, (x - 0.5 * size, y - 0.5 * size))
		
	def noise_patch(self, x, y, env = "gaussian", size = 96, stdev = 12, col1 = "white", col2 = "black", bgmode = "avg"):
	
		"""<DOC>
		Draws a patch of noise, with an envelope.
		
		Arguments:
		x -- The center X coordinate
		y -- The center Y coordinate
		
		Keyword arguments:	
		env -- Any of the following: "gaussian", "linear", "circular", "rectangle" (default = "gaussian")
		size -- Size in pixels (default = 96)
		stdev -- Standard deviation in pixels of the gaussian. Only applicable if env = "gaussian". (default = 12)
		phase -- Phase of the sinusoid [0.0 .. 1.0] (default = 0)
		col1: -- Human readable color for the tops (default = "white")
		col2 -- Human readable color for the troughs (default = "black")
		bgmode -- Specifies whether the background is the average of col1 and col2 (bgmode = "avg", a typical Gabor patch)
				  or equal to col2 ("col2"), useful for blending into the background. (default = "avg")
		</DOC>"""	
		
		surface = _noise_patch(env, size, stdev, col1, col2, bgmode)
		self.surface.blit(surface, (x - 0.5 * size, y - 0.5 * size))

"""
Static methods
"""

def init_display(experiment):

	"""
	Initialize the display before the experiment begins.
	
	Arguments:
	experiment -- An instance of libopensesame.experiment.experiment. The following properties are
				  of particular importance: experimnent.fullscreen (bool), experiment.width (int) and
				  experiment.height (int). The experiment also contains default font settings as
				  experriment.font_family (str) and experiment.font_size (int).
	"""
			
	# Intialize PyGame
	pygame.init()

	# Set the window icon
	surf = pygame.Surface( (32, 32) )
	surf.fill( (255, 255, 255) )
	pygame.draw.circle(surf, (0, 0, 255), (16, 16), 10, 4)
	pygame.display.set_icon(surf)
	
	# Determine the video mode
	mode = pygame.HWSURFACE | pygame.DOUBLEBUF
	if pygame.display.mode_ok(experiment.resolution, mode):	
		print "video.legacy.init_display(): video mode ok"
	else:
		print "video.legacy.init_display(): warning: video mode not ok"
		
	if experiment.fullscreen:
		mode = mode | pygame.FULLSCREEN
						
	# Create the window and the surface
	experiment.window = pygame.display.set_mode(experiment.resolution, mode)					
	pygame.display.set_caption(experiment.title)
	pygame.mouse.set_visible(False)
	experiment.surface = pygame.display.get_surface()

	# Create a font, falling back to the default font
	experiment.font = pygame.font.Font(experiment.resource("%s.ttf" % experiment.font_family), experiment.font_size)			
	if experiment.font == None:
		if experiment.debug:
			print "legacy.init_display(): '%s.ttf' not found, falling back to default font" % experiment.font_family
		experiment.font = pygame.font.Font(None, experiment.font_size)
		
	# Set the time function to use pygame
	experiment._time_func = pygame.time.get_ticks
		
def close_display(experiment):

	"""
	Close the display after the experiment is finished.
	
	Arguments:
	experiment -- An instance of libopensesame.experiment.experiment	
	"""
	
	pygame.display.quit()
	
"""
The functions below are specific to the legacy backend and do not have
to be implemented in other backends.
"""
	
canvas_cache = {}
				
def _color(color):

	"""
	See canvas.color()
	"""

	if type(color) == str:
		return pygame.Color(color)
	elif type(color) == int:
		pygame.Color(color, color, color, 255)
	elif type(color) == float:
		i = int(255 * color)
		pygame.Color(i, i, i, 255)
	elif type(color) == tuple:
		if len(color) == 3:
			return pygame.Color(color[0], color[1], color[2], 255)
		elif len(color) > 3:
			return pygame.Color(color[0], color[1], color[2], color[3])
		else:
			return pygame.Color("white")
	else:
		return pygame.Color("white")		
				
def _gabor(orient, freq, env = "gaussian", size = 96, stdev = 12, phase = 0, col1 = "white", col2 = "black", bgmode = "avg"):

	"""
	Returns a pygame surface containing a Gabor patch
	See canvas.gabor()
	"""
		
	# Generating a Gabor patch takes quite some time, so keep
	# a cache of previously generated Gabor patches to speed up
	# the process.
	global canvas_cache
	key = "gabor_%s_%s_%s_%s_%s_%s_%s_%s_%s" % (orient, freq, env, size, stdev, phase, col1, col2, bgmode)
	if key in canvas_cache:
		return canvas_cache[key]
		
	# Create a surface
	surface = pygame.Surface( (size, size) )
	px = pygame.PixelArray(surface)
	
	# Conver the orientation to radians
	orient = math.radians(orient)			
		
	col1 = _color(col1)
	col2 = _color(col2)
			
	# rx and ry reflect the real coordinates in the
	# target image
	for rx in range(size):
		for ry in range(size):
		
			# Distance from the center
			dx = rx - 0.5 * size 
			dy = ry - 0.5 * size
	
			# Get the coordinates (x, y) in the unrotated
			# Gabor patch
			t = math.atan2(dy, dx) + orient
			r = math.sqrt(dx ** 2 + dy ** 2)
			ux = r * math.cos(t)
			uy = r * math.sin(t)
			
			# Get the amplitude without the envelope (0 .. 1)
			amp = 0.5 + 0.5 * math.cos(2.0 * math.pi * (ux * freq + phase))
			
			# The envelope adjustment
			if env == "gaussian":
				f = math.exp(-0.5 * (ux / stdev) ** 2 - 0.5 * (uy / stdev) ** 2)
			elif env == "linear":
				f = max(0, (0.5 * size - r) / (0.5 * size))
			elif env == "circle":
				if (r > 0.5 * size):
					f = 0.0
				else:
					f = 1.0
			else:
				f = 1.0
				
			# Apply the envelope
			if bgmode == "avg":
				amp = amp * f + 0.5 * (1.0 - f)
			else:
				amp = amp * f
				
			r = col1.r * amp + col2.r * (1.0 - amp)
			g = col1.g * amp + col2.g * (1.0 - amp)
			b = col1.b * amp + col2.b * (1.0 - amp)
			
			px[rx][ry] = r, g, b
			
	canvas_cache[key] = surface
			
	del px
	return surface		
	
def _noise_patch(env = "gaussian", size = 96, stdev = 12, col1 = "white", col2 = "black", bgmode = "avg"):

	"""
	Returns a pygame surface containing a noise patch.
	See canvas.noise_patch()
	"""
	
	# Generating a noise patch takes quite some time, so keep
	# a cache of previously generated noise patches to speed up
	# the process.	
	global canvas_cache
	key = "noise_%s_%s_%s_%s_%s_%s" % (env, size, stdev, col1, col2, bgmode)
	if key in canvas_cache:
		return canvas_cache[key]	
	
	# Create a surface
	surface = pygame.Surface( (size, size) )
	px = pygame.PixelArray(surface)
		
	col1 = _color(col1)
	col2 = _color(col2)
			
	# rx and ry reflect the real coordinates in the
	# target image
	for rx in range(size):
		for ry in range(size):
		
			# Distance from the center
			ux = rx - 0.5 * size 
			uy = ry - 0.5 * size
			r = math.sqrt(ux ** 2 + uy ** 2)			
				
			# Get the amplitude without the envelope (0 .. 1)
			amp = random.random()
			
			# The envelope adjustment
			if env == "gaussian":
				f = math.exp(-0.5 * (ux / stdev) ** 2 - 0.5 * (uy / stdev) ** 2)
			elif env == "linear":
				f = max(0, (0.5 * size - r) / (0.5 * size))
			elif env == "circle":
				if (r > 0.5 * size):
					f = 0.0
				else:
					f = 1.0
			else:
				f = 1.0
				
			# Apply the envelope
			if bgmode == "avg":
				amp = amp * f + 0.5 * (1.0 - f)
			else:
				amp = amp * f
				
			r = col1.r * amp + col2.r * (1.0 - amp)
			g = col1.g * amp + col2.g * (1.0 - amp)
			b = col1.b * amp + col2.b * (1.0 - amp)
			
			px[rx][ry] = r, g, b
			
	canvas_cache[key] = surface
			
	del px
	return surface

