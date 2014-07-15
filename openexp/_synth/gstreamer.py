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

import os
import sys
import threading
import time

import openexp._sampler.gstreamer
from openexp.keyboard import keyboard
from libopensesame.exceptions import osexception

# Gstreamer components

# If The Gstreamer SDK is found in the plugin folder, add the relevant paths
# so that we use this framework. This is Windows only.
if os.name == "nt":
	if hasattr(sys,"frozen") and sys.frozen in ("windows_exe", "console_exe"):
		exe_path = os.path.dirname(sys.executable)
		os.environ["PATH"] = os.path.join(exe_path, "gstreamer", "dll") + ';' + os.environ["PATH"]
		os.environ["GST_PLUGIN_PATH"] = os.path.join(exe_path, "gstreamer", "plugins")
		sys.path.append(os.path.join(exe_path, "gstreamer", "python"))		
	else:
		os.environ["PATH"] = os.path.join(os.environ["GSTREAMER_SDK_ROOT_X86"],"bin") + ';' + os.environ["PATH"]
		sys.path.append(os.path.join(os.environ["GSTREAMER_SDK_ROOT_X86"],"lib","python2.7","site-packages"))
if os.name == "posix" and sys.platform == "darwin":
	# For OS X
	# When installed with the GStreamer SDK installers from GStreamer.com
	sys.path.append("/Library/Frameworks/GStreamer.framework/Versions/Current/lib/python2.7/site-packages")
		
# Try to load Gstreamer
try:
	import pygst
	pygst.require("0.10")
	import gst
except:
	raise osexception("OpenSesame could not find the GStreamer framework!")
	
	
	

class gstreamer(openexp._sampler.gstreamer.gstreamer):
	"""The synth generates a sound"""

	settings = None

	def __init__(self, experiment, osc="sine", freq=440, length=100, attack=0, decay=5):

		"""See openexp._synth.legacy"""
		
		# If the frequency is not an int, convert it to an int
		try:
			int(freq)
		except:
			freq = self.key_to_freq(freq)

		# Set the oscillator function
		if osc == "sine":
			wave = 0
		elif osc == "saw":
			wave = 2
		elif osc == "square":
			wave = 1
		elif osc == "white_noise":
			wave = 5
		else:
			raise osexception( \
				"synth.__init__(): '%s' is not a valid oscillator, exception 'sine', 'saw', 'square', or 'white_noise'" \
				% osc)

		self.experiment = experiment
		self.keyboard = keyboard(experiment)
		
		# Handler of Gstreamer messages
		self.gst_listener = threading.Thread(target=self._monitor_events, args=())
		
		pipeline = 'audiotestsrc wave={0} freq={1} ! pitch name=pitcher ! audiopanorama name=panner ! volume name=volume ! audioconvert ! autoaudiosink'.format(wave, freq)
		self.player = gst.parse_launch(pipeline)	
		self.panner = self.player.get_by_name("panner")
		self.pitcher = self.player.get_by_name("pitcher")
		self.vol_control = self.player.get_by_name("volume")
				
		self._playing = False
		self._stop_after = length
		self._fade_in = attack
		self._fade_out = decay
		self._volume = 1.0	
		
	def _monitor_events(self):
		
		"""See openexp._synth.legacy"""
		
		while self.experiment.time() - self._starttime <= self._stop_after:						
			passed_time = self.experiment.time() - self._starttime
			
			# Take care of sound fading in, if applicable
			if self._fade_in > 0 and passed_time < self._fade_in:
				vol = float(passed_time)/self._fade_in * self._volume					
				self.vol_control.set_property("volume",vol)
				
			# Take care of sound fading in, if applicable
			if self._fade_out > 0 and passed_time >= self._stop_after - self._fade_out:
				vol = max(0,(self._stop_after - passed_time)/float(self._fade_out) * self._volume)
				self.vol_control.set_property("volume",vol)
					
			time.sleep(0.001)

		self.player.set_state(gst.STATE_NULL)
		self._playing = False		
					
	def play(self, block=False):

		"""See openexp._synth.legacy"""

		if self._fade_in > 0:
			self.vol_control.set_property("volume", 0)

		self._starttime = self.experiment.time()				
		self.gst_listener.start()		
		self.player.set_state(gst.STATE_PLAYING)
		self._playing = True

		if block:
			self.wait()
			
	def wait(self):

		"""See openexp._synth.legacy"""
						
		while self._playing:			
			self.keyboard.flush()

	def volume(self, vol):

		"""See openexp._synth.legacy"""

		if type(vol) not in (int, float) or vol < 0 or vol > 1:
			raise osexception( \
				u"openexp._sampler.gstreamer.volume() requires a number between 0.0 and 1.0")

		self._volume = vol
		self.vol_control.set_property("volume",vol)	
	

	def key_to_freq(self, key):

		"""See openexp._synth.legacy"""

		if not type(key) in [str,unicode] or len(key) < 2:
			raise osexception( \
				"synth.key_to_freq(): '{0}' is not a valid note, expecting something like 'A1'".format(key))

		n = key[:-1].lower()
		try:
			o = int(key[-1])
		except:
			raise osexception( \
				"synth.key_to_freq(): '%s' is not a valid note, expecting something like 'A1'" % key)

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