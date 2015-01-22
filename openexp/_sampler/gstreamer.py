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

from libopensesame.exceptions import osexception
from openexp.keyboard import keyboard
from openexp._sampler import sampler
import os
import sys
import urlparse, urllib		# To build the URI that gst requires
import threading
import time

# Gstreamer components

# If The Gstreamer SDK is found in the plugin folder, add the relevant paths
# so that we use this framework. This is Windows only.
if os.name == "nt":
	if hasattr(sys,"frozen") and sys.frozen in ("windows_exe", "console_exe"):
		exe_path = os.path.dirname(sys.executable)
		os.environ["PATH"] = os.path.join(exe_path, "gstreamer", "dll") + ';' \
			+ os.environ["PATH"]
		os.environ["GST_PLUGIN_PATH"] = os.path.join(exe_path, "gstreamer",
			"plugins")
		sys.path.append(os.path.join(exe_path, "gstreamer", "python"))
	else:
		os.environ["PATH"] = os.path.join(os.environ["GSTREAMER_SDK_ROOT_X86"],
			"bin") + ';' + os.environ["PATH"]
		sys.path.append(os.path.join(os.environ["GSTREAMER_SDK_ROOT_X86"],
			"lib","python2.7","site-packages"))
if os.name == "posix" and sys.platform == "darwin":
	# For OS X
	# When installed with the GStreamer SDK installers from GStreamer.com
	sys.path.append(
		"/Library/Frameworks/GStreamer.framework/Versions/Current/lib/python2.7/site-packages")

# Try to load Gstreamer
try:
	import pygst
	pygst.require("0.10")
	import gst
except:
	raise osexception("OpenSesame could not find the GStreamer framework!")


class gstreamer(sampler.sampler):

	"""
	desc:
		This is a sampler backend built on top of gstreamer.
		For function specifications and docstrings, see
		`openexp._sampler.sampler`.
	"""

	# The settings variable is used by the GUI to provide a list of back-end
	# settings
	settings = None

	def __init__(self, experiment, src):

		# Create required elements
		self.panner = gst.element_factory_make("audiopanorama","panner")
		self.pitcher = gst.element_factory_make("pitch","pitch_controller")
		convert = gst.element_factory_make("audioconvert", "convert")
		audiosink = gst.element_factory_make("autoaudiosink","playback")

		# Put in bin and link elements together
		output_bin = gst.Bin("postprocessing")
		output_bin.add_many(self.pitcher, self.panner, convert, audiosink)
		gst.element_link_many(self.pitcher, self.panner, convert, audiosink)

		# Create pad (entry point for playbin2 in output_bin)
		pad = self.pitcher.get_static_pad("sink")
		ghost_pad = gst.GhostPad("sink", pad)
		ghost_pad.set_active(True)
		output_bin.add_pad(ghost_pad)

		# Create player and route output to bin
		self.player = gst.element_factory_make("playbin2", "player")
		self.player.set_property("audio-sink", output_bin)

		# Create bus reference to keep track of what's happening in the player
		self.bus = self.player.get_bus()
		self.bus.enable_sync_message_emission()

		if src is not None:
			if not os.path.exists(src):
				raise osexception(
					u"openexp._sampler.gstreamer.__init__() the file '%s' does not exist" \
					% src)
			else:
				# Determine URI to file source
				src = os.path.abspath(src)
				src = urlparse.urljoin('file:', urllib.pathname2url(src))

			self.player.set_property("uri", src)
			self.player.set_state(gst.STATE_PAUSED)

		self.experiment = experiment
		self.keyboard = keyboard(experiment)

		# Handler of Gstreamer messages
		self.gst_listener = threading.Thread(target=self._monitor_events,
			args=())

		self._playing = False
		self._end_of_stream_reached = False
		self._stop_after = 0
		self._fade_in = 0
		self._volume = 1.0

	def _monitor_events(self):

		"""
		desc:
			TODO: Provide description.
		"""

		while not self._end_of_stream_reached:
			event = self.bus.pop()
			if event:
				if event.type == gst.MESSAGE_EOS:
					self.stop()
				# On error print and quit
				if event.type == gst.MESSAGE_ERROR:
					err, debug_info = event.parse_error()
					print u"Gst Error: %s" % err, debug_info
					self.stop()
					raise Exception(u"Gst Error: %s" % err, debug_info)
			else:
				time.sleep(0.001)
			if self._stop_after:
				if self.experiment.time() - self._starttime > self._stop_after:
					self.stop()
			if self._fade_in > 0:
				passed_time = self.experiment.time() - self._starttime
				if  passed_time < self._fade_in:
					vol = float(passed_time)/self._fade_in * self._volume
					self.player.set_property("volume",vol)

	def volume(self, vol):

		if type(vol) not in (int, float) or vol < 0 or vol > 1:
			raise osexception(
				u"openexp._sampler.gstreamer.volume() requires a number between 0.0 and 1.0")
		self._volume = vol
		self.player.set_property("volume", vol)

	def pitch(self, p):

		if type(p) not in (int, float) or p <= 0:
			raise osexception(
				u"openexp._sampler.gstreamer.pitch() requires a positive number")
		if p == 1:
			return
		self.pitcher.set_property("pitch", p)

	def pan(self, p):

		if type(p) not in (int, float) and p not in (u"left", u"right"):
			raise osexception(
				u"openexp._sampler.gstreamer.pan() requires a number or 'left', 'right'")
		if p == 0:
			return
		if p == "left":
			p = -1.0
		elif p == "right":
			p = 1.0
		else:
			p /= 20.0
		self.panner.set_property("panorama", p)

	def play(self, block=False):

		# Rewind file is it has been completely played before
		if self._end_of_stream_reached:
			self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, 1.0)
			self._end_of_stream_reached = False
		if self._fade_in > 0:
			self.player.set_property("volume", 0)
		self._starttime = self.experiment.time()
		self.gst_listener.start()
		self.player.set_state(gst.STATE_PLAYING)
		self._playing = True
		if block:
			self.wait()

	def stop(self):

		if self.player.get_state()[1].value_name != "GST_STATE_NULL":
			self._playing = False
			self._end_of_stream_reached = True
			self.player.set_state(gst.STATE_NULL)

	def pause(self):

		if self.player.get_state()[1].value_name == "GST_STATE_PLAYING":
			self.player.set_state(gst.STATE_PAUSED)
			self._playing = False

	def resume(self):

		if self.player.get_state()[1].value_name == "GST_STATE_PAUSED":
			self.player.set_state(gst.STATE_PLAYING)
			self._playing = True

	def is_playing(self):

		return self._playing

	def wait(self):

		while not self._end_of_stream_reached:
			self.keyboard.flush()

def init_sound(experiment):

	pass

def close_sound(experiment):

	pass
