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

# If available, use the yaml.inherit metaclass to inherit docstrings
try:
	from yamldoc import inherit as docinherit
except:
	docinherit = type

from openexp.sampler import sampler
from libopensesame.exceptions import osexception

class synth(object):

	"""
	desc: |
		The `synth` class provides basic sound synthesis functionality.

		__Example:__

		~~~ {.python}
		# Generate and play a simple tone
		from openexp.synth import synth
		my_synth = synth(exp, osc='saw', freq='b2', attack=250, length=500)
		my_synth.play()
		~~~

		__Function list:__

		%--
		toc:
			mindepth: 2
			maxdepth: 2
		--%
	"""

	__metaclass__ = docinherit

	def __init__(self, experiment, osc="sine", freq=440, length=100, attack=0,
		decay=5):

		"""
		desc:
			Initializes the synthesizer.

		arguments:
			experiment:
				desc:		The experiment object.
				type:		experiment

		keywords:
			osc:
				desc:	Oscillator, can be "sine", "saw", "square" or
						"white_noise".
				type:	[str, unicode]
			freq:
				desc:	Frequency, either an integer value (value in hertz) or a
						string ("A1", "eb2", etc.).
				type:	[str, unicode, int, float]
			length:
				desc:	The length of the sound in milliseconds.
				type:	[int, float]
			attack:
				desc:	The attack (fade-in) time in milliseconds.
				type:	[int, float]
			decay:
				desc:	The decay (fade-out) time in milliseconds.
				type:	[int, float]

		example: |
			from openexp.synth import synth
			my_synth = synth(exp, freq='b2', length=500)
		"""

		import numpy as np
		from scipy import signal
		global np
		global signal

		self.experiment = experiment
		# We need to multiply the rate by two to get a stereo signal
		rate = 2*self.experiment.get_check(u'sampler_frequency', 48100)
		if not hasattr(self, u'osc_%s' % osc):
			raise osexception(u'Invalid oscillator for synth: %s' % osc)
		osc_fnc = getattr(self, u'osc_%s' % osc)
		signal = osc_fnc(self.key_to_freq(freq), length, rate)
		envelope = self.envelope(length, attack, decay, rate)
		sound = self.to_int_16(signal * envelope)
		self.sampler = sampler(experiment, sound)

	def key_to_freq(self, key):

		"""
		desc:
			Converts a key (e.g., A1) to a frequency.

		arguments:
			key:
				desc:	A string like "A1", "eb2", etc, or a numeric frequency
						(in which case the frequency is simply returned as a
						float).
				type:	[str, unicode, int, float]

		returns:
			desc:		A frequency in hertz.
			type:		float

		example: |
			from openexp.synth import synth
			my_synth = synth(exp)
			print('An a2 is %d Hz' % my_synth.key_to_freq('a2'))
		"""

		if type(key) in [int, float]:
			return key
		if not isinstance(key, basestring) or len(key) < 2:
			raise osexception(
				"synth.key_to_freq(): '%s' is not a valid note, expecting something like 'A1'")
		n = key[:-1].lower()
		try:
			o = int(key[-1])
		except:
			raise osexception(
				"synth.key_to_freq(): '%s' is not a valid note, expecting something like 'A1'")
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
			freq = f * o
		return freq

	def osc_square(self, freq, length, rate):

		"""
		desc:
			A square-wave oscillator.

		visible:
			False
		"""

		length *= .001
		t = np.linspace(0, length, length*rate)
		a = signal.square(2*np.pi*freq*t)
		return a

	def osc_saw(self, freq, length, rate):

		"""
		desc:
			A saw-wave oscillator.

		visible:
			False
		"""

		length *= .001
		t = np.linspace(0, length, length*rate)
		a = signal.sawtooth(2*np.pi*freq*t)
		return a

	def osc_sine(self, freq, length, rate):

		"""
		desc:
			A sine-wave oscillator.

		visible:
			False
		"""

		length *= .001
		t = np.linspace(0, length, length*rate)
		a = np.sin(2*np.pi*freq*t)
		return a

	def osc_white_noise(self, freq, length, rate):

		"""
		desc:
			A white-noise oscillator.

		visible:
			False
		"""

		length *= .001
		a = np.random.random(length*rate)*2 - 1
		return a

	def envelope(self, length, attack, decay, rate):

		"""
		desc:
			An envelope generator that determines the volume profile of the
			sound.

		visible:
			False
		"""

		length *= .001
		attack *= .001
		decay *= .001
		e = np.ones(length*rate)
		attack = int(attack*rate)
		e[:attack] = np.linspace(0, 1, attack)
		decay = int(decay*rate)
		e[-decay:] = np.linspace(1, 0, decay)
		return e

	def to_int_16(self, a):

		"""
		desc:
			Converts the float array to an 16 bit int array, which is a more
			typical sound format.

		visible:
			False
		"""

		a *= 32767
		return a.astype(np.int16)

	@property
	def is_playing(self):

		"""
		name: 	is_playing
		desc:	See `sampler.is_playing`.
		"""

		return self.sampler.is_playing

	@property
	def pan(self):

		"""
		name: 	pan
		desc:	See `sampler.pan`.
		"""

		return self.sampler.pan

	@property
	def pause(self):

		"""
		name: 	pause
		desc:	See `sampler.pause`.
		"""

		return self.sampler.pause

	@property
	def pitch(self):

		"""
		name: 	pitch
		desc:	See `sampler.pitch`.
		"""

		return self.sampler.pitch

	@property
	def play(self):

		"""
		name: 	play
		desc:	See `sampler.play`.
		"""

		return self.sampler.play

	@property
	def resume(self):

		"""
		name: 	resume
		desc:	See `sampler.resume`.
		"""

		return self.sampler.resume

	@property
	def stop_after(self):

		"""
		name: 	stop_after
		desc:	See `sampler.stop_after`.
		"""

		return self.sampler.stop_after

	@property
	def volume(self):

		"""
		name: 	volume
		desc:	See `sampler.volume`.
		"""

		return self.sampler.volume

	@property
	def wait(self):

		"""
		name: 	wait
		desc:	See `sampler.wait`.
		"""

		return self.sampler.wait
