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
	This is a canvas backend which uses PsychoPy
	"""

	def __init__(self, experiment, keylist = None, timeout = None):
	
		"""
		Intializes the keyboard object.
		
		Arguments:
		experiment -- an instance of libopensesame.experiment.experiment
		
		Keyword arguments:
		keylist -- a list of human readable keys that are accepted or None
				   to accept all keys (default = None)
		timeout -- an integer value specifying a timeout in milliseconds or
				   None for no timeout (default = None)
		"""	
		
		if experiment.canvas_backend != "psycho":
			raise openexp.exceptions.response_error("The psycho keyboard backend must be used in combination with the psycho canvas backend!")		
		
		self.experiment = experiment
		self.set_keylist(keylist)
		self.set_timeout(timeout)
		
	def valid_keys(self):
	
		"""
		Generates a list of valid key names
		
		Returns:
		A list of names
		"""
		
		l = []
		for i in dir(pyglet.window.key):
			if type(eval("pyglet.window.key.%s" % i)) == int:
				l.append(i)
		return l
				
	def set_keylist(self, keylist = None):
	
		"""
		Sets a list of accepted keys

		Keyword arguments:
		keylist -- a list of human readable keys that are accepted or None
				   to accept all keys (default = None)		
		"""	
		
		if keylist == None:
			self._keylist = None
		else:
			for key in keylist:
				try:
					eval("pyglet.window.key.%s" % key.upper())
				except:
					raise openexp.exceptions.response_error("The key '%s' is not recognized by the psycho keyboard backend. Please refer to <a href='http://pyglet.org/doc/api/pyglet.window.key-module.html'>http://pyglet.org/doc/api/pyglet.window.key-module.html</a> for a list of valid keys." % key)
		
			self._keylist = keylist
							
	def set_timeout(self, timeout = None):
	
		"""
		Sets a timeout
		
		Keyword arguments:
		timeout -- an integer value specifying a timeout in milliseconds or
				   None for no timeout (default = None)		
		"""	
	
		self.timeout = timeout
				
	def get_key(self, keylist = None, timeout = None):
	
		"""
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
		"""	
		
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
	
		while timeout == None or time - start_time <= timeout:
			time = 1000.0 * self.experiment.clock.getTime()		
			keys = event.getKeys(_keylist, timeStamped = self.experiment.clock)						
			for key, time in keys:						
				time *= 1000.0			
				if key == "escape":
					raise openexp.exceptions.response_error("The escape key was pressed.")
				elif keylist == None or key in keylist:
					return key, time
					
		return None, time
				
	def get_mods(self):
	
		"""
		Returns a list of keyboard moderators (e.g., shift, alt, etc.) that are
		currently pressed.
		
		Returns:
		A list of keyboard moderators. An empty list is returned if no moderators
		are pressed.
		"""	
		
		pass
		
	def shift(self, key):
	
		"""
		Returns the character that results from pressing a key together with the
		shift moderator. E.g., "3" + "Shift" -> "#". This function is not
		particularly elegant as it does not take locales into account and assumes
		a standard US keyboard.
		
		Arguments:
		key -- A character
		
		Returns:
		The character that results from combining the input key with shift.
		"""	
	
		pass
		
	def to_int(self, key):
	
		"""
		Returns the ASCII key code of a given key
		
		Arguments:
		key -- a key in character or ASCII keycode notation
		
		Returns:
		A key in ASCII keycode notation
		"""	
	
		return ord(key)
		
	def to_chr(self, key):
	
		"""
		Returns the character notation of a given key
		
		Arguments:
		key -- a key in character or ASCII keycode notation
		
		Returns:
		A key in character notation
		"""

		if key == None:
			return "timeout"	
		return key
		
	def synonyms(self, key):
	
		"""
		Gives a list of synonyms for a key, either codes or names
		
		Returns:
		A list of synonyms
		"""
		
		if key == int:
			l = [pyglet.window.key.symbol_string(key).lower()]
			if l[-1].upper() != l[-1].lower():
				l.append(l[-1].upper())			
			return l
		if key.upper() == key.lower():
			return key	
		return [key.upper(), key.lower()]
		
	def flush(self):
	
		"""
		Clears all pending input, not limited to the keyboard
		
		Exceptions:
		A response_error if 'escape' was pressed
		
		Returns:
		True if a key had been pressed (i.e., if there was something
		to flush) and False otherwise
		"""	

		keypressed = False
		for key in event.getKeys():
			if key == "escape":
				raise openexp.exceptions.response_error("The escape key was pressed.")
			keypressed = True		
		return keypressed

