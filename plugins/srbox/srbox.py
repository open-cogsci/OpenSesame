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
import imp
import os
import os.path
from PyQt4 import QtGui, QtCore

class srbox(item.item, generic_response.generic_response):

	"""A plug-in for using the serial response box"""

	def __init__(self, name, experiment, string=None):

		"""
		Constructor
		
		Arguments:
		name -- item name
		experiment -- opensesame experiment
		
		Keywords arguments:
		string -- definition string (default=None)
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

		# The parent handles the rest of the contruction
		item.item.__init__(self, name, experiment, string)
		
	def prepare(self):

		"""
		Prepare the item
		
		Returns:
		True on success, False on failure		
		"""

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
		
			# Prepare the device string
			dev = self.get("dev")
			if dev == "autodetect":
				dev = None
		
			# Dynamically load an srbox instance
			if not hasattr(self.experiment, "srbox"):				
				path = os.path.join(os.path.dirname(__file__), "libsrbox.py")
				_srbox = imp.load_source("libsrbox", path)
				self.experiment.srbox = _srbox.libsrbox(self.experiment, dev)

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
				self._resp_func = self.experiment.srbox.get_button_press

		self.prepare_timeout()

		# Report success
		return True

	def run(self):

		"""
		Run the item
		
		Returns:
		True on success, False on failure				
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
				resp = self._keyboard.to_chr(resp)
				if resp != "timeout":
					resp = int(resp)
			except:
				raise exceptions.runtime_error("An error occured in srbox '%s': Only number keys are accepted in dummy mode" % self.name)

		else:
			# Get the response
			try:
				self.experiment.srbox.send(self._lights)
				self.experiment.srbox.start()
				resp, self.experiment.end_response_interval = \
					self._resp_func(self._allowed_responses, self._timeout)
				self.experiment.srbox.stop()
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
		
	def var_info(self):

		return generic_response.generic_response.var_info(self)			

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


