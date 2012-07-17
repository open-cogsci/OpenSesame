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
from expyriment import control, stimuli, misc, io
from expyriment.misc.geometry import coordinates2position as c2p, \
	points_to_vertices as p2v

class xpyriment(openexp._canvas.legacy.legacy):

	"""This is a canvas backend built on top of Expyriment"""	
	
	def __init__(self, experiment, bgcolor=None, fgcolor=None):
		
		"""See openexp._canvas.legacy"""
		
		self.experiment = experiment
		if fgcolor == None:
			fgcolor = self.experiment.get('foreground')
		if bgcolor == None:
			bgcolor = self.experiment.get('background')
		self.set_fgcolor(fgcolor)
		self.set_bgcolor(bgcolor)
		self.set_font(self.experiment.font_family, self.experiment.font_size)
		self.penwidth = 1
		self.ellipse_res = 100
		self.aa = 10
		self.clear()
		
	def set_font(self, style, size, italic=False, bold=False):
	
		"""See openexp._canvas.legacy"""
		
		self.font_style = style
		self.font_size = size
		self.font_italic = italic
		self.font_bold = bold		
				
	def flip(self, x=True, y=False):
		
		"""See openexp._canvas.legacy"""
		
		# TODO
		raise openexp.exceptions.canvas_error( \
			"openexp._canvas.xpyriment.flip(): the flip() function has not been implemented for the psycho back-end!")		
		
	def copy(self, canvas):
	
		"""See openexp._canvas.legacy"""
		
		self.stim_list = copy.deepcopy(canvas.stim_list)
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
		stim = stimuli.Dot(8, colour=color, position=c2p((x,y)))
		stim.preload()		
		self.stim_list.append(stim)
		stim = stimuli.Dot(2, colour=self.bgcolor, position=c2p((x,y)))	
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
			pos = c2p((x+w/2,y+w/2))
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
		
		h *= .5
		w *= .5
		l = np.linspace(0, 2*np.pi, self.ellipse_res)		
		if fill:
			_x = np.cos(l)*w + x+w
			_y = np.sin(l)*h + y+h
		else:
			x1 = np.cos(l)*w + x+w
			y1 = np.sin(l)*h + y+h
			l = np.linspace(2*np.pi, 0, self.ellipse_res)
			x2 = np.cos(l)*(w-self.penwidth) + x+w
			y2 = np.sin(l)*(h-self.penwidth) + y+h
			_x = np.concatenate((x1, x2))
			_y = np.concatenate((y1, y2))
		self.polygon(zip(_x, _y), fill=True, color=color)
			
	def polygon(self, vertices, fill=False, color=None):
		
		"""See openexp._canvas.legacy"""
		
		if fill:
			if color != None: color = self.color(color)
			else: color = self.fgcolor			
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
				anti_aliasing=self.aa)
			l = p2v([c2p(p) for p in vertices])		
			for v in l: stim.add_vertex(v)
			stim.preload()
			self.stim_list.append(stim)
		else:
			# Unfilled shapes are drawn using lines
			for i in range(len(vertices)-1):
				x1, y1 = vertices[i]
				x2, y2 = vertices[i+1]
				self.line(x1, y1, x2, y2, color=color)
				
	def text_size(self, text):
	
		"""See openexp._canvas.legacy"""
		
		stim = stimuli.TextLine(text, text_font=self.font_style, text_size= \
			self.font_size)
		return stim._create_surface().get_width(), \
			stim._create_surface().get_height()
				
	def text(self, text, center=True, x=None, y=None, color=None):
		
		"""See openexp._canvas.legacy"""
		
		if color != None: color = self.color(color)
		else: color = self.fgcolor
		if x == None: x = self.xcenter()
		if y == None: y = self.ycenter()		
		if center:
			dx = 0		
			dy = 0
		else:
			dx, dy = self.text_size(text)
			dx /= 2
			dy /= 2
		try:
			_font = self.experiment.resource("%s.ttf" % self.font_style)
		except:
			_font = self.font_style
		stim = stimuli.TextLine(text, position=c2p((x+dx,y+dy)), text_colour=color, \
			text_font=_font, text_size=self.font_size, text_bold=\
			self.font_bold, text_italic=self.font_italic)
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
	
	io.defaults.mouse_track_button_events = False	
	control.defaults.initialize_delay = 0
	control.defaults.event_logging = 0
	control.defaults.window_mode = experiment.get('fullscreen') == 'no'
	control.defaults.fast_quit = True
	control.defaults.window_size = experiment.get('width'), \
		experiment.get('height')
	control.defaults.auto_create_subject_id = True	
	exp = control.initialize()	
	experiment._time_func = _time
	experiment._sleep_func = exp.clock.wait
	experiment.time = experiment._time_func
	experiment.sleep = experiment._sleep_func
	experiment.window = exp.screen._surface
	
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
		

