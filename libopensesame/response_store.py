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
from libopensesame.exceptions import osexception


class response(object):

	"""
	desc:
		A single response.
	"""

	def __init__(self, response_store, response=None, correct=None,
		response_time=None, item=None, feedback=True):

		self._response_store = response_store

		# Sanity checks
		if not isinstance(response_time, (int, float)) and \
			response_time is not None:
			raise osexception(u'response should be a numeric value or None')
		if response_time is None:
			self.response_time = None
		else:
			self.response_time = float(response_time)
		self.response = response
		self.item = item
		self.feedback = feedback
		if correct not in (0, 1, True, False, None):
			raise osexception(
				u'correct should be 0, 1, True, False, or None')
		if correct is None:
			self.correct = None
		else:
			self.correct = int(correct)

	def match(self, **kwdict):

		for key, val in kwdict.items():
			if getattr(self, key) != val:
				return False
		return True

	def matchnot(self, **kwdict):

		for key, val in kwdict.items():
			if getattr(self, key) == val:
				return False
		return True

	def __str__(self):

		return u'response(response=%s,response_time=%s,correct=%s,item=%s,feedback=%s)' \
			% (self.response, self.response_time, self.correct, self.item, \
			self.feedback)


class response_store(object):

	def __init__(self, experiment):

		self._experiment = experiment
		self._responses = []
		self._feedback_from = 0

	@property
	def acc(self):

		l = self.select(feedback=True).selectnot(correct=None).correct
		if not l:
			return u'undefined'
		return 100.*sum(l)/len(l)

	@property
	def avg_rt(self):

		l = self.select(feedback=True).selectnot(response_time=None) \
			.response_time
		if not l:
			return u'undefined'
		return 1.*sum(l)/len(l)

	@property
	def response(self):

		return [r.response for r in self._responses]

	@property
	def correct(self):

		return [r.correct for r in self._responses]

	@property
	def response_time(self):

		return [r.response_time for r in self._responses]

	@property
	def item(self):

		return [r.item for r in self._responses]

	@property
	def feedback(self):

		return [r.item for r in self._responses]

	@property
	def var(self):

		return self._experiment.var

	def add(self, **kwdict):

		if u'response' not in kwdict or u'response_time' not in kwdict \
			or u'correct' not in kwdict:
			raise osexception(
				u'response, response_time, and correct are required keywords')
		r = response(self, **kwdict)
		if r.correct is None:
			correct = u'undefined'
		else:
			correct = r.correct
		self._responses.append(r)
		self.var.response = r.response
		self.var.response_time = r.response_time
		self.var.correct = correct
		if u'item' in kwdict:
			self.var.set(u'response_%s' % kwdict[u'item'], r.response)
			self.var.set(u'response_time_%s' % kwdict[u'item'], r.response_time)
			self.var.set(u'correct_%s' % kwdict[u'item'], correct)
		self.var.acc = self.var.accuracy = self.acc
		self.var.avg_rt = self.avg_rt
		# Old variables, mostly for backwards compatibility
		rs = self.select(feedback=True)
		self.var.accuracy = self.var.acc
		self.var.average_response_time = self.var.avg_rt
		self.var.total_response_time = sum(
			rs.selectnot(response_time=None).response_time)
		self.var.total_responses = len(rs)
		self.var.total_correct = len(rs.select(correct=1))

	def reset_feedback(self):

		for r in self._responses:
			r.feedback = False

	def select(self, **kwdict):

		rs = response_store(self._experiment)
		for r in self._responses:
			if r.match(**kwdict):
				rs._responses.append(r)
		return rs

	def selectnot(self, **kwdict):

		rs = response_store(self._experiment)
		for r in self._responses:
			if r.matchnot(**kwdict):
				rs._responses.append(r)
		return rs

	def __len__(self):

		return len(self._responses)

	def __getitem__(self, key):

		return self._responses[key]

	def __str__(self):

		s = u'%d responses (last first):\n' % len(self)
		for r in self[::-1]:
			s += str(r) + u'\n'
		return s
