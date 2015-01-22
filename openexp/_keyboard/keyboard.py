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

# If available, use the yaml.inherit metaclass to copy the docstrings from
# keyboard onto the back-end-specific implementations of this class
# (legacy, etc.)
try:
	from yamldoc import inherit as docinherit
except:
	docinherit = type

class keyboard(object):

	"""
	desc: |
		The `keyboard` class is used to collect keyboard responses.

		__Example:__

		~~~ {.python}
		# Wait for a 'z' or 'x' key with a timeout of 3000 ms
		from openexp.keyboard import keyboard
		my_keyboard = keyboard(exp, keylist=['z', 'x'], timeout=3000)
		start_time = self.time()
		key, end_time = my_keyboard.get_key()
		exp.set('response', key)
		exp.set('response_time', end_time - start_time)
		~~~

		__Function list:__

		%--
		toc:
			mindepth: 2
			maxdepth: 2
		--%

		%--
		constant:
			arg_keylist:
				A list of human-readable keys that are accepted or `None` to
				accept all keys.
			arg_timeout:
				A numeric value specifying a timeout in milliseconds or `None`
				for no (i.e. infinite) timeout.
		--%
	"""

	__metaclass__ = docinherit

	def __init__(self, experiment, keylist=None, timeout=None):

		"""
		desc: |
			Constructor. Intializes the keyboard object.

			Keys can be identified either by character or name. This is case
			insensitive. Naming keys using ASCII (integer) key codes is
			deprecated.

			For example:

			- The key 'a' is represented by 'a' and 'A'.
			- The up arrow is represented by 'up' and 'UP'.
			- The '/' key is represented by '/', 'slash', and 'SLASH'.
			- The spacebar is represented by 'space' and 'SPACE'.

			For a complete list of available key names, click on the
			'list available keys' button in the keyboard_response tab within
			OpenSesame.

		arguments:
			experiment:
				desc:		The experiment object.
				type:		experiment

		keywords:
			keylist:
				desc:	"%arg_keylist"
				type:	[list, NoneType]
			timeout:
				desc:	"%arg_timeout"
				type:	[int, float, NoneType]

		example: |
			from openexp.keyboard import keyboard
			my_keyboard = keyboard(exp, keylist=['z', 'm'], timeout=2000)
		"""

		raise NotImplementedError()

	def set_keylist(self, keylist=None):

		"""
		desc:
			Sets the list of accepted keys.

		keywords:
			keylist:
				desc:	"%arg_keylist"
				type:	[list, NoneType]

		example: |
			from openexp.keyboard import keyboard
			my_keyboard = keyboard(exp)
			my_keyboard.set_keylist( ['z', 'm'] )
		"""

		if keylist is None:
			self._keylist = None
		else:
			self._keylist = []
			for key in keylist:
				self._keylist += self.synonyms(key)

	def set_timeout(self, timeout=None):

		"""
		desc:
			Sets a timeout.

		keywords:
			timeout:
				desc:	"%arg_timeout"
				type:	[int, float, NoneType]

		example: |
			from openexp.keyboard import keyboard
			my_keyboard = keyboard(exp)
			my_keyboard.set_timeout(2000)
		"""

		self.timeout = timeout

	def get_key(self, keylist=None, timeout=None):

		"""
		desc:
			Collects a single key press.

		keywords:
			keylist:
				desc:	"%arg_keylist"
				type:	[list, NoneType]
			timeout:
				desc:	"%arg_timeout"
				type:	[int, float, NoneType]

		returns:
			desc:		A `(key, timestamp)` tuple. `key` is None if a timeout
						occurs.
			type:		tuple

		example: |
			from openexp.keyboard import keyboard
			my_keyboard = keyboard(exp, timeout=2000)
			response, timestamp = my_keyboard.get_key()
			if response is None:
				print('A timeout occurred!')
		"""

		raise NotImplementedError()

	def get_mods(self):

		"""
		desc:
			Returns a list of keyboard moderators (e.g., shift, alt, etc.) that
			are currently pressed.

		returns:
			desc:	A list of keyboard moderators. An empty list is returned if
					no moderators are pressed.
			type:	list

		example: |
			from openexp.keyboard import keyboard
			my_keyboard = keyboard(exp)
			moderators = my_keyboard.get_mods()
			if 'shift' in moderators:
				print('The shift-key is down!')
		"""

		raise NotImplementedError()

	def valid_keys(self):

		"""
		desc:
			Tries to guess which key names are accepted by the back-end. For
			internal use.

		visible:
			False

		returns:
			desc:	A list of valid key names.
			type:	list
		"""

		raise NotImplementedError()

	def synonyms(self, key):

		"""
		desc:
			Gives a list of synonyms for a key, either codes or names. Synonyms
			include all variables as types and as Unicode strings
			(if applicable).

		visible:
			False

		returns:
			desc:	A list of synonyms
			type:	list
		"""

		raise NotImplementedError()

	def flush(self):

		"""
		desc:
			Clears all pending keyboard input, not limited to the keyboard.

		returns:
			desc:	True if a key had been pressed (i.e., if there was something
					to flush) and False otherwise.
			type:	bool

		Example: |
			from openexp.keyboard import keyboard
			my_keyboard = keyboard(exp)
			my_keyboard.flush()
			response, timestamp = my_keyboard.get_key()
		"""

		raise NotImplementedError()

	def show_virtual_keyboard(self, visible=True):

		"""
		desc: |
			Shows or hides a virtual keyboard if this is supported by the
			back-end. This function is only necessary if you want the virtual
			keyboard to remain visible while collecting multicharacter
			responses. Otherwise, [keyboard.get_key] will implicitly shown and
			hide the keyboard for a single-character response.

			This function does nothing for back-ends that do not support virtual
			keyboards.

		keywords:
			visible:
				desc:	True if the keyboard should be shown, False otherwise.
				type:	bool

		example: |
			from openexp.keyboard import keyboard
			my_keyboard = keyboard(exp)
			my_keyboard.show_virtual_keyboard(True)
			response1, timestamp2 = my_keyboard.get_key()
			response2, timestamp2 = my_keyboard.get_key()
			my_keyboard.show_virtual_keyboard(False)
		"""

		pass
