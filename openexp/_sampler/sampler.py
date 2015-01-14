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

# If available, use the yaml.inherit metaclass to copy the docstrings from
# mouse onto the back-end-specific implementations of this class
# (legacy, etc.)
try:
	from yamldoc import inherit as docinherit
except:
	docinherit = type

from libopensesame.exceptions import osexception

class sampler(object):

	"""
	desc: |
		The `sampler` module provides functionality to play sound samples in
		`.ogg` and `.wav` format (Audacity is an excellent free tool to convert
		samples from other formats).

		__Important note:__

		If you find that your sample plays to slowly (low pitch) or too quickly
		(high pitch), make sure that the sampling rate of your sample matches
		the sampling rate of the sampler back-end as specified under back-end
		settings.

		__Example:__

		~~~ {.python}
		from openexp.sampler import sampler
		my_sampler = sampler(exp, exp.get_file('bark.ogg'))
		my_sampler.play()
		~~~

		__Function list:__

		%--
		toc:
			mindepth: 2
			maxdepth: 2
		--%
	"""

	__metaclass__ = docinherit

	def __init__(self, experiment, src):

		"""
		desc:
			Initializes the sampler with a specified file.

		arguments:
			experiment:
				desc:	The experiment object.
				type:	experiment
			src:
				desc:	The full path to a `.wav` or `.ogg` file.
				type:	[unicode, str]

		example: |
			from openexp.sampler import sampler
			src = exp.get_file('my_sound.ogg')
			my_sampler = sampler(exp, src)
		"""

		raise NotImplementedError()

	def stop_after(self, ms):

		"""
		desc:
			Specifies a duration after which the sampler stops playing.

		arguments:
			ms:
				desc:	An integer value specifying the duration in
						milliseconds.
				type:	int

		example: |
			from openexp.sampler import sampler
			src = exp.get_file('my_sound.ogg')
			my_sampler = sampler(exp, src)
			my_sampler.stop_after(100)
		"""

		if type(ms) != int or ms < 0:
			raise osexception(
				u"openexp._sampler.legacy.stop_after() requires a positive integer")
		self._stop_after = ms

	def fade_in(self, ms):

		"""
		desc:
			Sets a fade-in time in milliseconds.

		arguments:
			ms:
				desc:	An integer value specifying the duration in
						milliseconds.
				type:	int

		example: |
			from openexp.sampler import sampler
			src = exp.get_file('my_sound.ogg')
			my_sampler = sampler(exp, src)
			my_sampler.fade_in(100)
		"""

		if type(ms) != int or ms < 0:
			raise osexception(
				u"openexp._sampler.legacy.fade_in() requires a positive integer")
		self._fade_in = ms

	def volume(self, vol):

		"""
		desc:
			Sets the volume.

		arguments:
			vol:
				desc:	A volume level between 0.0 (silent) and 1.0 (full).
				type:	[int, float]

		example: |
			from openexp.sampler import sampler
			src = exp.get_file('my_sound.ogg')
			my_sampler = sampler(exp, src)
			my_sampler.volume(0.5)
		"""

		raise NotImplementedError()

	def pitch(self, p):

		"""
		desc:
			Sets the relative pitch of the sample.

		arguments:
			p:
				desc:	The pitch. p > 1.0 slows the sample down, p < 1.0 speeds
						the sample up.
				type:	[int, float]

		example: |
			from openexp.sampler import sampler
			src = exp.get_file('my_sound.ogg')
			my_sampler = sampler(exp, src)
			my_sampler.pitch(2.0)
		"""

		raise NotImplementedError()

	def pan(self, p):

		"""
		desc:
			Sets the panning of the sample. The volume of the "unpanned" channel
			decreases, the volume of the other channel remains the same. To
			fully mute one channel specify "left" (mutes right, pans to left) or
			"right" (mutes left, pans to right").

		arguments:
			p:
				desc:	Panning. A float (p < 0 = to left, p > 0 = to right) or
						string ("left" or "right").
				type:	[int, float, str, unicode]

		example: |
			from openexp.sampler import sampler
			src = exp.get_file('my_sound.ogg')
			my_sampler = sampler(exp, src)
			my_sampler.pan('left')
		"""

		raise NotImplementedError()

	def play(self, block=False):

		"""
		desc:
			Plays the sound.

		keywords:
			block:
				desc:	If True, the function blocks until the sound is
						finished. If False, the function returns right away
						and the sound is played in the background.
				type:	bool

		example: |
			from openexp.sampler import sampler
			src = exp.get_file('my_sound.ogg')
			my_sampler = sampler(exp, src)
			my_sampler.play()
		"""

		raise NotImplementedError()

	def stop(self):

		"""
		desc:
			Stops the currently playing sound (if any).

		example: |
			from openexp.sampler import sampler
			src = exp.get_file('my_sound.ogg')
			my_sampler = sampler(exp, src)
			my_sampler.play()
			self.sleep(100)
			my_sampler.stop()
		"""

		raise NotImplementedError()

	def pause(self):

		"""
		desc:
			Pauses playback (if any).

		example: |
			from openexp.sampler import sampler
			src = exp.get_file('my_sound.ogg')
			my_sampler = sampler(exp, src)
			my_sampler.play()
			self.sleep(100)
			my_sampler.pause()
			self.sleep(100)
			my_sampler.resume()
		"""

		raise NotImplementedError()

	def resume(self):

		"""
		desc:
			Resumes playback (if any).

		example: |
			from openexp.sampler import sampler
			src = exp.get_file('my_sound.ogg')
			my_sampler = sampler(exp, src)
			my_sampler.play()
			self.sleep(100)
			my_sampler.pause()
			self.sleep(100)
			my_sampler.resume()
		"""

		raise NotImplementedError()

	def is_playing(self):

		"""
		desc:
			Checks if a sound is currently playing.

		returns:
			desc:	True if a sound is playing, False if not.
			type:	bool

		Example: |
			from openexp.sampler import sampler
			src = exp.get_file('my_sound.ogg')
			my_sampler = sampler(exp, src)
			my_sampler.play()
			self.sleep(100)
			if my_sampler.is_playing():
				print('The sampler is still playing!')
		"""

		raise NotImplementedError()

	def wait(self):

		"""
		desc:
			Blocks until the sound has finished playing or returns right away if
			no sound is playing.

		example: |
			from openexp.sampler import sampler
			src = exp.get_file('my_sound.ogg')
			my_sampler = sampler(exp, src)
			my_sampler.play()
			my_sampler.wait()
			print('The sampler is finished!')
		"""

		raise NotImplementedError()

def init_sound(experiment):

	"""
	desc:
		Initializes the pygame mixer before the experiment begins.

	arguments:
		experiment:
			desc:	The experiment object.
			type:	experiment
	"""

	raise NotImplementedError()

def close_sound(experiment):

	"""
	desc:
		Closes the mixer after the experiment is finished.

	arguments:
		experiment:
			desc:	The experiment object.
			type:	experiment
	"""

	raise NotImplementedError()
