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
import pyglet
import math
import openexp._canvas.legacy
from libopensesame.exceptions import osexception
from libopensesame import debug, html
try: # Try both import statements
	from PIL import Image
except:
	import Image
import numpy as np
import os.path

try:
	from psychopy import core, visual, logging
except:
	raise osexception(
		u'Failed to import PsychoPy, probably because it is not (correctly) installed. For installation instructions, please visit http://www.psychopy.org/.')
if not hasattr(visual, u'ImageStim'):
	raise osexception( \
		u'PsychoPy is missing the ImageStim() class. Please update your version of PsychoPy! For installation instructions, please visit http://www.psychopy.org/.')
if not hasattr(visual, u'GratingStim'):
	raise osexception( \
		u'PsychoPy is missing the GratingStim() class. Please update your version of PsychoPy! For installation instructions, please visit http://www.psychopy.org/.')

class psycho(openexp._canvas.legacy.legacy):

	"""This is a canvas backend built on top of PsychoPy (with Pyglet)"""

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
		u'psychopy_screen' : {
			u'name' : u'Screen',
			u'description' : u'The physical screen that is used',
			u'default' : 0,
			},
		u'psychopy_suppress_warnings' : {
			u'name' : u'Suppress warnings',
			u'description' : u'Set PsychoPy logging level to "critical"',
			u'default' : u'yes',
			}
		}

	def __init__(self, experiment, bgcolor=None, fgcolor=None, auto_prepare= \
		True):

		"""See openexp._canvas.legacy"""

		self.experiment = experiment
		self.html = html.html()
		self.min_penwidth = 1
		if fgcolor == None:
			fgcolor = self.experiment.get(u"foreground")
		if bgcolor == None:
			bgcolor = self.experiment.get(u"background")
		self.set_fgcolor(fgcolor)
		self.set_bgcolor(bgcolor)
		self.set_penwidth(1)
		self.bidi = self.experiment.get(u'bidi')==u'yes'
		self.set_font(style=self.experiment.font_family, size= \
			self.experiment.font_size, bold=self.experiment.font_bold==u'yes', \
			italic=self.experiment.font_italic==u'yes', underline= \
			self.experiment.font_underline==u'yes')
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

	def color(self, color):

		"""See openexp._canvas.legacy"""

		if type(color) in (tuple, list):
			# PsycoPy want tuples to be between 0 and 1, so we normalize the
			# tuple if the format is incorrect (i.e. 0-255).
			r = color[0]
			g = color[1]
			b = color[2]
			if r>1 or g>1 or b>1:
				r = 1.*r/255
				g = 1.*g/255
				b = 1.*b/255
				color = r,g,b
		return color

	def flip(self, x=True, y=False):

		"""See openexp._canvas.legacy"""

		# TODO
		raise osexception( \
			u"openexp._canvas.psycho.flip(): the flip() function has not been implemented for the psycho back-end!")

	def copy(self, canvas):

		"""See openexp._canvas.legacy"""

		self.stim_list = canvas.stim_list + []
		self.bgcolor = canvas.bgcolor
		self.fgcolor = canvas.fgcolor
		self.penwidth = canvas.penwidth

	def show(self):

		"""See openexp._canvas.legacy"""

		for stim in self.stim_list:
			stim.draw()
		self.experiment.window.flip(clearBuffer = True)
		return 1000.0 * self.experiment.clock.getTime()

	def clear(self, color=None):

		"""See openexp._canvas.legacy"""

		self.stim_list = []
		if color != None:
			color = self.color(color)
		else:
			color = self.bgcolor
		if self.experiment.background != color:
			# The background is simply a rectangle, because of the double flip
			# required by set_color()
			self.rect(0, 0, self.experiment.width, self.experiment.height, \
				color=color, fill=True)

	def circle(self, x, y, r, fill=False, color=None):

		"""See openexp._canvas.legacy"""

		self.ellipse(x-r, y-r, 2*r, 2*r, fill = fill, color = color)

	def line(self, sx, sy, ex, ey, color=None):

		"""See openexp._canvas.legacy"""


		if color == None:
			color = self.fgcolor
		self.shapestim( [[sx, sy], [ex, ey]], color = color)

	def rect(self, x, y, w, h, fill=False, color=None):

		"""See openexp._canvas.legacy"""

		if color == None:
			color = self.fgcolor
		else:
			color = self.color(color)

		if not fill:
			self.shapestim( [[x, y], [x+w, y], [x+w, y+h], [x, y+h]], color, \
				close=True)
		else:
			pos = x + w/2 - self.xcenter(), self.ycenter() - y - h/2
			stim = visual.GratingStim(win=self.experiment.window, pos=pos, \
				size=[w, h], color=color, tex=None, interpolate=False)
			self.stim_list.append(stim)

	def ellipse(self, x, y, w, h, fill=False, color=None):

		"""See openexp._canvas.legacy"""

		if color != None:
			color = self.color(color)
		else:
			color = self.fgcolor

		pos = x - self.xcenter() + w/2, self.ycenter() - y - h/2

		stim = visual.GratingStim(win=self.experiment.window, mask=u'circle', \
			pos=pos, size=[w, h], color=color, tex=None, interpolate=True)
		self.stim_list.append(stim)

		if not fill:
			stim = visual.GratingStim(win = self.experiment.window, \
				mask=u'circle', pos=pos, size=[w-2*self.penwidth, \
				h-2*self.penwidth], color=self.bgcolor, tex=None, \
				interpolate=True)
			self.stim_list.append(stim)

	def polygon(self, vertices, fill=False, color=None):

		"""See openexp._canvas.legacy"""

		self.shapestim(vertices, fill=fill, color=color, fix_coor=True, \
			close=True)
		
	def set_font(self, style=None, size=None, italic=None, bold=None, \
		underline=None):
		
		"""See openexp._canvas.legacy"""
		
		if style != None:
			# If a font is taken from the file pool, it is not registered with
			# PyGlet, and we therefore need to register it now.
			if self.experiment.file_in_pool(u'%s.ttf' % style):
				font_path = self.experiment.get_file(u'%s.ttf' % style)
				register_font(font_path)
		openexp._canvas.legacy.legacy.set_font(self, style=style, size=size, \
			italic=italic, bold=bold, underline=underline)

	def text_size(self, text):

		"""See openexp._canvas.legacy"""

		self._text(text, 0, 0)
		s = self.stim_list.pop()
		t = pyglet.font.Text(s._font, text)
		return t.width, t.height

	def _text(self, text, x, y):

		"""See openexp._canvas.legacy"""
		
		if self.font_style in self.font_map:
			font = self.font_map[self.font_style]
		else:
			font = self.font_style
		pos = x - self.xcenter(), self.ycenter() - y
		stim = visual.TextStim(win=self.experiment.window, text=text, \
			alignHoriz=u'left', alignVert=u'top', pos=pos, color=self.fgcolor, \
			font=font, height= self.font_size, wrapWidth= \
			self.experiment.width, bold=self.font_bold, italic=self.font_italic)
		self.stim_list.append(stim)

	def textline(self, text, line, color=None):

		"""See openexp._canvas.legacy"""

		self.text(text, True, self.xcenter(), self.ycenter() + 1.5 * line * \
			self.font_size, color = color)

	def image(self, fname, center=True, x=None, y=None, scale=None):

		"""See openexp._canvas.legacy"""

		im = Image.open(fname)

		if scale != None:
			w = im.size[0] * scale
			h = im.size[1] * scale
		else:
			w, h = im.size

		# Calculate the position
		if x == None:
			x = self.xcenter()
		if y == None:
			y = self.ycenter()
		if not center:
			x += w/2
			y += h/2
		pos = x - self.xcenter(), self.ycenter() - y

		stim = visual.ImageStim(win=self.experiment.window, image=fname, \
			pos=pos, size=(w,h))
		self.stim_list.append(stim)

	def gabor(self, x, y, orient, freq, env=u"gaussian", size=96, stdev=12, \
		phase=0, col1=u"white", col2=None, bgmode=None):

		"""See openexp._canvas.legacy"""

		pos = x - self.xcenter(), self.ycenter() - y
		_env, _size, s = self.env_to_mask(env, size, stdev)
		p = visual.GratingStim(win=self.experiment.window, pos=pos, ori=-orient,
			mask=_env, size=_size, sf=freq, phase=phase, color=col1)
		self.stim_list.append(p)

	def noise_patch(self, x, y, env=u"gaussian", size=96, stdev=12, \
		col1=u"white", col2=u"black", bgmode=u"avg"):

		"""See openexp._canvas.legacy"""

		pos = x - self.xcenter(), self.ycenter() - y
		_env, _size, s = self.env_to_mask(env, size, stdev)
		tex = 2*(np.random.random([s,s])-0.5)
		p = visual.GratingStim(win=self.experiment.window, tex=tex, pos=pos,
			mask=_env, size=_size, color=col1)
		self.stim_list.append(p)

	def env_to_mask(self, env, size, stdev):

		"""
		* Note: Specific to the PsychoPy backend, primarily intended for
				internal use. Using this function directly will break your
				experiment when switching backends.

		Converts an envelope name to a PsychoPy mask. Also returns the
		appropriate patch size and the smallest power-of-two size

		Arguments:
		env -- an envelope name
		size -- a size value

		Returns:
		A (psychopy_mask, mask_size, power_of_two_size) tuple
		"""

		env = openexp._canvas.legacy._match_env(env)

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

	def shapestim(self, vertices, color=None, fill=False, fix_coor=True, \
		close=False):

		"""
		* Note: Specific to the PsychoPy backend, primarily intended for
				internal use. Using this function directly will break your
				experiment when switching backends.

		Draws a stimulus definied by a list of vertices

		Arguments:
		vertices -- A list of lists, like [[0,0],[10,10]] containing the
					vertices of the shape

		Keyword arguments:
		color -- the color of the shape
		fill -- a boolean indicating wether the shape should be filles
		fix_coor -- a boolean indicating whether the vertices are in OpenSesame
					or PsychoPy format
		"""

		if fix_coor:
			# Convert the coordinates into the PsychoPy format, in which 0,0 is
			# the center of the screen and negative y-coordinates are down.
			_vertices = []
			for x, y in vertices:
				_vertices.append( [x - self.xcenter(), self.ycenter() - y] )
		else:
			_vertices = vertices

		if color == None:
			color = self.fgcolor
		if fill:
			fill = color
		else:
			fill = None

		stim = visual.ShapeStim(self.experiment.window, units="pix", \
			lineWidth=self.penwidth, vertices=_vertices, lineColor=color, \
			closeShape=close, fillColor=fill, interpolate=False)
		self.stim_list.append(stim)

"""
Static methods
"""

# Store the experiment as a singleton, to be used in the _time() function
_experiment = None
# Contains a list of fonts that have been explicitly registered with PyGlet
_registered_fonts = []

def init_display(experiment):

	"""See openexp._canvas.legacy"""

	global _experiment
	_experiment = experiment
	# Set the PsychoPy monitor, default to testMonitor
	monitor = experiment.get_check(u'psychopy_monitor', u'testMonitor')
	waitblanking = experiment.get_check(u'psychopy_waitblanking', u'yes', \
		[u'yes', u'no']) == u'yes'
	screen = experiment.get_check(u'psychopy_screen', 0)
	# Print some information to the debug window
	print u'openexp._canvas.psycho.init_display(): waitblanking = %s' % \
		waitblanking
	print u'openexp._canvas.psycho.init_display(): monitor = %s' % monitor
	print u'openexp._canvas.psycho.init_display(): screen = %s' % screen
	# Initialize the PsychoPy window and set various functions
	experiment.window = visual.Window( experiment.resolution(), screen=screen, \
		waitBlanking=waitblanking, fullscr=experiment.fullscreen, \
		monitor=monitor, units=u'pix', rgb=experiment.background)
	experiment.window.setMouseVisible(False)
	experiment.clock = core.Clock()
	experiment._time_func = _time
	experiment._sleep_func = _sleep
	experiment.time = experiment._time_func
	experiment.sleep = experiment._sleep_func	
	experiment.window.winHandle.set_caption(u'OpenSesame (PsychoPy backend)')
	# Register the built-in OpenSesame fonts.
	for font in [u'sans', u'serif', u'mono', u'arabic', u'hebrew', u'hindi', \
		u'chinese-japanese-korean']:
		font_path = experiment.resource(u'%s.ttf' % font)
		register_font(font_path)
	# Override the default quit function, so that the application is not exited
	core.quit = _psychopy_clean_quit
	# Optionally change the logging level to avoid a lot of warnings in the
	# debug window
	if experiment.get_check(u'psychopy_suppress_warnings', u'yes'):
		logging.console.setLevel(logging.CRITICAL)
	# We need to initialize the pygame mixer, because PsychoPy uses that as well
	pygame.mixer.init()
	
def close_display(experiment):

	"""See openexp._canvas.legacy"""

	# This causes a (harmless) exception in some cases, so we catch it to
	# prevent confusion.
	try:
		experiment.window.close()
	except:
		debug.msg(u'An error occurred while closing the PsychoPy window.', \
			reason=u'warning')
		
def register_font(font_path):
	
	"""
	Register a font with PyGlet. If the font has already been registered, this
	function does nothing.
	
	Arguments:
	font_path	--	The full path to the font file.
	"""
	
	global _registered_fonts
	if font_path in _registered_fonts:
		return
	debug.msg(u'registering %s' % font_path)
	pyglet.font.add_file(font_path)
	_registered_fonts.append(font_path)

def _time():

	"""See openexp._canvas.legacy"""

	global _experiment
	return 1000.0*_experiment.clock.getTime()

def _sleep(ms):

	"""See openexp._canvas.legacy"""

	core.wait(.001*ms)

def _psychopy_clean_quit():
	
	"""
	When PsychoPy encounters an error, it does a sys.exit() which is not what
	we want, because it closes OpenSesame altogether. Instead, we nicely inform
	the user that PsychoPy has signalled an error.
	"""
	
	raise osexception( \
		u'PsychoPy encountered an error and aborted the program. See the debug window for PsychoPy error messages.')