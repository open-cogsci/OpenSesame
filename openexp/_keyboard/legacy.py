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

import pygame
from pygame.locals import *
from string import whitespace, printable
from libopensesame.exceptions import osexception

# Whitespace and empty strings are not acceptable names for keys. These should
# be converted to descriptions, e.g. '\t' to 'tab'
invalid_unicode = [u''] + list(whitespace)

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
	   osexception with a clear and descriptive error
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
		- The key 'a' is represented by 'a' and 'A'.
		- The up arrow is represented by 'up' and 'UP'.
		- The '/' key is represented by '/', 'slash', and 'SLASH'.
		- The spacebar is represented by 'space' and 'SPACE'.

		For a complete list of available key names, click on the 'list available #
		keys' button in the keyboard_response tab within OpenSesame.

		Arguments:
		experiment -- An instance of libopensesame.experiment.experiment.

		Keyword arguments:
		keylist -- A list of human-readable keys that are accepted or None to #
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
			if i[:2] == u"K_":
				code = getattr(pygame, i)
				name1 = self.key_name(code).lower()
				name2 = name1.upper()
				name3 = i[2:].lower()
				name4 = name3.upper()
				self.key_code_to_name[code] = [name1, name2, name3, name4]
				try:
					i = int(name5)
					self.key_code_to_name[code].append(name5)
				except:
					pass
				self.key_name_to_code[name1] = code
				self.key_name_to_code[name2] = code
				self.key_name_to_code[name3] = code
				self.key_name_to_code[name4] = code
		self.persistent_virtual_keyboard = False
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
		keylist -- A list of human-readable keys that are accepted or None to #
				   use the default. This parameter does not change the default #
				   keylist (default=None).
		timeout -- An integer value specifying a timeout in milliseconds or None #
				   to use the default. This parameter does not change the #
				   default timeout (default=None).

		Exceptions:
		An osexception if 'escape' was pressed.

		Returns:
		A (key, timestamp) tuple. The key is None if a timeout occurs.

		Example:
		>>> from openexp.keyboard import keyboard
		>>> my_keyboard = keyboard(exp, timeout=2000)
		>>> response, timestamp = my_keyboard.get_key()
		>>> if response == None:
		>>> 	print('A timeout occurred!')
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
					raise osexception(u'The escape key was pressed.')
				if event.unicode in invalid_unicode or event.unicode not in \
					printable:
					key = self.key_name(event.key)
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
		>>> 	print('The shift-key is down!')
		</DOC>"""

		l = []
		mods = pygame.key.get_mods()
		if mods & KMOD_LSHIFT or mods & KMOD_RSHIFT or mods & KMOD_SHIFT:
			l.append(u"shift")
		if mods & KMOD_LCTRL or mods & KMOD_RCTRL or mods & KMOD_CTRL:
			l.append(u"ctrl")
		if mods & KMOD_LALT or mods & KMOD_RALT or mods & KMOD_ALT:
			l.append(u"alt")
		if mods & KMOD_LMETA or mods & KMOD_RMETA or mods & KMOD_META:
			l.append(u"meta")
		return l

	def shift(self, key, mods=[u"shift"]):

		"""
		DEPRECATED

		This function has been deprecated as of 0.27.4. Shift is handled
		transparently by keyboard.get_key()

		Arguments:
		key 	--	A key.

		Keyword arguments:
		mods	--	A list of keyboard modifiers.

		Exception:
		This function always raises an exception
		"""

		raise osexception( \
			u"keyboard.shift() is deprecated")

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

		raise osexception( \
			u"keyboard.to_int() is deprecated")

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
		Gives a list of synonyms for a key, either codes or names. Synonyms
		include all variables as types and as Unicode strings (if applicable).

		Returns:
		A list of synonyms
		"""

		# If the key is not familiar, simply return it plus its string
		# representation.
		if key not in self.key_name_to_code:
			return [key, self.experiment.unistr(key)]
		return self.key_code_to_name[self.key_name_to_code[key]]

	def flush(self):

		"""<DOC>
		Clears all pending input, not limited to the keyboard.

		Exceptions:
		An osexception if 'escape' was pressed

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
					raise osexception( \
						u"The escape key was pressed.")
		return keypressed

	def key_name(self, key):

		"""
		Returns the name that corresponds to a key code. This intercepts the
		pygame.key.name() function, to prevent invalid names like '[1]'.

		Arguments:
		key		--	A key code.

		Returns:
		A unicode string corresponding to the key code.
		"""

		return unicode(pygame.key.name(key)).replace(u'[', u'') \
			.replace(u']', u'')

	def show_virtual_keyboard(self, visible=True):

		"""<DOC>
		Shows or hides a virtual keyboard if this is supported by the back-end.
		This function is only necessary if you want the virtual keyboard to
		remain visible while collecting multicharacter responses. Otherwise,
		get_key() will implicitly shown and hide the keyboard for a single-
		character response.

		This function does nothing for back-ends that do not support virtual
		keyboards.

		Arguments:
		visible		--	True if the keyboard should be shown, False otherwise.

		Example:
		>>> from openexp.keyboard import keyboard
		>>> my_keyboard = keyboard(exp)
		>>> my_keyboard.show_virtual_keyboard(True)
		>>> response1, timestamp2 = my_keyboard.get_key()
		>>> response2, timestamp2 = my_keyboard.get_key()
		>>> my_keyboard.show_virtual_keyboard(False)
		</DOC>"""

		pass
