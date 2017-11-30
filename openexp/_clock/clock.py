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


class Clock(object):

	"""
	desc: |
		The `clock` object offers basic time functions. A `clock` object is
		created automatically when the experiment starts.

		__Example__:

		~~~ .python
		# Get the timestamp before and after sleeping for 1000 ms
		t0 = clock.time()
		clock.sleep(1000)
		t1 = clock.time()
		time_passed = t1 - t0
		print(u'This should be 1000: %s' % time_passed)
		~~~

		[TOC]
	"""

	def __init__(self, experiment):

		"""
		visible: False

		desc:
			Constructor to create a new `clock` object. You do not generally
			call this constructor directly, because a `clock` object is created
			automatically when the experiment is launched.

		arguments:
			experiment:
				desc:	The experiment object.
				type:	experiment
		"""

		self.experiment = experiment

	def time(self):

		"""
		desc:
			Gives a current timestamp in milliseconds. The absolute meaning of
			the timestamp (i.e. when it was 0) depends on the backend.

		returns:
			desc:	A timestamp.
			type:	float

		example: |
			t = clock.time()
			print(u'The current time is %f' % t)
		"""

		raise NotImplementedError()

	def sleep(self, ms):

		"""
		desc:
			Sleeps (pauses) for a period.

		arguments:
			ms:
				desc:	The number of milliseconds to sleep for.
				type:	[int, float]

		example: |
			# Create two canvas objects ...
			my_canvas1 = Canvas()
			my_canvas1.text(u'1')
			my_canvas2 = Canvas()
			my_canvas2.text(u'2')
			# ... and show them with 1 s in between
			my_canvas1.show()
			clock.sleep(1000)
			my_canvas2.show()
		"""

		raise NotImplementedError()

	def loop_for(self, ms, throttle=None, t0=None):

		"""
		desc: |
			*New in v3.2.0*

			An iterator that loops for a fixed time.

		arguments:
			ms:
				desc:	The number of milliseconds to loop for.
				type:	[int. float]

		keywords:
			throttle:
				desc:	A period to sleep for in between each iteration.
				type:	[NoneType, float, int]
			t0:
				desc:	A starting time. If `None`, the starting time is the
						moment at which the iteration starts.
				type:	[NoneType, float, int]

		returns:
			desc:	An Iterator over times in milliseconds that have passed
					since `t0`.

		example: |
			for ms in clock.loop_for(100, throttle=10):
				print(ms)
		"""

		if t0 is None:
			t0 = self.time()
		while True:
			dt = self.time() - t0
			if dt >= ms:
				break
			yield dt
			if throttle is not None:
				self.sleep(throttle)


# Non PEP-8 alias for backwards compatibility
clock = Clock
