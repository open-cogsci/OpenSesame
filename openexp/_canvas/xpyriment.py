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

import numpy as np
import copy
import openexp._canvas.legacy
import openexp.exceptions
import pygame
from expyriment import control, stimuli, misc, io
from expyriment.misc.geometry import coordinates2position, \
	points_to_vertices as p2v
	
	
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

class xpyriment(openexp._canvas.legacy.legacy):

	"""This is a canvas backend built on top of Expyriment"""	
	
	settings = {
		"expyriment_opengl" : {
			"name" : "Use OpenGL",
			"description" : "Use OpenGL mode for better temporal precision",
			"default" : "yes"
			},
		}
	
	def __init__(self, experiment, bgcolor=None, fgcolor=None):
		
		"""See openexp._canvas.legacy"""
		
		self.experiment = experiment
		if fgcolor == None:
			fgcolor = self.experiment.get('foreground')
		if bgcolor == None:
			bgcolor = self.experiment.get('background')
		self.set_fgcolor(fgcolor)
		self.set_bgcolor(bgcolor)
		self.set_font(style=self.experiment.font_family, size= \
			self.experiment.font_size, bold=self.experiment.font_bold=='yes', \
			italic=self.experiment.font_italic=='yes', underline= \
			self.experiment.font_underline=='yes')
		self.penwidth = 1
		self.ellipse_res = 100
		self.aa = 10
		self.clear()
						
	def flip(self, x=True, y=False):
		
		"""See openexp._canvas.legacy"""
		
		# TODO
		raise openexp.exceptions.canvas_error( \
			"openexp._canvas.xpyriment.flip(): the flip() function has not been implemented for the psycho back-end!")		
		
	def copy(self, canvas):
	
		"""See openexp._canvas.legacy"""
		
		self.stim_list = [stim.copy() for stim in canvas.stim_list]
		self.font_style = canvas.font_style
		self.font_style = canvas.font_style
		self.penwidth = canvas.penwidth
		self.aa = canvas.aa
		self.fgcolor = canvas.fgcolor
		self.bgcolor = canvas.bgcolor		
		
	def show(self):
		
		"""See openexp._canvas.legacy"""
		
		for stim in self.stim_list[:-1]:
			stim.present(clear=False, update=False)
		self.stim_list[-1].present(clear=False)
		return self.experiment.time()
		
	def clear(self, color=None):
	
		"""See openexp._canvas.legacy"""
		
		if color != None: color = self.color(color)
		else: color = self.bgcolor		
		self.stim_list = [stimuli.BlankScreen(color)]
		
	def fixdot(self, x=None, y=None, color=None):
		
		"""See openexp._canvas.legacy"""

		if color != None: color = self.color(color)
		else: color = self.fgcolor		
		if x == None: x = self.xcenter()			
		if y == None: y = self.ycenter()					
		stim = stimuli.Circle(16, colour=color, position=c2p((x,y)))
		stim.preload()		
		self.stim_list.append(stim)
		stim = stimuli.Circle(4, colour=self.bgcolor, position=c2p((x,y)))	
		stim.preload()		
		self.stim_list.append(stim)		
		
	def line(self, sx, sy, ex, ey, color=None):
		
		"""See openexp._canvas.legacy"""
		
		if color != None: color = self.color(color)
		else: color = self.fgcolor		
		stim = stimuli.Line(c2p((sx,sy)), c2p((ex,ey)), line_width= \
			self.penwidth, colour=color, anti_aliasing=self.aa)
		stim.preload()			
		self.stim_list.append(stim)
		
	def rect(self, x, y, w, h, fill=False, color=None):
		
		"""See openexp._canvas.legacy"""

		if fill:		
			if color != None: color = self.color(color)
			else: color = self.fgcolor			
			# The position of the stimulus is the center, not the top-left
			pos = c2p((x+w/2,y+h/2))
			stim = stimuli.Rectangle(size=(w,h), position=pos, colour= \
				color, anti_aliasing=self.aa)
			stim.preload()
			self.stim_list.append(stim)
		# Unfilled shapes are drawn using lines			
		else:
			self.line(x, y, x+w, y, color=color)
			self.line(x, y, x, y+h, color=color)
			self.line(x+w, y, x+w, y+h, color=color)
			self.line(x, y+h, x+w, y+h, color=color)
			
	def ellipse(self, x, y, w, h, fill=False, color=None):
		
		"""See openexp._canvas.legacy"""
		
		if color != None: color = self.color(color)
		else: color = self.fgcolor
		if fill: line_width = 0
		else: line_width = self.penwidth
		pos = c2p((x+w/2,y+h/2))
		stim = stimuli.Ellipse((w, h), colour=color, line_width=line_width, \
			position=pos)
		stim.preload()
		self.stim_list.append(stim)
			
	def polygon(self, vertices, fill=False, color=None):
		
		"""See openexp._canvas.legacy"""
		
		if color != None: color = self.color(color)
		else: color = self.fgcolor
		if fill: line_width = 0
		else: line_width = self.penwidth		
		# The coordinate transformations are a bit awkard. Shape expects
		# a list of vertices that start form (0,0), but the position of the
		# shape is the center of the shape. So we first need to determine
		# the center of the polygon=(min+max)/2 and then convert the list
		# of vertices to a format that's acceptable to Shape			
		center = (min(p[0] for p in vertices) + \
			max(p[0] for p in vertices)) / 2, \
			(min(p[1] for p in vertices) + \
			max(p[1] for p in vertices)) / 2
		stim = stimuli.Shape(colour=color, position=c2p(center), \
			anti_aliasing=self.aa, line_width=line_width)
		l = p2v([c2p(p) for p in vertices])		
		for v in l: stim.add_vertex(v)
		stim.preload()
		self.stim_list.append(stim)						
				
	def text_size(self, text):
	
		"""See openexp._canvas.legacy"""
		
		try:
			_font = self.experiment.resource("%s.ttf" % self.font_style)
		except:
			_font = self.font_style					
		stim = stimuli.TextLine(text, text_font=_font, \
			text_size=self.font_size, text_bold=self.font_bold, \
			text_italic=self.font_italic)	
		surf = stim._create_surface()
		return surf.get_width(), surf.get_height()				
		
	def _text(self, text, x, y):
	
		"""See openexp._canvas.legacy"""
		
		try:			
			_font = self.experiment.resource("%s.ttf" % self.font_style)
		except:
			_font = self.font_style
			
		w, h = self.text_size(text)
		x += w/2
		y += h/2
			
		stim = stimuli.TextLine(text, position=c2p((x,y)), \
			text_colour=self.fgcolor, text_font=_font, \
			text_size=self.font_size, text_bold=self.font_bold, \
			text_italic=self.font_italic, text_underline=self.font_underline)			
		self.stim_list.append(stim)				
		
	def textline(self, text, line, color=None):
		
		"""See openexp._canvas.legacy"""
		
		size = self.text_size(text)
		self.text(text, True, self.xcenter(), self.ycenter()+1.5*line*size[1], \
			color=color)				
		
	def image(self, fname, center=True, x=None, y=None, scale=None):
		
		"""See openexp._canvas.legacy"""
		
		if x == None: x = self.xcenter()
		if y == None: y = self.ycenter()
		if center == False:
			surf = pygame.image.load(fname)
			if scale == None:
				x += surf.get_width()/2
				y += surf.get_height()/2
			else:
				x += scale*surf.get_width()/2
				y += scale*surf.get_height()/2			
		stim = stimuli.Picture(fname, position=c2p((x,y)))
		if scale != None: stim.scale( (scale, scale) )
		self.stim_list.append(stim)
		
	def gabor(self, x, y, orient, freq, env="gaussian", size=96, stdev=12, \
		phase=0, col1="white", col2="black", bgmode="avg"):

		"""See openexp._canvas.legacy"""
		
		surface = openexp._canvas.legacy._gabor(orient, freq, env, size, \
			stdev, phase, col1, col2, bgmode)
		stim = stimuli._visual.Visual(position=c2p((x,y)))
		stim._surface = surface
		stim.preload()		
		self.stim_list.append(stim)
		
	def noise_patch(self, x, y, env="gaussian", size=96, stdev=12, \
		col1="white", col2="black", bgmode="avg"):
		
		"""See openexp._canvas.legacy"""
		
		surface = openexp._canvas.legacy._noise_patch(env, size, stdev, col1, \
			col2, bgmode)
		stim = stimuli._visual.Visual(position=c2p((x,y)))
		stim._surface = surface
		stim.preload()
		self.stim_list.append(stim)

"""
Static methods
"""

def init_display(experiment):

	"""See openexp._canvas.legacy"""

	global exp
	
	# Configure Expyriment
	io.defaults.mouse_track_button_events = False	
	control.defaults.initialize_delay = 0
	control.defaults.event_logging = 0
	control.defaults.window_mode = experiment.get('fullscreen') == 'no'
	control.defaults.fast_quit = True
	control.defaults.window_size = experiment.resolution()
	control.defaults.auto_create_subject_id = True	
	control.defaults.open_gl = experiment.get_check('expyriment_opengl', \
		xpyriment.settings['expyriment_opengl']['default']) == 'yes'
	
	# Initialize
	exp = control.initialize()	
	experiment._time_func = _time
	experiment._sleep_func = exp.clock.wait
	experiment.time = experiment._time_func
	experiment.sleep = experiment._sleep_func
	experiment.window = exp.screen._surface
	experiment.expyriment = exp
	
	# TODO: In order to set the window title and to allow mouse responses we
	# need to bypass expyriment for now
	import pygame
	pygame.display.set_caption('OpenSesame (Expyriment backend)')
	pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
	pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
					
def close_display(experiment):

	"""See openexp._canvas.legacy"""
	
	control.end()
	
def _time():

	"""See openexp._canvas.legacy"""

	global exp
	return exp.clock.time
		

