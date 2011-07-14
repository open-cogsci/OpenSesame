#!/usr/bin/env python
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

from libopensesame import item, generic_response, exceptions
from libqtopensesame import qtplugin
import openexp.keyboard
import serial
import time
import os
import os.path

from PyQt4 import QtGui, QtCore

version = 0.14

_time_func = None

class srbox(item.item, generic_response.generic_response):

	"""
	This class (the class with the same name as the module)
	handles the basic functionality of the item. It does
	not deal with GUI stuff.
	"""

	def __init__(self, name, experiment, string = None):

		"""
		Constructor
		"""

		# The item_typeshould match the name of the module
		self.item_type = "srbox"

		# Provide a short accurate description of the items functionality
		self.description = "Collects input from a serial response box (Psychology Software Tools) or compatible devices"

		# Set some item-specific variables
		self.timeout = "infinite"
		self.lights = ""
		self.dev = "autodetect"
		self.dummy = "no"

		# The connection to the box
		_srbox = None

		# The parent handles the rest of the contruction
		item.item.__init__(self, name, experiment, string)

	def prepare(self):

		"""
		Prepare the item.
		"""

		global _time_func

		_time_func = self.experiment._time_func

		# Pass the word on to the parent
		item.item.prepare(self)

		# Prepare the allowed responses
		if self.has("allowed_responses"):
			self._allowed_responses = []
			for r in str(self.get("allowed_responses")).split(";"):
				if r.strip() != "":
					try:
						r = int(r)
					except:
						raise exceptions.runtime_error("'%s' is not a valid response in srbox '%s'. Expecting a number in the range 0 .. 5." % (r, self.name))

					if r < 0 or r > 255:
						raise exceptions.runtime_error("'%s' is not a valid response in srbox '%s'. Expecting a number in the range 0 .. 5." % (r, self.name))

					self._allowed_responses.append(r)

			if len(self._allowed_responses) == 0:
				self._allowed_responses = None
		else:
			self._allowed_responses = None

		if self.experiment.debug:
			print "srbox.prepare(): allowed responses set to %s" % self._allowed_responses

		self._keyboard = openexp.keyboard.keyboard(self.experiment)
		if self.has("dummy") and self.get("dummy") == "yes":
			self._resp_func = self._keyboard.get_key

		else:

			global _srbox

			if _srbox == None:
				srbox_init(self.dev, self.experiment.debug)
				if _srbox == None:
					raise exceptions.runtime_error("Failed to open the serial response box in srbox '%s'" % self.name)

			# Prepare the light byte
			s = "010" # Control string
			for i in range(5):
				if str(5 - i) in str(self.get("lights")):
					s += "1"
				else:
					s += "0"
			self._lights = chr(int(s, 2))
			if self.experiment.debug:
				print "srbox.prepare(): lights string set to %s (%s)" % (s, self.get("lights"))

			# Prepare auto response
			if self.experiment.auto_response:
				self._resp_func = self.auto_responder
			else:
				self._resp_func = srbox_get

		self.prepare_timeout()

		# Report success
		return True

	def run(self):

		"""
		Run the item.
		"""

		# Set the onset time
		self.set_item_onset()

		# Flush the keyboard so we can use the escape key
		self._keyboard.flush()

		# If no start response interval has been set, set it to the onset of
		# the current response item
		if self.experiment.start_response_interval == None:
			self.experiment.start_response_interval = self.get("time_%s" % self.name)

		if self.has("dummy") and self.get("dummy") == "yes":

			# In dummy mode, we simply take the numeric keys from the keyboard instead of an sr-box
			resp, self.experiment.end_response_interval = self._resp_func(None, self._timeout)
			try:
				resp = int(self._keyboard.to_chr(resp))
			except:
				raise exceptions.runtime_error("An error occured in srbox '%s': Only number keys are accepted in dummy mode" % self.name)

		else:
			# Get the response
			try:
				srbox_send(self._lights, self.experiment.debug)
				srbox_start(self.experiment.debug)
				self.experiment.end_response_interval, resp = self._resp_func(self._allowed_responses, self._timeout)
				srbox_stop(self.experiment.debug)
			except Exception as e:
				raise exceptions.runtime_error("An error occured in srbox '%s': %s." % (self.name, e))

		if self.experiment.debug:
			print "srbox.run(): received %s" % resp

		if type(resp) == list:
			self.experiment.response = resp[0]
		else:
			self.experiment.response = resp

		generic_response.generic_response.response_bookkeeping(self)
			
		# Report success
		return True

class qtsrbox(srbox, qtplugin.qtplugin):

	"""
	This class (the class named qt[name of module] handles
	the GUI part of the plugin. For more information about
	GUI programming using PyQt4, see:
	<http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/classes.html>
	"""

	def __init__(self, name, experiment, string = None):

		"""
		Constructor
		"""

		# Pass the word on to the parents
		srbox.__init__(self, name, experiment, string)
		qtplugin.qtplugin.__init__(self, __file__)

	def init_edit_widget(self):

		"""
		This function creates the controls for the edit
		widget.
		"""

		global version

		# Lock the widget until we're doing creating it
		self.lock = True

		# Pass the word on to the parent
		qtplugin.qtplugin.init_edit_widget(self, False)

		# Create the controls
		#
		# A number of convenience functions are available which
		# automatically create controls, which are also automatically
		# updated and applied. If you set the varname to None, the
		# controls will be created, but not automatically updated
		# and applied.
		#
		# qtplugin.add_combobox_control(varname, label, list_of_options)
		# - creates a QComboBox
		# qtplugin.add_line_edit_control(varname, label)
		# - creates a QLineEdit
		# qtplugin.add_spinbox_control(varname, label, min, max, suffix = suffix, prefix = prefix)

		self.add_combobox_control("dummy", "Dummy mode (use keyboard instead)", ["no", "yes"])
		self.add_line_edit_control("dev", "Device name", tooltip = "Expecting a valid device name. Leave empty for autodetect.", default = "autodetect")
		self.add_line_edit_control("correct_response", "Correct response", tooltip = "Expecting a button number (1 .. 5)")
		self.add_line_edit_control("allowed_responses", "Allowed responses", tooltip = "Expecting a semicolon-separated list of button numbers, e.g., 1;3;4")
		self.add_line_edit_control("timeout", "Timeout", tooltip = "Expecting a value in milliseconds or 'infinite'", default = "infinite")
		self.add_line_edit_control("lights", "Turn on lights", tooltip = "Expecting a semicolon-separated list of light numbers, e.g., 1;3;4")
		self.add_text("<small><b>SRBox OpenSesame Plugin v%.2f</b></small>" % version)

		# Add a stretch to the edit_vbox, so that the controls do not
		# stretch to the bottom of the window.
		self.edit_vbox.addStretch()

		# Unlock
		self.lock = True

	def apply_edit_changes(self):

		"""
		Set the variables based on the controls
		"""

		# Abort if the parent reports failure of if the controls are locked
		if not qtplugin.qtplugin.apply_edit_changes(self, False) or self.lock:
			return False

		# Refresh the main window, so that changes become visible everywhere
		self.experiment.main_window.refresh(self.name)

		# Report success
		return True

	def edit_widget(self):

		"""
		Set the controls based on the variables
		"""

		# Lock the controls, otherwise a recursive loop might aris
		# in which updating the controls causes the variables to be
		# updated, which causes the controls to be updated, etc...
		self.lock = True

		# Let the parent handle everything
		qtplugin.qtplugin.edit_widget(self)

		# Unlock
		self.lock = False

		# Return the _edit_widget
		return self._edit_widget

"""
Static functions. These functions handle the actual communication
with the SR Box.
"""

_srbox = None

KEY1 = int('11111110', 2)
KEY2 = int('11111101', 2)
KEY3 = int('11111011', 2)
KEY4 = int('11110111', 2)
KEY5 = int('11101111', 2)

# The PST sr box only supports five keys, but some
# of the VU boxes use higher key numbers.
KEY6 = int('11011111', 2)
KEY7 = int('10111111', 2)
KEY8 = int('01111111', 2)

def srbox_init(dev = None, debug = True):

	"""
	Intialize the SR box
	"""

	global _srbox

	# If a device has been specified, use it
	if dev not in (None, "", "autodetect"):
		try:
			_srbox = serial.Serial(dev, timeout = 0, baudrate = 19200)
		except Exception as e:
			_srbox = None
			if debug:
				print "srbox.srbox_init(): %s" % e
			return

	else:

		# Else determine the common name of the
		# serial devices on the current platform
		if os.name == "nt":

			# And find the first accessible device
			for i in range(255):
				try:
					dev = "COM%d" % i
					_srbox = serial.Serial(dev, timeout = 0, baudrate = 19200)
					break
				except Exception as e:
					_srbox = None
					pass

		elif os.name == "posix":

			for path in os.listdir("/dev"):
				if path[:3] == "tty":
					try:
						dev = "/dev/%s" % path
						_srbox = serial.Serial(dev, timeout = 0, baudrate = 19200)
						break
					except Exception as e:
						_srbox = None
						pass
		else:
			return

	if debug:
		print "srbox.srbox_init(): Using device %s" % dev

	# Turn off all lights
	if _srbox != None:
		_srbox.write('\x64')

def srbox_send(ch, debug = True):

	"""
	Sends a single character
	"""

	global _srbox

	_srbox.write(ch)

def srbox_start(debug = True):

	"""
	Make the sr box start sending bytes
	"""

	global _srbox

	# Write the start byte
	_srbox.write('\xA0')
	_srbox.flushOutput()
	_srbox.flushInput()

def srbox_stop(debug = True):

	"""
	Make the sr box stop sending bytes
	"""

	global _srbox

	# Write the stop byte and flush the input
	_srbox.write('\x20')
	_srbox.flushOutput()
	_srbox.flushInput()

def srbox_get(allowed_keys = None, timeout = None, debug = True):

	"""
	Get a buttonclick from the SR box. There are 5 possible buttons.
	Returns a timestamp, buttonlist tuple.
	"""

	global _srbox, KEY1, KEY2, KEY3, KEY4, KEY5, _time_func

	# Flush the input
	#_srbox.flushInput()

	c = _time_func()
	t = c
	while timeout == None or t - c < timeout:

		j = _srbox.read(1)
		t = _time_func()
		if j != "" and j != '\x00':
			k = ord(j)

			if k != 0:
				l = []
				if k | KEY1 == 255 and (allowed_keys == None or 1 in allowed_keys):
					l.append(1)
				if k | KEY2 == 255 and (allowed_keys == None or 2 in allowed_keys):
					l.append(2)
				if k | KEY3 == 255 and (allowed_keys == None or 3 in allowed_keys):
					l.append(3)
				if k | KEY4 == 255 and (allowed_keys == None or 4 in allowed_keys):
					l.append(4)
				if k | KEY5 == 255 and (allowed_keys == None or 5 in allowed_keys):
					l.append(5)
				if k | KEY6 == 255 and (allowed_keys == None or 6 in allowed_keys):
					l.append(6)
				if k | KEY7 == 255 and (allowed_keys == None or 7 in allowed_keys):
					l.append(7)
				if k | KEY8 == 255 and (allowed_keys == None or 8 in allowed_keys):
					l.append(8)
				if len(l) > 0:
					return t, l

	return t, None

if __name__ == "__main__":

	"""
	Call the plugin as main script to do some testing.
	"""

	print "Initializing ... "
	srbox_init()

	if _srbox == None:
		print "Error"
		quit()

	print "Done"
	print "Starting ..."
	srbox_start()
	print "Done"
	print "Getting ..."
	while True:
		time, resp = srbox_get()
		print resp
		if 1 in resp:
			break
		break
	print "Done"
	print "Stopping ..."
	srbox_stop()
	print "Done"

