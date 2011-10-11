"""
This file is part of openexp.

openexp is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

openexp is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with openexp.  If not, see <http://www.gnu.org/licenses/>.
"""

import pygame
from pygame.locals import *
import openexp.keyboard

class legacy:

	"""
	The legacy backend is the default backend which uses PyGame to handle all
	keyboard input. This is essentially a class based on the openexp.response
	module, which is now deprecated.

	This class can serve as a template for creating new OpenSesame keyboard input
	backends. The new backend can be activated by adding "set keyboard_backend [name]"

	A few guidelines:
	-- Acceptable key-formats are characters and integers, interpreted as ASCII key codes.
	-- Moderators are represented by the following strings: "shift", "alt", "control" and "meta"
	-- Catch exceptions wherever possible and raise an openexp.exceptions.canvas_error
	   with a clear and descriptive error message.
	-- Do not deviate from the guidelines. All back-ends should be interchangeable and
	   transparent to OpenSesame. You are free to add functionality to this class, to be
	   used in inline scripts, but this should not break the basic functionality.
	-- Print debugging output only if experiment.debug == True and preferrably in the
	   following format: "template.__init__(): Debug message here".
	"""

	key_map = {
		"1" : "!", "2" : "@", "3" : "#", "4" : "$", "5" : "%", \
		"6" : "^", "7" : "&", "8" : "*", "9" : "(", "0" : ")", \
		"-" : "_", "=" : "+", "[" : "{", "]" : "}", "\\" : "|", \
		";" : ":", "\"" : "'", "," : "<", "." : ">", "/" : "?"
		}

	def __init__(self, experiment, keylist = None, timeout = None):

		"""<DOC>
		Intializes the keyboard object.

		Arguments:
		experiment -- an instance of libopensesame.experiment.experiment

		Keyword arguments:
		keylist -- a list of human readable keys that are accepted or None
				   to accept all keys (default = None)
		timeout -- an integer value specifying a timeout in milliseconds or
				   None for no timeout (default = None)
		</DOC>"""

		# Create a dictionary to map character representations to
		# ASCII codes
		pygame.init()
		self.key_codes = {}
		for i in dir(pygame):
			if i[:2] == "K_":
				code = eval("pygame.%s" % i)
				name1 = pygame.key.name(code).lower()
				name2 = name1.upper()
				name3 = i[2:].lower()
				name4 = name3.upper()
				self.key_codes[name1] = code
				self.key_codes[name2] = code
				self.key_codes[name3] = code
				self.key_codes[name4] = code				

		self.experiment = experiment
		self.set_keylist(keylist)
		self.set_timeout(timeout)
		
	def set_keylist(self, keylist = None):

		"""<DOC>
		Sets a list of accepted keys

		Keyword arguments:
		keylist -- a list of human readable keys that are accepted or None
				   to accept all keys (default = None)
		</DOC>"""

		if keylist == None:
			self._keylist = None
		else:
			self._keylist = []
			for key in keylist:
				self._keylist.append(self.to_int(key))

	def set_timeout(self, timeout = None):

		"""<DOC>
		Sets a timeout

		Keyword arguments:
		timeout -- an integer value specifying a timeout in milliseconds or
				   None for no timeout (default = None)
		</DOC>"""

		self.timeout = timeout

	def get_key(self, keylist = None, timeout = None):

		"""<DOC>
		Waits for keyboard input

		Keyword arguments:
		keylist -- a list of human readable keys that are accepted or None
				   to use the default. This parameter does not change the
				   default keylist. (default = None)
		timeout -- an integer value specifying a timeout in milliseconds or
				   None to use the default. This parameter does not change the
				   default timeout. (default = None)
				   
		Exceptions:
		A response_error if 'escape' was pressed				   

		Returns:
		A (key, timestamp) tuple. The key is None if a timeout occurs.
		</DOC>"""

		if keylist == None:
			keylist = self._keylist
		if timeout == None:
			timeout = self.timeout

		start_time = pygame.time.get_ticks()
		time = start_time

		while timeout == None or time - start_time <= timeout:
			time = pygame.time.get_ticks()
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						raise openexp.exceptions.response_error("The escape key was pressed.")
					if keylist == None or event.key in keylist:
						return event.key, time

		return None, time

	def get_mods(self):

		"""<DOC>
		Returns a list of keyboard moderators (e.g., shift, alt, etc.) that are
		currently pressed.

		Returns:
		A list of keyboard moderators. An empty list is returned if no moderators
		are pressed.
		</DOC>"""

		l = []
		mods = pygame.key.get_mods()
		if mods & KMOD_LSHIFT or mods & KMOD_RSHIFT or mods & KMOD_SHIFT:
			l.append("shift")
		if mods & KMOD_LCTRL or mods & KMOD_RCTRL or mods & KMOD_CTRL:
			l.append("ctrl")
		if mods & KMOD_LALT or mods & KMOD_RALT or mods & KMOD_ALT:
			l.append("alt")
		if mods & KMOD_LMETA or mods & KMOD_RMETA or mods & KMOD_META:
			l.append("meta")
		return l

	def shift(self, key, mods = ["shift"]):

		"""<DOC>
		Returns the character that results from pressing a key together with the
		moderators, typically a shift. E.g., "3" + "Shift" -> "#". This function
		is not particularly elegant as it does not take locales into account and
		assumes a standard US keyboard.

		Arguments:
		key -- A character

		Keyword arguments:
		mods -- a list of keyboard moderators (default = ["shift"])

		Returns:
		The character that results from combining the input key with shift.
		</DOC>"""

		if chr(key).isalpha():
			if "shift" in mods:
				return chr(key).upper()
			else:
				return chr(key).lower()

		if "shift" in mods:
			if chr(key) not in self.key_map:
				return ""
			return self.key_map[chr(key)]

		return chr(key)

	def to_int(self, key):

		"""<DOC>
		Returns the ASCII key code of a given key

		Arguments:
		key -- a key in character or ASCII keycode notation

		Returns:
		A key in ASCII keycode notation
		</DOC>"""

		if type(key) == int:
			return key
		if key == "timeout":
			return None
		if key not in self.key_codes:
			raise openexp.exceptions.response_error("'%s' is not a valid keyboard input character." % key)
		return self.key_codes[key]

	def to_chr(self, key):

		"""<DOC>
		Returns the character notation of a given key

		Arguments:
		key -- a key in character or ASCII keycode notation
		
		Returns:
		A key in character notation
		</DOC>"""

		if key == None:
			return "timeout"
		if type(key) == str or type(key) == chr:
			return key
		return pygame.key.name(key)
		
	def valid_keys(self):
	
		"""<DOC>
		Generates a list of valid key names
		
		Returns:
		A list of valid key names
		</DOC>"""
		
		return self.key_codes							
		
	def synonyms(self, key):
	
		"""
		Gives a list of synonyms for a key, either codes or names
		
		Returns:
		A list of synonyms
		"""
		
		if type(key) == str:
			return self.synonyms(self.to_int(key))			
		l = []
		for name, code in self.key_codes.iteritems():
			if code == key:
				l.append(name)
		return l

	def flush(self):

		"""<DOC>
		Clears all pending input, not limited to the keyboard
		
		Exceptions:
		A response_error if 'escape' was pressed		

		Returns:
		True if a key had been pressed (i.e., if there was something
		to flush) and False otherwise
		</DOC>"""

		keypressed = False
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				keypressed = True
				if event.key == pygame.K_ESCAPE:
					raise openexp.exceptions.response_error("The escape key was pressed.")
		return keypressed

