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

import numpy as np
import copy
from openexp._canvas import canvas
from libopensesame.exceptions import osexception
from libopensesame import debug, html
import pygame
try:
	from expyriment import control, stimuli, misc, io
	from expyriment.misc.geometry import coordinates2position, \
		points_to_vertices as p2v
except:
	raise osexception(
		u'Failed to import expyriment, probably because it is not (correctly) installed. For installation instructions, please visit http://www.expyriment.org/.')

def c2p(pos):

	"""
	Converts coordinates (where 0,0 is the display center) to position (where
	0,0 is the top-left). This function is used instead of coordinates2position,
	because we want the virtual screen to be centered in fullscreen mode.

	Arguments:
	pos -- an (x,y) tuple

	Returns:
	An (x,y) tuple
	"""

	return pos[0] - control.defaults.window_size[0]/2, \
		control.defaults.window_size[1]/2 - pos[1]

class xpyriment(canvas.canvas):

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

	def __init__(self, experiment, bgcolor=None, fgcolor=None,
		auto_prepare=True):

		self.experiment = experiment
		self.html = html.html()
		self.auto_prepare = auto_prepare
		self.prepared = False
		if fgcolor == None:
			fgcolor = self.experiment.get(u'foreground')
		if bgcolor == None:
			bgcolor = self.experiment.get(u'background')
		self.set_fgcolor(fgcolor)
		self.set_bgcolor(bgcolor)
		self.bidi = self.experiment.get(u'bidi')==u'yes'
		self.set_font(style=self.experiment.font_family, size= \
			self.experiment.font_size, bold=self.experiment.font_bold==u'yes', \
			italic=self.experiment.font_italic==u'yes', underline= \
			self.experiment.font_underline==u'yes')
		self.penwidth = 1
		self.aa = 10
		self.clear()

	def color(self, color):

		return canvas._color(color)

	def copy(self, canvas):

		self.fgcolor = canvas.fgcolor
		self.bgcolor = canvas.bgcolor
		self.font_style = canvas.font_style
		self.font_size = canvas.font_size
		self.font_italic = canvas.font_italic
		self.font_bold = canvas.font_bold
		self.font_underline = canvas.font_underline
		self.penwidth = canvas.penwidth
		self.auto_prepare = canvas.auto_prepare
		self.aa = canvas.aa
		self.prepared = False
		self.clear()
		self.stim_list = [stim.copy() for stim in canvas.stim_list]
		if self.auto_prepare:
			self.prepare()
		canvas.prepared = False

	def add_stim(self, stim, prepare=True):

		"""
		desc:
			Adds a stimulus to the stimulus list.

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
				colour=self._canvas_color)
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

	def clear(self, color=None):

		if color != None: self._canvas_color = self.color(color)
		else: self._canvas_color = self.bgcolor
		self.stim_list = []
		self.prepare()

	def line(self, sx, sy, ex, ey, color=None, penwidth=None):

		if penwidth == None: penwidth = self.penwidth
		if color != None: color = self.color(color)
		else: color = self.fgcolor
		stim = stimuli.Line(c2p((sx,sy)), c2p((ex,ey)),
			line_width=penwidth, colour=color, anti_aliasing=self.aa)
		self.add_stim(stim)

	def rect(self, x, y, w, h, fill=False, color=None, penwidth=None):

		if fill:
			if color != None: color = self.color(color)
			else: color = self.fgcolor
			# The position of the stimulus is the center, not the top-left
			pos = c2p((x+w/2,y+h/2))
			stim = stimuli.Rectangle(size=(w,h), position=pos,
				colour=color)
			self.add_stim(stim)
		# Unfilled shapes are drawn using a polygon
		else:
			# For now, do not use a polygon, because it's really slow when
			# rendering, which is particularly problematic for forms.
			# self.polygon( [(x,y), (x+w,y), (x+w,y+w), (x,y+w), (x,y)], \
			# color=color)
			self.line(x, y, x+w, y, color=color, penwidth=penwidth)
			self.line(x+w, y, x+w, y+h, color=color, penwidth=penwidth)
			self.line(x, y+h, x+w, y+h, color=color, penwidth=penwidth)
			self.line(x, y, x, y+h, color=color, penwidth=penwidth)

	def ellipse(self, x, y, w, h, fill=False, color=None, penwidth=None):

		if color != None: color = self.color(color)
		else: color = self.fgcolor
		if penwidth == None: penwidth = self.penwidth
		else: line_width = penwidth
		if fill: line_width = 0
		elif penwidth != None: line_width = penwidth
		else: line_width = self.penwidth
		pos = c2p((x+w/2,y+h/2))
		stim = stimuli.Ellipse((w, h), colour=color, line_width=line_width,
			position=pos)
		self.add_stim(stim)

	def polygon(self, vertices, fill=False, color=None, penwidth=None):

		if penwidth == None: penwidth = self.penwidth
		if color != None: color = self.color(color)
		else: color = self.fgcolor
		if fill: line_width = 0
		else: line_width = penwidth
		# The coordinate transformations are a bit awkard. Shape expects
		# a list of vertices that start form (0,0), but the position of the
		# shape is the center of the shape. So we first need to determine
		# the center of the polygon=(min+max)/2 and then convert the list
		# of vertices to a format that's acceptable to Shape
		center = (min(p[0] for p in vertices) + \
			max(p[0] for p in vertices)) / 2, \
			(min(p[1] for p in vertices) + \
			max(p[1] for p in vertices)) / 2
		stim = stimuli.Shape(colour=color, position=c2p(center),
			anti_aliasing=self.aa, line_width=line_width)
		l = p2v([c2p(p) for p in vertices])
		for v in l: stim.add_vertex(v)
		self.add_stim(stim)

	def set_bgcolor(self, color):

		self.bgcolor = self.color(color)
		self._canvas_color = self.bgcolor

	def _text_size(self, text):

		try:
			_font = self.experiment.resource(u"%s.ttf" % self.font_style)
		except:
			_font = self.font_style
		stim = stimuli.TextLine(text, text_font=_font, \
			text_size=self.font_size, text_bold=self.font_bold, \
			text_italic=self.font_italic)
		surf = stim._create_surface()
		return surf.get_width(), surf.get_height()

	def _text(self, text, x, y):

		try:
			_font = self.experiment.resource(u"%s.ttf" % self.font_style)
		except:
			_font = self.font_style

		w, h = self.text_size(text)
		x += w/2
		y += h/2

		stim = stimuli.TextLine(text, position=c2p((x,y)),
			text_colour=self.fgcolor, text_font=_font,
			text_size=self.font_size, text_bold=self.font_bold,
			text_italic=self.font_italic, text_underline=self.font_underline)
		self.add_stim(stim)

	def textline(self, text, line, color=None):

		size = self.text_size(text)
		self.text(text, True, self.xcenter(), self.ycenter()+1.5*line*size[1],
			color=color)

	def image(self, fname, center=True, x=None, y=None, scale=None):

		if x == None: x = self.xcenter()
		if y == None: y = self.ycenter()
		if center == False:
			if isinstance(fname, unicode):
				_fname = fname.encode(self.experiment.encoding)
			else:
				_fname = fname
			surf = pygame.image.load(_fname)
			if scale == None:
				x += surf.get_width()/2
				y += surf.get_height()/2
			else:
				x += scale*surf.get_width()/2
				y += scale*surf.get_height()/2
		stim = stimuli.Picture(fname, position=c2p((x,y)))
		if scale != None: stim.scale( (scale, scale) )
		self.add_stim(stim)

	def gabor(self, x, y, orient, freq, env=u"gaussian", size=96, stdev=12,
		phase=0, col1=u"white", col2=u"black", bgmode=u"avg"):

		surface = canvas._gabor(orient, freq, env, size, stdev, phase, col1,
			col2, bgmode)
		stim = stimuli._visual.Visual(position=c2p((x,y)))
		stim._surface = surface
		self.add_stim(stim)

	def noise_patch(self, x, y, env=u"gaussian", size=96, stdev=12,
		col1=u"white", col2=u"black", bgmode=u"avg"):

		surface = canvas._noise_patch(env, size, stdev, col1, col2, bgmode)
		stim = stimuli._visual.Visual(position=c2p((x,y)))
		stim._surface = surface
		self.add_stim(stim)

def init_display(experiment):

	import pygame

	# Configure Expyriment
	io.defaults.mouse_track_button_events = False
	control.defaults.initialize_delay = 0
	control.defaults.event_logging = 0
	control.defaults.window_mode = experiment.get(u'fullscreen') == u'no'
	control.defaults.fast_quit = True
	control.defaults.window_size = experiment.resolution()
	control.defaults.auto_create_subject_id = True
	control.defaults.open_gl = experiment.get_check(u'expyriment_opengl', \
		xpyriment.settings[u'expyriment_opengl'][u'default']) == u'yes'
	control.defaults.audiosystem_sample_rate = experiment.get(u'sound_freq')
	control.defaults.audiosystem_bit_depth = experiment.get(u'sound_sample_size')
	control.defaults.audiosystem_channels = experiment.get(u'sound_channels')
	control.defaults.audiosystem_buffer_size = experiment.get(u'sound_buf_size')

	# Initialize
	exp = control.initialize()
	experiment._time_func = pygame.time.get_ticks
	experiment._sleep_func = pygame.time.delay
	experiment.time = experiment._time_func
	experiment.sleep = experiment._sleep_func
	experiment.window = exp.screen._surface
	experiment.expyriment = exp

	# TODO: In order to set the window title and to allow mouse responses we
	# need to bypass expyriment for now
	pygame.display.set_caption(u'OpenSesame (Expyriment backend)')
	pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
	pygame.event.set_allowed(pygame.MOUSEBUTTONUP)

def close_display(experiment):

	control.end()
