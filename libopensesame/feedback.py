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

from libopensesame import sketchpad, exceptions
import shlex

class feedback(sketchpad.sketchpad):

	def __init__(self, name, experiment, string = None):
	
		"""
		Initialize the feedback
		"""

		self.description = "Provides feedback to the participant"		
		sketchpad.sketchpad.__init__(self, name, experiment, string)				
		self.item_type = "feedback"			
		
	def prepare(self):
		
		"""
		The feedback display does it's preparation
		during the run phase
		"""
		
		return True
		
	def run(self):
	
		"""
		Do the actual logging
		"""
		
		try:
			if not sketchpad.sketchpad.prepare(self):
				return False
		except exceptions.script_error as e:
			raise exceptions.runtime_error("Failed to create feedback item '%s'" % self.name)
			
		# Reset the bookkeeping
		self.experiment.total_responses = 0
		self.experiment.total_correct = 0
		self.experiment.total_response_time = 0
			
		return sketchpad.sketchpad.run(self)			
						
