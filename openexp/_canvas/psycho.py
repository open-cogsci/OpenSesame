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
import pyglet
from openexp.backend import configurable
from openexp._canvas import canvas
from openexp.color import color
from openexp._coordinates.psycho import psycho as psycho_coordinates
from libopensesame.exceptions import osexception
from libopensesame import debug
try: # Try both import statements
	from PIL import Image
except:
	import Image
import numpy as np

try:
	from psychopy import core, visual, logging, event
except:
	raise osexception(
		u'Failed to import PsychoPy, probably because it is not (correctly) installed. For installation instructions, please visit http://www.psychopy.org/.')
if not hasattr(visual, u'ImageStim'):
	raise osexception(
		u'PsychoPy is missing the ImageStim() class. Please update your version of PsychoPy! For installation instructions, please visit http://www.psychopy.org/.')
if not hasattr(visual, u'GratingStim'):
	raise osexception(
		u'PsychoPy is missing the GratingStim() class. Please update your version of PsychoPy! For installation instructions, please visit http://www.psychopy.org/.')

import psychopy, warnings
from distutils.version import StrictVersion
try:
	psypy_vers = StrictVersion(psychopy.__version__)
except ValueError:
	warnings.warn(u'Invalid version number %s of PsychoPy'%psychopy.__version__)
else:
	if psypy_vers.version < (1,84,1):
		warnings.warn(u'Your PsychoPy version is outdated. To draw complex '
			u'shapes that include holes, concavities, etc., please update to '
			u'PsychoPy version 1.84.1 or higher.')

# Store the experiment as a singleton, to be used in the _time() function
_experiment = None
# Store the old display gamma value
_old_gamma = None
# Contains a list of fonts that have been explicitly registered with PyGlet
_registered_fonts = []

class psycho(canvas.canvas, psycho_coordinates):

	"""
	desc:
		This is a canvas backend built on top of PsychoPy (with Pyglet).
		For function specifications and docstrings, see
		`openexp._canvas.canvas`.
	"""

	# The settings variable is used by the GUI to provide a list of back-end
	# settings
	settings = {
		u'psychopy_waitblanking' : {
			u'name' : u'Wait for blanking',
			u'description' : u'Block until the display has been shown',
			u'default' : u'yes'
			},
		u'psychopy_monitor' : {
			u'name' : u'Monitor',
			u'description' : u'Virtual monitor',
			u'default' : u'testMonitor'
			},
		u"psychopy_screen" : {
			u"name" : u"Screen",
			u"description" : u"The physical screen that is used",
			u"default" : 0,
			},
		u"psychopy_gamma" : {
			u"name" : u"Gamma",
			u"description" : u"Display gamma value display",
			u"default" : u"unchanged",
			},
		u'psychopy_suppress_warnings' : {
			u'name' : u'Suppress warnings',
			u'description' : u'Set PsychoPy logging level to "critical"',
			u'default' : u'yes',
			}
		}

	def __init__(self, experiment, auto_prepare=True, **style_args):

		canvas.canvas.__init__(self, experiment, auto_prepare=auto_prepare,
			**style_args)
		psycho_coordinates.__init__(self)
		self.min_penwidth = 1
		# We need to map the simple font names used by OpenSesame onto the
		# actual names of the fonts.
		self.font_map = {
			u"sans" : u"Droid Sans",
			u"serif" : u"Droid Serif",
			u"mono" : u"Droid Sans Mono",
			u'hebrew' : u'Alef',
			u'hindi' : u'Lohit Hindi',
			u'arabic' : u'Droid Arabic Naskh',
			u'chinese-japanese-korean' : u'WenQuanYi Micro Hei',
			}
		self.clear()

	def set_config(self, **cfg):

		if u'font_family' in cfg:
			style = cfg[u'font_family']
			# If a font is taken from the file pool, it is not registered with
			# PyGlet, and we therefore need to register it now.
			if self.experiment.file_in_pool(u'%s.ttf' % style):
				font_path = self.experiment.pool[u'%s.ttf' % style]
				register_font(font_path)
		canvas.canvas.set_config(self, **cfg)

	def copy(self, canvas):

		self.stim_list = canvas.stim_list + []
		self.set_config(**canvas.get_config())

	def show(self):

		for stim in self.stim_list:
			stim.draw()
		self.experiment.window.flip(clearBuffer=True)
		return self.experiment.clock.time()

	@configurable
	def clear(self):

		self.stim_list = []
		if self.uniform_coordinates:
			x, y = -self._width/2, -self._height/2
		else:
			x, y = 0, 0
		self.rect(x, y, self._width, self._height,
			color=self.background_color.backend_color, fill=True)

	@configurable
	def line(self, sx, sy, ex, ey):

		self.shapestim( [(sx, sy), (ex, ey)])

	@configurable
	def rect(self, x, y, w, h):

		if not self.fill:
			self.shapestim( [[x, y], [x+w, y], [x+w, y+h], [x, y+h]],
				close=True)
		else:
			pos = self.to_xy(x+w/2, y+h/2)
			stim = visual.GratingStim(win=self.experiment.window, pos=pos,
				size=[w, h], color=self.color.backend_color, tex=None,
				interpolate=False)
			self.stim_list.append(stim)

	@configurable
	def ellipse(self, x, y, w, h):

		pos = self.to_xy(x+w/2, y+h/2)
		stim = visual.GratingStim(win=self.experiment.window, mask=u'circle',
			pos=pos, size=[w, h], color=self.color.backend_color, tex=None,
			interpolate=True)
		self.stim_list.append(stim)
		if not self.fill:
			stim = visual.GratingStim(win=self.experiment.window,
				mask=u'circle', pos=pos, size=[w-2*self.penwidth,
				h-2*self.penwidth], color=self.background_color.backend_color,
				tex=None, interpolate=True)
			self.stim_list.append(stim)

	@configurable
	def polygon(self, vertices):

		self.shapestim(vertices, fix_coor=True, close=True)

	def _text_size(self, text):

		self._text(text, 0, 0)
		s = self.stim_list.pop()
		t = pyglet.font.Text(s._font, text)
		return t.width, t.height

	def _text(self, text, x, y):

		if self.font_family in self.font_map:
			font = self.font_map[self.font_family]
		else:
			font = self.font_family
		pos = self.to_xy(x, y)
		stim = visual.TextStim(win=self.experiment.window, text=text,
			alignHoriz=u'left', alignVert=u'top', pos=pos,
			color=self.color.backend_color, font=font, height= self.font_size,
			wrapWidth=self._width, bold=self.font_bold, italic=self.font_italic)
		self.stim_list.append(stim)

	def image(self, fname, center=True, x=None, y=None, scale=None):

		im = Image.open(fname)

		if scale is not None:
			w = im.size[0] * scale
			h = im.size[1] * scale
		else:
			w, h = im.size

		pos = self.to_xy(x, y)
		if not center:
			x += w/2
			y += h/2
		stim = visual.ImageStim(win=self.experiment.window, image=fname,
			pos=pos, size=(w,h))
		self.stim_list.append(stim)

	def gabor(self, x, y, orient, freq, env=u"gaussian", size=96, stdev=12,
		phase=0, col1=u"white", col2=u'black', bgmode=u'avg'):

		pos = self.to_xy(x, y)
		_env, _size, s = self.env_to_mask(env, size, stdev)
		p = visual.GratingStim(win=self.experiment.window, pos=pos, ori=-orient,
			mask=_env, size=_size, sf=freq, phase=phase, color=col1)
		self.stim_list.append(p)

	def noise_patch(self, x, y, env=u"gaussian", size=96, stdev=12,
		col1=u"white", col2=u"black", bgmode=u"avg"):

		pos = self.to_xy(x, y)
		_env, _size, s = self.env_to_mask(env, size, stdev)
		tex = 2*(np.random.random([s,s])-0.5)
		p = visual.GratingStim(win=self.experiment.window, tex=tex, pos=pos,
			mask=_env, size=_size, color=col1)
		self.stim_list.append(p)

	def env_to_mask(self, env, size, stdev):

		"""
		desc:
			Converts an envelope name to a PsychoPy mask. Also returns the
			appropriate patch size and the smallest power-of-two size

			__Note:__

			Specific to the PsychoPy backend, primarily intended for internal
			use. Using this function directly will break your experiment when
			switching backends.

		arguments:
			env:	An envelope name.
			size:	A size value.

		returns:
			A (psychopy_mask, mask_size, power_of_two_size) tuple.
		"""

		env = canvas._match_env(env)

		# Get the smallest power-of-two size
		i = 2
		while size / (i) > 0:
			i = 2*i
		s = i

		# Create a PsychoPy mask
		if env == u"c":
			_env = u"circle"
			_size = size
		elif env == u"g":
			_env = u"gauss"
			_size = 6*stdev
		elif env == u"r":
			_env = u"None"
			_size = size
		elif env == u"l":
			_env = np.zeros([s,s])
			for x in range(s):
				for y in range(s):
					r = np.sqrt((x-s/2)**2+(y-s/2)**2)
					_env[x,y] = (max(0, (0.5*s-r) / (0.5*s))-0.5)*2
			_size = size
		return	(_env, _size, s)

	def shapestim(self, vertices, fix_coor=True, close=False):

		"""
		desc:
			Draws a stimulus definied by a list of vertices

			__Note:__

			Specific to the PsychoPy backend, primarily intended for internal
			use. Using this function directly will break your experiment when
			switching backends.

		arguments:
			vertices:	A list of lists, like [[0,0],[10,10]] containing the
						vertices of the shape

		keywords:
			fix_coor:	A boolean indicating whether the vertices are in
						OpenSesame or PsychoPy format.
			close:		Indicates whether the shape should be closed.
		"""

		if fix_coor:
			_vertices = [self.to_xy(tuple(xy)) for xy in vertices]
		else:
			_vertices = vertices
		if self.fill:
			fill_color = self.color.backend_color
		else:
			fill_color = None
		stim = visual.ShapeStim(self.experiment.window, units=u"pix",
			lineWidth=self.penwidth, vertices=_vertices,
			lineColor=self.color.backend_color, closeShape=close,
			fillColor=fill_color, interpolate=False)
		self.stim_list.append(stim)

	@staticmethod
	def init_display(experiment):

		global _experiment, _old_gamma
		_experiment = experiment
		# Set the PsychoPy monitor, default to testMonitor
		monitor = experiment.var.get(u'psychopy_monitor', u'testMonitor')
		waitblanking = experiment.var.get(u'psychopy_waitblanking', u'yes', \
			[u'yes', u'no']) == u'yes'
		screen = experiment.var.get(u'psychopy_screen', 0)
		# Print some information to the debug window
		print(u'openexp._canvas.psycho.init_display(): waitblanking = %s' % \
			waitblanking)
		print(u'openexp._canvas.psycho.init_display(): monitor = %s' % monitor)
		print(u'openexp._canvas.psycho.init_display(): screen = %s' % screen)
		# Initialize the PsychoPy window and set various functions

		experiment.window = visual.Window(experiment.resolution(),
			screen=screen, waitBlanking=waitblanking,
			fullscr=experiment.var.fullscreen==u'yes', monitor=monitor,
			units=u'pix',
			rgb=color(experiment, experiment.var.background).backend_color,
			winType=u'pyglet', allowStencil=True)
		event.Mouse(visible=False, win=experiment.window)
		experiment.window.winHandle.set_caption(u'OpenSesame (PsychoPy backend)')
		# Set Gamma value if specified
		gamma = experiment.var.get(u'psychopy_gamma', u'unchanged')
		if type(gamma) in (int, float) and gamma > 0:
			_old_gamma = experiment.window.gamma
			experiment.window.setGamma(gamma)
		elif gamma != u'unchanged':
			raise osexception( \
				u'Gamma should be a positive numeric value or "unchanged"')
		# Register the built-in OpenSesame fonts.
		for font in [u'sans', u'serif', u'mono', u'arabic', u'hebrew', u'hindi',
			u'chinese-japanese-korean']:
			font_path = experiment.resource(u'%s.ttf' % font)
			register_font(font_path)
		# Override the default quit function, so that the application is not exited
		core.quit = _psychopy_clean_quit
		# Optionally change the logging level to avoid a lot of warnings in the
		# debug window
		if experiment.var.get(u'psychopy_suppress_warnings', u'yes'):
			logging.console.setLevel(logging.CRITICAL)
		# We need to initialize the pygame mixer, because PsychoPy uses that as well
		pygame.mixer.init()

	@staticmethod
	def close_display(experiment):

		global _old_gamma
		# Restore display gamma if necessary
		if _old_gamma is not None:
			experiment.window.setGamma(_old_gamma)
		# This causes a (harmless) exception in some cases, so we catch it to
		# prevent confusion
		try:
			experiment.window.close()
		except:
			debug.msg(u'An error occurred while closing the PsychoPy window.',
				reason=u'warning')

def register_font(font_path):

	"""
	desc:
		Register a font with PyGlet. If the font has already been registered,
		this function does nothing.

	arguments:
		font_path:	The full path to the font file.
	"""

	global _registered_fonts
	if font_path in _registered_fonts:
		return
	debug.msg(u'registering %s' % font_path)
	pyglet.font.add_file(font_path)
	_registered_fonts.append(font_path)

def _psychopy_clean_quit():

	"""
	desc:
		When PsychoPy encounters an error, it does a sys.exit() which is not
		what we want, because it closes OpenSesame altogether. Instead, we
		nicely inform the user that PsychoPy has signalled an error.
	"""

	raise osexception( \
		u'PsychoPy encountered an error and aborted the program. See the debug window for PsychoPy error messages.')
