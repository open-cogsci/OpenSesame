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
from libqtopensesame.misc.config import cfg
import time

class undo_stack(object):

	def __init__(self):

		self.current = {}
		self.history = []
		self.future = []

	def set_current(self, key, state):

		self.current[key] = state, time.time()

	def add(self, key, state):

		self.future = []
		if key == u'__experiment__':
			self.history.append( (u'__experiment__', state) )
			return
		timestamp = time.time()
		if key in self.current:
			_state, _timestamp = self.current[key]
			if _state == state:
				return
			if _timestamp >= timestamp-1:
				self.current[key] = state, timestamp
				return
			self.history.append( (key, self.current[key][0]) )
		self.current[key] = state, timestamp
		if len(self.history) > cfg.max_undo_history:
			self.history = self.history[-cfg.max_undo_history:]

	def can_undo(self):

		return len(self.history) > 0

	def can_redo(self):

		return len(self.future) > 0

	def __len__(self):

		return len(self.history)

	def pop(self, l1, l2):

		if len(l1) == 0:
			return None, None
		key, state = l1.pop()
		if key == u'__experiment__':
			self.future = []
			_key, _state = l1.pop()
			if _key != u'__experiment__':
				return None, None
			return _key, _state
		l2.append( (key, self.current[key][0]) )
		self.current[key] = state, time.time()
		return key, state

	def undo(self):

		return self.pop(self.history, self.future)

	def redo(self):

		return self.pop(self.future, self.history)

	def peek(self, i=-1):

		if len(self.history) == 0:
			return None, None
		return self.history[i]
