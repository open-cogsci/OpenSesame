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

import openexp.exceptions
import openexp._keyboard.legacy
from psychopy import event
import pyglet.window.key

class psycho(openexp._keyboard.legacy.legacy):

	"""
	This is a canvas backend that uses PsychoPy
	"""
	
	# The keymap is an incomplete attempt at translating keys from the PyGame 
	# names to the names used by PsychoPy
	keymap = {
		'!' : 'exclamation',
		'"' : 'doublequote',
		'#' : 'hash',
		'$' : 'dollar',
		'&' : 'ampersand',
		'\'' : 'quoteleft',
		'(' : None,
		')' : None,
		'*' : 'asterisk',
		'+' : 'plus',
		',' : 'comma',
		'-' : 'minus',
		'.' : None,
		'/' : 'slash',
		':' : 'colin',
		';' : 'semicolon',
		'=' : 'equal',
		'>' : 'greater',
		'?' : 'question',
		'@' : 'at',
		'[' : 'bracketleft',
		'\\' : 'backslash',
		']' : 'bracketright',
		'^' : None,
		'_' : 'underscore'
		}	

	def __init__(self, experiment, keylist=None, timeout=None):

		"""See openexp._keyboard.legacy"""

		if experiment.canvas_backend != "psycho":
			raise openexp.exceptions.response_error( \
				"The psycho keyboard backend must be used in combination with the psycho canvas backend!")

		self.experiment = experiment
		self.set_keylist(keylist)
		self.set_timeout(timeout)				

	def valid_keys(self):

		"""See openexp._keyboard.legacy"""

		l = []
		for i in dir(pyglet.window.key):
			if isinstance(getattr(pyglet.window.key, i), int):
				l.append(i)
		return l

	def set_keylist(self, keylist=None):

		"""See openexp._keyboard.legacy"""

		if keylist == None:
			self._keylist = None
		else:
			_keylist = []
			for key in keylist:
				if key in self.keymap:
					_keylist.append(self.keymap[key])
				else:				
					if not hasattr(pyglet.window.key, key.upper()) and not \
						hasattr(pyglet.window.key, "NUM_%s" % key):
						raise openexp.exceptions.response_error( \
							"The key '%s' is not recognized by the psycho keyboard backend. Please refer to <a href='http://pyglet.org/doc/api/pyglet.window.key-module.html'>http://pyglet.org/doc/api/pyglet.window.key-module.html</a> for a list of valid keys." \
							% key)
					_keylist.append(key)
			self._keylist = _keylist

	def set_timeout(self, timeout=None):

		"""See openexp._keyboard.legacy"""

		self.timeout = timeout

	def get_key(self, keylist=None, timeout=None):

		"""See openexp._keyboard.legacy"""

		if keylist == None:
			keylist = self._keylist
		if timeout == None:
			timeout = self.timeout

		if keylist == None:
			_keylist = None
		else:
			_keylist = keylist + ["escape"]
			
		start_time = 1000.0 * self.experiment.clock.getTime()
		time = start_time
		
		while True:
			time = 1000.0 * self.experiment.clock.getTime()
			keys = event.getKeys(_keylist, timeStamped=self.experiment.clock)
			for key, time in keys:
				time *= 1000.0
				if key == "escape":
					raise openexp.exceptions.response_error( \
						"The escape key was pressed.")
				elif keylist == None or key in keylist:				
					return key, time
			if timeout != None and time-start_time >= timeout:
				break

		return None, time

	def get_mods(self):

		"""See openexp._keyboard.legacy"""

		# TODO: Accept moderator keys
		return []

	def shift(self, key):

		"""See openexp._keyboard.legacy"""

		# TODO: Accept moderator keys
		return key

	def synonyms(self, key):

		"""See openexp._keyboard.legacy"""
		
		# Respond correctly if a keycode is passed, rather than a Unicode string
		# key description.
		if type(key) == int:
			l = [key, pyglet.window.key.symbol_string(key).lower()]
			if l[-1].upper() != l[-1].lower():
				l.append(l[-1].upper())
			return l
		
		# Sanity check
		if not isinstance(key, basestring):
			raise openexp.exceptions( \
				'Key names should be string or numeric, not %s' % type(key))
		
		# Make a list of all conceivable ways that a key might be referred to.
		l = [key, key.upper()]
		if key.upper() != key.lower():
			l.append(key.lower())
		for char, name in self.keymap.items():
			if key == char:
				l.append(name)
			if key.lower() == name:
				l.append(char)	
		# Make sure that we can deal with None/ timeout responses
		if key.lower() == 'none':
			l.append(None)
		# Make sure that we convert numeric strings to ints as well
		try:
			i = int(key)
			l.append(i)
		except:
			pass
		print 'Synonym for %s (%s) == %s' % (key, type(key), l)
		return l

	def flush(self):

		"""See openexp._keyboard.legacy"""

		keypressed = False
		for key in event.getKeys():
			if key == "escape":
				raise openexp.exceptions.response_error( \
					"The escape key was pressed.")
			keypressed = True
		return keypressed

