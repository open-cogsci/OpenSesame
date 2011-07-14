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

from openexp import trial, canvas, sampler
import warnings
import random
import os.path
import pygame
from pygame.locals import *

class experiment:
	
	def __init__(self):
		
		"""Constructor"""
				
		self.order = "random"		
		self.nr_trials_per_block = 0		
		self.nr_practice_trials = 0
		self.nr_practice_trials_per_block = 0
		self.bg_color = 0, 0, 0
		self.fg_color = 255, 255, 255
		self.sound_freq = 48000
		self.sound_sample_size = -16 # Negative values means signed sample values, see PyGame doc
		self.sound_channels = 2
		self.sound_buf_size = 512
		self.resources = {}
		
		# Backend parameters
		self.canvas_backend = "legacy"
		self.keyboard_backend = "legacy"
		self.mouse_backend = "legacy"
		self.sampler_backend = "legacy"
		self.synth_backend = "legacy"

		# Display parameters
		self.resolution = 1024, 768
		self.fullscreen = False
		
		self.title = "OpenExp"
					
		self.font_size = 18
		self.font_family = "mono"
		
		self.trials = []	
		self.logfile = None	
		
		random.seed()	
				
	def init_sound(self):
	
		"""Intialize the pygame mixer"""
		
		sampler.freq = self.sound_freq
		print "experiment.init_sound(): sampling freq = %d, buffer size = %d" % (self.sound_freq, self.sound_buf_size)		
		pygame.mixer.pre_init(self.sound_freq, self.sound_sample_size, self.sound_channels, self.sound_buf_size)
				
	def init_display(self, defaultlog = False):
		
		"""Initialize the canvas backend"""
				
		canvas.init_display(self)				
		
	def init_log(self):
	
		"""Open the logile"""
		
		# Open the logfile
		if self.logfile != None:
			self.log = open(self.logfile, "w")
		else:
			self.logfile = "defaultlog.txt"
			self.log = open("defaultlog.txt", "w")		
			
		print "experiment.init_log(): using '%s' as logfile" % self.logfile	
		
	def _time(self):
	
		"""
		This function is used for timing, but should be set
		by the canvas backend. See openexp._canvas.legacy.init_display()
		for an example.
		"""
		
		raise openexp.exceptions.openexp_error("experiment._time(): This function should be set by the canvas backend.")
		
	def end(self):
	
		"""End the experiment"""
		
		try:
			self.log.close()		
		except:
			pass
			
		pygame.mixer.quit()
		canvas.close_display(self)
		
	def resource(self, name):
	
		"""
		Retrieve a file from the resources folder
		
		Arguments:
		name -- the file name
		
		Returns:
		The full path to the file in the resources folder
		"""
		
		if name in self.resources:
			return self.resources[name]
		
		path = os.path.join("resources", name)
		
		if os.path.exists(path):
			return os.path.join("resources", name)		
		
		if os.name == "posix":
			path = "/usr/share/opensesame/resources/%s" % name
			if os.path.exists(path):
				return path				
				
		raise Exception("The resource '%s' could not be found in libqtopensesame.experiment.resource()" % name)
		
