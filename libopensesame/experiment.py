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

from libopensesame.item_store import item_store
from libopensesame.exceptions import osexception
from libopensesame import misc, item, plugins, debug
import os.path
import shutil
import sys
import time
import tarfile
import tempfile
import codecs

# Contains a list of all pool folders, which need to be removed on program exit
pool_folders = []

class experiment(item.item):

	"""The main experiment class, which is the first item to be called"""

	def __init__(self, name=u'experiment', string=None, pool_folder=None, experiment_path=None, fullscreen=False, auto_response=False, logfile=u'defaultlog.csv', subject_nr=0):

		"""<DOC>
		Constructor. The experiment is created automatically be OpenSesame and #
		you will generally not need to create it yourself.

		Keyword arguments:
		name 			--	The name of the experiment. (default=u'experiment')
		string 			--	A string containing the experiment definition. #
							(default=None)
		pool_folder		--	A specific folder to be used for the file pool. #
							(default=None)
		experiment_path	--	The path of the experiment file. (default=None)
		fullscreen		--	Indicates whether the experiment should be #
							executed in fullscreen. (default=False)
		auto_response	--	Indicates whether auto-response mode should be #
							enabled. (default=False)
		logfile			--	The logfile path. (default=u'defaultlog.csv')
		subject_nr		--	The subject number. (default=0)
		</DOC>"""

		global pool_folders

		self.items = item_store(self)
		self.running = False
		self.auto_response = auto_response
		self.plugin_folder = u'plugins'
		self.start_response_interval = None
		self.cleanup_functions = []
		self.restart = False
		self.title = u'My Experiment'
		self.transparent_variables = u'no'
		self.bidi = u'no'

		# Set default variables
		self.start = u'experiment'

		# Sound parameters
		self.sound_freq = 48000
		self.sound_sample_size = -16 # Negative values mean signed
		self.sound_channels = 2
		self.sound_buf_size = 512
		self.resources = {}

		# Backend parameters
		self.canvas_backend = u'xpyriment'
		self.keyboard_backend = u'legacy'
		self.mouse_backend = u'xpyriment'
		self.sampler_backend = u'legacy'
		self.synth_backend = u'legacy'

		# Save the date and time, and the version of OpenSesame
		self.datetime = time.strftime(u'%c').decode(self.encoding, u'ignore')
		self.opensesame_version = misc.version
		self.opensesame_codename = misc.codename

		# Display parameters
		self.width = 1024
		self.height = 768
		self.background = u'black'
		self.foreground = u'white'
		self.fullscreen = fullscreen

		# Font parameters
		self.font_size = 18
		self.font_family = u'mono'
		self.font_italic = u'no'
		self.font_bold = u'no'
		self.font_underline = u'no'

		# Logfile parameters
		self._log = None
		self.logfile = logfile

		# This is some duplication of the option parser in qtopensesame,
		# but nevertheless keep it so we don't need qtopensesame
		self.debug = debug.enabled
		self._stack = debug.stack

		# Pool folder
		if pool_folder == None:
			# On some systems tempfile.mkdtemp() triggers a UnicodeDecodeError.
			# This is resolved by passing the dir explicitly as a Unicode
			# string. This fix has been adapted from:
			# - <http://bugs.python.org/issue1681974>
			self.pool_folder = tempfile.mkdtemp(suffix= \
				u'.opensesame_pool', dir=tempfile.gettempdir().decode( \
				encoding=misc.filesystem_encoding()))
			pool_folders.append(self.pool_folder)
			debug.msg(u'creating new pool folder')
		else:
			debug.msg(u'reusing existing pool folder')
			self.pool_folder = pool_folder
		debug.msg(u'pool folder is \'%s\'' % self.pool_folder)

		string = self.open(string)
		item.item.__init__(self, name, self, string)

		# Default subject info
		self.set_subject(subject_nr)
		# Restore experiment path
		if experiment_path != None:
			self.fallback_pool_folder = os.path.join(experiment_path, u'__pool__')
			self.experiment_path = experiment_path
		else:
			self.fallback_pool_folder = None

	def module_container(self):

		"""Specify the module that contains the item modules"""

		return u'libopensesame'

	def item_prefix(self):

		"""
		A prefix for the plug-in classes, so that [prefix][plugin] class is used
		instead of the [plugin] class.
		"""

		return u''

	def set_subject(self, nr):

		"""<DOC>
		Sets the subject number and parity (even/ odd). This function is #
		called automatically when an experiment is started, so you do not #
		generally need to call it yourself.

		Arguments:
		nr	--	The subject nr.

		Example:
		>>> exp.set_subject(1)
		>>> print('Subject nr = %d' % exp.get('subject_nr'))
		>>> print('Subject parity = %s' % exp.get('subject_parity'))
		</DOC>"""

		# Set the subject nr and parity
		self.set(u'subject_nr', nr)
		if nr % 2 == 0:
			self.set(u'subject_parity', u'even')
		else:
			self.set(u'subject_parity', u'odd')

	def read_definition(self, s):

		"""
		Extracts a the definition of a single item from the string.

		Arguments:
		s	--	The definition string.

		Returns:
		A (str, str) tuple with the full string minus the definition string
		and the definition string.
		"""

		# Read the string until the end of the definition
		def_str = u''
		line = next(s, None)
		if line == None:
			return None, u''
		get_next = False
		while True:
			if len(line) > 0:
				if line[0] != u'\t':
					break
				else:
					def_str += line + u'\n'
			line = next(s, None)
			if line == None:
				break
		return line, def_str

	def from_string(self, string):

		"""
		Reads the entire experiment from a string.

		Arguments:
		string	--	The definition string.
		"""

		debug.msg(u"building experiment")
		s = iter(string.split("\n"));
		line = next(s, None)
		while line != None:
			get_next = True
			try:
				l = self.split(line)
			except ValueError as e:
				raise osexception( \
					u"Failed to parse script. Maybe it contains illegal characters or unclosed quotes?", \
					exception=e)
			if len(l) > 0:
				self.parse_variable(line)
				# Parse definitions
				if l[0] == u"define":
					if len(l) != 3:
						raise osexception( \
							u'Failed to parse definition', line=line)
					item_type = l[1]
					item_name = self.sanitize(l[2])
					line, def_str = self.read_definition(s)
					get_next = False
					self.items.new(item_type, item_name, def_str)
			# Advance to next line
			if get_next:
				line = next(s, None)

	def run(self):

		"""Runs the experiment."""

		self.save_state()
		self.running = True
		self.init_display()
		self.init_sound()
		self.init_log()
		self.reset_feedback()

		print(u"experiment.run(): experiment started at %s" % time.ctime())

		if self.start in self.items:
			self.items[self.start].prepare()
			self.items[self.start].run()
		else:
			raise osexception( \
				"Could not find item '%s', which is the entry point of the experiment" \
				% self.start)

		print(u"experiment.run(): experiment finished at %s" % time.ctime())

		self.end()

	def cleanup(self):

		"""Calls all the cleanup functions."""

		while len(self.cleanup_functions) > 0:
			func = self.cleanup_functions.pop()
			debug.msg(u"calling cleanup function")
			func()

	def end(self):

		"""Nicely ends the experiment."""

		from openexp import sampler, canvas
		self.running = False
		try:
			self._log.flush()
			os.fsync(self._log)
			self._log.close()
		except:
			pass
		sampler.close_sound(self)
		canvas.close_display(self)
		self.cleanup()
		self.restore_state()

	def to_string(self):

		"""
		Encodes the experiment into a string.

		Returns:
		A Unicode definition string for the experiment.
		"""

		s = u'# Generated by OpenSesame %s (%s)\n' % (misc.version, \
			misc.codename) + \
			u'# %s (%s)\n' % (time.ctime(), os.name) + \
			u'# <http://www.cogsci.nl/opensesame>\n\n'
		for var in self.variables:
			s += self.variable_to_string(var)
		s += u'\n'
		for item in sorted(self.items):
			s += self.items[item].to_string() + u'\n'
		return s

	def resource(self, name):

		"""
		Retrieves a file from the resources folder.

		Arguments:
		name	--	The file name.

		Returns:
		A Unicode string with the full path to the file in the resources
		folder.
		"""

		name = self.unistr(name)
		if self != None:
			if name in self.resources:
				return self.resources[name]
			if os.path.exists(self.get_file(name)):
				return self.get_file(name)
		path = misc.resource(name)
		if path == None:
			raise Exception( \
				u"The resource '%s' could not be found in libopensesame.experiment.resource()" \
				% name)
		return path

	def get_file(self, path):

		"""<DOC>
		Returns the path to a file. First checks if the file is in the file pool #
		and then the folder of the current experiment (if any), or in the #
		`__pool__` subfolder of the current experiment. Otherwise, simply #
		returns the path.

		Arguments:
		path	--	The filename.

		Returns:
		The full path to the file.

		Example:
		>>> image_path = exp.get_file('my_image.png')
		>>> my_canvas = exp.offline_canvas()
		>>> my_canvas.image(image_path)
		</DOC>"""

		path = self.unistr(path)
		if path.strip() == u'':
			raise osexception(
				u"An empty string was passed to experiment.get_file(). Please "
				u"specify a valid filename.")
		if os.path.exists(os.path.join(self.pool_folder, path)):
			return os.path.join(self.pool_folder, path)
		if self.experiment_path != None:
			if os.path.exists(os.path.join(self.experiment_path, path)):
				return os.path.join(self.experiment_path, path)
			if self.fallback_pool_folder != None and os.path.exists(
				os.path.join(self.experiment_path, self.fallback_pool_folder,
				path)):
				return os.path.join(self.experiment_path,
					self.fallback_pool_folder, path)
		return path

	def file_in_pool(self, path):

		"""<DOC>
		Checks if a file is in the file pool.

		Returns:
		A Boolean indicating if the file is in the pool.

		Example:
		>>> if not exp.file_in_pool('my_image.png'):
		>>> 	print('my_image.png could not be found!')
		>>> else:
		>>> 	image_path = exp.get_file('my_image.png')
		>>> 	my_canvas = exp.offline_canvas()
		>>> 	my_canvas.image(image_path)
		</DOC>"""

		return os.path.exists(self.get_file(path))

	def save(self, path, overwrite=False):

		"""
		Saves the experiment to file. If no extension is provided,
		.opensesame.tar.gz is chosen by default.

		Arguments:
		path		--	The target file to save to.

		Keyword arguments:
		overwrite	--	A boolean indicating if existing files should be
						overwritten. (default=False)

		Returns:
		The path on successfull saving or False otherwise.
		"""

		if isinstance(path, str):
			path = path.decode(self.encoding)
		debug.msg(u'asked to save "%s"' % path)
		# Determine the extension
		ext = os.path.splitext(path)[1].lower()
		# If the extension is .opensesame, save the script as plain text
		if ext == u'.opensesame':
			if os.path.exists(path) and not overwrite:
				return False
			debug.msg(u'saving as .opensesame file')
			f = open(path, u'w')
			f.write(self.usanitize(self.to_string()))
			f.close()
			self.experiment_path = os.path.dirname(path)
			return path
		# Use the .opensesame.tar.gz extension by default
		if path[-len(u'.opensesame.tar.gz'):] != u'.opensesame.tar.gz':
			path += u'.opensesame.tar.gz'
		if os.path.exists(path) and not overwrite:
			return False
		debug.msg(u"saving as .opensesame.tar.gz file")
		# Write the script to a text file
		script = self.to_string()
		script_path = os.path.join(self.pool_folder, u'script.opensesame')
		f = open(script_path, u"w")
		f.write(self.usanitize(script))
		f.close()
		# Create the archive in a a temporary folder and move it afterwards.
		# This hack is needed, because tarfile fails on a Unicode path.
		tmp_path = tempfile.mktemp(suffix=u'.opensesame.tar.gz')
		tar = tarfile.open(tmp_path, u'w:gz')
		tar.add(script_path, u'script.opensesame')
		os.remove(script_path)
		# We also create a temporary pool folder, where all the filenames are
		# Unicode sanitized to ASCII format. Again, this is necessary to deal
		# with poor Unicode support in .tar.gz.
		tmp_pool = tempfile.mkdtemp(suffix=u'.opensesame.pool')
		for fname in os.listdir(self.pool_folder):
			sname = self.usanitize(fname)
			shutil.copyfile(os.path.join(self.pool_folder, fname), \
				os.path.join(tmp_pool, sname))
		tar.add(tmp_pool, u'pool', True)
		tar.close()
		# Move the file to the intended location
		shutil.move(tmp_path, path)
		self.experiment_path = os.path.dirname(path)
		return path

	def open(self, src):

		"""
		If the path exists, open the file, extract the pool and return the
		contents of the script.opensesame. Otherwise just return the input
		string, because it probably was a definition to begin with.

		Arguments:
		src		--	A definition string or a file to be opened.

		Returns:
		A unicode defition string.
		"""

		# If the path is not a path at all, but a string containing
		# the script, return it. Also, convert the path back to Unicode before
		# returning.
		if not os.path.exists(src):
			debug.msg(u'opening from unicode string')
			self.experiment_path = None
			if isinstance(src, unicode):
				return src
			return src.decode(self.encoding, u'replace')
		# If the file is a regular text script,
		# read it and return it
		ext = u'.opensesame.tar.gz'
		if src[-len(ext):] != ext:
			debug.msg(u'opening .opensesame file')
			self.experiment_path = os.path.dirname(src)
			return self.unsanitize(open(src, u'rU').read())
		debug.msg(u"opening .opensesame.tar.gz file")
		# If the file is a .tar.gz archive, extract the pool to the pool folder
		# and return the contents of opensesame.script.
		tar = tarfile.open(src, u'r:gz')
		for name in tar.getnames():
			# Here, all paths except name are Unicode. In addition, fname is
			# Unicode unsanitized, because the files as saved are Unicode
			# sanitized (see save()).
			uname = name.decode(self.encoding)
			folder, fname = os.path.split(uname)
			fname = self.unsanitize(fname)
			if folder == u"pool":
				debug.msg(u"extracting '%s'" % uname)
				tar.extract(name, self.pool_folder.encode( \
					misc.filesystem_encoding()))
				os.rename(os.path.join(self.pool_folder, uname), \
					os.path.join(self.pool_folder, fname))
				os.rmdir(os.path.join(self.pool_folder, folder))
		script_path = os.path.join(self.pool_folder, u"script.opensesame")
		tar.extract(u"script.opensesame", self.pool_folder)
		script = self.unsanitize(open(script_path, u"rU").read())
		os.remove(script_path)
		self.experiment_path = os.path.dirname(src)
		return script

	def reset_feedback(self):

		"""Resets the feedback variables (acc, avg_rt, etc.)."""

		self.total_responses = 0
		self.total_correct = 0
		self.total_response_time = 0
		self.avg_rt = u"undefined"
		self.average_response_time = u"undefined"
		self.accuracy = u"undefined"
		self.acc = u"undefined"

	def var_info(self):

		"""
		Returns a list of (name, value) tuples with variable descriptions
		for the main experiment.

		Returns:
		A list of tuples.
		"""

		l = []
		for var in self.variables:
			l.append( (var, self.variables[var]) )
		return l

	def var_list(self, filt=u''):

		"""
		Returns a list of (name, value, description) tuples with variable
		descriptions for all items

		Keyword arguments:
		filt	--	A search string to filter by. (default=u'')

		Returns:
		A list of tupless
		"""

		l = []
		# Create a dictionary of items that also includes the experiment
		item_dict = dict(self.items.items() + [(u'global', self)]).items()
		seen = []
		for item_name, item in item_dict:
			# Create a dictionary of variables that includes the broadcasted
			# ones as wel as the indirectly registered ones (using item.set())
			var_dict = item.var_info() + item.variables.items()
			for var, val in var_dict:
				if var not in seen and (filt in var.lower() or filt in \
					self.unistr(val).lower() or filt in item_name.lower()):
					l.append( (var, val, item_name) )
					seen.append(var)
		return l

	def init_sound(self):

		"""Intializes the sound backend."""

		from openexp import sampler
		sampler.init_sound(self)

	def init_display(self):

		"""Initializes the canvas backend."""

		from openexp import canvas
		canvas.init_display(self)

	def init_log(self):

		"""Opens the logile."""

		# Do not open the logfile if it's already open
		if self._log != None:
			return
		# If only a filename is present, we interpret this filename as relative
		# to the experiment folder, instead of relative to the current working
		# directory.
		if os.path.basename(self.logfile) == self.logfile and \
			self.experiment_path != None:
			self.logfile = os.path.join(self.experiment_path, self.logfile)
		# Open the logfile
		self._log = codecs.open(self.logfile, u'w', encoding=self.encoding)
		print(u"experiment.init_log(): using '%s' as logfile (%s)" % \
			(self.logfile, self.encoding))

	def save_state(self):

		"""
		Saves the system state so that it can be restored after the experiment.
		"""

		from libopensesame import inline_script
		inline_script.save_state()

	def restore_state(self):

		"""Restores the system to the state as saved by save_state()."""

		from libopensesame import inline_script
		inline_script.restore_state()

	def _sleep_func(self, ms):

		"""
		Sleeps for a specific time.

		* This is a stub that should be replaced by a proper function by the
		  canvas backend. See openexp._canvas.legacy.init_display()

		Arguments:
		ms	--	The sleep duration.
		"""

		raise osexception( \
			u"experiment._sleep_func(): This function should be set by the canvas backend.")

	def _time_func(self):

		"""
		Gets the time.

		* This is a stub that should be replaced by a proper function by the
		  canvas backend. See openexp._canvas.legacy.init_display()

		Returns:
		A timestamp in milliseconds. Depending on the backend, this may be an
		int or a float.
		"""

		raise osexception( \
			u"experiment._time_func(): This function should be set by the canvas backend.")


def clean_up(verbose=False):

	"""
	Cleans up the temporary pool folders.

	Keyword arguments:
	verbose		--	A boolean indicating if debugging output should be given.
					(default=False)
	"""

	from openexp import canvas
	global pool_folders
	if verbose:
		print(u"experiment.clean_up()")

	for path in pool_folders:
		if verbose:
			print(u"experiment.clean_up(): removing '%s'" % path)
		try:
			shutil.rmtree(path)
		except:
			if verbose:
				print(u"experiment.clean_up(): failed to remove '%s'" % path)
	canvas.clean_up(verbose)


