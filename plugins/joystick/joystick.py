"""
30-05-2012
Author: Edwin Dalmaijer

This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame. If not, see <http://www.gnu.org/licenses/>.
"""

from libopensesame import item, generic_response, exceptions, debug
from libqtopensesame import qtplugin
import openexp.keyboard
import imp
import os
import os.path
from PyQt4 import QtGui, QtCore

class joystick(item.item, generic_response.generic_response):
	
	"""A plug-in for using a joystick/gamepad"""
	
	def __init__(self, name, experiment, string=None):
		
		"""
		Constructor
		
		Arguments:
		name		item name
		experiment	OpenSesame experiment
		
		Keyword arguments:
		string		definition string (default=None)
		"""
		
		# The item_type should match the name of the module
		self.item_type = "joystick"
		
		# Short and accurate discription of items function
		self.description = "Collects input from a joystick or gamepad"
		
		# Some item-specific variables
		self.timeout = "infinite"
		self.allowed_responses = "1;2"
		self.dummy = "no"
		
		# The parent handles the rest of the construction
		item.item.__init__(self, name, experiment, string)
		
	def prepare(self):
		
		"""
		Prepare the item
		
		Returns:
		True on succes, False on failure
		"""
		
		# Pass the word on to the parent
		item.item.prepare(self)
		
		# Prepare the allowed responses
		if self.has("allowed_responses"):
			self._allowed_responses = []
			for r in self.unistr(self.get("allowed_responses")).split(";"):
				if r.strip() != "":
					try:
						r = int(r)
					except:
						raise exceptions.runtime_error( \
							"'%s' is not a valid response on your joystick/gamepad. Expecting a number in the range of 1 to the amount of buttons." \
							% (r,self.name))
					if r < 0 or r > 255:
						raise exceptions.runtime_error( \
							"'%s' is not a valid response on your joystick/gamepad. Expecting a number in the range of 1 to the amount of buttons." \
							% (r, self.name))
					self._allowed_responses.append(r)
			if len(self._allowed_responses) == 0:
				self._allowed_responses = None
		else:
			self._allowed_responses = None
			
		debug.msg("allowed responses has been set to %s" % self._allowed_responses)
		
		# In case of dummy-mode:
		self._keyboard = openexp.keyboard.keyboard(self.experiment)
		if self.has("dummy") and self.get("dummy") == "yes":
			self._resp_func = self._keyboard.get_key
			
		# Not in dummy-mode:
		else:
			
			# Prepare joybuttonlist and timeout
			joybuttonlist = self.get("_allowed_responses")
			timeout = self.get("timeout")
			
			# Dynamically load a joystick instance
			if not hasattr(self.experiment, "joystick"):
				path = os.path.join(os.path.dirname(__file__), "libjoystick.py")
				_joystick = imp.load_source("libjoystick", path)
				self.experiment.joystick = _joystick.libjoystick(self.experiment, [joybuttonlist, timeout])
				#self.experiment.cleanup_functions.append(self.close)
				
			# Prepare auto response
			if self.experiment.auto_response:
				self._resp_func = self.auto_responder
			else:
				self._resp_func = self.experiment.joystick.get_joybutton
				
		self.prepare_timeout()
		
		# Report succes
		return True
	
	def run(self):
		
		"""
		Run the item
		
		Returns:
		True on succes, False on failure
		"""
		
		# Set the onset time
		self.set_item_onset()
		
		# Flush keyboard, so the escape key can be used
		self._keyboard.flush()
		
		# If no start response interval has been set, set it to the onset of
		# the current response item
		if self.experiment.start_response_interval == None:
			self.experiment.start_response_interval = self.get("time_%s" \
																% self.name)
		if self.has("dummy") and self.get("dummy") == "yes":
			
			# In dummy mode, no one can hear you scream! Oh, and we simply
			# take input from the keyboard
			resp, self.experiment.end_response_interval = self._resp_func( \
				None, self._timeout)
			try:
				resp = self._keyboard.to_chr(resp)
				if resp != "timeout":
					resp = int(resp)
			except:
				raise exceptions.runtime_error( \
					"An error occured in joystick '%s': Only number keys are accepted in dummy mode" \
					% self.name)
			
		else:
			# Get the response
			try:
				resp, self.experiment.end_response_interval = \
						self._resp_func(self._allowed_responses, self._timeout)
			except Exception as e:
				raise exceptions.runtime_error( \
					"An error occured in joystick '%s': '%s." % (self.name, e))
			
		debug.msg("received %s" % resp)
		self.experiment.response = resp
		generic_response.generic_response.response_bookkeeping(self)
		
		# Report succes
		return True
	
	def var_info(self):
		
		return generic_response.generic_response.var_info(self)
	
class qtjoystick(joystick, qtplugin.qtplugin):
	
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
		
		# Pass the word on to the parent
		joystick.__init__(self, name, experiment, string)
		qtplugin.qtplugin.__init__(self, __file__)
		
	def init_edit_widget(self):
		
		"""
		This function creates the controls for the edit
		widget.
		"""
		
		global version
		
		# Lock the widget until it's done being created
		self.lock = True
		
		# Pass the word on to the parent
		qtplugin.qtplugin.init_edit_widget(self, False)
		
		# Create the controls
		#
		# A number of convenience functions is available that
		# automatically create controls, that are automatically
		# updated and applied as well. If you set the varname
		# to None, the controls will be created, but not
		# automatically updated and applied
		#
		# qtplugin.add_combobox_control(varname, label, list_of_options)
		# - creates a QComboBox
		# qtplugin.add_line_edit_control(varname, label)
		# - creates a QLineEdit
		# qtplugin.add_spinbox_control(varname, label, min, max, suffix = suffix, prefix = prefix)
		# - creates a QSpinbox
		
		self.add_combobox_control("dummy", \
									"Dummy mode (use keyboard instead of joystick)", ["no", "yes"])
		self.add_line_edit_control("correct_response", "Correct response", \
									tooltip="Expecting a number between 1 and the number of joybuttons")
		self.add_line_edit_control("allowed_responses", "Allowed responses", \
									tooltip="Expecting a semicolon-separated list of joybutton numbers, e.g. 1;2;4")
		self.add_line_edit_control("timeout", "Timeout", \
									tooltip="Expecting a value in milliseconds of 'infinite'", default="infinite")
		# Add a stretch to the edit_vbox, so that the controls do not
		# stretch to the bottom of the window
		self.edit_vbox.addStretch()

		# Unlock
		self.lock = False
		
	def apply_edit_changes(self):
		
		""""
		Set the variables based on the controls
		"""
		
		# Abort if parent reports failure or if the item controls are locked
		if not qtplugin.qtplugin.apply_edit_changes(self,False) or self.lock:
			return False
		
		# Refresh the main window, so that changes become visible everywhere
		self.experiment.main_window.refresh(self.name)
		
		# Report succes
		return True
	
	def edit_widget(self):
		"""
		Set the controls based on the variables
		"""
		# Lock the controls, otherwise a recursive loop might arise
		# in which updating the controls causes the variables to be
		# updated, which causes the controls to be updated etc.
		self.lock = True
		# Let the parent handle everything
		qtplugin.qtplugin.edit_widget(self)
		# Unlock
		self.lock = False
		# Return the edit_widget
		return self._edit_widget