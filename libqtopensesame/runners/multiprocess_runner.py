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
import os
import sys
from libqtopensesame.runners import base_runner
from PyQt4 import QtGui
from libopensesame.exceptions import osexception

class multiprocess_runner(base_runner):

	"""Runs an experiment in another process using multiprocessing."""

	def execute(self):

		"""See base_runner.execute()."""

		import platform
		# In OS X the multiprocessing module is horribly broken, but a fixed
		# version has been released as the 'billiard' module
		if platform.system() == 'Darwin':
			import billiard as multiprocessing
			multiprocessing.forking_enable(0)
		else:
			import multiprocessing

		from libqtopensesame.misc import process, _
		from libopensesame import misc
		self._workspace_globals = {}
		if os.name == u'nt' or (sys.platform == u'darwin' \
			and not hasattr(sys,"frozen")):
			# Under Windows and OSX, the multiprocess runner assumes that there
			# is a file called `opensesame.py` or `opensesame.pyc`. If this file
			# does not exist, try to copy it from the main script
			# (`opensesame`). If this fails, provide an informative error
			# message.
			os_folder = misc.opensesame_folder()

			# misc.opensesame_folder() doesn't work for OSX and returns None then,
			# so determine OpenSesame's rootdir in another way
			if os_folder is None:
				os_folder = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))

			if not os.path.exists(os.path.join(os_folder, u'opensesame.pyc')) \
				and not os.path.exists(os.path.join(os_folder, u'opensesame.py')):
				import shutil
				try:
					shutil.copyfile(os.path.join(os_folder, u'opensesame'),
						os.path.join(os_folder, u'opensesame.py'))
				except Exception as e:
					return osexception(
						_(u'Failed to copy `opensesame` to `opensesame.py`, which is required for the multiprocess runner. Please copy the file manually, or select a different runner under Preferences.'), exception=e)
		self.channel = multiprocessing.Queue()
		self.exp_process = process.ExperimentProcess(self.experiment,
			self.channel)
		# Start process!
		self.exp_process.start()
		# Wait for experiment to finish.
		# Listen for incoming messages in the meantime.
		while self.exp_process.is_alive() or not self.channel.empty():
			QtGui.QApplication.processEvents()
			# Make sure None is not printed. Ugly hack for a bug in the Queue
			# class?
			self.console.suppress_stdout()
			# Wait for messages. Will throw Exception if no message is received
			# before timeout.
			try:
				msg = self.channel.get(True, 0.05)
			except:
				continue
			# Restore connection to stdout
			self.console.capture_stdout()
			# print('recv: %s (%s)' % (type(msg), msg))
			if isinstance(msg, basestring):
				sys.stdout.write(safe_decode(msg, errors='ignore'))
				continue
			# Capture exceptions
			if isinstance(msg, Exception):
				return msg
			# The workspace globals are sent as a dict. A special __pause__ key
			# indicates whether the experiment should be paused or resumed.
			if isinstance(msg, dict):
				self._workspace_globals = msg
				if u'__pause__' in msg:
					if msg[u'__pause__']:
						self.pause()
					else:
						self.resume()
				continue
			# Anything that is not a string, not an Exception, and not None is
			# unexpected
			return osexception(
				u"Illegal message type received from child process: %s (%s)" \
				% (msg, type(msg)))
		# Return None if experiment finished without problems
		return None

	def workspace_globals(self):

		"""See base_runner."""

		return self._workspace_globals
