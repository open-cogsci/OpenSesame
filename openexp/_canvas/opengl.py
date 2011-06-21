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
import openexp._canvas.legacy
import openexp.exceptions
import math
import subprocess
import os
import os.path
import tempfile

import libopengl

class opengl(openexp._canvas.legacy.legacy):

	def __init__(self, experiment, bgcolor = None, fgcolor = None):

		"""
		Initializes the canvas
		"""

		self.experiment = experiment
		
		if fgcolor == None:
			fgcolor = self.experiment.get("foreground")
		if bgcolor == None:
			bgcolor = self.experiment.get("background")	
			
		self.fgcolor = self.color(fgcolor)
		self.bgcolor = self.color(bgcolor)
		self.penwidth = 1
		self.antialias = True
		self.font = self.experiment.font

		# set to have no objects
		self.showables = []
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

		return openexp._canvas.legacy._color(color)

	def flip(self, x = True, y = False):

		"""
		Flips the canvas along the x- or y-axis
		"""

		#self.surface = pygame.transform.flip(self.surface, x, y)
		# will have to flip each object and adjust it's location accordingly
		pass

	def copy(self, canvas):

		"""
		Copies the contents of another canvas
		"""
		# PBS: do we need a deep copy here
		self.showables = [s.copy() for s in canvas.showables]

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

		for s,loc in self.showables:
			s.show(loc[0],loc[1])
		libopengl.doBlockingFlip()
		return pygame.time.get_ticks()

	def clear(self, color = None):

		"""
		Clears the canvas
		"""
		if color is None:
			color = self.bgcolor
		else:
			color = self.color(color)

		# clear the showable list
		self.showables = []
		surface = pygame.Surface(self.experiment.resolution)
		surface.fill(color)
		self.showables.append((libopengl.LowImage(surface), (0,0)))

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

	def fixdot(self, x = None, y = None):

		"""
		Draws a fixation dot
		"""

		if x == None:
			x = self.xcenter()

		if y == None:
			y = self.ycenter()

		r1 = 8
		r2 = 2
		surface = pygame.Surface((r1*2,r1*2), SRCALPHA)

		pygame.draw.circle(surface, self.fgcolor, (r1, r1), r1, 0)
		pygame.draw.circle(surface, self.bgcolor, (r1, r1), r2, 0)

		self.showables.append((libopengl.LowImage(surface),
				       (x-r1,y-r1)))

	def circle(self, x, y, r, fill = False):

		"""
		Draws a circle
		"""

		self.ellipse(x - r, y - r, 2 * r, 2 * r, fill)

	def line(self, sx, sy, ex, ey):

		"""
		Draws a line
		"""
		dy = abs(ey - sy) + 2*self.penwidth + 1
		dx = abs(ex - sx) + 2*self.penwidth + 1
		surface = pygame.Surface((dx,dy), SRCALPHA)

		if sx < ex:
			s_sx = self.penwidth
			s_ex = dx - self.penwidth - 1
		else:
			s_sx = dx - self.penwidth - 1
			s_ex = self.penwidth
		if sy < ey:
			s_sy = self.penwidth
			s_ey = dy - self.penwidth - 1
		else:
			s_sy = dy - self.penwidth - 1
			s_ey = self.penwidth

		pygame.draw.line(surface, self.fgcolor,
				 (s_sx, s_sy), (s_ex, s_ey),
				 self.penwidth)

		self.showables.append((libopengl.LowImage(surface,interpolate=False),
				       (min(sx,ex)-self.penwidth,
					min(sy,ey)-self.penwidth)))

	def arrow(self, sx, sy, ex, ey, arrow_size = 5):

		"""
		Draws an arrow
		"""

		dy = abs(ey - sy) + 2*arrow_size
		dx = abs(ex - sx) + 2*arrow_size
		surface = pygame.Surface((dx,dy), SRCALPHA)

		if sx < ex:
			s_sx = arrow_size
			s_ex = dx - arrow_size
		else:
			s_sx = dx - arrow_size
			s_ex = arrow_size
		if sy < ey:
			s_sy = arrow_size
			s_ey = dy - arrow_size
		else:
			s_sy = dy - arrow_size
			s_ey = arrow_size

		pygame.draw.line(surface, self.fgcolor,
				 (s_sx, s_sy), (s_ex, s_ey),
				 self.penwidth)

		a = math.atan2(s_ey - s_sy, s_ex - s_sx)

		_sx = s_ex + arrow_size * math.cos(a + math.radians(135))
		_sy = s_ey + arrow_size * math.sin(a + math.radians(135))
		pygame.draw.line(surface, self.fgcolor,
				 (_sx, _sy), (s_ex, s_ey), self.penwidth)

		_sx = s_ex + arrow_size * math.cos(a + math.radians(225))
		_sy = s_ey + arrow_size * math.sin(a + math.radians(225))
		pygame.draw.line(surface, self.fgcolor,
				 (_sx, _sy), (s_ex, s_ey), self.penwidth)

		self.showables.append((libopengl.LowImage(surface),
				       (min(sx,ex)+arrow_size,
					min(sy,ey)+arrow_size)))

	def rect(self, x, y, w, h, fill = False):

		"""
		Draws a rectangle
		"""
		if fill:
			surface = pygame.Surface((w,h), SRCALPHA)
			pygame.draw.rect(surface, self.fgcolor, (0, 0, w, h), 0)
			loc = (x,y)
		else:
			surface = pygame.Surface((w+2*self.penwidth,h+2*self.penwidth),
						 SRCALPHA)
			pygame.draw.rect(surface, self.fgcolor,
					 (self.penwidth, self.penwidth, w, h), self.penwidth)
			loc = (x-self.penwidth,y-self.penwidth)

		self.showables.append((libopengl.LowImage(surface),
				       loc))

	def ellipse(self, x, y, w, h, fill = False):

		"""
		Draws an ellipse
		"""

		x = int(x)
		y = int(y)
		w = int(w)
		h = int(h)

		if fill:
			surface = pygame.Surface((w,h), SRCALPHA)
			pygame.draw.ellipse(surface, self.fgcolor, (0, 0, w, h), 0)
			loc = (x,y)
		else:
			# Because the default way of drawing thick lines gives ugly results
			# for ellipses, we draw thick circles manually
			i = self.penwidth / 2.
			j = self.penwidth - i

			fgrect = (self.penwidth-i, self.penwidth-i,
				  self.penwidth+w+2*i, self.penwidth+h+2*i)
			bgrect = (self.penwidth+j, self.penwidth+j,
				  self.penwidth+w-2*j, self.penwidth+h-2*j)
			loc = (x-self.penwidth-i,y-self.penwidth-j)
			surface = pygame.Surface((w+2*self.penwidth+2,
						  h+2*self.penwidth+2),
						 SRCALPHA)
			pygame.draw.ellipse(surface, self.fgcolor,
					    fgrect, 0)
			pygame.draw.ellipse(surface, self.bgcolor,
					    bgrect, 0)

		self.showables.append((libopengl.LowImage(surface),
				       loc))

	def text_size(self, text):

		"""
		Returns the size of a string of text in
		pixels as a (w, h) tuple
		"""

		return self.font.size(text)

	def text(self, text, center = True, x = None, y = None):

		"""
		Draws text
		"""

		surface = self.font.render(text, self.antialias, self.fgcolor)
		size = self.font.size(text)

		if x == None:
			x = self.xcenter()

		if y == None:
			y = self.ycenter()

		if center:
			x -= size[0] / 2
			y -= size[1] / 2

		self.showables.append((libopengl.LowImage(surface),
				       (x,y)))

	def textline(self, text, line):

		"""
		Draws text. The position is specified by line, where
		0 is the central line, < 0 is above and > 0 is below.
		"""

		size = self.font.size(text)
		self.text(text, True, self.xcenter(), self.ycenter() + 1.5 * line * size[1])

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

		self.showables.append((libopengl.LowImage(surface),
				       (x,y)))


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

		surface = openexp._canvas.legacy._gabor(orient, freq, env, size, stdev, phase, col1, col2, bgmode)
		self.showables.append((libopengl.LowImage(surface),
				       (x - 0.5 * size, y - 0.5 * size)))

	def noise_patch(self, x, y, env = "gaussian", size = 96, stdev = 12, col1 = "white", col2 = "black", bgmode = "avg"):

		"""
		Draws a patch of noise, with an envelope applied over it.
		"""

		surface = openexp._canvas.legacy._noise_patch(env, size, stdev, col1, col2, bgmode)
		self.showables.append((libopengl.LowImage(surface),
				       (x - 0.5 * size, y - 0.5 * size)))

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
	mode = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.OPENGL
	if experiment.fullscreen:
		mode = mode | pygame.FULLSCREEN
	if pygame.display.mode_ok(experiment.resolution, mode):
		print "video.opengl.init_display(): video mode ok"
	else:
		print "video.opengl.init_display(): warning: video mode not ok"

	# Set the sync to VBL

	# PBS: Currently only for linux, must add in for OSX, but that
	# takes Objective C code.

	# Set for nVidia linux
	val = "1"
	os.environ["__GL_SYNC_TO_VBLANK"] = val
	# Set for recent linux Mesa DRI Radeon
	os.environ["LIBGL_SYNC_REFRESH"] = val

	# Create the window and the surface
	experiment.window = pygame.display.set_mode(experiment.resolution, mode)
	pygame.display.set_caption(experiment.title)
	pygame.mouse.set_visible(False)
	experiment.surface = pygame.display.get_surface()

	# Set the time function to use pygame
	experiment._time_func = pygame.time.get_ticks

	# Create a font, falling back to the default font
	experiment.font = pygame.font.Font(experiment.resource("%s.ttf" % experiment.font_family), experiment.font_size)
	if experiment.font == None:
		experiment.font = pygame.font.Font(None, experiment.font_size)

def close_display(experiment):

	"""
	Close the display
	"""

	pygame.display.quit()

