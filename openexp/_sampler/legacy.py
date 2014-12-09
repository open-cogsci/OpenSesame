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
from openexp._sampler import sampler
from libopensesame.exceptions import osexception
from libopensesame import misc
from openexp.keyboard import keyboard
import os.path
try:
	import numpy
except:
	numpy = None
try:
	import pygame.mixer as mixer
except ImportError:
	import android.mixer as mixer

class legacy(sampler.sampler):

	"""
	desc:
		This is a sampler backend built on top of PyGame.
		For function specifications and docstrings, see
		`openexp._sampler.sampler`.
	"""

	# The settings variable is used by the GUI to provide a list of back-end
	# settings
	settings = {
		u"sound_buf_size" : {
			u"name" : u"Sound buffer size",
			u"description" : u"Size of the sound buffer (increase if playback is choppy)",
			u"default" : 1024
			},
		u"sound_freq" : {
			u"name" : u"Sampling frequency",
			u"description" : u"Determines the sampling rate",
			u"default" : 48000
			},
		u"sound_sample_size" : {
			u"name" : u"Sample size",
			u"description" : u"Determines the bith depth (negative = signed)",
			u"default" : -16
			},
		"sound_channels" : {
			u"name" : u"The number of sound channels",
			u"description" : u"1 = mono, 2 = stereo",
			u"default" : 2
			},
		}

	def __init__(self, experiment, src):

		if src != None:
			if isinstance(src, basestring):
				if not os.path.exists(src):
					raise osexception( \
						u"openexp._sampler.legacy.__init__() the file '%s' does not exist" \
						% src)
				if os.path.splitext(src)[1].lower() not in (".ogg", ".wav"):
					raise osexception( \
						u"openexp._sampler.legacy.__init__() the file '%s' is not an .ogg or .wav file" \
						% src)
				# The mixer chokes on unicode pathnames that contain special
				# characters. To avoid this we convert to str with the filesystem
				# encoding.
				if isinstance(src, unicode):
					import sys
					src = src.encode(misc.filesystem_encoding())
			self.sound = mixer.Sound(src)
		self.experiment = experiment
		self.keyboard = keyboard(experiment)
		self._stop_after = 0
		self._fade_in = 0
		self._volume = 1.0

	def volume(self, vol):

		if type(vol) not in (int, float) or vol < 0 or vol > 1:
			raise osexception(
				u"openexp._sampler.legacy.volume() requires a number between 0.0 and 1.0")
		self._volume = vol
		self.sound.set_volume(vol)

	def pitch(self, p):

		# On Android, numpy does not exist and this is not supported
		if numpy == None:
			return
		if type(p) not in (int, float) or p <= 0:
			raise osexception(
				u"openexp._sampler.legacy.pitch() requires a positive number")
		if p == 1:
			return
		buf = pygame.sndarray.array(self.sound)
		_buf = []
		for i in range(int(float(len(buf)) / p)):
			_buf.append(buf[int(float(i) * p)])
		self.sound = pygame.sndarray.make_sound(
			numpy.array(_buf, dtype=u"int16"))

	def pan(self, p):

		# On Android, numpy does not exist and this is not supported
		if numpy == None:
			return
		if type(p) not in (int, float) and p not in (u"left", u"right"):
			raise osexception(
				u"openexp._sampler.legacy.pan() requires a number or 'left', 'right'")
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

	def play(self, block=False):

		self.sound.play(maxtime=self._stop_after, fade_ms=self._fade_in)
		if block:
			self.wait()

	def stop(self):

		mixer.stop()

	def pause(self):

		mixer.pause()

	def resume(self):

		mixer.unpause()

	def is_playing(self):

		return bool(mixer.get_busy())

	def wait(self):

		while mixer.get_busy():
			self.keyboard.flush()

def init_sound(experiment):

	print(
		u"openexp.sampler._legacy.init_sound(): sampling freq = %d, buffer size = %d" \
		% (experiment.sound_freq, experiment.sound_buf_size))
	if hasattr(mixer, u'get_init') and mixer.get_init():
		print(
			u'openexp.sampler._legacy.init_sound(): mixer already initialized, closing')
		pygame.mixer.quit()
	mixer.pre_init(experiment.sound_freq, experiment.sound_sample_size, \
		experiment.sound_channels, experiment.sound_buf_size)
	mixer.init()

def close_sound(experiment):

	mixer.quit()

