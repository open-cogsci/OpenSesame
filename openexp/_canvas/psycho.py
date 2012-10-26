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

import pyglet
import pygame
import math
import openexp._canvas.legacy
import openexp.exceptions
try: # Try both import statements
	from PIL import Image
except:
	import Image
import numpy as np
import os.path

try:
	x
	from psychopy import core, visual
except:
	raise openexp.exceptions.canvas_error(
		'Failed to import PsychoPy, probably because it is not (correctly) installed. For installation instructions, please visit http://www.psychopy.org/.')

class psycho(openexp._canvas.legacy.legacy):

	"""This is a canvas backend built on top of PsychoPy (with Pyglet)"""
	
	# The settings variable is used by the GUI to provide a list of back-end
	# settings
	settings = {
		"psychopy_waitblanking" : {
			"name" : "Wait for blanking",
			"description" : "Block until the display has been shown",
			"default" : "yes"
			},
		"psychopy_wintype" : {
			"name" : "Window type",
			"description" : "'pygame' or 'pyglet'",
			"default" : "pyglet"
			},			
		"psychopy_monitor" : {
			"name" : "Monitor",
			"description" : "Virtual monitor",
			"default" : "testMonitor"
			},						
		}		
	
	def __init__(self, experiment, bgcolor=None, fgcolor=None, auto_prepare=True):
		
		"""See openexp._canvas.legacy"""
		
		self.experiment = experiment
		self.min_penwidth = 1
		if fgcolor == None:
			fgcolor = self.experiment.get("foreground")
		if bgcolor == None:
			bgcolor = self.experiment.get("background")			
		self.set_fgcolor(fgcolor)
		self.set_bgcolor(bgcolor)
		self.set_penwidth(1)
		self.set_font(style=self.experiment.font_family, size= \
			self.experiment.font_size, bold=self.experiment.font_bold=='yes', \
			italic=self.experiment.font_italic=='yes', underline= \
			self.experiment.font_underline=='yes')
		# This font map converts the standard OpenSesame font names to ones that
		# are acceptable to PsychoPy (or PyGlet actually). For now, the
		# difference appears only to be capitalization.
		self.font_map = {"sans" : "Sans", "serif" : "Serif", "mono" : "Mono"}		
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
		raise openexp.exceptions.canvas_error( \
			"openexp._canvas.psycho.flip(): the flip() function has not been implemented for the psycho back-end!")		
		
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
		
	def fixdot(self, x=None, y=None, color=None):
		
		"""See openexp._canvas.legacy"""
		
		if x == None:
			x = self.xcenter()
		if y == None:
			y = self.ycenter()
		
		self.ellipse(x-8, y-8, 16, 16, fill = True, color = color)
		self.ellipse(x-2, y-2, 4, 4, fill = True, color = self.bgcolor)
		
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
			stim = visual.PatchStim(win = self.experiment.window, pos=pos, \
				size=[w, h], color=color, tex=None, interpolate=False)
			self.stim_list.append(stim)
			
	def ellipse(self, x, y, w, h, fill=False, color=None):
		
		"""See openexp._canvas.legacy"""
		
		if color != None:
			color = self.color(color)
		else:
			color = self.fgcolor
			
		pos = x - self.xcenter() + w/2, self.ycenter() - y - h/2

		stim = visual.PatchStim(win = self.experiment.window, mask="circle", \
			pos=pos, size=[w, h], color=color, tex=None, interpolate=True)
		self.stim_list.append(stim)
		
		if not fill:
			stim = visual.PatchStim(win = self.experiment.window, \
				mask="circle", pos=pos, size=[w-2*self.penwidth, \
				h-2*self.penwidth], color=self.bgcolor, tex=None, \
				interpolate=True)
			self.stim_list.append(stim)			
			
	def polygon(self, vertices, fill=False, color=None):
		
		"""See openexp._canvas.legacy"""
		
		self.shapestim(vertices, fill=fill, color=color, fix_coor=True, \
			close=True)
				
	def text_size(self, text):
	
		"""See openexp._canvas.legacy"""
		
		self._text(text, 0, 0)
		s = self.stim_list.pop()
		t = pyglet.font.Text(s._font, text)
		return t.width, t.height				
		
	def _text(self, text, x, y):
	
		"""See openexp._canvas.legacy"""
		
		pos = x - self.xcenter(), self.ycenter() - y		
		stim = visual.TextStim(win=self.experiment.window, text=text, \
			alignHoriz='left', alignVert='top', pos=pos, color=self.fgcolor, \
			font=self.font_map[self.font_style], height=self.font_size, \
			wrapWidth=self.experiment.width, bold=self.font_bold, italic= \
			self.font_italic)
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
				
		stim = visual.PatchStim(win = self.experiment.window, tex=fname, \
			pos=pos, size=(w,h))
		self.stim_list.append(stim)
		
	def gabor(self, x, y, orient, freq, env="gaussian", size=96, stdev=12, \
		phase=0, col1="white", col2=None, bgmode=None):
	
		"""See openexp._canvas.legacy"""
	
		pos = x - self.xcenter(), self.ycenter() - y		
		_env, _size, s = self.env_to_mask(env, size, stdev)				
		p = visual.PatchStim(win=self.experiment.window, pos=pos, ori=-orient,
			mask=_env, size=_size, sf=freq, phase=phase, color=col1)
		self.stim_list.append(p)
		
	def noise_patch(self, x, y, env="gaussian", size=96, stdev=12, \
		col1="white", col2="black", bgmode="avg"):
	
		"""See openexp._canvas.legacy"""
		
		pos = x - self.xcenter(), self.ycenter() - y				
		_env, _size, s = self.env_to_mask(env, size, stdev)			
		tex = 2*(np.random.random([s,s])-0.5)
		p = visual.PatchStim(win=self.experiment.window, tex=tex, pos=pos,
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
		print "size:", i
		s = i
				
		# Create a PsychoPy mask
		if env == "c":
			_env = "circle"
			_size = size
		elif env == "g":	
			_env = "gauss"
			_size = 6*stdev
		elif env == "r":
			_env = "None"
			_size = size
		elif env == "l":			
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

def init_display(experiment):

	"""See openexp._canvas.legacy"""
	
	global _experiment
	_experiment = experiment	
	
	# Set the PsychoPy monitor, default to testMonitor	
	monitor = experiment.get_check("psychopy_monitor", "testMonitor")
	wintype = experiment.get_check("psychopy_wintype", "pyglet", ["pyglet", "pygame"])
	waitblanking = experiment.get_check("psychopy_waitblanking", "yes", ["yes", "no"]) == "yes"
		
	print "openexp._canvas.psycho.init_display(): window type = %s" % wintype
	print "openexp._canvas.psycho.init_display(): waitblanking = %s" % waitblanking
	print "openexp._canvas.psycho.init_display(): monitor = %s" % monitor
			
	experiment.window = visual.Window( experiment.resolution(), \
		waitBlanking=waitblanking, fullscr=experiment.fullscreen, \
		monitor=monitor, units="pix", winType=wintype, \
		rgb=experiment.background)
	experiment.window.setMouseVisible(False)
	experiment.clock = core.Clock()	
	experiment._time_func = _time
	experiment._sleep_func = _sleep
	experiment.time = experiment._time_func
	experiment.sleep = experiment._sleep_func	

	# If pyglet is being used, change the window caption. Don't know how to do this for pygame (regular set_caption() is ineffective)
	if wintype == "pyglet":
		experiment.window.winHandle.set_caption("OpenSesame (PsychoPy backend)")
		
	pygame.mixer.init()	
				
def close_display(experiment):

	"""See openexp._canvas.legacy"""
	
	# This causes a (harmless) exception in some cases, so we catch it to prevent confusion 
	try:
		experiment.window.close()
	except:
		pass
	
def _time():

	"""See openexp._canvas.legacy"""

	global _experiment
	return 1000.0*_experiment.clock.getTime()
	
def _sleep(ms):

	"""See openexp._canvas.legacy"""
		
	core.wait(.001*ms)
