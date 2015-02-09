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
from string import whitespace
from libopensesame.exceptions import osexception
from openexp._keyboard import keyboard

# Whitespace, backspace, and empty strings are not acceptable names for keys.
# These should be converted to descriptions, e.g. '\t' to 'tab'
invalid_unicode = [u'', u'\x08'] + list(whitespace)

class legacy(keyboard.keyboard):

	"""
	desc:
		This is a keyboard backend built on top of PyGame.
		For function specifications and docstrings, see
		`openexp._keyboard.keyboard`.
	"""

	def __init__(self, experiment, keylist=None, timeout=None):

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

	def get_key(self, keylist=None, timeout=None):

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
				if event.unicode in invalid_unicode:
					key = self.key_name(event.key)
				else:
					key = event.unicode
				if keylist == None or key in keylist:
					return key, time
			if timeout != None and time-start_time >= timeout:
				break
		return None, time

	def get_mods(self):

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

	def valid_keys(self):

		return sorted(self.key_name_to_code.keys())

	def synonyms(self, key):

		# If the key is not familiar, simply return it plus its string
		# representation.
		if key not in self.key_name_to_code:
			return [key, self.experiment.unistr(key)]
		return self.key_code_to_name[self.key_name_to_code[key]]

	def flush(self):

		keypressed = False
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				keypressed = True
				if event.key == pygame.K_ESCAPE:
					raise osexception( \
						u"The escape key was pressed.")
		return keypressed

	def key_name(self, key):

		return unicode(pygame.key.name(key)).replace(u'[', u'').replace(u']',
			u'')
