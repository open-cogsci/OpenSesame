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

	def __init__(self, name, experiment, string=None):
	
		"""
		Constructor
		
		Arguments:
		name -- the item name
		experiment -- the experiment
		
		Keyword arguments:
		string -- a definitions tring (default=None)
		"""

		self.description = "Provides feedback to the participant"		
		self.reset_variables = "yes"		
		sketchpad.sketchpad.__init__(self, name, experiment, string)				
		self.item_type = "feedback"			
		
	def prepare(self):
		
		"""
		Prepare for running. In the case of the feedback display, this means
		doing nothing
		
		Returns:
		True
		"""
				
		return True
		
	def run(self):
	
		"""
		Run the item (ie., show the feedback item)
		
		Returns:
		True on success, False on Failure
		"""
		
		try:
			if not sketchpad.sketchpad.prepare(self):
				return False
		except exceptions.script_error as e:
			raise exceptions.runtime_error("Failed to create feedback item '%s'" % self.name)						
		if not sketchpad.sketchpad.run(self):
			return False			
		
		# Reset the bookkeeping		
		if self.reset_variables == "yes":
			self.experiment.reset_feedback()
						
