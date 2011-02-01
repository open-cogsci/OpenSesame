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
import openexp.exceptions
import numpy
import os.path

class sampler:

	"""
	The sampler loads a sound file in .ogg or .wav format
	from disk and plays it. The sampler offers a number of 
	basic operations, such as pitch, panning, and fade in.
	"""

	def __init__(self, src):
	
		"""
		Initialize the sampler with a specified file
		"""		
		
		if src != None:
			if not os.path.exists(src):
				raise openexp.exceptions.sample_error("sampler.__init__() the file '%s' does not exist" % src)
		
			if os.path.splitext(src)[1].lower() not in (".ogg", ".wav"):
				raise openexp.exceptions.sample_error("sampler.__init__() the file '%s' is not a .ogg or .wav file" % src)			
	
			self.sound = pygame.mixer.Sound(src)
		self._stop_after = 0
		self._fade_in = 0
		self._volume = 1.0				
		
	def stop_after(self, ms):
	
		"""
		Set the time in milliseconds after which the
		sampler should stop playing
		"""
	
		if type(ms) != int or ms < 0:
			raise openexp.exceptions.sample_error("sampler.stop_after() requires a positive integer")
		
		self._stop_after = ms

	def fade_in(self, ms):
	
		"""
		Set the fade-in time in milliseconds
		"""	
	
		if type(ms) != int or ms < 0:
			raise openexp.exceptions.sample_error("sampler.fade_in() requires a positive integer")
		
		self._fade_in = ms
		
	def volume(self, vol):
	
		"""
		Set the volume (0.0 to 1.0)
		"""
	
		if type(vol) not in (int, float) or vol < 0 or vol > 1:
			raise openexp.exceptions.sample_error("sampler.volume() requires a number between 0.0 and 1.0")
	
		self._volume = vol
		self.sound.set_volume(vol)
		
	def pitch(self, p):
		
		"""
		Set the relative pitch of the sample. p > 1.0 slows the sample
		down, p < 1.0 speeds the sample up
		"""
		
		if type(p) not in (int, float) or p <= 0:
			raise openexp.exceptions.sample_error("sampler.pitch() requires a positive number")		
			
		if p == 1:
			return
		
		buf = pygame.sndarray.array(self.sound)
		_buf = []
		
		for i in range(int(float(len(buf)) / p)):
			_buf.append(buf[int(float(i) * p)])

		self.sound = pygame.sndarray.make_sound(numpy.array(_buf, dtype="int16"))
		
	def pan(self, p):
	
		"""
		Sets the panning of the sample. p < 0 = to left, p > 0 = to right. The volume of the
		"unpanned" channel decreases, the volume of the other channel remains the same.
		To fully mute one channel specify "left" (mutes right, pans to left) or "right"
		(mutes left, pans to right"). 
		"""
		
		if type(p) not in (int, float) and p not in ("left", "right"):
			raise openexp.exceptions.sample_error("sampler.pan() requires a number or 'left', 'right'")		
			
		if p == 0:
			return
		
		buf = pygame.sndarray.array(self.sound)
		
		for i in range(len(buf)):
		
			l = buf[i][0]
			r = buf[i][1]
		
			if p == "left":
				r = 0
			elif p == "right":
				l = 0
			elif p < 0:
				r = int(float(r) / abs(p))
			else:
				l = int(float(l) / p)
			
			buf[i][0] = l
			buf[i][1] = r
		
		self.sound = pygame.sndarray.make_sound(numpy.array(buf))											
		
	def play(self, block = False):
	
		"""
		Play the sound. If block = True the functions waits until
		the sound is finished playing before it returns
		"""
	
		self.sound.play(maxtime = self._stop_after, fade_ms = self._fade_in)
		
		if block:
			while pygame.mixer.get_busy():
				pass
	
freq = 48000

	

