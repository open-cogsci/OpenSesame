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
import os
from libopensesame.exceptions import osexception
from libopensesame import debug
from libqtopensesame.misc import config
from libqtopensesame.runners import base_runner

from qtpy import QtWidgets
import time

class external_runner(base_runner):

	"""Runs an experiment using opensesamerun."""

	def execute(self):

		"""See base_runner.execute()."""

		import subprocess
		import tempfile
		try:
			# Temporary file for the standard output and experiment
			self.stdout = tempfile.mktemp(suffix=u".stdout")
			if self.experiment.experiment_path is None:
				raise osexception(u"Please save your experiment first, before "
					u"running it using opensesamerun")

			self.path = os.path.join(self.experiment.experiment_path,
				'.opensesamerun-tmp.osexp')
			self.experiment.save(self.path, True)
			debug.msg(u"experiment saved as '%s'" % self.path)
			# Determine the name of the executable
			if config.get_config(u'opensesamerun_exec') == u'':
				if os.name == u"nt":
					self.cmd = [u"opensesamerun.exe"]
				else:
					self.cmd = [u"opensesamerun"]
			else:
				self.cmd = config.get_config(u'opensesamerun_exec').split()
			self.cmd += [
				self.path,
				u"--logfile=%s" % self.experiment.logfile,
				u"--subject=%s" % self.experiment.var.subject_nr
				]
			if debug.enabled:
				self.cmd.append(u"--debug")
			if self.experiment.var.fullscreen == u'yes':
				self.cmd.append(u"--fullscreen")
			if u"--pylink" in sys.argv:
				self.cmd.append(u"--pylink")

			debug.msg(u"spawning opensesamerun as a separate process")
			# Call opensesamerun and wait for the process to complete
			try:
				p = subprocess.Popen(self.cmd, stdout = open(self.stdout, u"w"))
			except Exception as e:
				try:
					os.remove(self.path)
					os.remove(self.stdout)
				except:
					pass
				return e
			# Wait for OpenSesame run to complete, process events in the meantime,
			# to make sure that the new process is shown (otherwise it will crash
			# on Windows).
			retcode = None
			while retcode is None:
				retcode = p.poll()
				QtWidgets.QApplication.processEvents()
				time.sleep(1)
			debug.msg(u"opensesamerun returned %d" % retcode)
			print
			print(open(self.stdout, u"r").read())
			print
			# Clean up the temporary file
			try:
				os.remove(self.path)
				os.remove(self.stdout)
			except:
				pass
			return None
		except Exception as e:
			return e
