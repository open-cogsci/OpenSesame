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

import sys
from libqtopensesame.runners import base_runner
from StringIO import StringIO
from PyQt4 import QtGui
import time

class multiprocess_runner(base_runner):
	
	"""Runs an experiment in another process using multiprocessing."""
	
	def execute(self):		
		
		"""See base_runner.execute()."""
		
		import multiprocessing
		from libqtopensesame.misc import process
		self.channel = multiprocessing.Queue()
		self.exp_process = process.ExperimentProcess(self.experiment, \
			self.channel)
		# Start process!
		self.exp_process.start()
		# Variables used for ugly hack to suppress 'None' print by Queue.get()
		_stdout = sys.stdout	
		_pit = StringIO()
		# Wait for experiment to finish.
		# Listen for incoming messages in the meantime.
		while self.exp_process.is_alive() or not self.channel.empty():
			QtGui.QApplication.processEvents()
			# Make sure None is not printed. Ugly hack for a bug in the Queue
			# class?
			sys.stdout = _pit
			# Wait for messages. Will throw Exception if no message is received
			# before timeout.
			try:
				msg = self.channel.get(True, 0.05)
			except:
				msg = None
			# Restore connection to stdout
			sys.stdout = _stdout
			# For standard print statements
			if isinstance(msg, basestring):
				sys.stdout.write(msg)
			# Errors arrive as a tuple with (Error object, traceback)
			elif isinstance(msg, Exception):
				return msg
			# Anything that is not a string, not an Exception, and not None is
			# unexpected
			elif msg != None:
				return osexception( \
					u"Illegal message type received from child process: %s (%s)" \
					% (msg, type(msg)))
		# Return None if experiment finished without problems
		return None
