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
import os

class trial:
	
	def __init__(self, experiment):
		
		"""
		Initializes the trial
		"""
		
		self.rt = 0
		self.correct = True
		self.trialid = 0
		self.experiment = experiment
		
	def run(self):
		
		"""
		Override this function to implement the trial
		"""
		
		None
		
	def sleep(self, ms):
		
		"""
		Sleeps for a given time
		"""
		
		pygame.time.delay(ms)
		
	def time(self):
		
		"""
		Returns a timestamp of the current time
		"""
		
		return pygame.time.get_ticks()
	
	def log(self, msg):
		
		"""
		Write a message to the log file
		"""
		
		self.experiment.log.write("%s\n" % msg)
		
	def flush_log(self):
		
		"""
		Makes sure that the log is written to disk
		"""
		
		self.experiment.log.flush()
		os.fsync(self.experiment.log)
		
	def prepare(self):
		
		"""
		Do some preparatory stuff before running the trial
		"""
		
		self.log("start_trial = %d" % self.trialid)
		
	def finalize(self):
		
		"""
		Do some finalizing after running the trial
		"""
		
		self.log("rt = %d" % self.rt)
		self.log("correct = %s" % self.correct)
		self.log("end_trial\n")
		self.flush_log()
		
