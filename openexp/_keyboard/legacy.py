#-*- coding:utf-8 -*-

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

from string import whitespace, printable
import pygame
from pygame.locals import *
import openexp.keyboard

# Whitespace and empty strings are not acceptable names for keys. These should
# be converted to descriptions, e.g. '\t' to 'tab'
invalid_unicode = [''] + list(whitespace)

# This is a crude keymap that allows you to convert into the corresponding keys
# plus shift
key_map = {
	"1" : "!", "2" : "@", "3" : "#", "4" : "$", "5" : "%", "6" : "^", 
	"7" : "&", "8" : "*", "9" : "(", "0" : ")", "-" : "_", "=" : "+",
	"[" : "{", "]" : "}", "\\" : "|", ";" : ":", "\"" : "'", "," : "<",
	"." : ">", "/" : "?"
	}

class legacy:

	"""
	The legacy backend is the default backend which uses PyGame to handle all
	keyboard input. This is essentially a class based on the openexp.response
	module, which is now deprecated.

	This class can serve as a template for creating new OpenSesame keyboard
	input backends. The new backend can be activated by adding
	"set keyboard_backend [name]" to the OpenSesame script

	A few guidelines:
	-- Acceptable key-formats are characters and integers, interpreted as ASCII
	   key codes
	-- Moderators are represented by the following strings: "shift", "alt",
	   "control" and "meta"
	-- Catch exceptions wherever possible and raise an
	   openexp.exceptions.canvas_error with a clear and descriptive error
	   message
	-- Do not deviate from the guidelines. All back-ends should be
	   interchangeable and transparent to OpenSesame. You are free to add
	   functionality to this class, to be used in inline scripts, but this
	   should not break the basic functionality.
	"""
	
	def __init__(self, experiment, keylist=None, timeout=None):

		"""<DOC>
		Intializes the keyboard object.
		
		Keys can be identified either by character or name. This is case #
		insensitive. Naming keys using ASCII (integer) key codes is deprecated.

		For example:
		- The key 'a' is represented by 'a' and 'A'
		- The up arrow is represented by 'up' and 'UP'
		- The '/' key is represented by '/', 'slash', and 'SLASH'
		- The spacebar is represented by 'space' and 'SPACE'
		
		For a complete list of available key names, click on the 'list available #
		keys' button in the keyboard_response tab within OpenSesame.

		Arguments:
		experiment -- An instance of libopensesame.experiment.experiment.

		Keyword arguments:
		keylist -- A list of human readable keys that are accepted or None to #
				   accept all keys (default=None).
		timeout -- An integer value specifying a timeout in milliseconds or None #
				   for no timeout (default=None).
				   
		Example:
		>>> from openexp.keyboard import keyboard
		>>> my_keyboard = keyboard(exp, keylist=['z', 'm'], timeout=2000)
		</DOC>"""

		pygame.init()
		self.key_code_to_name = {}
		self.key_name_to_code = {}		
		for i in dir(pygame):
			if i[:2] == "K_":
				code = eval("pygame.%s" % i)
				name1 = pygame.key.name(code).lower()
				name2 = name1.upper()
				name3 = i[2:].lower()
				name4 = name3.upper()
				self.key_code_to_name[code] = name1, name2, name3, name4				
				self.key_name_to_code[name1] = code
				self.key_name_to_code[name2] = code
				self.key_name_to_code[name3] = code
				self.key_name_to_code[name4] = code				
		self.experiment = experiment
		self.set_keylist(keylist)
		self.set_timeout(timeout)		
		
	def set_keylist(self, keylist=None):

		"""<DOC>
		Sets a list of accepted keys.

		Keyword arguments:
		keylist -- A list of keys that are accepted or None to accept all keys #
				   (default=None).
				   
		Example:
		>>> from openexp.keyboard import keyboard
		>>> my_keyboard = keyboard(exp)
		>>> my_keyboard.set_keylist( ['z', 'm'] )
		</DOC>"""

		if keylist == None:
			self._keylist = None
		else:			
			self._keylist = []
			for key in keylist:
				self._keylist += self.synonyms(key)

	def set_timeout(self, timeout=None):

		"""<DOC>
		Sets a timeout.

		Keyword arguments:
		timeout -- An integer value specifying a timeout in milliseconds or None #
				   for no timeout (default=None).
				   
		Example:
		>>> from openexp.keyboard import keyboard
		>>> my_keyboard = keyboard(exp)
		>>> my_keyboard.set_timeout(2000)
		</DOC>"""

		self.timeout = timeout

	def get_key(self, keylist=None, timeout=None):

		"""<DOC>
		Waits for keyboard input.

		Keyword arguments:
		keylist -- A list of human readable keys that are accepted or None to #
				   use the default. This parameter does not change the default #
				   keylist (default=None).
		timeout -- An integer value specifying a timeout in milliseconds or None #
				   to use the default. This parameter does not change the #
				   default timeout (default=None).
				   
		Exceptions:
		A response_error if 'escape' was pressed.

		Returns:
		A (key, timestamp) tuple. The key is None if a timeout occurs.
		
		Example:
		>>> from openexp.keyboard import keyboard
		>>> my_keyboard = keyboard(exp, timeout=2000)
		>>> response, timestamp = my_keyboard.get_key()
		>>> if response == None:
		>>> 		print 'A timeout occurred!'
		</DOC>"""
				
		start_time = pygame.time.get_ticks()
		time = start_time		

		if keylist == None:
			keylist = self._keylist
		if timeout == None:
			timeout = self.timeout

		while True:
			time = pygame.time.get_ticks()
			for event in pygame.event.get():
				if event.type != pygame.KEYDOWN:
					continue
				if event.key == pygame.K_ESCAPE:
					raise openexp.exceptions.response_error( \
						"The escape key was pressed.")
				if event.unicode in invalid_unicode or event.unicode not in \
					printable:
					key = pygame.key.name(event.key)
				else:
					key = event.unicode
				if keylist == None or key in keylist:
					return key, time				
			if timeout != None and time-start_time >= timeout:
				break
		
		return None, time

	def get_mods(self):

		"""<DOC>
		Returns a list of keyboard moderators (e.g., shift, alt, etc.) that are #
		currently pressed.

		Returns:
		A list of keyboard moderators. An empty list is returned if no #
		moderators are pressed.

		Example:
		>>> from openexp.keyboard import keyboard
		>>> my_keyboard = keyboard(exp)
		>>> moderators = my_keyboard.get_mods()
		>>> if 'shift' in moderators:
		>>> 		print 'The shift-key is down!'
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

	def shift(self, key, mods=["shift"]):

		"""
		Returns the character that results from pressing a key together with the
		moderators, typically a shift. E.g., "3" + "Shift" -> "#". This function
		is not particularly elegant as it does not take locales into account and
		assumes a standard US keyboard.

		Arguments:
		key -- A character.

		Keyword arguments:
		mods -- A list of keyboard moderators (default=["shift"]).

		Returns:
		The character that results from combining the input key with shift.
		"""

		if key.isalpha():
			if "shift" in mods:
				return key.upper()
			else:
				return key.lower()

		if "shift" in mods:
			if key not in key_map:
				return ""
			return key_map[key]

		return key

	def to_int(self, key):

		"""
		DEPRECATED
		
		This function has been removed as of 0.26. Keys are now only referred to
		by their name and/ or character
		
		Arguments:
		key -- a key
		
		Exception:
		This function always raises an exception
		"""

		raise openexp.exceptions.response_error( \
			"keyboard.to_int() is deprecated")

	def to_chr(self, key):

		"""
		DEPRECATED
		
		This function is deprecated as of 0.26. Keys are now only referred to
		by their name and/ or character and this conversion function is no
		longer necessary. For backwards compatibility, the input argument is 
		silently returned.
		
		Arguments:
		key -- a key

		Returns:
		The key		
		"""

		return key
		
	def valid_keys(self):
	
		"""
		Generates a list of valid key names. Mostly for use by the GUI.
		
		Returns:
		A list of valid key names
		"""
		
		return sorted(self.key_name_to_code.keys())
		
	def synonyms(self, key):
	
		"""
		Gives a list of synonyms for a key, either codes or names
		
		Returns:
		A list of synonyms
		"""
		
		if key not in self.key_name_to_code:
			return [key]
		return self.key_code_to_name[self.key_name_to_code[key]]

	def flush(self):

		"""<DOC>
		Clears all pending input, not limited to the keyboard.
		
		Exceptions:
		A response_error if 'escape' was pressed
		
		Returns:
		True if a key had been pressed (i.e., if there was something #
		to flush) and False otherwise.
		
		Example:
		>>> from openexp.keyboard import keyboard
		>>> my_keyboard = keyboard(exp)
		>>> my_keyboard.flush()
		>>> response, timestamp = my_keyboard.get_key()
		</DOC>"""

		keypressed = False
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				keypressed = True
				if event.key == pygame.K_ESCAPE:
					raise openexp.exceptions.response_error( \
						"The escape key was pressed.")
		return keypressed

