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
from openexp.backend import backend, configurable
import warnings

class keyboard(backend):

	"""
	desc: |
		The `keyboard` class is used to collect keyboard responses.

		__Example:__

		~~~ .python
		# Wait for a 'z' or 'x' key with a timeout of 3000 ms
		my_keyboard = keyboard(keylist=['z', 'x'], timeout=3000)
		start_time = time()
		key, end_time = my_keyboard.get_key()
		var.response = key
		var.response_time = end_time - start_time
		~~~

		[TOC]

		## Things to know

		### Key names

		- Key names may differ between backends.
		- Keys can be identified either by character or name, and are
		  case-insentive. For example:
		  - The key 'a' is represented by 'a' and 'A'
		  - The up arrow is represented by 'up' and 'UP'
		  - The '/' key is represented by '/', 'slash', and 'SLASH'
		  - The spacebar is represented by 'space' and 'SPACE'
		- To find out the name of key, you can:
		  - Click on the 'list available keys' button of the
		    KEYBOARD_RESPONSE item.
		  - Collect a key press with a KEYBOARD_RESPONSE item, and display
		    the key name through a FEEDBACK item with the text 'You
		    pressed [response]' in it.

		### Response keywords

		Functions that accept `**resp_args` take the following keyword
		arguments:

		- `timeout` specifies a timeout value in milliseconds, or is set to
		  `None` to disable the timeout.
		- `keylist` specifies a list of keys that are accepted, or is set to
		  `None` accept all keys.

		~~~ .python
		# Get a left or right arrow press with a timeout of 3000 ms
		my_keyboard = keyboard()
		key, time = my_keyboard.get_key(keylist=[u'left', u'right'],
			timeout=3000)
		~~~

		Response keywords only affect the current operation (except when passed
		to [keyboard.\_\_init\_\_][__init__]). To change the behavior for all
		subsequent operations, set the response properties directly:

		~~~ .python
		# Get two key A or B presses with a 5000 ms timeout
		my_keyboard = keyboard()
		my_keyboard.keylist = [u'a', u'b']
		my_keyboard.timeout = 5000
		key1, time1 = my_keyboard.get_key()
		key2, time2 = my_keyboard.get_key()
		~~~

		Or pass the response options to [keyboard.\_\_init\_\_][__init__]:

		~~~ .python
		# Get two key A or B presses with a 5000 ms timeout
		my_keyboard = keyboard(keylist=[u'a', u'b'], timeout=5000)
		key1, time1 = my_keyboard.get_key()
		key2, time2 = my_keyboard.get_key()
		~~~
	"""

	def __init__(self, experiment, **resp_args):

		"""
		desc: |
			Constructor to create a new `keyboard` object. You do not generally
			call this constructor directly, but use the `keyboard()` function,
			which is described here: [/python/common/]().

		arguments:
			experiment:
				desc:		The experiment object.
				type:		experiment

		keyword-dict:
			resp_args:
				Optional [response keywords] (`timeout` and `keylist`) that will
				be used as the default for this `keyboard` object.

		example: |
			my_keyboard = keyboard(keylist=['z', 'm'], timeout=2000)
		"""

		self.experiment = experiment
		backend.__init__(self, configurables={
			u'timeout' : self.assert_numeric_or_None,
			u'keylist' : self.assert_list_or_None,
			}, **resp_args)

	def set_config(self, **cfg):

		# Add synonyms to keylist
		if u'keylist' in cfg and isinstance(cfg[u'keylist'], list):
			for key in list(cfg[u'keylist']):
				cfg[u'keylist'] += [key for key in self.synonyms(key) \
					if key not in cfg[u'keylist']]
		backend.set_config(self, **cfg)

	def default_config(self):

		return {
			u'timeout' 			: None,
			u'keylist'			: None,
			}

	@configurable
	def get_key(self, **resp_args):

		"""
		desc:
			Collects a single key press.

		keyword-dict:
			resp_args:
				Optional [response keywords] (`timeout` and `keylist`) that will
				be used for this call to [keyboard.get_key] this does not
				affect subsequent operations.

		returns:
			desc:		A `(key, timestamp)` tuple. `key` is None if a timeout
						occurs.
			type:		tuple

		example: |
			my_keyboard = keyboard()
			response, timestamp = my_keyboard.get_key(timeout=5000)
			if response is None:
				print(u'A timeout occurred!')
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
			my_keyboard = keyboard()
			moderators = my_keyboard.get_mods()
			if u'shift' in moderators:
				print(u'The shift-key is down!')
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
			my_keyboard = keyboard()
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
			my_keyboard = keyboard()
			my_keyboard.show_virtual_keyboard(True)
			response1, timestamp2 = my_keyboard.get_key()
			response2, timestamp2 = my_keyboard.get_key()
			my_keyboard.show_virtual_keyboard(False)
		"""

		pass

	# Deprecated functions

	def to_chr(self, key):

		"""
		visible:	False
		desc:		deprecated
		"""

		warnings.warn(u'keyboard.to_chr() has been deprecated.',
			DeprecationWarning)
		return key

	def set_keylist(self, keylist=None):

		"""
		visible:	False
		desc:		deprecated
		"""

		warnings.warn(u'keyboard.set_keylist() has been deprecated. '
			'Use keyboard.keylist instead.', DeprecationWarning)
		self.keylist = keylist

	def set_timeout(self, timeout=None):

		"""
		visible:	False
		desc:		deprecated
		"""

		warnings.warn(u'keyboard.set_timeout() has been deprecated. '
			'Use keyboard.timeout instead.', DeprecationWarning)
		self.timeout = timeout
