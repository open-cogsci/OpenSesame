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

from libopensesame.py3compat import *
from libopensesame.item import item
from libopensesame.exceptions import osexception

class base_response_item(item):

	process_feedback = False

	def prepare_response_func(self):

		raise NotImplementedError()

	def validate_response(self, response):

		return True

	def response_matches(self, test, ref):

		return test == ref

	def process_response(self, response_args):

		response, t1 = response_args
		if u'correct_response' in self.var:
			correct = self.response_matches(response, self.var.correct_response)
		else:
			correct = None
		self.responses.add(response=response, response_time=t1-self._t0,
			correct=correct, item=self.name, feedback=self.process_feedback)

	def prepare(self):

		self._timeout = self._prepare_timeout()
		self._allowed_responses = self._prepare_allowed_responses()
		self._collect_response = self.prepare_response_func()
		self._t0 = None

	def run(self):

		if self._t0 is None:
			self._t0 = self.set_item_onset()
		retval = self._collect_response()
		if retval is None:
			return
		self.process_response(retval)

	def var_info(self):

		l = []
		l.append( (u"response", u"[Depends on response]") )
		l.append( (u"response_time", u"[Depends on response]") )
		l.append( (u"response_%s" % self.name, u"[Depends on response]") )
		l.append( ("response_time_%s" % self.name, u"[Depends on response]") )
		if self.process_feedback:
			l.append( (u"correct", u"[Depends on response]") )
			l.append( (u"correct_%s" % self.name, u"[Depends on response]") )
			l.append( (u"average_response_time", u"[Depends on response]") )
			l.append( (u"avg_rt", u"[Depends on response]") )
			l.append( (u"accuracy", u"[Depends on response]") )
			l.append( (u"acc", u"[Depends on response]") )
		return item.var_info(self) + l

	# Private functions

	def _prepare_timeout(self):

		timeout = self.var.get(u'timeout', default=u'infinite')
		if timeout == u'infinite':
			return
		try:
			timeout = int(timeout)
			assert(timeout >= 0)
		except:
			raise osexception(
				u"'%s' is not a valid timeout. Expecting a positive integer or 'infinite'." \
				% timeout)
		return timeout

	def _prepare_allowed_responses(self):

		allowed_responses = safe_decode(
			self.var.get(u'allowed_responses', default=u''))
		if allowed_responses == u'':
			return
		if py3:
			allowed_responses = [r.strip() \
				for r in allowed_responses.split(';')]
		else:
			allowed_responses = [safe_decode(r.strip()) \
				for r in safe_encode(allowed_responses).split(';')]
		for r in allowed_responses:
			if not self.validate_response(r):
				raise osexception(u'Invalid value in allowed_responses: %s' % r)
		# If allowed responses are provided, the list should not be empty
		if not allowed_responses:
			raise osexception(u'allowed_responses should not be an empty list')
		return allowed_responses

	def _prepare_sleep_func(self, duration):

		if duration == 0:
			return lambda: None
		if self.var.duration > 0:
			return lambda: self.clock.sleep(self.var.duration)
		raise osexception(u'Duration should not be negative')
