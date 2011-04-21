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

from libopensesame import item, exceptions, plugins
import openexp.experiment
import openexp.canvas
import os.path
import shutil
import sys
import shlex
import time
import tarfile
import tempfile
import imp

pool_folders = []

class experiment(item.item, openexp.experiment.experiment):

	def __init__(self, name, string = None, pool_folder = None):
	
		"""
		Initialize the experiment		
		"""
		
		global pool_folders
		
		self.items = {}
		self.running = False
		self.auto_response = False
		self.plugin_folder = "plugins"
		self.start_response_interval = None
		self.cleanup_functions = []
		self.restart = False
		
		self.known_item_types = ["loop", "sequence", "keyboard_response", "mouse_response", "logger", "sketchpad", "feedback", "inline_script", "sampler", "synth"]
		
		# Set default variables
		self.compensation = 0		
		self.width = 1024
		self.height = 768
		self.background = "black"
		self.foreground = "white"
		self.start = "main"		
		
		# Variables used for bookkeeping responses
		self.total_correct = 0
		self.total_response_time = 0
		self.total_responses = 0
		
		# This is some duplication of the option parser in qtopensesame,
		# but nevertheless keep it so we don't need qtopensesame
		self.debug = "--debug" in sys.argv or "-d" in sys.argv

		# Pool folder
		if pool_folder == None:
			self.pool_folder = tempfile.mkdtemp(".opensesame_pool")
			pool_folders.append(self.pool_folder)
			if self.debug:
				print "experiment.__init__(): creating new pool folder"			
		else:
			if self.debug:
				print "experiment.__init__(): reusing existing pool folder"
			self.pool_folder = pool_folder
		if self.debug:
			print "experiment.__init__(): pool folder is '%s'" % self.pool_folder				
						
		openexp.experiment.experiment.__init__(self)
		
		string = self.open(string)		
		item.item.__init__(self, name, self, string)		
		
		if not self.has("subject_nr"):
			self.set("subject_nr", 0)
		
		if not self.has("subject_parity"):
			self.set("subject_parity", "even")
				
		self.resolution = self.width, self.height
				
	def module_container(self):
	
		"""
		Specifies where the experiment looks for modules
		"""
	
		return "libopensesame"
		
	def item_prefix(self):
	
		"""
		Specifies which class from the plugin should be loaded
		"""
		
		return ""
		
	def set_subject(self, nr):
	
		"""
		Set the subject number and parity
		"""
		
		# Set the subject nr and parity
		self.set("subject_nr", nr)		
		if nr % 2 == 0:
			self.set("subject_parity", "even")
		else:
			self.set("subject_parity", "odd")		
					
	def read_definition(self, s):
	
		"""
		Extract a single definition from the string
		"""
	
		# Read the string until the end of the definition 
		def_str = ""					
		line = next(s, None)
		if line == None:
			return None, ""
		get_next = False
		while True:					
			if len(line) > 0:
				if line[0] != "\t":
					break
				else:	
					def_str += line + "\n"
			line = next(s, None)
			if line == None:
				break
								
		return line, def_str		
		
	def parse_definition(self, item_type, item_name, string):
	
		"""
		Initialize a single definition, using the string, and
		add it to the dictionary of items
		"""
		
		if plugins.is_plugin(item_type):
		
			if self.debug:
				print "experiment.parse_definition(): loading plugin '%s'" % item_type

			try:
				item = plugins.load_plugin(item_type, item_name, self, string, self.item_prefix())
			except:
				raise exceptions.script_error("Failed load plugin '%s'" % item_type)
				
			self.items[item_name] = item			
									
		else:				
		
			# Load the module from the regular items			
			if self.debug:
				print "experiment.parse_definition(): loading core plugin '%s'" % item_type			
		
			if self.debug:
				exec("from %s import %s" % (self.module_container(), item_type))
			try:
				if not self.debug:
					exec("from %s import %s" % (self.module_container(), item_type))
			except:
				raise exceptions.script_error("Failed to import module '%s' as '%s'" % (item_type, item_name))
		
			cmd = "%(item_type)s.%(item_type)s(\"%(item_name)s\", self, \"\"\"%(string)s\"\"\")" % \
				{"item_type" : item_type, "item_name" : item_name, "string" : string.replace("\"", "\\\"")}		
			
			if self.debug:
				bytecode = compile(cmd, "<string>", "eval")
				self.items[item_name] = eval(bytecode)
			else:			
				try:
					bytecode = compile(cmd, "<string>", "eval")
					self.items[item_name] = eval(bytecode)
				except Exception as e:
					raise exceptions.script_error("Failed to instantiate module '%s' as '%s': %s" % (item_type, item_name, e))
			
	def from_string(self, string):
	
		"""
		Reads an experiment from a string
		"""				
	
		s = iter(string.split("\n"));
	
		line = next(s, None)
		while line != None:
					
			get_next = True
					
			try:
				l = shlex.split(line)
			except ValueError as e:
				raise exceptions.script_error("Failed to parse line '%s'. Maybe it contains illegal characters or unclosed quotes?" % line)
				
			if len(l) > 0:						
			
				self.parse_variable(line)
				
				# Parse definitions		
				if l[0] == "define":
					if len(l) != 3:
						raise exceptions.script_error("Failed to parse definition '%s'" % line)
						
					item_type = l[1]
					item_name = self.sanitize(l[2])
					line, def_str = self.read_definition(s)
					get_next = False
					self.parse_definition(item_type, item_name, def_str)
								
			if get_next:					
				line = next(s, None)			
				
	def run(self):
	
		"""
		Run the experiment
		"""		
		
		self.running = True
		self.init_sound()
		self.init_display(self.debug)		
		self.init_log()
		
		print "experiment.run(): experiment started at %s" % time.ctime()
		
		if self.start in self.items:
			exec("self.items[\"%s\"].prepare()" % self.start)			
			exec("self.items[\"%s\"].run()" % self.start)			
		else:
			raise exceptions.runtime_error("Could not find item '%s', which is the entry point of the experiment" % self.start)
			
		print "experiment.run(): experiment finished at %s" % time.ctime()			
		
		self.end()
				
	def cleanup(self):
	
		"""
		Calls all the cleanup functions and clears the cleanup_functions list		
		"""
		
		while len(self.cleanup_functions) > 0:
			func = self.cleanup_functions.pop()
			if self.debug:
				print "experiment.cleanup(): calling cleanup function"
			func()
		
	def end(self):
	
		"""
		Clean up after the experiment
		"""
	
		self.running = False
		openexp.experiment.experiment.end(self)
		self.cleanup()
		
	def levenshtein(self, s1, s2):
	
		"""
		Calculates the Levenshtein distance between two strings.
		Source:
		http://en.wikibooks.org/wiki/Algorithm_implementation/Strings/Levenshtein_distance#Python
		"""
	
		if len(s1) < len(s2):
		    return self.levenshtein(s2, s1)
		if not s1:
		    return len(s2)
	 
		previous_row = xrange(len(s2) + 1)
		for i, c1 in enumerate(s1):
		    current_row = [i + 1]
		    for j, c2 in enumerate(s2):
		        insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
		        deletions = current_row[j] + 1       # than s2
		        substitutions = previous_row[j] + (c1 != c2)
		        current_row.append(min(insertions, deletions, substitutions))
		    previous_row = current_row
	 
		return previous_row[-1]	
		
	def to_string(self):
	
		"""
		Encode the experiment into a string		
		"""	

		s = "# Generated by OpenSesame\n"
		s += "# %s\n" % time.ctime()
		s += "# \n"
		s += "# Copyright Sebastiaan Mathot (2010-2011)\n"	
		s += "# <http://www.cogsci.nl>\n\n"

		for var in self.variables:
			s += self.variable_to_string(var)
		s += "\n"
		for item in self.items:
			s += self.items[item].to_string() + "\n"
		return s
		
	def guess(self, string, options):
	
		"""
		Guess the correct string based on a list
		of possible strings				
		"""
		
		if string in options:
			return string
			
		best_match = None
		best_d = None
		for s in options:
			d = self.levenshtein(string, s)
			if best_match == None or best_d > d:
				best_d = d
				best_match = s
		return best_match
		
	def usanitize(self, s, strict = False):
	
		"""
		Convert all special characters to 
		U+XXXX notation
		"""
	
		try:
			string = str(s)
									
		except:		
	
			# If this doesn't work and the message isn't a QString either,
			# give up and return a warning string			
			if not hasattr(s, "toUtf8"):
				return "Error: Unable to create readable text from string"
			
			# Otherwise, walk through all characters and convert the unknown
			# characters to unicode notation. In strict mode unicode is ignored.
			string = ""			
			for i in range(s.count()):
				c = s.at(i)
				if c.unicode() > 127:
					if not strict:
						string += "U+%.4X" % c.unicode()
				else:
					string += c.toLatin1()
				
		return string
			
		
	def sanitize(self, s, strict = False):
	
		"""
		Remove invalid characters from the string
		"""

		string = self.usanitize(s, strict)
		
		# Walk through the string and strip out
		# quotes, slashes and newlines. In strict
		# mode we even only accept alphanumeric
		# characters and underscores
		s = ""
		for c in string:
			if strict:
				if c.isalnum() or c == "_":
					s += c
			elif c not in ("\"", "\\", "\n"):
				s += c
		return s
		
	def unsanitize(self, s):
	
		"""
		Convert the unicode notation back to actual unicode encoding
		"""
		
		s = unicode(s)
				
		while s.find("U+") >= 0:
			i = s.find("U+")			
			entity = s[i:i+6]
			s = s.replace(entity, unichr(int(entity[2:], 16)))
			
		return s			
		
	def get_file(self, path):
	
		"""
		Gets a file, but checks first if the file is in the pool
		"""
		
		if os.path.exists(os.path.join(self.pool_folder, path)):
			return os.path.join(self.pool_folder, path)
		return path
		
	def file_in_pool(self, path):
	
		"""
		Checks if a file is in the file pool
		"""
	
		return os.path.exists(os.path.join(self.pool_folder, path))
		
	def save(self, path, overwrite = False):
	
		"""
		Save an opensesame file to a .opensesame, and
		include the pool
		"""
		
		if self.debug:
			print "experiment.open(): asked to save '%s'" % path		
				
		# Determine the extension
		ext = os.path.splitext(path)[1].lower()
		
		# If the extension is .opensesame, save the script
		# as plain text
		if ext == ".opensesame":		
			if os.path.exists(path) and not overwrite:
				return False				
			if self.debug:
				print "experiment.open(): saving as .opensesame file"								
			f = open(path, "w")
			f.write(self.to_string())
			f.close()
			return path

		# Use the .opensesame.tar.gz extension by default
		if path[-len(".opensesame.tar.gz"):] != ".opensesame.tar.gz":
			path += ".opensesame.tar.gz"
			
		if os.path.exists(path) and not overwrite:
			return False

		if self.debug:
			print "experiment.open(): saving as .opensesame.tar.gz file"		
					
		# Write the script to a text file
		script = self.to_string()				
		script_path = os.path.join(self.pool_folder, "script.opensesame")
		f = open(script_path, "w")
		f.write(script)
		f.close()
		
		# Create the archive in a a temporary folder and move it
		# afterwards. This hack is needed, because tarfile fails
		# on a Unicode path.
		tmp_path = tempfile.mktemp(suffix = ".opensesame.tar.gz")
		tar = tarfile.open(tmp_path, "w:gz")
		tar.add(script_path, "script.opensesame")
		os.remove(script_path)
		tar.add(self.pool_folder, "pool", True)
		tar.close()		
		
		# Move the file to the intended location
		shutil.move(tmp_path, path)
		
		return path

	def open(self, path):
	
		"""
		If the path exists, open the file, extract the pool
		and return the contents of the script.opensesame.
		Otherwise just return the path
		"""
		
		# If the path is not a path at all, but a string containing
		# the script, return it
		if (type(path) != str and type(path) != unicode) or not os.path.exists(path):
			if self.debug:
				print "experiment.open(): opening from string"
			return path
		
		# If the file is a regular text script,
		# read it and return it
		ext = ".opensesame.tar.gz"
		if path[-len(ext):] != ext:
			if self.debug:
				print "experiment.open(): opening .opensesame file"		
			return open(path, "r").read()
			
		if self.debug:
			print "experiment.open(): opening .opensesame.tar.gz file"		
						
		# If the file is a .tar.gz archive, extract
		# the pool to the pool folder and return the
		# contents of opensesame.script
		tar = tarfile.open(path, "r:gz")
		for name in tar.getnames():
			folder, fname = os.path.split(name)
			if folder == "pool":
				if self.debug:
					print "experiment.open(): extracting '%s'" % name
				tar.extract(name, self.pool_folder)			
				os.rename(os.path.join(self.pool_folder, name), os.path.join(self.pool_folder, fname))
				os.rmdir(os.path.join(self.pool_folder, folder))
		
		script_path = os.path.join(self.pool_folder, "script.opensesame")
		tar.extract("script.opensesame", self.pool_folder)
		script = open(script_path, "r").read()
		os.remove(script_path)
		return script
		
	def var_info(self):
	
		"""
		Give a list of tuples with variable descriptions for
		the main experiment
		"""
		
		l = []
		
		for var in self.variables:
			l.append( (var, self.variables[var]) )
		
		return l											
		
	def var_list(self, filt = ""):
	
		"""
		Gives a list of tuples with variable descriptions for
		all items. The variables can be filtered.
		"""
		
		l = []
		
		i = 0
		for item in self.items:
			var_list = self.items[item].var_info()
			for var, val in var_list:
				if filt in str(var).lower() or filt in str(val).lower() or filt in item.lower():
					l.append( (var, val, item) )
				
		var_list = self.var_info()
		for var, val in var_list:
			if filt in str(var).lower() or filt in str(val).lower() or filt in "global":
				l.append( (var, val, "global") )
				
		return l
		
def clean_up(verbose = False):
	
	"""
	Cleans up the temporary pool folders
	"""
	
	global pool_folders
	
	if verbose:
		print "experiment.clean_up()"
	
	for path in pool_folders:
		if verbose:
			print "experiment.clean_up(): removing '%s'" % path
		try:
			shutil.rmtree(path)
		except:
			if verbose:
				print "experiment.clean_up(): failed to remove '%s'" % path
				
	openexp.canvas.clean_up(verbose)
	

