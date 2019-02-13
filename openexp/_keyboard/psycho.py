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
from libopensesame.exceptions import osexception
from openexp._keyboard.keyboard import Keyboard
from psychopy import event
import pyglet.window.key
from openexp.backend import configurable


class Psycho(Keyboard):

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

	def __init__(self, experiment, **resp_args):

		Keyboard.__init__(self, experiment, **resp_args)
		self._latest_modifiers = {}

	def valid_keys(self):

		l = []
		for i in dir(pyglet.window.key):
			if isinstance(getattr(pyglet.window.key, i), int):
				l.append(i)
		return l

	@configurable
	def get_key(self):

		keylist = self.keylist
		if keylist is not None:
			keylist += [u'escape']
		timeout = self.timeout
		start_time = self.experiment.clock.time()
		while True:
			# Don't use the timeStamped keyword, because it bugs on older
			# versions of PsychoPy (at least 1.79.01 under Ubuntu 14.04).
			# See https://github.com/smathot/OpenSesame/issues/381
			time = self.experiment.clock.time()
			keys = event.getKeys(keylist, modifiers=True)
			for key, modifiers in keys:
				if key == u'escape':
					self.experiment.pause()
				if keylist is None or key in keylist:
					self._latest_modifiers = modifiers
					return key, time
			if timeout is not None and time - start_time >= timeout:
				break
		self._latest_modifiers = {}
		return None, time

	def get_mods(self):

		return [
			m
			for m in (u'shift', u'ctrl', u'alt')
			if self._latest_modifiers.get(m, False)
		]

	def synonyms(self, key):

		if key is None:
			return [None, 'None', 'none', 'NONE']

		# Respond correctly if a keycode is passed, rather than a Unicode string
		# key description.
		if type(key) == int:
			l = [key, pyglet.window.key.symbol_string(key).lower()]
			if l[-1].upper() != l[-1].lower():
				l.append(l[-1].upper())
			return l

		# Sanity check
		if not isinstance(key, basestring):
			raise osexception(
				u'Key names should be string or numeric, not %s' % type(key))

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
		if key.lower() == u'none':
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
			if key == u"escape":
				self.experiment.pause()
			keypressed = True
		return keypressed

	def _keycode_to_str(self, keycode):

		return pyglet.window.key.symbol_string(keycode).lower()


# Non PEP-8 alias for backwards compatibility
psycho = Psycho
