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
import os
from libopensesame import debug, exceptions
from libqtopensesame.misc import config

from PyQt4 import QtGui
import time


"""
Default runner
"""

class inprocess_runner(object):
	"""
	Runs an experiment
	
	Arguments:
	experiment -- an instance of libopensesame.experiment.experiment
	"""
	def __init__(self, main_window, experiment):
		self.exp = experiment

	def execute(self):
		try:
			self.exp.run()
			self.exp.end()			
			return None
		except Exception as e:
			return e


"""
OpensesameRun runner
"""

class external_runner(object):		
	"""
	Runs an experiment using opensesamerun
	
	Arguments:
	experiment -- an instance of libopensesame.experiment.experiment
	"""
	
	def __init__(self, main_window, experiment):			
		self.exp = experiment
								
	def execute(self):
		import subprocess
		import tempfile
		
		try:
			# Temporary file for the standard output and experiment
			self.stdout = tempfile.mktemp(suffix = ".stdout")
			
			if self.exp.experiment_path is None:
				raise exceptions.runtime_error("Please save your experiment first, before running it using opensesamerun")
			
			self.path = os.path.join(self.exp.experiment_path, \
				'.opensesamerun-tmp.opensesame.tar.gz')
			self.exp.save(self.path, True)
			debug.msg("experiment saved as '%s'" % self.path)
			
			# Determine the name of the executable
			if config.get_config('opensesamerun_exec') == '':
				if os.name == "nt":
					self.cmd = ["opensesamerun.exe"]
				else:
					self.cmd = ["opensesamerun"]
			else:
				self.cmd = config.get_config('opensesamerun_exec').split()								
			
			self.cmd += [self.path, "--logfile=%s" % self.exp.logfile, "--subject=%s" \
				% self.exp.subject_nr]
			
			if debug.enabled:
				self.cmd.append("--debug")
			if self.exp.fullscreen:
				self.cmd.append("--fullscreen")
			if "--pylink" in sys.argv:
				self.cmd.append("--pylink")		
			
			
			debug.msg("spawning opensesamerun as a separate process")
			
			# Call opensesamerun and wait for the process to complete

			try:
				p = subprocess.Popen(self.cmd, stdout = open(self.stdout, "w"))
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
			while retcode == None:
				retcode = p.poll()
				QtGui.QApplication.processEvents()
				time.sleep(1)
			
			debug.msg("opensesamerun returned %d" % retcode)
			
			print			
			print open(self.stdout, "r").read()
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


"""
Multiprocessing runner
"""

class multiprocess_runner(object):
	"""
	Runs an experiment in another process using multiprocessing
	
	Arguments:
	experiment -- an instance of libopensesame.experiment.experiment
	"""
	
	def __init__(self, main_window, experiment):
		import multiprocessing
		from libopensesame import process
		self.channel = multiprocessing.JoinableQueue()	
		self.experiment = experiment
		self.exp_process = process.ExperimentProcess(experiment, self.channel)
		

	def execute(self):		
		try:		
			# Start process!			
			self.exp_process.start() 
			
			# Wait for experiment to finish.
			# Listen for incoming messages in the meantime.
			while self.exp_process.is_alive() or not self.channel.empty():
				QtGui.QApplication.processEvents()\
				# Check if messages are pending to be processed
				# Sleep otherwise
				if not self.channel.empty():
					msg = self.channel.get(False)
					
					# Notify process that message has been received
					self.channel.task_done()	
					
					# For standard print statements
					# Remove str when OS is completely unicode safe										
					if type(msg) in [str, unicode]:
						sys.stdout.write(msg)
					# Errors arrive as a tuple with (Error object, traceback)
					elif type(msg) == tuple and isinstance(msg[0], Exception):
						self.exp_process.terminate()  								
						return msg
					else:
						sys.stdout.write(RuntimeError("Illegal message type received from child process"))
				else:
					time.sleep(0.1)
										
			# Return None if experiment finished without problems			
			return None
	
		except Exception as e:
			return e