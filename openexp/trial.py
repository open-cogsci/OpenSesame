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

	"""
	Contains some basic functionality, but is essentially a remnant of the
	time when the openexp libraries were used to create an entire experiment,
	rather than as a back-end for the new, more advanced libopensesame modules
	"""
	
	def __init__(self, experiment):
		
		"""
		Constructor

		Arguments:
		experiment -- the experiment
		"""
		
		self.rt = 0
		self.correct = True
		self.trialid = 0
		self.experiment = experiment
		
	def run(self):
		
		"""Override this function to implement a trial"""
		
		pass
		
	def sleep(self, ms):
		
		"""<DOC>
		Sleep for a specified duration

		Arguments:
		ms -- a duration in milliseconds
		</DOC>"""
		
		pygame.time.delay(ms)
		
	def time(self):
		
		"""<DOC>
		Return current time

		Returns:
		A timestamp of the current time
		</DOC>"""
		
		return self.experiment._time_func()
	
	def log(self, msg):
		
		"""<DOC>
		Write a message to the log file

		msg -- a message
		</DOC>"""
		
		self.experiment.log.write("%s\n" % msg)
		
	def flush_log(self):
		
		"""<DOC>
		Force any pending write operations to the log file to be written
		to disk
		</DOC>"""
		
		self.experiment.log.flush()
		os.fsync(self.experiment.log)
		
	def prepare(self):
		
		"""Do some preparatory stuff before running the trial"""
		
		self.log("start_trial = %d" % self.trialid)
		
	def finalize(self):
		
		"""Do some finalizing after running the trial"""
		
		self.log("rt = %d" % self.rt)
		self.log("correct = %s" % self.correct)
		self.log("end_trial\n")
		self.flush_log()
		
