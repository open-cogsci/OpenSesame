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
import sys
import time
from libqtopensesame.runners import base_runner
from qtpy import QtWidgets
from libopensesame.exceptions import osexception

class multiprocess_runner(base_runner):

	"""Runs an experiment in another process using multiprocessing."""

	supports_kill = True

	def execute(self):

		"""See base_runner.execute()."""

		import platform
		if platform.system() == 'Darwin' and \
			sys.version_info < (3,4):
				# In OS X the multiprocessing module is horribly broken,
				# for python 2.7 but a fixed version has been released
				# as the 'billiard' module
				import billiard as multiprocessing
		else:
			import multiprocessing

		from libqtopensesame.misc import process, _

		self._workspace_globals = {}
		self.channel = multiprocessing.Queue()
		try:
			self.exp_process = process.ExperimentProcess(self.experiment,
				self.channel)
		except Exception as e:
			return osexception(_(u'Failed to initialize experiment process'),
				exception=e)
		self.console.set_workspace_globals({u'process' : self.exp_process})
		# Start process!
		self.exp_process.start()
		# Wait for experiment to finish.
		# Listen for incoming messages in the meantime.
		finished = False
		while self.exp_process.is_alive() or not self.channel.empty():
			# We need to process the GUI. To make the GUI feel more responsive
			# during pauses, we refresh the GUI more often when paused.
			QtWidgets.QApplication.processEvents()
			if self.paused:
				for i in range(25):
					time.sleep(.01)
					QtWidgets.QApplication.processEvents()
			# Wait for messages. Will throw Exception if no message is received
			# before timeout.
			try:
				msg = self.channel.get(True, 0.05)
			except:
				continue
			if isinstance(msg, basestring):
				sys.stdout.write(safe_decode(msg, errors=u'ignore'))
				continue
			# Capture exceptions
			if isinstance(msg, Exception):
				self.exp_process.join()
				self.exp_process.close()
				return msg
			# The workspace globals are sent as a dict. A special __pause__ key
			# indicates whether the experiment should be paused or resumed.
			if isinstance(msg, dict):
				self._workspace_globals = msg
				if u'__kill__' in msg:
					self.exp_process.kill()
				if u'__heartbeat__' in msg:
					self.console.set_workspace_globals(msg)
					self.main_window.extension_manager.fire(u'heartbeat')
				elif u'__pause__' in msg:
					if msg[u'__pause__']:
						self.pause()
					else:
						self.resume()
				elif u'__finished__' in msg:
					finished = True
				continue
			# Anything that is not a string, not an Exception, and not None is
			# unexpected
			return osexception(
				u"Illegal message type received from child process: %s (%s)" \
				% (msg, type(msg)))
		self.exp_process.join()
		self.exp_process.close()
		if not finished:
			if self.exp_process.killed:
				return osexception(u'The experiment process was killed.')
			else:
				return osexception(u'Python seems to have crashed. This should not '
					u'happen. If Python crashes often, please report it on the '
					u'OpenSesame forum.')

	def kill(self):

		"""See base_runner."""

		self.exp_process.kill()

	def workspace_globals(self):

		"""See base_runner."""

		return self._workspace_globals

	@staticmethod
	def has_heartbeat():

		"""See base_runner."""

		return True
