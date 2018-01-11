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
import platform
import sys
import os
import signal

if platform.system() == 'Darwin' and \
	sys.version_info < (3,4):
		# In OS X Python < 3.4 the multiprocessing module is horribly broken,
		# but a fixed version has been released as the 'billiard' module
		import billiard as multiprocessing
else:
	import multiprocessing

class OutputChannel:

	"""Passes messages from child process back to main process."""

	def __init__(self, channel, orig=None):

		"""
		Constructor.

		Arguments:
		channel	--	A multiprocessing.JoinableQueue object that is referenced
					from the main process.

		Keyword arguments:
		orig	--	The original stdout or stderr to also print the messages to.
		"""

		self.channel = channel
		self.orig = orig

	def write(self, m):

		"""
		Writes a message to the queue.

		Arguments
		m		--	The message to write. Should be a string or an (Exception,
					traceback) tuple.
		"""

		self.channel.put(m)

	def flush(self):

		"""Dummy function to mimic the stderr.flush() function."""

		if self.orig:
			self.orig.flush()
		else:
			pass

	def isatty(self):

		"""
		desc:
			Indicates that the output is not attached to a terminal.
		"""

		return False


class ExperimentProcess(multiprocessing.Process):

	"""Creates a new process to run an experiment in."""

	def __init__(self, exp, output):

		"""
		Constructor.

		Arguments
		exp		--	An instance of libopensesame.experiment.experiment
		output	--	A reference to the queue object created in and used to
					communicate with the main process.
		"""

		multiprocessing.Process.__init__(self)
		self.output = output
		# The experiment object is troublesome to serialize,
		# therefore pull out all relevant data to pass on to the new process
		# and rebuild the exp object in there.
		self.script = exp.to_string()
		self.pool_folder = exp.pool.folder()
		self.subject_nr = exp.var.subject_nr
		self.experiment_path = exp.experiment_path
		self.fullscreen = exp.var.fullscreen == u'yes'
		self.logfile = exp.logfile
		self.auto_response = exp.auto_response
		self.killed = False

	def run(self):

		"""
		Everything in this function is run in a new process, therefore all
		import statements are put in here. The function reroutes all output to
		stdin and stderr to the pipe to the main process so OpenSesame can
		handle all prints and errors.
		"""

		import os
		import sys
		from libopensesame import misc
		from libopensesame.experiment import experiment
		from libopensesame.exceptions import osexception
		# Under Windows, change the working directory to the OpenSesame folder,
		# so that the new process can find the main script.
		if os.name == u'nt':
			os.chdir(misc.opensesame_folder())
		# Reroute output to OpenSesame main process, so everything will be
		# printed in the Debug window there.
		pipeToMainProcess = OutputChannel(self.output)
		sys.stdout = pipeToMainProcess
		sys.stderr = pipeToMainProcess
		# First initialize the experiment and catch any resulting Exceptions
		try:
			exp = experiment(string=self.script, pool_folder= self.pool_folder,
				experiment_path=self.experiment_path,
				fullscreen=self.fullscreen, auto_response=self.auto_response,
				subject_nr=self.subject_nr, logfile=self.logfile)
		except Exception as e:
			if not isinstance(e, osexception):
				e = osexception(u'Unexpected error', exception=e)
			# Communicate the exception and exit with error
			self.output.put(e)
			sys.exit(1)
		print(u'Starting experiment as %s' % self.name)
		# Run the experiment and catch any Exceptions.
		e_run = None
		exp.set_output_channel(self.output)
		try:
			exp.run()
			print('done!')
		except Exception as e:
			if not isinstance(e, osexception):
				e_run = osexception(u'Unexpected error', exception=e)
			else:
				e_run = e
		exp.transmit_workspace()
		# End the experiment and catch any Exceptions. These exceptions are just
		# printed out and not explicitly passed on to the user, because they are
		# less important than the run-related exceptions.
		try:
			exp.end()
		except Exception as e_exp:
			print(u'An Exception occurred during exp.end(): %s' % e_exp)
		# Communicate the exception and exit with error
		if e_run is not None:
			self.output.put(e_run)
			sys.exit(1)
		# Exit with success
		sys.exit(0)

	def kill(self):

		print(u'Killing experiment process')
		os.kill(self.pid, signal.SIGKILL)
		self.killed = True
