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
from openexp._keyboard.legacy import *
import pygame
from openexp.backend import configurable
try:
	import android
except ImportError:
	android = None


class Droid(Legacy):

	"""
	desc: |
		This is a keyboard backend built on top of PyGame, adapted for Android
		devices.

		For function specifications and docstrings, see
		`openexp._keyboard.keyboard`.
	"""

	def _get_key_event(self, event_type):

		if not self.persistent_virtual_keyboard and android is not None:
			android.show_keyboard()
		start_time = pygame.time.get_ticks()
		time = start_time
		keylist = self.keylist
		timeout = self.timeout
		while True:
			time = pygame.time.get_ticks()
			for event in pygame.event.get(event_type):
				if event.key == pygame.K_ESCAPE:
					self.experiment.pause()
				# TODO The unicode mechanism that ensures compatibility between
				# keyboard layouts doesn't work for Android, so we use key
				# names. I'm not sure what effect this will have on non-QWERTY
				# virtual keyboards.
				if android is not None:
					key = pygame.key.name(event.key)
					if len(key) == 1 and (
						event.mod & pygame.KMOD_LSHIFT or
						event.mod & pygame.KMOD_RSHIFT
					):
						key = key.upper()
				else:
					# If we're not on Android, simply use the same logic as the
					# legacy back-end.
					if event.unicode in invalid_unicode:
						key = self.key_name(event.key)
					else:
						key = event.unicode
				if keylist is None or key in keylist:
					if not self.persistent_virtual_keyboard and android is not None:
						android.hide_keyboard()
					return key, time
			if timeout is not None and time-start_time >= timeout:
				break
			# Allow Android interrupt
			if android is not None and android.check_pause():
				android.wait_for_resume()
		if not self.persistent_virtual_keyboard and android is not None:
			android.hide_keyboard()
		return None, time

	def show_virtual_keyboard(self, visible=True):

		if android is None:
			return
		self.persistent_virtual_keyboard = visible
		if visible:
			android.show_keyboard()
		else:
			android.hide_keyboard()


# Non PEP-8 alias for backwards compatibility
droid = Droid
