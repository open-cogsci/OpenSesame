#-*- coding:utf-8 -*-

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
from libopensesame import debug
from libopensesame.signalslot import signal
from libopensesame.exceptions import osexception

class generic_response:

	"""
	Deals with overlapping functionality for items that are able to process a
	reponse.
	"""

	auto_response = u"a"
	process_feedback = False

	def init_signals(self):

		"""See item."""

		self.on_response = signal(self.experiment, args=[],
			kwargs=['response', 'response_time', 'correct'])
		self.on_correct = signal(self.experiment, args=[],
			kwargs=['response', 'response_time', 'correct'])
		self.on_incorrect = signal(self.experiment, args=[],
			kwargs=['response', 'response_time', 'correct'])
		self.on_timeout = signal(self.experiment, args=[],
			kwargs=['response', 'response_time', 'correct'])

	def prepare_timeout(self):

		"""Prepares the response timeout"""

		if self.get(u"timeout") == u"infinite":
			self._timeout = None
		else:
			try:
				self._timeout = int(self.get(u"timeout"))
			except:
				raise osexception( \
					u"'%s' is not a valid timeout in keyboard_response '%s'. Expecting a positive integer or 'infinite'." \
					% (self.get(u"timeout"), self.name))
			if self._timeout < 0:
				raise osexception( \
					u"'%s' is not a valid timeout in keyboard_response '%s'. Expecting a positive integer or 'infinite'." \
					% (self.get(u"timeout"), self.name))

	def auto_responder(self, dev=u'keyboard'):

		"""
		Mimicks participant responses.

		Keyword arguments:
		dev		--	The device that should be simulated. (default=u'keyboard')

		Returns:
		A simulated (response_time, response) tuple
		"""

		if self._timeout == None:
			self.sleep(random.randint(200, 1000))
		else:
			self.sleep(random.randint(min(self._timeout, 200), self._timeout))

		if self._allowed_responses == None:
			resp = self.auto_response
		else:
			resp = random.choice(self._allowed_responses)

		debug.msg(u"generic_response.auto_responder(): responding '%s'" % resp)
		if dev == u'mouse':
			pos = random.randint(0, self.get(u'width')), random.randint( \
				0, self.get(u'height'))
			return resp, pos, self.time()
		return resp, self.time()

	def auto_responder_mouse(self):

		"""An ugly hack to make auto-response work for mouse_response items."""

		return self.auto_responder(dev=u'mouse')

	def process_response_keypress(self, retval):

		"""Process a keypress response"""

		self.experiment.start_response_interval = self.sri
		key, self.experiment.end_response_interval = retval
		self.experiment.response = self.sanitize(key)
		self.synonyms = self._keyboard.synonyms(self.experiment.response)

	def process_response_mouseclick(self, retval):

		"""Process a mouseclick response"""

		self.experiment.start_response_interval = self.sri
		self.experiment.response, pos, self.experiment.end_response_interval = \
			retval
		self.synonyms = self._mouse.synonyms(self.experiment.response)
		if pos != None:
			self.experiment.cursor_x = pos[0]
			self.experiment.cursor_y = pos[1]
		else:
			self.experiment.cursor_x = u'NA'
			self.experiment.cursor_y = u'NA'

	def process_response(self):

		"""A generic method for handling response collection"""

		# Wait for a fixed duration
		retval = self._duration_func()
		self.synonyms = None

		# If the duration function did not give any kind of return value
		# there is no response to process
		if retval == None:
			return

		process_func = u"process_response_%s" % self.get(u"duration")
		if hasattr(self, process_func):
			getattr(self, process_func)(retval)
		else:
			raise osexception( \
				u"Don't know how to process responses for duration '%s' in item '%s'" \
				% (self.get(u"duration"), self.name))

		self.response_bookkeeping()

	def response_bookkeeping(self):

		"""Do some bookkeeping for the response"""

		# The respone and response_time variables are always set, for every
		# response item
		self.experiment.set(u"response_time", \
			self.experiment.end_response_interval - \
			self.experiment.start_response_interval)
		self.experiment.set(u"response_%s" % self.get(u"name"), \
			self.get(u"response"))
		self.experiment.set(u"response_time_%s" % self.get(u"name"), \
			self.get(u"response_time"))
		self.experiment.start_response_interval = None

		# But correctness information is only set for dedicated response items,
		# such as keyboard_response items, because otherwise we might confound
		# the feedback
		if self.process_feedback:
			debug.msg(u"processing feedback for '%s'" % self.name)
			if self.has(u"correct_response"):
				# If a correct_response has been defined, we use it to determine
				# accuracy etc.
				correct_response = self.get(u"correct_response")
				if hasattr(self, u"synonyms") and self.synonyms != None:
					if correct_response in self.synonyms or \
						self.unistr(correct_response) in self.synonyms:
						self.experiment.correct = 1
						self.experiment.total_correct += 1
					else:
						self.experiment.correct = 0
				else:
					if self.experiment.response in (correct_response, \
						self.unistr(correct_response)):
						self.experiment.correct = 1
						self.experiment.total_correct += 1
					else:
						self.experiment.correct = 0
			else:
				# If a correct_response hasn't been defined, we simply set
				# correct to undefined
				self.experiment.correct = u"undefined"
			# Do some response bookkeeping
			self.experiment.total_response_time += self.experiment.response_time
			self.experiment.total_responses += 1
			self.experiment.set(u"acc", 100.0 * self.experiment.total_correct / \
				self.experiment.total_responses)
			self.experiment.set(u"avg_rt", self.experiment.total_response_time / \
				self.experiment.total_responses)
			self.experiment.set(u"accuracy", self.experiment.acc)
			self.experiment.set(u"average_response_time", self.experiment.avg_rt)
			self.experiment.set(u"correct_%s" % self.get(u"name"), \
				self.get(u"correct"))
			# Send signals
			self.on_response.emit(response=self.experiment.response,
				response_time=self.experiment.response_time,
				correct=self.experiment.correct)
			if self._timeout != None \
				and self.experiment.response_time >= self._timeout:
				self.on_timeout.emit(response=self.experiment.response,
					response_time=self.experiment.response_time,
					correct=self.experiment.correct)
			elif self.experiment.correct == 1:
				self.on_correct.emit(response=self.experiment.response,
					response_time=self.experiment.response_time,
					correct=self.experiment.correct)
			elif self.experiment.correct == 0:
				self.on_incorrect.emit(response=self.experiment.response,
					response_time=self.experiment.response_time,
					correct=self.experiment.correct)

	def set_sri(self, reset=False):

		"""
		Sets the start of the response interval

		Keyword arguments:
		reset -- determines whether the start of the response interval should
				 be reset to the start of the current item (default=False)
		"""

		if reset:
			self.sri = self.get(u"time_%s" % self.name)
			self.experiment.start_response_interval = self.get("time_%s" % \
				self.name)

		if self.experiment.start_response_interval == None:
			self.sri = self.get(u"time_%s" % self.name)
		else:
			self.sri = self.experiment.start_response_interval

	def prepare_timeout(self):

		"""Prepare the response timeout"""

		# Set the timeout
		if not self.has(u"timeout") or self.get(u"timeout") == u"infinite":
			self._timeout = None
		else:
			try:
				self._timeout = int(self.get(u"timeout"))
			except:
				raise osexception( \
					u"'%s' is not a valid timeout in item '%s'. Expecting a positive integer or 'infinite'." \
					% (self.get(u"timeout"), self.name))
			if self._timeout < 0:
				raise osexception( \
					u"'%s' is not a valid timeout in item '%s'. Expecting a positive integer or 'infinite'." \
					% (self.get(u"timeout"), self.name))

	def prepare_allowed_responses(self):

		"""Prepare the allowed responses"""

		# Prepare the allowed responses
		dur = self.get(u"duration")
		if self.has(u"allowed_responses"):
			if dur == u"keypress":

				# Prepare valid keypress responses
				l = self.experiment.unistr(self.get(u"allowed_responses")).split( \
					u";")
				self._allowed_responses = l

			elif dur == u"mouseclick":

				# Prepare valid mouseclick responses
				self._allowed_responses = []
				for r in self.experiment.unistr(self.get( \
					u"allowed_responses")).split(";"):
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
								raise osexception( \
									u"Unknown allowed_response '%s' in mouse_response item '%s'" \
									% (r, self.name))
						except Exception as e:
							raise osexception( \
								u"Unknown allowed_response '%s' in mouse_response item '%s'" \
								% (r, self.name), exception=e)

			# If allowed responses are provided, the list should not be empty
			if len(self._allowed_responses) == 0:
				raise osexception( \
					u"'%s' are not valid allowed responses in keyboard_response '%s'" \
					% (self.get(u"allowed_responses"), self.name))
		else:
			self._allowed_responses = None

	def prepare_duration(self):

		"""Prepare the duration"""

		if type(self.get(u"duration")) == int:

			# Prepare a duration in milliseconds
			self._duration = int(self.get(u"duration"))
			if self._duration == 0:
				self._duration_func = self.dummy
			else:
				self._duration_func = self.sleep_for_duration

		else:

			# Prepare a special duration, such as 'keypress', which are
			# handles by special functions
			prepare_func = u"prepare_duration_%s" % self.get(u"duration")
			if hasattr(self, prepare_func):
				getattr(self, prepare_func)()
			else:
				raise osexception( \
					u"'%s' is not a valid duration in item '%s'" % \
					(self.get(u"duration"), self.name))

	def prepare_duration_keypress(self):

		"""Prepare a keypress duration"""

		self._keyboard = openexp.keyboard.keyboard(self.experiment)
		if self.experiment.auto_response:
			self._duration_func = self.auto_responder
		else:
			self._keyboard.set_timeout(self._timeout)
			self._keyboard.set_keylist(self._allowed_responses)
			self._duration_func = self._keyboard.get_key

	def prepare_duration_mouseclick(self):

		"""Prepare a mouseclick duration"""

		self._mouse = openexp.mouse.mouse(self.experiment)
		if self.experiment.auto_response:
			self._duration_func = self.auto_responder_mouse
		else:
			# Prepare mouseclick
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

	def var_info(self):

		"""
		Return a list of dictionaries with variable descriptions

		Returns:
		A list of (name, description) tuples
		"""

		l = []
		l.append( (u"response", u"[Depends on response]") )
		l.append( (u"response_time", u"[Depends on response]") )
		l.append( (u"response_%s" % self.get(u"name", _eval=False), \
			u"[Depends on response]") )
		l.append( ("response_time_%s" % self.get(u"name", _eval=False), \
			u"[Depends on response]") )
		if self.process_feedback:
			l.append( (u"correct", u"[Depends on response]") )
			l.append( (u"correct_%s" % self.get(u"name", _eval=False), \
				u"[Depends on response]") )
			l.append( (u"average_response_time", u"[Depends on response]") )
			l.append( (u"avg_rt", u"[Depends on response]") )
			l.append( (u"accuracy", u"[Depends on response]") )
			l.append( (u"acc", u"[Depends on response]") )
		return l
