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
from libopensesame.exceptions import osexception
import os.path
try:
	import numpy
except:
	numpy = None
try:
	import pygame.mixer as mixer
except ImportError:
	import android.mixer as mixer	

class legacy:

	"""
	The sampler loads a sound file in .ogg or .wav format from disk and plays
	it back. The sampler offers a number of basic operations, such as pitch,
	panning, and fade in.
	"""


	# The settings variable is used by the GUI to provide a list of back-end
	# settings
	settings = {
		"sound_buf_size" : {
			"name" : "Sound buffer size",
			"description" : "Size of the sound buffer (increase if playback is choppy)",
			"default" : 1024
			},
		"sound_freq" : {
			"name" : "Sampling frequency",
			"description" : "Determines the sampling rate",
			"default" : 48000
			},
		"sound_sample_size" : {
			"name" : "Sample size",
			"description" : "Determines the bith depth (negative = signed)",
			"default" : -16
			},
		"sound_channels" : {
			"name" : "The number of sound channels",
			"description" : "1 = mono, 2 = stereo",
			"default" : 2
			},
		}

	def __init__(self, experiment, src):

		"""<DOC>
		Initializes the sampler with a specified file.

		Arguments:
		experiment -- An instance of libopensesame.experiment.experiment.
		src -- A path to a .wav or .ogg file.
		
		Example:
		>>> from openexp.sampler import sampler
		>>> src = exp.get_file('my_sound.ogg')
		>>> my_sampler = sampler(exp, src)
		</DOC>"""

		if src != None:
			if not os.path.exists(src):
				raise osexception( \
					"openexp._sampler.legacy.__init__() the file '%s' does not exist" \
					% src)

			if os.path.splitext(src)[1].lower() not in (".ogg", ".wav"):
				raise osexception( \
					"openexp._sampler.legacy.__init__() the file '%s' is not an .ogg or .wav file" \
					% src)

			self.sound = mixer.Sound(src)

		self.experiment = experiment
		self._stop_after = 0
		self._fade_in = 0
		self._volume = 1.0

	def stop_after(self, ms):

		"""<DOC>
		Specifies a duration after which the sampler stops playing.

		Arguments:
		ms -- An integer value specifying the duration in milliseconds.
		
		Example:
		>>> from openexp.sampler import sampler
		>>> src = exp.get_file('my_sound.ogg')
		>>> my_sampler = sampler(exp, src)
		>>> my_sampler.stop_after(100)		
		</DOC>"""

		if type(ms) != int or ms < 0:
			raise osexception("openexp._sampler.legacy.stop_after() requires a positive integer")

		self._stop_after = ms

	def fade_in(self, ms):

		"""<DOC>
		Sets the fade-in time in milliseconds.

		Arguments:
		ms -- An integer value specifying the duration in milliseconds.
		
		Example:
		>>> from openexp.sampler import sampler
		>>> src = exp.get_file('my_sound.ogg')
		>>> my_sampler = sampler(exp, src)
		>>> my_sampler.fade_in(100)		
		</DOC>"""

		if type(ms) != int or ms < 0:
			raise osexception("openexp._sampler.legacy.fade_in() requires a positive integer")

		self._fade_in = ms

	def volume(self, vol):

		"""<DOC>
		Sets the volume.

		Arguments:
		vol -- A volume between 0.0 and 1.0
		
		Example:
		>>> from openexp.sampler import sampler
		>>> src = exp.get_file('my_sound.ogg')
		>>> my_sampler = sampler(exp, src)
		>>> my_sampler.volume(0.5)
		</DOC>"""

		if type(vol) not in (int, float) or vol < 0 or vol > 1:
			raise osexception("openexp._sampler.legacy.volume() requires a number between 0.0 and 1.0")

		self._volume = vol
		self.sound.set_volume(vol)

	def pitch(self, p):

		"""<DOC>
		Sets the relative pitch of the sample.

		Arguments:
		p -- The pitch. p > 1.0 slows the sample down, p < 1.0 speeds #
				the sample up.
		
		Example:
		>>> from openexp.sampler import sampler
		>>> src = exp.get_file('my_sound.ogg')
		>>> my_sampler = sampler(exp, src)
		>>> my_sampler.pitch(2.0)
		</DOC>"""

		# On Android, numpy does not exist and this is not supported
		if numpy == None:			
			return

		if type(p) not in (int, float) or p <= 0:
			raise osexception( \
				"openexp._sampler.legacy.pitch() requires a positive number")

		if p == 1:
			return

		buf = pygame.sndarray.array(self.sound)
		_buf = []

		for i in range(int(float(len(buf)) / p)):
			_buf.append(buf[int(float(i) * p)])

		self.sound = pygame.sndarray.make_sound(numpy.array(_buf, \
			dtype="int16"))

	def pan(self, p):

		"""<DOC>
		Sets the panning of the sample. The volume of the "unpanned" channel #
		decreases, the volume of the other channel remains the same. To fully #
		mute one channel specify "left" (mutes right, pans to left) or "right" #
		(mutes left, pans to right").

		Arguments:
		p -- Panning. A float (p < 0 = to left, p > 0 = to right) or string #
			 ("left" or "right").
		
		Example:
		>>> from openexp.sampler import sampler
		>>> src = exp.get_file('my_sound.ogg')
		>>> my_sampler = sampler(exp, src)
		>>> my_sampler.pan('left')
		</DOC>"""
		
		# On Android, numpy does not exist and this is not supported
		if numpy == None:			
			return
		
		if type(p) not in (int, float) and p not in ("left", "right"):
			raise osexception("openexp._sampler.legacy.pan() requires a number or 'left', 'right'")

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
		Plays the sound.

		Keyword arguments:
		block -- If True, block until the sound is finished (default = False).
		
		Example:
		>>> from openexp.sampler import sampler
		>>> src = exp.get_file('my_sound.ogg')
		>>> my_sampler = sampler(exp, src)
		>>> my_sampler.play()
		</DOC>"""

		self.sound.play(maxtime = self._stop_after, fade_ms = self._fade_in)
		if block:
			self.wait()

	def stop(self):

		"""<DOC>
		Stops the currently playing sound (if any).
		
		Example:
		>>> from openexp.sampler import sampler
		>>> src = exp.get_file('my_sound.ogg')
		>>> my_sampler = sampler(exp, src)
		>>> my_sampler.play()
		>>> self.sleep(100)
		>>> my_sampler.stop()
		</DOC>"""

		mixer.stop()

	def pause(self):

		"""<DOC>
		Pauses playback (if any).
		
		Example:
		>>> from openexp.sampler import sampler
		>>> src = exp.get_file('my_sound.ogg')
		>>> my_sampler = sampler(exp, src)
		>>> my_sampler.play()
		>>> self.sleep(100)
		>>> my_sampler.pause()				
		>>> self.sleep(100)
		>>> my_sampler.resume()				
		</DOC>"""

		mixer.pause()

	def resume(self):

		"""<DOC>
		Resumes playback (if any).
		
		Example:
		>>> from openexp.sampler import sampler
		>>> src = exp.get_file('my_sound.ogg')
		>>> my_sampler = sampler(exp, src)
		>>> my_sampler.play()
		>>> self.sleep(100)
		>>> my_sampler.pause()				
		>>> self.sleep(100)
		>>> my_sampler.resume()				
		</DOC>"""

		mixer.unpause()

	def is_playing(self):

		"""<DOC>
		Checks if a sound is currently playing.

		Returns:
		True if a sound is playing, False if not.

		Example:
		>>> from openexp.sampler import sampler
		>>> src = exp.get_file('my_sound.ogg')
		>>> my_sampler = sampler(exp, src)
		>>> my_sampler.play()
		>>> self.sleep(100)
		>>> if my_sampler.is_playing():
		>>> 	print 'The sampler is still playing!'
		</DOC>"""

		return bool(mixer.get_busy())

	def wait(self):

		"""<DOC>
		Blocks until the sound has finished playing or returns right away if no #
		sound is playing.
		
		Example:
		>>> from openexp.sampler import sampler
		>>> src = exp.get_file('my_sound.ogg')
		>>> my_sampler = sampler(exp, src)
		>>> my_sampler.play()
		>>> my_sampler.wait()
		>>> print 'The sampler is finished!'
		</DOC>"""

		while mixer.get_busy():
			pass

def init_sound(experiment):

	"""
	Initializes the pygame mixer before the experiment begins.

	Arguments:
	experiment -- An instance of libopensesame.experiment.experiment
	"""

	print "openexp.sampler._legacy.init_sound(): sampling freq = %d, buffer size = %d" \
		% (experiment.sound_freq, experiment.sound_buf_size)
	if hasattr(mixer, 'get_init') and mixer.get_init():
		print 'openexp.sampler._legacy.init_sound(): mixer already initialized, closing'
		pygame.mixer.quit()
	mixer.pre_init(experiment.sound_freq, experiment.sound_sample_size, \
		experiment.sound_channels, experiment.sound_buf_size)	
	mixer.init()


def close_sound(experiment):

	"""
	Closes the mixer after the experiment is finished.

	Arguments:
	experiment -- An instance of libopensesame.experiment.experiment
	"""

	mixer.quit()

