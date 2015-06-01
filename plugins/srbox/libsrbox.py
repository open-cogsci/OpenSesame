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

from libopensesame.exceptions import osexception
from libopensesame import debug
import serial
import os

class libsrbox:

	"""
	desc: |
		If you insert the srbox plugin at the start of your experiment, an
		instance of `libsrbox` automatically becomes part of the experiment
		object and can be accessed from within an inline_script item as
		`exp.srbox`.

		__Important note 1:__

		If you do not specify a device, the plug-in will try to autodetect the
		SR Box port. However, on some systems this freezes the experiment, so
		it is better to explicitly specify a device.

		__Important note 2:__

		You need to call [libsrbox.start] to put the SR Box in sending mode,
		before calling [libsrbox.get_button_press] to collect a button press.

		__Function list:__

		%--
		toc:
			mindepth: 2
			maxdepth: 2
		--%

		__Example:__

		~~~ {.python}
		t0 = self.time()
		exp.srbox.start()
		buttonlist, t1 = exp.srbox.get_button_press(allowed_buttons=[1,2])
		if 1 in buttonlist:
			response_time = t1 - t0
			print('Button 1 was pressed in %d ms!' % response_time)
		exp.srbox.stop()
		~~~
	"""

	# The PST sr box only supports five buttons, but some of the VU boxes use
	# higher button numbers
	BUTTON1 = int('11111110', 2)
	BUTTON2 = int('11111101', 2)
	BUTTON3 = int('11111011', 2)
	BUTTON4 = int('11110111', 2)
	BUTTON5 = int('11101111', 2)
	BUTTON6 = int('11011111', 2)
	BUTTON7 = int('10111111', 2)
	BUTTON8 = int('01111111', 2)

	def __init__(self, experiment, dev=None):

		"""
		desc:
			Constructor. An `srbox` object is created automatically by the
			`srbox` plug-in, and you do not generally need to call the
			constructor yourself.

		arguments:
			experiment:
				desc:	An Opensesame experiment.
				type:	experiment

		keywowrds:
			dev:
				desc:	The srbox device port or `None` for auto-detect.
				type:	[str, unicode, NoneType]
		"""

		self.experiment = experiment
		self._srbox = None

		# If a device has been specified, use it
		if dev not in (None, "", "autodetect"):
			try:
				self._srbox = serial.Serial(dev, timeout=0, baudrate=19200)
			except Exception as e:
				raise osexception( \
					"Failed to open device port '%s' in libsrbox: '%s'" \
					% (dev, e))

		else:
			# Else determine the common name of the serial devices on the
			# platform and find the first accessible device. On Windows,
			# devices are labeled COM[X], on Linux there are labeled /dev/tty[X]
			if os.name == "nt":
				for i in range(255):
					try:
						dev = "COM%d" % (i+1) #as COM ports start from 1 on Windows
						self._srbox = serial.Serial(dev, timeout=0, \
							baudrate=19200)
						break
					except Exception as e:
						self._srbox = None
						pass

			elif os.name == "posix":
				for path in os.listdir("/dev"):
					if path[:3] == "tty":
						try:
							dev = "/dev/%s" % path
							self._srbox = serial.Serial(dev, timeout=0, \
								baudrate=19200)
							break
						except Exception as e:
							self._srbox = None
							pass
			else:
				raise osexception( \
					"libsrbox does not know how to auto-detect the SR Box on your platform. Please specify a device.")

		if self._srbox == None:
			raise osexception( \
				"libsrbox failed to auto-detect an SR Box. Please specify a device.")
		debug.msg("using device %s" % dev)
		# Turn off all lights
		if self._srbox != None:
			self._srbox.write('\x00')

	def send(self, ch):

		"""
		desc:
			Sends a single character to the SR Box.

		arguments:
			ch:
				desc:	The character to send.
				type:	str
		"""

		self._srbox.write(ch)

	def start(self):

		"""
		desc:
			Turns on sending mode, so that the SR Box starts to send output.
			The SR Box must be in sending mode when you call
			[libsrbox.get_button_press].
		"""

		# Write the start byte
		self._srbox.flushOutput()
		self._srbox.flushInput()
		self._srbox.write('\xA0')

	def stop(self):

		"""
		desc:
			Turns off sending mode, so that the SR Box stops giving output.
		"""

		# Write the stop byte and flush the input
		self._srbox.flushOutput()
		self._srbox.flushInput()
		self._srbox.write('\x20')

	def get_button_press(self, allowed_buttons=None, timeout=None):

		"""
		desc:
			Collect a button press from the SR box. This function will return
			right away if a button is already pressed.

		keywords:
			allowed_buttons:
				desc:	A list of buttons that are accepted or `None` to accept
						all buttons. Valid buttons are integers 1 through 8.
				type:	[list, NoneType]
			timeout:
				desc:	A timeout value in milliseconds or `None` for no
						timeout.
				type:	[int, float, NoneType]

		returns:
			desc:	A timestamp, buttonlist tuple. The buttonlist consists of a
					list of button numbers.
			type:	tuple
		"""

		c = self.experiment.time()
		t = c
		while timeout == None or t - c < timeout:

			j = self._srbox.read(1)
			t = self.experiment.time()
			if j != "" and j != '\x00':
				k = ord(j)

				if k != 0:
					l = []
					if k | self.BUTTON1 == 255 and (allowed_buttons == None or \
						1 in allowed_buttons):
						l.append(1)
					if k | self.BUTTON2 == 255 and (allowed_buttons == None or \
						2 in allowed_buttons):
						l.append(2)
					if k | self.BUTTON3 == 255 and (allowed_buttons == None or \
						3 in allowed_buttons):
						l.append(3)
					if k | self.BUTTON4 == 255 and (allowed_buttons == None or \
						4 in allowed_buttons):
						l.append(4)
					if k | self.BUTTON5 == 255 and (allowed_buttons == None or \
						5 in allowed_buttons):
						l.append(5)
					if k | self.BUTTON6 == 255 and (allowed_buttons == None or \
						6 in allowed_buttons):
						l.append(6)
					if k | self.BUTTON7 == 255 and (allowed_buttons == None or \
						7 in allowed_buttons):
						l.append(7)
					if k | self.BUTTON8 == 255 and (allowed_buttons == None or \
						8 in allowed_buttons):
						l.append(8)
					if l != []:
						return l, t
		return None, t

	def close(self):

		"""
		desc:
			Closes the connection to the srbox.
		"""

		self._srbox.close()
