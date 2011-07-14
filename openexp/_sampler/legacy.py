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

class legacy:

	"""
	The sampler loads a sound file in .ogg or .wav format
	from disk and plays it. The sampler offers a number of 
	basic operations, such as pitch, panning, and fade in.
	"""

	def __init__(self, experiment, src):
	
		"""<DOC>		
		Initialize the sampler with a specified file
		
		Arguments:
		experiment -- An instance of libopensesame.experiment.experiment
		src -- A path to a .wav or .ogg file
		</DOC>"""		
		
		if src != None:
			if not os.path.exists(src):
				raise openexp.exceptions.sample_error("openexp._sampler.legacy.__init__() the file '%s' does not exist" % src)
		
			if os.path.splitext(src)[1].lower() not in (".ogg", ".wav"):
				raise openexp.exceptions.sample_error("openexp._sampler.legacy.__init__() the file '%s' is not an .ogg or .wav file" % src)			
	
			self.sound = pygame.mixer.Sound(src)
			
		self.experiment = experiment
		self._stop_after = 0
		self._fade_in = 0
		self._volume = 1.0				
		
	def stop_after(self, ms):
	
		"""<DOC>
		Specify a duration after which the sampler stops playing
		
		Arguments:
		ms -- A duration in milliseconds
		</DOC>"""
	
		if type(ms) != int or ms < 0:
			raise openexp.exceptions.sample_error("openexp._sampler.legacy.stop_after() requires a positive integer")
		
		self._stop_after = ms

	def fade_in(self, ms):
	
		"""<DOC>
		Set the fade-in time in milliseconds
		
		Arguments:
		ms - A duration in milliseconds
		</DOC>"""	
	
		if type(ms) != int or ms < 0:
			raise openexp.exceptions.sample_error("openexp._sampler.legacy.fade_in() requires a positive integer")
		
		self._fade_in = ms
		
	def volume(self, vol):
	
		"""<DOC>
		Set the volume
		
		Arguments:
		vol -- A volume between 0.0 and 1.0
		</DOC>"""
	
		if type(vol) not in (int, float) or vol < 0 or vol > 1:
			raise openexp.exceptions.sample_error("openexp._sampler.legacy.volume() requires a number between 0.0 and 1.0")
	
		self._volume = vol
		self.sound.set_volume(vol)
		
	def pitch(self, p):
		
		"""<DOC>
		Set the relative pitch of the sample
		
		Arguments:
		p -- The pitch. p > 1.0 slows the sample down, p < 1.0 speeds the sample up
		</DOC>"""
		
		if type(p) not in (int, float) or p <= 0:
			raise openexp.exceptions.sample_error("openexp._sampler.legacy.pitch() requires a positive number")		
			
		if p == 1:
			return
		
		buf = pygame.sndarray.array(self.sound)
		_buf = []
		
		for i in range(int(float(len(buf)) / p)):
			_buf.append(buf[int(float(i) * p)])

		self.sound = pygame.sndarray.make_sound(numpy.array(_buf, dtype="int16"))
		
	def pan(self, p):
	
		"""<DOC>
		Sets the panning of the sample. The volume of the "unpanned" channel
		decreases, the volume of the other channel remains the same. To fully
		mute one channel specify "left" (mutes right, pans to left) or "right"
		(mutes left, pans to right"). 
		
		Arguments:
		p -- Panning. A float (p < 0 = to left, p > 0 = to right) or string ("left" or "right")
		</DOC>"""
		
		if type(p) not in (int, float) and p not in ("left", "right"):
			raise openexp.exceptions.sample_error("openexp._sampler.legacy.pan() requires a number or 'left', 'right'")		
			
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
	
		"""<DOC>
		Play the sound
		
		Keyword arguments:
		block -- If True, block until the sound is finished. (default == False)
		</DOC>"""
	
		self.sound.play(maxtime = self._stop_after, fade_ms = self._fade_in)		
		if block:
			self.wait()
						
	def stop(self):
	
		"""<DOC>
		Stops the currently playing sound (if any)
		</DOC>"""
		
		pygame.mixer.stop()
		
	def pause(self):
	
		"""<DOC>
		Pauses playback (if any)
		</DOC>"""
		
		pygame.mixer.pause()
		
	def resume(self):
	
		"""<DOC>
		Resumes playback (if any)
		</DOC>"""
		
		pygame.mixer.unpause()
		
	def is_playing(self):
	
		"""<DOC>
		Checks if a sound is currently playing
		
		Returns:
		True if a sound is playing, False if not
		</DOC>"""
		
		return pygame.mixer.get_busy()		
		
	def wait(self):
	
		"""<DOC>
		Blocks until the sound has finished playing or
		returns right away if no sound is playing
		</DOC>"""
		
		while pygame.mixer.get_busy():
			pass
	
freq = 48000

	

