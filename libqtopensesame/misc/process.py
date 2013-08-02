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
	""" Passes messages from child process back to main process
	
	Arguments:
		channel -- a multiprocessing.JoinableQueue object that is referenced
			from the main process
			
	Keyword arguments
		orig -- the original stdout or stderr to also print the messages to
			
	"""
	def __init__(self,channel,orig=None):
		self.channel = channel
		self.orig = orig
		
	def write(self, m):
		"""
		Write a message to the queue
		
		Arguments
			m -- the message to write. Should be a string or a 
				(Exception, traceback) tuple
		"""
		self.channel.put(m)
		
#		if self.orig:
#			self.orig.write(m)
			
	def flush(self):
		""" Dummy function to mimic the stderr.flush() function (crashes otherwise) """
		if self.orig:
			self.orig.flush()
		else:
			pass



class ExperimentProcess(multiprocessing.Process):

	""" Creates a new process to run an experiment in
	Arguments
		exp - an instance of libopensesame.experiment.experiment
		output - a reference to the queue object created in and used to communicate with the main process
	"""
	
	def __init__(self, exp, output):
		multiprocessing.Process.__init__(self)
		self.output = output
		
		# The experiment object is troublesome to serialize,
		# therefore pull out all relevant data to pass on to the new process
		# and rebuild the exp object from there.
		
		self.script = exp.to_string()
		self.pool_folder = exp.pool_folder
		self.subject_nr = exp.subject_nr
		self.path = exp.experiment_path
		self.fullscreen = exp.fullscreen
		self.logfile = exp.logfile
		self.auto_response = exp.auto_response
				
		
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
		pipeToMainProcess = OutputChannel(self.output)		
		sys.stdout = pipeToMainProcess
		sys.stderr = pipeToMainProcess
		
		os.chdir("../..")	
					
		try:							
			import libopensesame.misc
			import libopensesame.experiment
			
			
			# Determine subject parity
			if self.subject_nr % 2:
				sp = u"even"
			else:
				sp = u"odd"	
			
						
			exp = libopensesame.experiment.experiment("Experiment", self.script, self.pool_folder)				
			exp.set_subject(self.subject_nr)
			exp.set(u"subject_parity", sp)
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
			
		