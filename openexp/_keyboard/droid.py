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
import sys
import openexp
from openexp._keyboard.legacy import *

try:
	import android
except ImportError:
	android = None

class droid(legacy):

	"""
	desc: |
		This is a keyboard backend built on top of PyGame, adapted for Android
		devices.

		For function specifications and docstrings, see
		`openexp._keyboard.keyboard`.
	"""

	def get_key(self, keylist=None, timeout=None):

		if not self.persistent_virtual_keyboard and android != None:
			android.show_keyboard()
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
					raise osexception("The escape key was pressed.")
				# TODO The unicode mechanism that ensures compatibility between
				# keyboard layouts doesn't work for Android, so we use key
				# names. I'm not sure what effect this will have on non-QWERTY
				# virtual keyboards.
				if android != None:
					key = pygame.key.name(event.key)
				else:
					# If we're not on Android, simply use the same logic as the
					# legacy back-end.
					if event.unicode in invalid_unicode or \
						event.unicode not in printable:
						key = self.key_name(event.key)
					else:
						key = event.unicode
				if keylist == None or key in keylist:
					if not self.persistent_virtual_keyboard and android != None:
						android.hide_keyboard()
					return key, time
			if timeout != None and time-start_time >= timeout:
				break
			# Allow Android interrupt
			if android != None and android.check_pause():
				android.wait_for_resume()
		if not self.persistent_virtual_keyboard and android != None:
			android.hide_keyboard()
		return None, time

	def show_virtual_keyboard(self, visible=True):

		if android == None:
			return
		self.persistent_virtual_keyboard = visible
		if visible:
			android.show_keyboard()
		else:
			android.hide_keyboard()
