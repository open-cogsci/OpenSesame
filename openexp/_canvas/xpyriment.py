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
from openexp._canvas import canvas
from libopensesame.exceptions import osexception
from openexp.backend import configurable
import pygame
try:
	from expyriment import control, stimuli, io
	from expyriment.misc.geometry import points_to_vertices as p2v
except:
	raise osexception(
		u'Failed to import expyriment, probably because it is not (correctly) installed. For installation instructions, please visit http://www.expyriment.org/.')
from openexp._coordinates.xpyriment import xpyriment as xpyriment_coordinates

class xpyriment(canvas.canvas, xpyriment_coordinates):

	"""
	desc:
		This is a canvas backend built on top of Expyriment.
		For function specifications and docstrings, see
		`openexp._canvas.canvas`.
	"""

	settings = {
		u"expyriment_opengl" : {
			u"name" : u"Use OpenGL",
			u"description" : u"Use OpenGL mode for better temporal precision",
			u"default" : u"yes"
			},
		}

	def __init__(self, experiment, auto_prepare=True, **style_args):

		canvas.canvas.__init__(self, experiment, auto_prepare=auto_prepare,
			**style_args)
		xpyriment_coordinates.__init__(self)
		self.prepared = False
		self.aa = 10
		self.clear()

	def copy(self, canvas):

		self.set_config(**canvas.get_config())
		self.auto_prepare = canvas.auto_prepare
		self.aa = canvas.aa
		self.prepared = False
		self.stim_list = [stim.copy() for stim in canvas.stim_list]
		if self.auto_prepare:
			self.prepare()
		canvas.prepared = False

	def add_stim(self, stim, prepare=True):

		"""
		desc:
			Adds a stimulus to the stimulus list.

			Note: For internal use.

		arguments:
			stim:		the stimulus

		keywords:
			prepare:	indicates whether we should prepare.
		"""

		self.stim_list.append(stim)
		self.prepared = False
		if prepare and self.auto_prepare:
			self.prepare()

	def prepare(self):

		if not self.prepared:
			self._canvas = stimuli.Canvas(
				self.experiment.expyriment.screen.size,
				colour=self.background_color.backend_color)
			for stim in self.stim_list:
				stim.plot(self._canvas)
			self._canvas.preload()
			self.prepared = True
		return self.experiment.time()

	def show(self):

		if not self.prepared: self.prepare()
		self._canvas.present()
		self.experiment.last_shown_canvas = self._canvas
		return self.experiment.time()

	@configurable
	def clear(self):

		self.stim_list = []
		self.prepared = False
		if self.auto_prepare:
			self.prepare()

	@configurable
	def line(self, sx, sy, ex, ey):

		stim = stimuli.Line(self.to_xy((sx,sy)), self.to_xy((ex,ey)),
			line_width=self.penwidth, colour=self.color.backend_color,
			anti_aliasing=self.aa)
		self.add_stim(stim)

	@configurable
	def rect(self, x, y, w, h):

		if self.fill:
			# The position of the stimulus is the center, not the top-left
			pos = self.to_xy((x+w/2,y+h/2))
			stim = stimuli.Rectangle(size=(w,h), position=pos,
				colour=self.color.backend_color)
			self.add_stim(stim)
		# Unfilled shapes are drawn using a polygon
		else:
			# For now, do not use a polygon, because it's really slow when
			# rendering, which is particularly problematic for forms.
			# self.polygon( [(x,y), (x+w,y), (x+w,y+w), (x,y+w), (x,y)], \
			# color=color)
			self.line(x, y, x+w, y)
			self.line(x+w, y, x+w, y+h)
			self.line(x, y+h, x+w, y+h)
			self.line(x, y, x, y+h)

	@configurable
	def ellipse(self, x, y, w, h):

		if self.fill:
			line_width = 0
		else:
			line_width = self.penwidth
		pos = self.to_xy((x+w/2,y+h/2))
		stim = stimuli.Ellipse((w/2, h/2), colour=self.color.backend_color,
			line_width=line_width, position=pos)
		self.add_stim(stim)

	@configurable
	def polygon(self, vertices):

		if self.fill:
			line_width = 0
		else:
			line_width = self.penwidth
		# The coordinate transformations are a bit awkard. Shape expects
		# a list of vertices that start form (0,0), but the position of the
		# shape is the center of the shape. So we first need to determine
		# the center of the polygon=(min+max)/2 and then convert the list
		# of vertices to a format that's acceptable to Shape
		center = (min(p[0] for p in vertices) + \
			max(p[0] for p in vertices)) / 2, \
			(min(p[1] for p in vertices) + \
			max(p[1] for p in vertices)) / 2
		stim = stimuli.Shape(colour=self.color.backend_color,
			position=self.to_xy(center), anti_aliasing=self.aa,
			line_width=line_width)
		l = p2v([self.to_xy(p) for p in vertices])
		for v in l: stim.add_vertex(v)
		self.add_stim(stim)


	def _text_size(self, text):

		try:
			_font = self.experiment.resource(u"%s.ttf" % self.font_family)
		except:
			_font = self.font_family
		stim = stimuli.TextLine(text, text_font=_font,
			text_size=self.font_size, text_bold=self.font_bold,
			text_italic=self.font_italic)
		surf = stim._create_surface()
		return surf.get_width(), surf.get_height()

	def _text(self, text, x, y):

		try:
			_font = self.experiment.resource(u"%s.ttf" % self.font_family)
		except:
			_font = self.font_family

		w, h = self.text_size(text)
		x += w/2
		y += h/2

		stim = stimuli.TextLine(text, position=self.to_xy((x,y)),
			text_colour=self.color.backend_color, text_font=_font,
			text_size=self.font_size, text_bold=self.font_bold,
			text_italic=self.font_italic, text_underline=self.font_underline)
		self.add_stim(stim)

	def image(self, fname, center=True, x=None, y=None, scale=None):

		x, y = self.to_xy(x, y)
		if not center:
			_fname = safe_decode(fname)
			try:
				surf = pygame.image.load(_fname)
			except pygame.error:
				raise osexception(
					u"'%s' is not a supported image format" % fname)
			if scale is None:
				x += surf.get_width()/2
				y -= surf.get_height()/2
			else:
				x += scale*surf.get_width()/2
				y -= scale*surf.get_height()/2
		stim = stimuli.Picture(fname, position=(x,y))
		if scale is not None: stim.scale( (scale, scale) )
		self.add_stim(stim)

	def gabor(self, x, y, orient, freq, env=u"gaussian", size=96, stdev=12,
		phase=0, col1=u"white", col2=u"black", bgmode=u"avg"):

		surface = canvas._gabor(orient, freq, env, size, stdev, phase, col1,
			col2, bgmode)
		stim = stimuli._visual.Visual(position=self.to_xy((x,y)))
		stim._surface = surface
		self.add_stim(stim)

	def noise_patch(self, x, y, env=u"gaussian", size=96, stdev=12,
		col1=u"white", col2=u"black", bgmode=u"avg"):

		surface = canvas._noise_patch(env, size, stdev, col1, col2, bgmode)
		stim = stimuli._visual.Visual(position=self.to_xy((x,y)))
		stim._surface = surface
		self.add_stim(stim)

	@staticmethod
	def init_display(experiment):

		import pygame

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

		# Initialize. If Expyriment jumps into interactive mode, it reads from
		# the stdin, and crashes. Thus we explicitly disable the interactive-
		# mode detection.
		control._experiment_control.is_interactive_mode = lambda: False
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
