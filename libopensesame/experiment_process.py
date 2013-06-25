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
import multiprocessing

class OutputChannel:
	def __init__(self,channel,orig=None, mode="standard"):
		self.channel = channel
		self.orig = orig
		self.mode = mode
		
	def write(self, m):
		self.channel.put(m)
		
		if self.orig:
			self.orig.write(m)
			
	def flush(self):
		if self.orig:
			self.orig.flush()
		else:
			pass



class ExperimentProcess(multiprocessing.Process):
	
	def __init__(self, output):
		""" Constructor
		provide a reference to the pipe object used to communicate with the main process
		"""
		
		multiprocessing.Process.__init__(self)
		self.output = output
		self.script = ""
		self.path = ""
		self.pool_folder = ""
		self.fullscreen = True
		self.subject_nr = None
		self.logfile = ""
		self.auto_response = False
		
		
	def run(self):
		""" Everything in this function is run in a new process, therefore all import statements are put in here
		The function reroutes all output to stdin and stderr to the pipe to the main process so OpenSesame can handle all prints and errors				
		"""
		import os, sys
		
		if os.name == "nt":
			import imp
			if (hasattr(sys, "frozen") or hasattr(sys, "importers") or \
				imp.is_frozen("__main__")):
				path = os.path.dirname(sys.executable)
			else:
				path = os.path.dirname(__file__)
			if path != '':
				os.chdir(path)
				if path not in sys.path:
					sys.path.append(path)

		# Reroute output to OpenSesame main process, so everything will be printed in the Debug window there		
		sys.stdout = OutputChannel(self.output)
		sys.stderr = OutputChannel(self.output)
	
		os.chdir("..")
	
		try:	
			# Check if all required data is available
			if self.script == "":
				raise RuntimeError("Script to run not specified")
			if self.path == "":
				raise RuntimeError("Experiment path not specified")
			if self.pool_folder == "":
				raise RuntimeError("Pool folder not set")
			if self.logfile == "" :
				raise RuntimeError("Save location of logfile not specified")
			if self.subject_nr is None:
				raise RuntimeError("Subject number not specified")
						
			import libopensesame.misc
			import libopensesame.experiment
			
			# Determine subject parity
			if self.subject_nr % 2:
				sp = "even"
			else:
				sp = "odd"	
						
			exp = libopensesame.experiment.experiment("Experiment", self.script, self.pool_folder)
				
			exp.set_subject(self.subject_nr)
			exp.set("subject_parity", sp)
			exp.experiment_path = self.path
			exp.fullscreen = self.fullscreen
			exp.logfile = self.logfile
			exp.auto_response = self.auto_response
			print "Starting experiment as %s" % self.name
			exp.run()
			exp.end()
			libopensesame.experiment.clean_up(exp.debug)	# Is this still necessary if the process gets killed afterwards anyway?									
			sys.exit(0)	# Quit process without error
		except Exception as e:
			import traceback
			self.output.put((e, traceback.format_exc()))
			sys.exit(1)
			
		