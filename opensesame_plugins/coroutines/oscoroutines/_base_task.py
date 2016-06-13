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

class base_task(object):

	"""
	desc:
		A task controls the coroutine for one item.
	"""

	ALIVE = 0
	DEAD = 1
	ABORT = 2

	def __init__(self, coroutines, start_time, end_time):

		"""
		desc:
			Constructor.

		arguments:
			start_time:
				desc:	The start-time of the coroutine.
				type:	int
			end_time:
				desc:	The end-time of the coroutine.
				type:	int
		"""

		if not (isinstance(start_time, (int, float)) and start_time >= 0) or \
			not (isinstance(end_time, (int, float)) and end_time >= start_time):
			raise osexception(
				(u'Start (now: %s) and end (now: %s) time need to be '
				u'non-negative numeric values and end time needs to be equal to '
				u' or higher than start time') % (start_time, end_time))
		self.start_time = start_time
		self.end_time = end_time
		self.coroutines = coroutines

	def started(self, dt):

		"""
		arguments:
			dt:
				desc:	The current time relative to onset of the coroutines.
				type:	int

		returns:
			desc:	True if the current item is started, False otherwise.
			type:	bool
		"""

		return dt >= self.start_time

	def stopped(self, dt):

		"""
		desc:
			Checks whether an item is stopped, and sends the stop signal to the
			item if it should be stopped.

		arguments:
			dt:
				desc:	The current time relative to onset of the coroutines.
				type:	int

		returns:
			desc:	True if the current item is started, False otherwise.
			type:	bool
		"""

		if dt < self.end_time:
			return False
		try:
			self.coroutine.send(False)
		except StopIteration:
			self.coroutines.event('stopped %s' % self.coroutine)
		return True

	def kill(self):

		"""
		desc:
			Sends the stop signal to an item.
		"""

		try:
			self.coroutine.send(False)
		except StopIteration:
			self.coroutines.event('killed %s' % self.coroutine)

	def launch(self):

		"""
		desc:
			Launches an item. All items are launched at coroutine start.
		"""

		raise NotImplementedError()

	def step(self):

		"""
		desc:
			Lets the item yield one cycle.
		"""

		try:
			if self.coroutine.send(True) is False:
				return self.ABORT
		except StopIteration:
			self.coroutines.event('died %s' % self.coroutine)
			return self.DEAD
		return self.ALIVE
