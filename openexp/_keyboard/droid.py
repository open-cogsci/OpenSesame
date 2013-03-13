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
	Keyboard back-end for Android devices. Only changes the legacy back-end by
	allowing Android-specific interrupts.
	"""			

	def get_key(self, keylist=None, timeout=None):

		"""See openexp._keyboard.legacy"""
		
		if android != None:
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
					raise openexp.exceptions.response_error( \
						"The escape key was pressed.")
				# TODO The unicode mechanism that ensures compatibility between
				# keyboard layouts doesn't work for Android, so we use key
				# names. I'm not sure what effect this will have on non-QWERTY
				# virtual keyboards.
				key = pygame.key.name(event.key)
				if keylist == None or key in keylist:
					if android != None:
						android.hide_keyboard()
					return key, time				
			if timeout != None and time-start_time >= timeout:
				break
			# Allow Android interrupt
			if android != None and android.check_pause():
				android.wait_for_resume()
		if android != None:
			android.hide_keyboard()				
		return None, time