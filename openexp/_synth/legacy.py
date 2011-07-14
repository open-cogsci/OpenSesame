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

import openexp._sampler.legacy
import openexp.exceptions
import math
import numpy
import pygame
import random

class legacy(openexp._sampler.legacy.legacy):

	"""
	The synth generates a sound
	"""

	def __init__(self, experiment, osc = "sine", freq = 440, length = 100, attack = 0, decay = 5):
	
		"""<DOC>
		Initialize the synthesizer
		
		Arguments:
		experiment -- an instance of libopensesame.experiment.experiment
		
		Keyword arguments:
		osc -- oscillator, can be "sine", "saw", "square" or "white_noise" (default = "sine")
		freq -- frequency, either an int (value in hertz) or a string ("A1", "eb2", etc.) (default = 440)
		length -- the length of the sound in milliseconds (default = 100)
		attack -- the attack (fade-in) time in milliseconds (default = 0)
		decay -- the decay (fade-out) time in milliseconds (default = 5)
		</DOC>"""
	
		openexp._sampler.legacy.legacy.__init__(self, experiment, None)
		
		# The frequency is not an int, convert it to an int
		try:
			int(freq)
		except:
			freq = self.key_to_freq(freq)
		
		# Set the oscillator function
		if osc == "sine":
			_func = math.sin
		elif osc == "saw":
			_func = self.saw
		elif osc == "square":
			_func = self.square
		elif osc == "white_noise":
			_func = self.white_noise
		else:
			raise openexp.exceptions.synth_error("synth.__init__(): '%s' is not a valid oscillator, exception 'sine', 'saw', 'square', or 'white_noise'" % osc)
	
		l = []

		attack = attack * openexp.sampler.freq / 1000
		decay = decay * openexp.sampler.freq / 1000
		amp = 32767 / 2
		sps = openexp.sampler.freq # samples per second
		cps = float(sps / freq) # cycles per sample
		slen = openexp.sampler.freq * length / 1000 # nr of samples
	
		for i in range(slen):
			p = float((i % cps)) / cps * 2 * math.pi
			v = int(amp * (_func(p)))			
			if i < attack:
				v = int(v * float(i) / attack)				
			if i > slen - decay:
				v = int(v * (float(slen) - float(i)) / decay)			
			l.append(v)
			l.append(v)
			
		b = numpy.array(l, dtype="int16").reshape(len(l) / 2, 2)				 
			
		self.sound = pygame.mixer.Sound(b)
		
	def key_to_freq(self, key):
	
		"""<DOC>
		Convert a key (e.g., A1) to a frequency
		
		Arguments:
		key -- a string like "A1", "eb2", etc.
		
		Returns:
		An int containing the frequency in Hertz
		</DOC>"""
		
		if type(key) != str or len(key) < 2:
			raise openexp.exceptions.synth_error("synth.key_to_freq(): '%s' is not a valid note, expecting something like 'A1'")			
		
		n = key[:-1].lower()
		try:
			o = int(key[-1])
		except:
			raise openexp.exceptions.synth_error("synth.key_to_freq(): '%s' is not a valid note, expecting something like 'A1'")								
			
		if n == "a":
			f = 440.0
		elif n == "a#" or n == "bb":
			f = 466.16
		elif n == "b":
			f = 493.92
		elif n == "c":
			f = 523.28
		elif n == "c#" or n == "db":
			f = 554.40
		elif n == "d":
			f = 587.36
		elif n == "d#" or n == "eb":
			f = 698.47
		elif n == "e":
			f = 659.48
		elif n == "f":
			f = 698.48
		elif n == "f#" or n == "gb":
			f = 740.00
		elif n == "g":
			f = 784.00
		elif n == "ab" or n == "g#":
			f == 830.64
			
		if o < 1:
			o = 0.5 ** (abs(o) + 1)			
			freq = f * o
		else:
			freq = f ** o
			
		return freq
	
	def saw(self, phase):
	
		"""
		* For internal use
		
		Generates a saw wave
		"""
		
		phase = phase % math.pi		
		
		return float(phase) / (0.5 * math.pi) - 1.0

				
	def square(self, phase):
	
		"""
		* For internal use

		Generates a square wave
		"""

		if phase < math.pi:
			return 1
		return -1
		
	def white_noise(self, phase):
	
		"""
		* For internal use

		Generates random noise
		"""
		
		return random.random()

		
