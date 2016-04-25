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

class clock(object):

	"""
	desc: |
		The `clock` offers basic time functions.

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
			my_canvas1 = canvas()
			my_canvas1.text(u'1')
			my_canvas2 = canvas()
			my_canvas2.text(u'2')
			# ... and show them with 1 s in between
			my_canvas1.show()
			clock.sleep(1000)
			my_canvas2.show()
		"""

		raise NotImplementedError()
