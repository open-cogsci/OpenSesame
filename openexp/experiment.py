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
		
		"""
		Initializes the experiment
		"""
				
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
		self.sound_backend = "legacy"

		# Display parameters
		self.resolution = 1024, 768
		self.fullscreen = False
		
		self.title = "OpenExp"
					
		self.font_size = 18
		self.font_family = "mono"
		
		self.trials = []	
		self.logfile = None	
		
		random.seed()	
		
	def init_experiment(self):
		
		"""
		Override this function to set some general settings for the experiment
		"""			
		
		return
		
	def init_sound(self):
	
		"""
		Intializes the pygame mixer
		"""
		
		sampler.freq = self.sound_freq
		print "experiment.init_sound(): sampling freq = %d, buffer size = %d" % (self.sound_freq, self.sound_buf_size)		
		pygame.mixer.pre_init(self.sound_freq, self.sound_sample_size, self.sound_channels, self.sound_buf_size)
		
	def init_icon(self):
	
		"""
		Set the window icon
		"""
		
		surf = pygame.Surface( (32, 32) )
		surf.fill( (255, 255, 255) )
		pygame.draw.circle(surf, (0, 0, 255), (16, 16), 10, 4)
		pygame.display.set_icon(surf)
		
	def init_display(self, defaultlog = False):
		
		"""
		Initializes the display
		"""
				
		canvas.init_display(self)
				
	def init_trials(self):
		
		"""
		Override this function to generate the trial list
		"""
		
		self.trials = []
		
	def init_log(self):
	
		"""
		Open the logile
		"""
		
		# Open the logfile
		if self.logfile != None:
			self.log = open(self.logfile, "w")
		else:
			self.logfile = "defaultlog.txt"
			self.log = open("defaultlog.txt", "w")		
			
		print "experiment.init_log(): using '%s' as logfile" % self.logfile		
		
	def run(self):
		
		"""
		Runs all trials
		"""
		
		self.init_experiment()
		self.init_sound()				
		self.init_display()		
		self.init_trials()		
		self.init_log()

		if type(self.trials) != list or len(self.trials) == 0:			
			warnings.warn("experiment.trials should be a non-empty list")
		
		if self.order == "random":
			random.shuffle(self.trials)
		elif self.order != "sequential":
			warnings.warn("experiment.order should be 'random' or 'sequential', not '%s'. Falling back to 'sequential'." % self.order)		
					
		self.feedback_start_experiment()
		
		# Run the practice trials
		if self.nr_practice_trials > 0:			
			trialid = 0
			avg_rt = 0.0
			avg_correct = 0.0
			block_nr = 1
			for trial in self.trials[:self.nr_practice_trials]:
				trial.trialid = 10000 + trialid # Practice trials have a trialid >= 10000
				trial.prepare()
				trial.run()											
				trial.finalize()													
				trialid += 1
				
				avg_rt += trial.rt / self.nr_practice_trials_per_block
				if trial.correct:
					avg_correct += 100.0 / self.nr_practice_trials_per_block
				
				if self.nr_practice_trials_per_block > 0 and trialid % self.nr_practice_trials_per_block == 0:					
					self.feedback_end_block(True, block_nr, self.nr_practice_trials / self.nr_practice_trials_per_block, avg_rt, avg_correct)
					avg_rt = 0.0
					avg_correct = 0.0
					block_nr += 1
					
			self.feedback_end_practice()

			if self.order == "random":
				random.shuffle(self.trials)					
		
		# Run the experimental trials
		trialid = 0
		avg_rt = 0.0
		avg_correct = 0.0
		block_nr = 1	
		for trial in self.trials:
			trial.trialid = trialid
			trial.prepare()
			trial.run()											
			trial.finalize()
			trialid += 1
			
			avg_rt += trial.rt / self.nr_trials_per_block
			if trial.correct:
				avg_correct += 100.0 / self.nr_trials_per_block
			
			if self.nr_trials_per_block > 0 and trialid % self.nr_trials_per_block == 0:					
				self.feedback_end_block(False, block_nr, len(self.trials) / self.nr_trials_per_block, avg_rt, avg_correct)
				avg_rt = 0.0
				avg_correct = 0.0
				block_nr += 1		
			
		self.feedback_end_experiment()
		
		self.end()
		
	def feedback_end_block(self, practice, current_block, nr_of_blocks, avg_rt, avg_correct):
		
		"""
		Provides feedback after every block
		"""
		
		c = canvas.canvas(self, self.bg_color)
		c.set_fgcolor(self.fg_color)
		c.textline("Einde van blok %d van %d" % (current_block, nr_of_blocks), -2)
		c.textline("Reactiesnelheid: %dms" % avg_rt, -1)
		c.textline("Percentage correct: %.0f%%" % avg_correct, 0)
		c.textline("Druk op een toets om verder te gaan", 2)
		c.show()		
		self.wait()
		
	def feedback_end_practice(self):
		
		"""
		Provides feedback after the practice phae
		"""		
		
		c = canvas.canvas(self, self.bg_color)
		c.set_fgcolor(self.fg_color)		
		c.textline("Einde van de oefenphase", -2)
		c.textline("Het echte experiment begint nu", -1)
		c.textline("Druk op een toets om verder te gaan", 1)
		c.show()		
		self.wait()		
		
	def feedback_start_experiment(self):
		
		"""
		Provides feedback before the experiment
		"""		
		
		c = canvas.canvas(self, self.bg_color)
		c.set_fgcolor(self.fg_color)		
		c.textline("Druk op een toets om te beginnen", 0)
		c.show()		
		self.wait()		
		
	def feedback_end_experiment(self):
		
		"""
		Provides feedback after the experiment
		"""		
		
		c = canvas.canvas(self, self.bg_color)
		c.set_fgcolor(self.fg_color)		
		c.textline("Het experiment is afgelopen", -1)
		c.textline("Bedankt voor het meedoen!", 0)
		c.show()		
		self.wait()
		
	def wait(self):
	
		"""
		Waits until a key has been pressed. Override
		this function to use a different wait method,
		such as a buttonbox press.
		"""
		
		response.get_key()		
		
	def end(self):
	
		"""
		Exit the experiment
		"""
		
		try:
			self.log.close()		
		except:
			pass
			
		pygame.mixer.quit()
		canvas.close_display(self)
		
	def resource(self, name):
	
		"""
		Get a file from the resources folder
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
		
