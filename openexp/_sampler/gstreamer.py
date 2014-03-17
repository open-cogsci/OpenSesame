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

from libopensesame.exceptions import osexception
from openexp.keyboard import keyboard
import os
import sys
import urlparse, urllib		# To build the URI that gst requires
import threading
import numpy

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
	

class gstreamer:
	"""
	The sampler loads a sound file in .ogg or .wav format from disk and plays
	it back. The sampler offers a number of basic operations, such as pitch,
	panning, and fade in.
	"""
	
	# The settings variable is used by the GUI to provide a list of back-end
	# settings
	settings = None

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

		self.player = gst.element_factory_make("playbin2", "player")	
		self.bus = self.player.get_bus()		
		self.bus.enable_sync_message_emission()

		if src != None:
			if not os.path.exists(src):
				raise osexception( \
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
		self.gst_listener = threading.Thread(target=self._monitor_events, args=())
		
		self._playing = False
		self._end_of_stream_reached = False
		self._stop_after = 0
		self._fade_in = 0
		self._volume = 1.0
		
	def _monitor_events(self):
		
		"""
		Process gstreamer events in the background. (To allow playback of sound
		even when experiment continues
						
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
				self.experiment.sleep(5)
				
			if self._stop_after:
				print self.experiment.time() - self._starttime
				if self.experiment.time() - self._starttime > self._stop_after:					
					self.stop()
				
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
			raise osexception( \
				u"openexp._sampler.legacy.stop_after() requires a positive integer")

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
			raise osexception( \
				u"openexp._sampler.gstreamer.fade_in() requires a positive integer")

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
			raise osexception( \
				u"openexp._sampler.gstreamer.volume() requires a number between 0.0 and 1.0")

		self._volume = vol
		self.player.set_property("volume",vol)

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
				u"openexp._sampler.gstreamer.pitch() requires a positive number")

		if p == 1:
			return

#		buf = pygame.sndarray.array(self.sound)
#		_buf = []
#
#		for i in range(int(float(len(buf)) / p)):
#			_buf.append(buf[int(float(i) * p)])
#
#		self.sound = pygame.sndarray.make_sound(numpy.array(_buf, \
#			dtype=u"int16"))

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

		if type(p) not in (int, float) and p not in (u"left", u"right"):
			raise osexception( \
				u"openexp._sampler.gstreamer.pan() requires a number or 'left', 'right'")

		if p == 0:
			return

#		buf = pygame.sndarray.array(self.sound)
#
#		for i in range(len(buf)):
#
#			l = buf[i][0]
#			r = buf[i][1]
#
#			if p == "left":
#				r = 0
#			elif p == "right":
#				l = 0
#			elif p < 0:
#				r = int(float(r) / abs(p))
#			else:
#				l = int(float(l) / p)
#
#			buf[i][0] = l
#			buf[i][1] = r
#
#		self.sound = pygame.sndarray.make_sound(numpy.array(buf))

	def play(self, block=False):

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

		# Rewind file is it has been completely played before
		if self._end_of_stream_reached:		
			self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, 1.0)
			self._end_of_stream_reached = False

		print self._stop_after

		self._starttime = self.experiment.time()				
		self.gst_listener.start()
		
		self.player.set_state(gst.STATE_PLAYING)
		self._playing = True

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
		
		if self.player.get_state()[1].value_name != "GST_STATE_NULL":
			self._playing = False
			self._end_of_stream_reached = True
			self.player.set_state(gst.STATE_NULL)
			print "STOPPED PLAYBACK!"

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

		self.player.set_state(gst.STATE_PAUSED)
		if self.player.get_state()[1].value_name == "GST_STATE_PLAYING":
			self.player.set_state(gst.STATE_PAUSED)
			self._playing = False

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

		if self.player.get_state()[1].value_name == "GST_STATE_PAUSED":
			self.player.set_state(gst.STATE_PLAYING)
			self._playing = True

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
		>>> 	print('The sampler is still playing!')
		</DOC>"""
		
		return self._playing
	
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
		>>> print('The sampler is finished!')
		</DOC>"""
						
		while not self._end_of_stream_reached:			
			self.keyboard.flush()
			

def init_sound(experiment):

	"""
	Initializes the pygame mixer before the experiment begins.

	Arguments:
	experiment -- An instance of libopensesame.experiment.experiment
	"""
	pass

def close_sound(experiment):

	"""
	Closes the mixer after the experiment is finished.

	Arguments:
	experiment -- An instance of libopensesame.experiment.experiment
	"""

	pass

