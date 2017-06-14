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
from pygame.locals import *
import os
import pygame
import platform
from libopensesame.exceptions import osexception
from libopensesame import debug
from openexp.backend import configurable
from openexp._canvas import canvas
from openexp._coordinates.legacy import legacy as legacy_coordinates

# PyGame 1.9.2 suffers from character encoding issues. To get around those, we
# pass file objects directly to PyGame, instead of paths. These file objects
# need to remain open in the case of fonts, otherwise the associated font object
# won't work anymore. So here we keep a list of all open file objects, which are
# closed when the display is closed. In addition, we keep track of font objects
# so that we don't repeatedly initialize the same font.
#
# A bug report regarding character encoding is here:
# - https://bitbucket.org/pygame/pygame/issues/196/\
#   font-file-name-containing-unicode-error
fileobjects = []
fonts = {}

class legacy(canvas.canvas, legacy_coordinates):

	"""
	desc:
		This is a canvas backend built on top of PyGame.
		For function specifications and docstrings, see
		`openexp._canvas.canvas`.
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

	def __init__(self, experiment, auto_prepare=True, **style_args):

		canvas.canvas.__init__(self, experiment, auto_prepare=auto_prepare,
			**style_args)
		legacy_coordinates.__init__(self)
		self.antialias = True
		self.surface = self.experiment.surface.copy()
		self.clear()
		if platform.system() == u'Darwin':
			self.show = self._show_macos

	def set_config(self, **cfg):

		canvas.canvas.set_config(self, **cfg)
		for key, val in cfg.items():
			if u'font_' in key:
				self._font = None
		if self._font is None:
			# First see if the font refers to a file in the resources/ filepool
			self._font = self._pygame_font(self.experiment, self.font_family,
				self.font_size)
			self._font.set_bold(self.font_bold)
			self._font.set_italic(self.font_italic)
			self._font.set_underline(self.font_underline)

	def copy(self, canvas):

		self.surface = canvas.surface.copy()
		self.set_config(**canvas.get_config())

	def show(self):

		self.experiment.surface.blit(self.surface, (0, 0))
		self.experiment.last_shown_canvas = self.surface
		pygame.display.flip()
		return pygame.time.get_ticks()
		
	def _show_macos(self):
		
		"""
		visible: False
		
		desc:
			On Mac OS, the display is sometimes not refreshed unless there is
			some interaction with the event loop. Therefor we implement this
			hack which is only used on Mac OS.
		"""

		self.experiment.surface.blit(self.surface, (0, 0))
		self.experiment.last_shown_canvas = self.surface
		pygame.display.flip()
		pygame.event.pump()
		return pygame.time.get_ticks()
		
	@configurable
	def clear(self):

		self.surface.fill(self.background_color.backend_color)

	@configurable
	def line(self, sx, sy, ex, ey):

		sx, sy = self.to_xy(sx, sy)
		ex, ey = self.to_xy(ex, ey)
		pygame.draw.line(self.surface, self.color.backend_color, (sx, sy),
			(ex, ey), self.penwidth)

	@configurable
	def rect(self, x, y, w, h):

		x, y = self.to_xy(x, y)
		if self.fill:
			pygame.draw.rect(self.surface, self.color.backend_color,
				(x, y, w, h), 0)
		else:
			pygame.draw.rect(self.surface, self.color.backend_color,
				(x, y, w, h), self.penwidth)

	@configurable
	def ellipse(self, x, y, w, h):

		x = int(x)
		y = int(y)
		w = int(w)
		h = int(h)
		x, y = self.to_xy(x, y)
		if self.fill:
			pygame.draw.ellipse(self.surface, self.color.backend_color,
				(x, y, w, h), 0)
		else:
			# Use experyiment's method to draw ellipses with a transparent
			# interior by using the transparent colorkey method. This involves
			# some trickery by making a separate surface of which a certain color
			# is designated as transparent and draw the ellipse on there first. 
			# When being blit onto another surface, this transparent color 
			# (e.g. the ellipses interior is not blitted with the rest.
			line_width = self.penwidth
			size = (w, h)
			
			surface = pygame.surface.Surface(
				[p + line_width for p in size],
				pygame.SRCALPHA).convert_alpha()
			
			pygame.draw.ellipse(surface, (0, 0, 0), pygame.Rect(
				(0, 0),
				[p + line_width for p in size]))
			
			tmp = pygame.surface.Surface(
				[p - line_width for p in size])
			tmp.fill([0, 0, 0])
			tmp.set_colorkey([255, 255, 255])

			hole = pygame.surface.Surface(
				[p - line_width for p in size],
				pygame.SRCALPHA).convert_alpha()
			
			pygame.draw.ellipse(tmp, (255, 255, 255), pygame.Rect(
				    (0, 0), [p - line_width for p in size]))
			hole.blit(tmp, (0, 0))
			surface.blit(hole, (line_width, line_width),
				special_flags=pygame.BLEND_RGBA_MIN)
			surface.fill(self.color.backend_color,
				special_flags=pygame.BLEND_RGB_MAX)
			# The line_width affects the temp's surface size, so use it to correct the
			# positioning when blitting.
			self.surface.blit(surface, (x-line_width/2, y-line_width/2) )

	@configurable
	def polygon(self, vertices):

		vertices = [self.to_xy(x, y) for x, y in vertices]
		if self.fill:
			penwidth = 0
		else:
			penwidth = self.penwidth
		pygame.draw.polygon(self.surface, self.color.backend_color, vertices,
			penwidth)

	def _text(self, text, x, y):

		surface = self._font.render(text, self.antialias,
			self.color.backend_color)
		x, y = self.to_xy(x, y)
		self.surface.blit(surface, (x, y))

	def _text_size(self, text):

		return self._font.size(text)

	def image(self, fname, center=True, x=None, y=None, scale=None):

		fname = safe_decode(fname)
		if not os.path.isfile(fname):
			raise osexception(u'"%s" does not exist' % fname)
		with open(fname, u'rb') as fd:
			try:
				surface = pygame.image.load(fd)
			except pygame.error:
				raise osexception(
					u"'%s' is not a supported image format" % fname)
		if scale is not None:
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
		x, y = self.to_xy(x, y)
		if center:
			x -= size[0] / 2
			y -= size[1] / 2
		self.surface.blit(surface, (x, y))

	def gabor(self, x, y, orient, freq, env=u"gaussian", size=96, stdev=12,
		phase=0, col1=u"white", col2=u"black", bgmode=u"avg"):

		surface = canvas._gabor(orient, freq, env, size, stdev, phase, col1,
			col2, bgmode)
		x, y = self.to_xy(x, y)
		self.surface.blit(surface, (x - 0.5 * size, y - 0.5 * size))

	def noise_patch(self, x, y, env=u"gaussian", size=96, stdev=12,
		col1=u"white", col2=u"black", bgmode=u"avg"):

		surface = canvas._noise_patch(env, size, stdev, col1, col2, bgmode)
		x, y = self.to_xy(x, y)
		self.surface.blit(surface, (x - 0.5 * size, y - 0.5 * size))

	@staticmethod
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
		if experiment.var.get(u"pygame_hwsurface", u"yes",
			[u"yes", u"no"]) == u"yes":
			mode = mode | pygame.HWSURFACE
			print(
				u"openexp._canvas.legacy.init_display(): enabling hardware surface")
		else:
			print(
				u"openexp._canvas.legacy.init_display(): not enabling hardware surface")

		if experiment.var.get(u"pygame_doublebuf", u"yes",
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

		if experiment.var.fullscreen == u'yes':
			mode = mode | pygame.FULLSCREEN

		if experiment.var.get(u'pygame_window_frame', u'yes', [u'yes', u'no']) \
			== u'no':
			mode = mode | pygame.NOFRAME

		if experiment.var.get(u'pygame_window_pos', u'auto') != u'auto':
			os.environ[u'SDL_VIDEO_WINDOW_POS'] = experiment.var.get(
				u'pygame_window_pos')

		# Create the window and the surface
		experiment.window = pygame.display.set_mode(experiment.resolution(), mode)
		pygame.display.set_caption(u'OpenSesame (legacy backend)')
		pygame.mouse.set_visible(False)
		experiment.surface = pygame.display.get_surface()
		experiment.font = legacy._pygame_font(experiment, experiment.var.font_family,
			experiment.var.font_size)

	@staticmethod
	def close_display(experiment):

		while fileobjects:
			fileobjects.pop().close()
		while fonts:
			fonts.pop(list(fonts.keys())[0], None)
		pygame.display.quit()

	@staticmethod
	def _pygame_font(experiment, family, size):

		"""
		visible: False

		desc:
			A helper function to create a pygame.font.Font object.

		arguments:
			experiment:	The experiment object.
			family:		The font family.
			size:		The font size.

		returns:
			type:	Font
		"""

		if (family, size) in fonts:
			return fonts[(family, size)]
		try:
			path = experiment.resource(u'%s.ttf' % family)
		except:
			# If the family cannot be found in the filepool, assume that it is
			# a system font.
			font = pygame.font.SysFont(family, size)
		else:
			fd = open(path, u'rb')
			fileobjects.append(fd)
			font = pygame.font.Font(fd, size)
		fonts[(family, size)] = font
		return font
