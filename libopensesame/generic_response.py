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

import random

class generic_response:

	def prepare_timeout(self):
	
		"""
		Prepares the response timeout
		"""

		if self.get("timeout") == "infinite":
			self._timeout = None
		else:
			try:
				self._timeout = int(self.get("timeout"))
			except:
				raise exceptions.runtime_error("'%s' is not a valid timeout in keyboard_response '%s'. Expecting a positive integer or 'infinite'." % (self.get("timeout"), self.name))				
			if self._timeout < 0:
				raise exceptions.runtime_error("'%s' is not a valid timeout in keyboard_response '%s'. Expecting a positive integer or 'infinite'." % (self.get("timeout"), self.name))											
				
	def auto_responder(self, allowed_responses, timeout):
	
		"""
		Mimick participant responses
		"""			
		
		if timeout == None:
			self.sleep(random.randint(200, 1000))
		else:
			self.sleep(random.randint(min(timeout, 200), timeout))
		
		if allowed_responses == None:
			return self.auto_response
			
		return self.time(), random.choice(allowed_responses)
				
	def process_response(self, correct_response):
	
		"""
		Does some bookkeeping for the response
		collection.
		"""
	
		if correct_response == "undefined":
			self.experiment.correct = "undefined"		
		else:
			if self.experiment.response == correct_response:
				self.experiment.correct = 1
				self.experiment.total_correct += 1
			else:
				self.experiment.correct = 0
				
		self.experiment.acc = 100.0 * self.experiment.total_correct / self.experiment.total_responses
		self.experiment.avg_rt = self.experiment.total_response_time / self.experiment.total_responses
		
		self.experiment.accuracy = self.experiment.acc
		self.experiment.average_response_time = self.experiment.avg_rt
				
		self.experiment.start_response_interval = None								
