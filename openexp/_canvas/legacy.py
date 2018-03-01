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
from openexp.backend import configurable
from openexp._canvas.canvas import Canvas
from openexp._coordinates.legacy import Legacy as LegacyCoordinates

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


class Legacy(Canvas, LegacyCoordinates):

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

		Canvas.__init__(self, experiment, auto_prepare=auto_prepare,
			**style_args)
		LegacyCoordinates.__init__(self)
		self.antialias = True
		self.surface = self.experiment.surface.copy()
		self.clear()
		if platform.system() == u'Darwin':
			self.show = self._show_macos

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

	def prepare(self):

		"""
		desc:
			Finishes pending canvas operations (if any), so that a subsequent
			call to [canvas.show] is extra fast. It's only necessary to call
			this function if you have disabled `auto_prepare` in
			[canvas.__init__].
		"""

		self.surface.fill(self.background_color.backend_color)
		Canvas.prepare(self)

	def redraw(self):

		if not self.auto_prepare:
			return
		self.prepare()

	def set_config(self, **cfg):

		Canvas.set_config(self, **cfg)
		if hasattr(self, u'surface'):
			self.redraw()

	def copy(self, canvas):

		self.surface = canvas.surface.copy()
		Canvas.copy(self, canvas)

	@configurable
	def clear(self):

		self.surface.fill(self.background_color.backend_color)
		self._elements = {}


	def _text_size(self, text):

		return self._font.size(text)

	@staticmethod
	def init_display(experiment):

		def p(msg):

			print(u'openexp._canvas.legacy.init_display(): %s' % msg)

		# Intialize PyGame and set the Window icon
		pygame.init()
		surf = pygame.Surface( (32, 32) )
		surf.fill( (255, 255, 255) )
		pygame.draw.circle(surf, (0, 0, 255), (16, 16), 10, 4)
		pygame.display.set_icon(surf)
		# Determine the video mode
		mode = 0
		if (
			experiment.var.get(u"pygame_hwsurface", u"yes", [u"yes", u"no"])
			== u"yes"
		):
			mode = mode | pygame.HWSURFACE
			p(u'enabling hardware surface')
		else:
			p(u'not enabling hardware surface')
		if (
			experiment.var.get(u"pygame_doublebuf", u"yes", [u"yes", u"no"])
			== u"yes"
		):
			mode = mode | pygame.DOUBLEBUF
			p(u'enabling double buffering')
		else:
			p(u'not enabling double buffering')
		if pygame.display.mode_ok(experiment.resolution(), mode):
			p(u'video mode ok')
		else:
			p(u'warning: video mode not ok')
		if experiment.var.fullscreen == u'yes':
			mode = mode | pygame.FULLSCREEN
		if (
			experiment.var.get(u'pygame_window_frame', u'yes', [u'yes', u'no'])
			== u'no'
		):
			mode = mode | pygame.NOFRAME
		if experiment.var.get(u'pygame_window_pos', u'auto') != u'auto':
			os.environ[u'SDL_VIDEO_WINDOW_POS'] = experiment.var.get(
				u'pygame_window_pos'
			)
		# Create the window and the surface
		experiment.window = pygame.display.set_mode(experiment.resolution(), mode)
		pygame.display.set_caption(u'OpenSesame (legacy backend)')
		pygame.mouse.set_visible(False)
		experiment.surface = pygame.display.get_surface()
		# Disable mouse-motion events because they fill up the cue
		pygame.event.set_blocked(pygame.MOUSEMOTION)

	@staticmethod
	def close_display(experiment):

		while fileobjects:
			fileobjects.pop().close()
		while fonts:
			fonts.pop(list(fonts.keys())[0], None)
		pygame.display.quit()


# Non PEP-8 alias for backwards compatibility
legacy = Legacy
