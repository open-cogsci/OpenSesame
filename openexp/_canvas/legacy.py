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

import pygame
from pygame.locals import *
import os
from libopensesame.exceptions import osexception
from libopensesame import debug, html, misc
from openexp._canvas import canvas

class legacy(canvas.canvas):

	"""
	desc:
		Legacy canvas back-end.
	"""

	# The settings variable is used by the GUI to provide a list of back-end
	# settings
	settings = {
		u"pygame_hwsurface" : {
			u"name" : u"Hardware surface",
			u"description" : u"Create a hardware surface",
			u"default" : u"yes"
			},
		u"pygame_doublebuf" : {
			u"name" : u"Double buffering",
			u"description" : u"Use double buffering",
			u"default" : u"yes"
			},
		u"pygame_window_frame" : {
			u"name" : u"Draw window frame",
			u"description" : u"Draw a frame in window mode",
			u"default" : u"yes",
			},
		u"pygame_window_pos" : {
			u"name" : u"Window position",
			u"description" : u"Window position in window mode (format: 'x,y' or 'auto')",
			u"default" : u"auto",
			}
		}

	def __init__(self, experiment, bgcolor=None, fgcolor=None,
		auto_prepare=True):

		self.experiment = experiment
		self.html = html.html()
		if fgcolor == None:
			fgcolor = self.experiment.get(u"foreground")
		if bgcolor == None:
			bgcolor = self.experiment.get(u"background")
		self.set_fgcolor(fgcolor)
		self.set_bgcolor(bgcolor)
		self.penwidth = 1
		self.antialias = True
		self.surface = self.experiment.surface.copy()
		self._current_font = None
		self.bidi = self.experiment.get(u'bidi')==u'yes'
		self.set_font(style=self.experiment.font_family, size= \
			self.experiment.font_size, bold=self.experiment.font_bold==u'yes', \
			italic=self.experiment.font_italic==u'yes', underline= \
			self.experiment.font_underline==u'yes')
		self.clear()

	def color(self, color):

		return canvas._color(color)

	def _font(self):

		"""
		desc:
			Creates a PyGame font instance based on the current font settings.

		returns:
			A PyGame font.
		"""

		if self._current_font == None:
			# First see if the font refers to a file in the resources/ filepool
			try:
				font_path = self.experiment.resource(u'%s.ttf' % \
					self.font_style)
				self._current_font = pygame.font.Font(font_path, self.font_size)
			# If not, try to match a system font
			except:
				self._current_font = pygame.font.SysFont(self.font_style, \
					self.font_size)
			self._current_font.set_bold(self.font_bold)
			self._current_font.set_italic(self.font_italic)
			self._current_font.set_underline(self.font_underline)
		return self._current_font

	def copy(self, canvas):

		self.surface = canvas.surface.copy()
		self.font_style = canvas.font_style
		self.font_style = canvas.font_style
		self.penwidth = canvas.penwidth
		self.fgcolor = canvas.fgcolor
		self.bgcolor = canvas.bgcolor

	def show(self):

		self.experiment.surface.blit(self.surface, (0, 0))
		self.experiment.last_shown_canvas = self.surface
		pygame.display.flip()
		return pygame.time.get_ticks()


	def clear(self, color=None):

		if color != None:
			color = self.color(color)
		else:
			color = self.bgcolor
		self.surface.fill(color)

	def set_font(self, style=None, size=None, italic=None, bold=None,
		underline=None):

		self._current_font = None
		super(legacy, self).set_font(style=style, size=size, italic=italic,
			bold=bold, underline=underline)

	def line(self, sx, sy, ex, ey, color=None, penwidth=None):

		if color != None:
			color = self.color(color)
		else:
			color = self.fgcolor
		if penwidth == None:
			penwidth = self.penwidth
		pygame.draw.line(self.surface, color, (sx, sy), (ex, ey), penwidth)

	def rect(self, x, y, w, h, fill=False, color=None, penwidth=None):

		if color != None:
			color = self.color(color)
		else:
			color = self.fgcolor
		if penwidth == None:
			penwidth = self.penwidth
		if fill:
			pygame.draw.rect(self.surface, color, (x, y, w, h), 0)
		else:
			pygame.draw.rect(self.surface, color, (x, y, w, h), penwidth)

	def ellipse(self, x, y, w, h, fill=False, color=None, penwidth=None):

		if color != None:
			color = self.color(color)
		else:
			color = self.fgcolor
		if penwidth == None:
			penwidth = self.penwidth
		x = int(x)
		y = int(y)
		w = int(w)
		h = int(h)
		if fill:
			pygame.draw.ellipse(self.surface, color, (x, y, w, h), 0)
		else:
			# Because the default way of drawing thick lines gives ugly results
			# for ellipses, we draw thick ellipses manually, by drawing an
			# ellipse with the background color inside of it
			i = penwidth / 2
			j = penwidth - i
			pygame.draw.ellipse(self.surface, color, (x-i, y-i, w+2*i, h+2*i),
				0)
			pygame.draw.ellipse(self.surface, self.bgcolor, (x+j, y+j, w-2*j,
				h-2*j), 0)

	def polygon(self, vertices, fill=False, color=None, penwidth=None):

		if color != None:
			color = self.color(color)
		else:
			color = self.fgcolor
		if penwidth == None:
			penwidth = self.penwidth
		if fill:
			width = 0
		else:
			width = penwidth
		pygame.draw.polygon(self.surface, color, vertices, width)

	def _text(self, text, x, y):

		font = self._font()
		surface = font.render(text, self.antialias, self.fgcolor)
		self.surface.blit(surface, (x, y))

	def _text_size(self, text):

		return self._font().size(text)

	def image(self, fname, center=True, x=None, y=None, scale=None):

		if isinstance(fname, unicode):
			_fname = fname.encode(self.experiment.encoding)
		else:
			_fname = fname
		try:
			surface = pygame.image.load(_fname)
		except pygame.error as e:
			raise osexception(
				u"'%s' is not a supported image format" % fname)
		if scale != None:
			try:
				surface = pygame.transform.smoothscale(surface,
					(int(surface.get_width()*scale),
					int(surface.get_height()*scale)))
			except:
				debug.msg(u"smooth scaling failed for '%s'" % fname,
					reason=u"warning")
				surface = pygame.transform.scale(surface,
					(int(surface.get_width()*scale),
					int(surface.get_height()*scale)))
		size = surface.get_size()
		if x == None:
			x = self.xcenter()
		if y == None:
			y = self.ycenter()
		if center:
			x -= size[0] / 2
			y -= size[1] / 2
		self.surface.blit(surface, (x, y))

	def gabor(self, x, y, orient, freq, env=u"gaussian", size=96, stdev=12,
		phase=0, col1=u"white", col2=u"black", bgmode=u"avg"):

		surface = canvas._gabor(orient, freq, env, size, stdev, phase, col1,
			col2, bgmode)
		self.surface.blit(surface, (x - 0.5 * size, y - 0.5 * size))

	def noise_patch(self, x, y, env=u"gaussian", size=96, stdev=12,
		col1=u"white", col2=u"black", bgmode=u"avg"):

		surface = canvas._noise_patch(env, size, stdev, col1, col2, bgmode)
		self.surface.blit(surface, (x - 0.5 * size, y - 0.5 * size))

def init_display(experiment):

	# Intialize PyGame
	pygame.init()

	# Set the window icon
	surf = pygame.Surface( (32, 32) )
	surf.fill( (255, 255, 255) )
	pygame.draw.circle(surf, (0, 0, 255), (16, 16), 10, 4)
	pygame.display.set_icon(surf)

	# Determine the video mode
	mode = 0
	if experiment.get_check(u"pygame_hwsurface", u"yes",
		[u"yes", u"no"]) == u"yes":
		mode = mode | pygame.HWSURFACE
		print(
			u"openexp._canvas.legacy.init_display(): enabling hardware surface")
	else:
		print(
			u"openexp._canvas.legacy.init_display(): not enabling hardware surface")

	if experiment.get_check(u"pygame_doublebuf", u"yes",
		[u"yes", u"no"]) == u"yes":
		mode = mode | pygame.DOUBLEBUF
		print(
			u"openexp._canvas.legacy.init_display(): enabling double buffering")
	else:
		print(
			u"openexp._canvas.legacy.init_display(): not enabling double buffering")

	if pygame.display.mode_ok(experiment.resolution(), mode):
		print(u"openexp._canvas.legacy.init_display(): video mode ok")
	else:
		print(
			u"openexp._canvas.legacy.init_display(): warning: video mode not ok")

	if experiment.fullscreen:
		mode = mode | pygame.FULLSCREEN

	if experiment.get_check(u'pygame_window_frame', u'yes', [u'yes', u'no']) \
		== u'no':
		mode = mode | pygame.NOFRAME

	if experiment.get_check(u'pygame_window_pos', u'auto') != u'auto':
		os.environ[u'SDL_VIDEO_WINDOW_POS'] = experiment.get(
			u'pygame_window_pos')

	# Create the window and the surface
	experiment.window = pygame.display.set_mode(experiment.resolution(), mode)
	pygame.display.set_caption(u'OpenSesame (legacy backend)')
	pygame.mouse.set_visible(False)
	experiment.surface = pygame.display.get_surface()

	# Create a font, falling back to the default font
	experiment.font = pygame.font.Font(experiment.resource(
		u"%s.ttf" % experiment.font_family), experiment.font_size)
	if experiment.font == None:
		debug.msg(u"'%s.ttf' not found, falling back to default font" \
			% experiment.font_family)
		experiment.font = pygame.font.Font(None, experiment.font_size)

	# Set the time functions to use pygame
	experiment._time_func = pygame.time.get_ticks
	experiment._sleep_func = pygame.time.delay
	experiment.time = experiment._time_func
	experiment.sleep = experiment._sleep_func

def close_display(experiment):

	pygame.display.quit()
