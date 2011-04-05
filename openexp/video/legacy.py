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

class legacy(openexp.canvas.canvas):
	
	def __init__(self, experiment, bgcolor = "black", fgcolor = "white"):
		
		"""
		Initializes the canvas
		"""
		
		self.experiment = experiment
		self.fgcolor = self.color(fgcolor)
		self.bgcolor = self.color(bgcolor)
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
		
		"""
		Flips the canvas along the x- or y-axis
		"""
		
		self.surface = pygame.transform.flip(self.surface, x, y)
		
		
	def copy(self, canvas):
	
		"""
		Copies the contents of another canvas
		"""
		
		self.surface = canvas.surface.copy()
		
	def xcenter(self):
		
		"""
		Returns the center X coordinate of the canvas
		"""
		
		return self.experiment.resolution[0] / 2
	
	def ycenter(self):
		
		"""
		Returns the center Y coordinate of the canvas
		"""
		
		return self.experiment.resolution[1] / 2	
		
	def show(self):
		
		"""
		Shows the canvas and returns the time at
		which the display whas shown. Waits for
		v-sync if enabled.		
		"""

		self.experiment.surface.blit(self.surface, (0, 0))		
		pygame.display.flip()
		return pygame.time.get_ticks()
		
	def clear(self, color = None):
		
		"""
		Clears the canvas
		"""
		
		if color != None:
			color = self.color(color)
		else:
			color = self.bgcolor
		
		self.surface.fill(color)
		
	def set_penwidth(self, penwidth):
		
		"""
		Sets the pen width
		"""
		
		self.penwidth = penwidth
		
	def set_fgcolor(self, color):
		
		"""
		Sets the foreground color
		"""
		
		self.fgcolor = self.color(color)		
		
	def set_bgcolor(self, color):
		
		"""
		Sets the background color
		"""

		self.bgcolor = self.color(color)	
		
	def set_font(self, style, size):
	
		"""
		Sets the font style and size. OpenExp searches
		for a [style].ttf font in the resources folder. 		
		Possible styles are
		sans
		serif
		mono
		"""
		
		self.font = pygame.font.Font(self.experiment.resource("%s.ttf" % style), size)
		
	def fixdot(self, x = None, y = None, color = None):
		
		"""
		Draws a fixation dot
		"""

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
		
		"""
		Draws a circle
		"""
						
		self.ellipse(x - r, y - r, 2 * r, 2 * r, fill = fill, color = color)

	def line(self, sx, sy, ex, ey, color = None):
		
		"""
		Draws a line
		"""
		
		if color != None:
			color = self.color(color)
		else:
			color = self.fgcolor
				
		pygame.draw.line(self.surface, color, (sx, sy), (ex, ey), self.penwidth)
		
	def arrow(self, sx, sy, ex, ey, arrow_size = 5, color = None):
		
		"""
		Draws an arrow
		"""
		
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
		
		"""
		Draws a rectangle
		"""
		
		if color != None:
			color = self.color(color)
		else:
			color = self.fgcolor		
		
		if fill:
			pygame.draw.rect(self.surface, color, (x, y, w, h), 0)
		else:
			pygame.draw.rect(self.surface, color, (x, y, w, h), self.penwidth)
			
	def ellipse(self, x, y, w, h, fill = False, color = None):
		
		"""
		Draws an ellipse
		"""
		
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
	
		"""
		Returns the size of a string of text in
		pixels as a (w, h) tuple
		"""
		
		return self.font.size(text)				
		
	def text(self, text, center = True, x = None, y = None, color = None):
		
		"""
		Draws text
		"""
		
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
		
		"""
		Draws text. The position is specified by line, where
		0 is the central line, < 0 is above and > 0 is below.
		"""
		
		size = self.font.size(text)
		self.text(text, True, self.xcenter(), self.ycenter() + 1.5 * line * size[1], color = color)
		
	def image(self, fname, center = True, x = None, y = None, scale = None):
		
		"""
		Draws an image from file
		"""
		
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
	
		"""
		Draws a Gabor patch. This function is derived from the online Gabor patch generator
		<http://www.cogsci.nl/software/online-gabor-patch-generator>	
	
		orient: orientation in degrees [0 .. 360]
		freq: frequency in cycles/px
		env: envelope (gaussian/ linear/ circular/ rectangle)
		size: size in px
		stdev: standard deviation of the gaussian (only applicable if env == gaussian)
		phase: phase [0 .. 1]
		col1: color of tops
		col2: color of troughs
		bgmode: color of the background (avg/ col2)
		"""	
	
		surface = _gabor(orient, freq, env, size, stdev, phase, col1, col2, bgmode)
		self.surface.blit(surface, (x - 0.5 * size, y - 0.5 * size))
		
	def noise_patch(self, x, y, env = "gaussian", size = 96, stdev = 12, col1 = "white", col2 = "black", bgmode = "avg"):
	
		"""
		Draws a patch of noise, with an envelope applied over it.
		"""
		
		surface = _noise_patch(env, size, stdev, col1, col2, bgmode)
		self.surface.blit(surface, (x - 0.5 * size, y - 0.5 * size))

"""
Static methods
"""

canvas_cache = {}

def init_display(experiment):

	"""
	Initializes the display
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
						
	# Create the window and the surface
	experiment.window = pygame.display.set_mode(experiment.resolution, mode)					
	pygame.display.set_caption(experiment.title)
	pygame.mouse.set_visible(False)
	experiment.surface = pygame.display.get_surface()

	# Create a font, falling back to the default font
	experiment.font = pygame.font.Font(experiment.resource("%s.ttf" % experiment.font_family), experiment.font_size)			
	if experiment.font == None:
		experiment.font = pygame.font.Font(None, experiment.font_size)
		
def close_display(experiment):

	"""
	Close the display
	"""
	
	pygame.display.quit()
				
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

def gabor_file(orient, freq, env = "gaussian", size = 96, stdev = 12, phase = 0, col1 = "white", col2 = "black", bgmode = "avg"):

	"""
	Creates a temporary file containing a Gabor patch.
	See canvas.gabor()
	"""
	
	surface = _gabor(orient, freq, env, size, stdev, phase, col1, col2, bgmode)
	
	tmp = tempfile.mkstemp(suffix = ".png")	[1]
	pygame.image.save(surface, tmp)
	openexp.canvas.temp_files.append(tmp)
	
	return tmp
	
def noise_file(env = "gaussian", size = 96, stdev = 12, col1 = "white", col2 = "black", bgmode = "avg"):

	"""
	Creates a temporary file containing a noise patch.
	See canvas.noise_patch()
	"""
	
	surface = _noise_patch(env, size, stdev, col1, col2, bgmode)
	
	tmp = tempfile.mkstemp(suffix = ".png")	[1]
	pygame.image.save(surface, tmp)
	openexp.canvas.temp_files.append(tmp)
	
	return tmp
	
