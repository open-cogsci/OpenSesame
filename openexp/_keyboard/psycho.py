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

from libopensesame.exceptions import osexception
from openexp._keyboard import keyboard
from psychopy import event
import pyglet.window.key

class psycho(keyboard.keyboard):

	"""
	desc:
		This is a keyboard backend built on top of PsychoPy.
		For function specifications and docstrings, see
		`openexp._keyboard.keyboard`.
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

		if experiment.canvas_backend != u"psycho":
			raise osexception(
				u"The psycho keyboard backend must be used in combination with "
				u"the psycho canvas backend!")
		self.experiment = experiment
		self.set_keylist(keylist)
		self.set_timeout(timeout)

	def valid_keys(self):

		l = []
		for i in dir(pyglet.window.key):
			if isinstance(getattr(pyglet.window.key, i), int):
				l.append(i)
		return l

	def get_key(self, keylist=None, timeout=None):

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
					raise osexception("The escape key was pressed.")
				elif keylist == None or key in keylist:
					return key, time
			if timeout != None and time-start_time >= timeout:
				break

		return None, time

	def get_mods(self):

		# TODO: Accept moderator keys
		return []

	def synonyms(self, key):

		# Respond correctly if a keycode is passed, rather than a Unicode string
		# key description.
		if type(key) == int:
			l = [key, pyglet.window.key.symbol_string(key).lower()]
			if l[-1].upper() != l[-1].lower():
				l.append(l[-1].upper())
			return l
		
		# Sanity check
		if not isinstance(key, basestring):
			raise osexception('Key names should be string or numeric, not %s' \
				% type(key))
		
		# Make a list of all conceivable ways that a key might be referred to.
		l = [key]
		if key != key.upper():
			l.append(key.upper())
		if key != key.lower():
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
		return l

	def flush(self):

		keypressed = False
		for key in event.getKeys():
			if key == "escape":
				raise osexception("The escape key was pressed.")
			keypressed = True
		return keypressed

