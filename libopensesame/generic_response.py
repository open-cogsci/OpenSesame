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
import openexp.keyboard
import openexp.mouse
from libopensesame import exceptions

class generic_response:

	"""
	Deals with overlapping functionality for response items, such as

	Core items:
	- keyboard_response
	- mouse_response
	- synth
	- sampler (via synth)

	(Known) plug-ins
	- text_input
	- text_display
	- media_player
	- srbox
	"""

	def prepare_timeout(self):

		"""Prepares the response timeout"""

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

		Arguments:
		allowed_responses -- a list with allowed responses
		timeout -- the timout

		Returns:
		A simulated (response_time, response) tuple
		"""

		if timeout == None:
			self.sleep(random.randint(200, 1000))
		else:
			self.sleep(random.randint(min(timeout, 200), timeout))

		if allowed_responses == None:
			return self.auto_response

		return self.time(), random.choice(allowed_responses)

	def process_response_keypress(self, retval):

		"""Process a keypress response"""

		self.experiment.start_response_interval = self.sri			
		key, self.experiment.end_response_interval = retval
		self.experiment.response = self._keyboard.to_chr(key)

	def process_response_mouseclick(self, retval):

		"""Process a mouseclick response"""

		self.experiment.start_response_interval = self.sri			
		self.experiment.response, pos, self.experiment.end_response_interval = retval		
		
	def process_response(self):

		"""A generic method for handling response collection"""

		# Wait for a fixed duration
		retval = self._duration_func()

		# If the duration function did not give any kind of return value
		# there is no response to process
		if retval == None:
			return

		process_func = "process_response_%s" % self.get("duration")
		if hasattr(self, process_func):
			exec("self.%s(retval)" % process_func)
		else:
			raise exceptions.runtime_error("Don't know how to process responses for duration '%s' in item '%s'" % (self.get("duration"), self.name))

		self.response_bookkeeping()

	def response_bookkeeping(self):

		"""Do some bookkeeping for the response"""

		# Set the correct response
		if self.has("correct_response"):
			correct_response = self.get("correct_response")
		else:
			correct_response = "undefined"			
		
		if correct_response == "undefined":
			self.experiment.correct = "undefined"
		else:
			if self.experiment.response == correct_response:
				self.experiment.correct = 1
				self.experiment.total_correct += 1
			else:
				self.experiment.correct = 0

		self.experiment.set("response_time", self.experiment.end_response_interval - self.experiment.start_response_interval)
		self.experiment.total_response_time += self.experiment.response_time
		self.experiment.total_responses += 1
		self.experiment.set("acc", 100.0 * self.experiment.total_correct / self.experiment.total_responses)
		self.experiment.set("avg_rt", self.experiment.total_response_time / self.experiment.total_responses)
		self.experiment.set("accuracy", self.experiment.acc)
		self.experiment.set("average_response_time", self.experiment.avg_rt)
		self.experiment.start_response_interval = None

	def set_sri(self, reset = False):

		"""
		Sets the start of the response interval

		Keyword arguments:
		reset -- determines whether the start of the response interval should
				 should be reset to the start of the current item (default = False)
		"""

		if reset:
			self.sri = self.get("time_%s" % self.name)
			self.experiment.start_response_interval = self.get("time_%s" % self.name)

		if self.experiment.start_response_interval == None:
			self.sri = self.get("time_%s" % self.name)
		else:
			self.sri = self.experiment.start_response_interval		

	def prepare_timeout(self):

		"""Prepare the response timeout"""

		# Set the timeout
		if not self.has("timeout") or self.get("timeout") == "infinite":
			self._timeout = None
		else:
			try:
				self._timeout = int(self.get("timeout"))
			except:
				raise exceptions.runtime_error("'%s' is not a valid timeout in item '%s'. Expecting a positive integer or 'infinite'." % (self.get("timeout"), self.name))
			if self._timeout < 0:
				raise exceptions.runtime_error("'%s' is not a valid timeout in item '%s'. Expecting a positive integer or 'infinite'." % (self.get("timeout"), self.name))				

	def prepare_compensation(self):

		"""Prepare the duration compensation"""

		# Prepare the compensation function
		if self.has("compensation"):
			try:
				self._compensation = int(self.get("compensation"))
			except:
				raise exceptions.runtime_error("Variable 'compensation' should be numeric and not '%s' in %s item '%s'" % (self.get("compensation"), self.item_type, self.name))
		else:
			self._compensation = 0

	def prepare_allowed_responses(self):

		"""Prepare the allowed responses"""

		# Prepare the allowed responses
		dur = self.get("duration")				
		if self.has("allowed_responses"):
			if dur == "keypress":

				# Prepare valid keypress responses
				l = str(self.get("allowed_responses")).split(";")
				self._allowed_responses = l
				
			elif dur == "mouseclick":
				
				# Prepare valid mouseclick responses
				self._allowed_responses = []
				for r in str(self.get("allowed_responses")).split(";"):
					if r in self.resp_codes.values():
						for code, resp in self.resp_codes.items():
							if resp == r:
								self._allowed_responses.append(code)
					else:
						try:
							r = int(r)
							if r in self.resp_codes:
								self._allowed_responses.append(r)
							else:
								raise exceptions.runtime_error("Unknown allowed_response '%s' in mouse_response item '%s'" % (r, self.name))
						except ValueError:
							raise exceptions.runtime_error("Unknown allowed_response '%s' in mouse_response item '%s'" % (r, self.name))

			# If allowed responses are provided, the list should not be empty
			if len(self._allowed_responses) == 0:
				raise exceptions.runtime_error("'%s' are not valid allowed responses in keyboard_response '%s'" % (self.get("allowed_responses"), self.name))
		else:
			self._allowed_responses = None		

	def prepare_duration(self):

		"""Prepare the duration"""

		if type(self.get("duration")) == int:

			# Prepare a duration in milliseconds
			self._duration = int(self.get("duration"))			
			if self._duration == 0:
				self._duration_func = self.dummy
			else:
				self.prepare_compensation()
				if self._compensation != 0:
					self._duration_func = self.sleep_for_comp_duration
				else:
					self._duration_func = self.sleep_for_duration

		else:

			# Prepare a special duration, such as 'keypress', which are
			# handles by special functions
			prepare_func = "prepare_duration_%s" % self.get("duration")
			if hasattr(self, prepare_func):
				exec("self.%s()" % prepare_func)
			else:
				raise exceptions.runtime_error("'%s' is not a valid duration in item '%s'" % (self.get("duration"), self.name))

	def prepare_duration_keypress(self):

		"""Prepare a keypress duration"""

		if self.experiment.auto_response:

			# Auto-response
			self._duration_func = self.sleep_for_duration
			self._duration = 500
		else:

			# Prepare keypress
			self._keyboard = openexp.keyboard.keyboard(self.experiment)
			self._keyboard.set_timeout(self._timeout)
			self._keyboard.set_keylist(self._allowed_responses)
			self._duration_func = self._keyboard.get_key

	def prepare_duration_mouseclick(self):

		"""Prepare a mouseclick duration"""

		if self.experiment.auto_response:

			# Auto-response
			self._duration_func = self.sleep_for_duration
			self._duration = 500
		else:		

			# Prepare mouseclick
			self._mouse = openexp.mouse.mouse(self.experiment)
			self._mouse.set_timeout(self._timeout)
			self._mouse.set_buttonlist(self._allowed_responses)				
			self._duration_func = self._mouse.get_click

	def prepare(self):
	
		"""A generic method for preparing a response item"""

		self.prepare_timeout()
		self.prepare_allowed_responses()
		self.prepare_duration()			

	def sleep_for_duration(self):
	
		"""Sleep for a specified time"""
		
		self.sleep(self._duration)	
		
	def sleep_for_comp_duration(self):
	
		"""Sleep for a specified time, taking the compensation into account"""
		
		self.sleep(self._duration - self._compensation)									

	def var_info(self):

		"""
		Return a list of dictionaries with variable descriptions

		Returns:
		A list of (name, description) tuples
		"""

		l = []
		l.append( ("response", "<i>Depends on response</i>") )
		l.append( ("correct", "<i>Depends on response</i>") )
		l.append( ("response_time", "<i>Depends on response</i>") )
		l.append( ("average_response_time", "<i>Depends on response</i>") )
		l.append( ("avg_rt", "<i>Depends on response</i>") )
		l.append( ("accuracy", "<i>Depends on response</i>") )
		l.append( ("acc", "<i>Depends on response</i>") )

		return l