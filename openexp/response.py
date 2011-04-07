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

print "*** openexp.response: This module is deprecated and may be removed in future versions of OpenSesame. Please use openexp.keyboard and/ or openexp.mouse instead."

import openexp.exceptions	
import warnings
import pygame
from pygame.locals import *
import openexp.exceptions

key_codes = {}
key_map = {
	"1" : "!", "2" : "@", "3" : "#", "4" : "$", "5" : "%",\
	"6" : "^", "7" : "&", "8" : "*", "9" : "(", "0" : ")", \
	"-" : "_", "=" : "+", "[" : "{", "]" : "}", "\\" : "|", \
	";" : ":", "\"" : "'", "," : "<", "." : ">", "/" : "?"
	}

def init_key_codes():
	
	"""
	Make a dictionary which maps all human
	readable key names to pygame values
	"""
	
	global key_codes

	for i in dir(pygame):
		if i[:2] == "K_":
			code = eval("pygame.%s" % i)
			name = pygame.key.name(code)		
			key_codes[name] = code
	
def get_key(keylist = None, timeout = None):
	
	"""
	Waits until a key has been pressed.
	Returns a timestamp and the pressed key
	"""
	
	start_time = pygame.time.get_ticks()
	time = start_time
	
	while timeout == None or time - start_time < timeout:

		time = pygame.time.get_ticks()
		
		for event in pygame.event.get():		

			if event.type == KEYDOWN:
			
				if event.key == pygame.K_ESCAPE:
					raise openexp.exceptions.response_error("The escape key was pressed.")
					
				if keylist == None or event.key in keylist:				
					return time, event.key
					
	return time, None
	
def key_mods():

	"""
	Returns a list of key moderator that are currently
	pressed. Moderators are:
	- shift
	- ctrl
	- alt
	- meta
	- super
	"""
	
	l = []
	mods = pygame.key.get_mods()
	if mods & KMOD_LSHIFT or mods & KMOD_RSHIFT or mods & KMOD_SHIFT:
		l.append("shift")
	if mods & KMOD_LCTRL or mods & KMOD_RCTRL or mods & KMOD_CTRL:
		l.append("ctrl")
	if mods & KMOD_LALT or mods & KMOD_RALT or mods & KMOD_ALT:
		l.append("alt")
	if mods & KMOD_LMETA or mods & KMOD_RMETA or mods & KMOD_META:
		l.append("meta")
	return l
	
def map_key(key, mods):

	"""
	Returns the character which results from pressing
	key while holding down moderator keys. E.g., 
	"1" + shift = "!"
	"""
	
	global key_map
		
	if chr(key).isalpha():
		if "shift" in mods:
			return chr(key).upper()
		else:
			return chr(key).lower()
			
	if "shift" in mods:
		if chr(key) not in key_map:
			return ""
		return key_map[chr(key)]
		
	return chr(key)
					
def get_mouse(buttonlist = None, timeout = None):

	"""
	Waits until a mousebutton has been pressed.
	Returns a timestamp, the pressed mousebutton
	and the location of the mousecursor.
	"""
	
	start_time = pygame.time.get_ticks()
	time = start_time	
	
	while timeout == None or time - start_time < timeout:

		time = pygame.time.get_ticks()

		for event in pygame.event.get():
			
			if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
				raise openexp.exceptions.response_error("The escape key was pressed.")							
			
			if event.type == MOUSEBUTTONDOWN:
				if buttonlist == None or event.button in buttonlist:
					return time, event.button, event.pos	
					
	return time, None, (-1, -1)
					
def set_mouse_cursor_visible(visible = True):

	"""
	Sets the visibility of the mouse cursor
	"""
	
	pygame.mouse.set_visible(visible)				
				
def flush():

	"""
	Flushes all events so we don't mess up by double keypresses etc. Returns True if
	a key has been rpessed
	"""

	keypressed = False
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			keypressed = True
			if event.key == pygame.K_ESCAPE:			
				raise openexp.exceptions.response_error("The escape key was pressed.")
				
	return keypressed
				
def keys(keylist):
	
	"""
	Translates a list of keys from strings to the correct pygame values
	"""
	
	global key_codes
	
	l = []
	for key in keylist:
	
		key = key.strip()
		
		if key in key_codes:
			l.append(key_codes[key])
		else:
			try:
				l.append(eval("pygame.K_%s" % key))
			except:
				raise openexp.exceptions.response_error("The key '%s' is undefined. See http://www.pygame.org/docs/ref/key.html for valid keys" % key)
		
	return l

def key(k):
	
	"""
	Translates a key from a string to the correct pygame value
	"""
	
	return keys( [k] )[0]

def key_name(k):

	"""
	Returns the readable name for pygame key
	"""
	
	if k == None:
		return "timeout"
	
	return pygame.key.name(k)

init_key_codes()
