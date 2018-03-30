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
import pygame
from collections import OrderedDict
from openexp._canvas.canvas import Canvas
from libopensesame.exceptions import osexception
from openexp.backend import configurable
from expyriment import io, control, stimuli
from openexp._coordinates.xpyriment import Xpyriment as XpyrimentCoordinates


class Xpyriment(Canvas, XpyrimentCoordinates):

	"""
	desc:
		This is a canvas backend built on top of Expyriment. For function
		specifications and docstrings, see `openexp._canvas.canvas`.
	"""

	settings = {
		u"expyriment_opengl" : {
			u"name" : u"Use OpenGL",
			u"description" : u"Use OpenGL mode for better temporal precision",
			u"default" : u"yes"
		}
	}

	def __init__(self, experiment, auto_prepare=True, **style_args):

		Canvas.__init__(self, experiment, auto_prepare=auto_prepare,
			**style_args)
		XpyrimentCoordinates.__init__(self)
		self.clear()

	@configurable
	def clear(self):

		self._elements = OrderedDict()
		self._set_background()

	def set_config(self, **cfg):

		Canvas.set_config(self, **cfg)
		if u'background_color' in cfg:
			self._set_background()

	def show(self):

		# First create a flat list of all elements, including elements that are
		# part of a group. Then we show them, clearing the display on the first,
		# and updating the display on the last.
		elements = [e for g in self._elements.values() if g.visible for e in g]
		self._background.present(clear=True, update=not elements)
		while elements:
			e = elements.pop(0)
			e.show(clear=False, update=not elements)
		return self.experiment.clock.time()

	def _set_background(self):

		self._background = stimuli.BlankScreen(
			colour=self.background_color.backend_color
		)
		self._background.preload()		

	@staticmethod
	def init_display(experiment):

		# Configure Expyriment
		io.defaults.mouse_track_button_events = False
		control.defaults.initialize_delay = 0
		control.defaults.event_logging = 0
		control.defaults.window_mode = experiment.var.fullscreen != u'yes'
		control.defaults.fast_quit = True
		control.defaults.window_size = experiment.resolution()
		control.defaults.auto_create_subject_id = True
		control.defaults.open_gl = experiment.var.get(u'expyriment_opengl',
			xpyriment.settings[u'expyriment_opengl'][u'default']) == u'yes'
		control.defaults.audiosystem_sample_rate = experiment.var.sound_freq
		control.defaults.audiosystem_bit_depth = \
			experiment.var.sound_sample_size
		control.defaults.audiosystem_channels = experiment.var.sound_channels
		control.defaults.audiosystem_buffer_size = \
			experiment.var.sound_buf_size
		control.defaults.audiosystem_autostart = False
		# Initialize. If Expyriment jumps into interactive mode, it reads from
		# the stdin, and crashes. Thus we explicitly disable the interactive-
		# mode detection. The is_interactive_mode() function is located
		# differently in different versions of expyriment, and hence we monkey
		# patch it twice.
		control._experiment_control.misc.is_interactive_mode = \
			control._experiment_control.is_interactive_mode = \
			lambda: False
		exp = control.initialize()
		experiment.window = exp.screen._surface
		experiment.expyriment = exp
		# TODO: In order to set the window title and to allow mouse responses we
		# need to bypass expyriment for now
		pygame.display.set_caption(u'OpenSesame (Expyriment backend)')
		pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
		pygame.event.set_allowed(pygame.MOUSEBUTTONUP)

	@staticmethod
	def close_display(experiment):

		control.end()


# Non PEP-8 alias for backwards compatibility
xpyriment = Xpyriment
