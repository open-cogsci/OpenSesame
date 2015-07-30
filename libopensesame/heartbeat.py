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
import threading
import time

class heartbeat(threading.Thread):

	"""
	desc:
		A thread that sends regular heartbeats to the launch process (if any).
		A heartbeat is a transfer of the experiment workspace.
	"""

	def __init__(self, exp, interval=1):

		"""
		desc:
			Constructor.

		arguments:
			exp:
				desc:	The experiment object.
				type:	experiment

		keywords:
			interval:
				desc:	The heartbeat interval in seconds.
				type:	[float, int]
		"""

		super(heartbeat, self).__init__()
		self.exp = exp
		self.interval = interval
		self.lock = threading.Lock()

	def run(self):

		"""
		desc:
			Runs the heartbeat loop.
		"""

		while self.exp.running:
			time.sleep(self.interval)
			self.beat()

	def beat(self):

		"""
		desc:
			Sends a single heartbeat.
		"""

		self.lock.acquire()
		self.exp.transmit_workspace(__heartbeat__=True)
		self.lock.release()
