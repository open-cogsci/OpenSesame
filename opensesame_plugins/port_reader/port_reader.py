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
from libopensesame import item, generic_response
from libopensesame.oslogging import oslogger
from libqtopensesame import qtplugin
try:
	from ctypes import windll
except:
	oslogger.warning(
		"failed to load ctypes.windll mode (only dummy mode will be available)"
	)


class port_reader(item.item, generic_response.generic_response):

	"""A plug-in to collect responses from a port (Window only)"""

	description = \
		u"Collects input from a port for the purpose of response collection"

	def reset(self):

		"""item.item."""

		self.var.timeout = "infinite"
		self.var.port = 889
		self.var.resting_value = 127
		self.var.auto_response = 255 # 'a'
		self.var.duration = "portinput"
		self.var.dummy = "no"
		self.process_feedback = True

	def get_portinput(self):

		"""Read port input"""

		while True:
			val = self._port.Inp32(self.port)
			time = self.time()
			if val != self.resting_value:
				break
			if self._timeout is not None and time - self.sri > self._timeout:
				val = "timeout"
				break
		return val, time

	def prepare_duration_portinput(self):

		"""Prepare a portinput duration"""

		if self.experiment.auto_response:
			self._duration_func = self.sleep_for_duration
			self._duration = 500
		else:
			try:
				self._port = windll.inpout32
			except:
				raise osexception( \
					"Failed to load inpout32.dll in port_reader '%s'" \
					% self.name)
			self._duration_func = self.get_portinput

	def process_response_portinput(self, retval):

		"""Process a portinput response"""

		self.experiment._start_response_interval = self.sri
		self.experiment.response, self.experiment.end_response_interval = retval

	def prepare(self):

		"""
		Prepare the item

		Returns:
		True on success, False on failure
		"""

		if self.dummy == "yes":
			self.duration = "keypress"

		item.item.prepare(self)
		generic_response.generic_response.prepare(self)
		return True

	def run(self):

		"""
		Runs the item

		Returns:
		True on success, False on failure
		"""

		# Record the onset of the current item
		self.set_item_onset()
		self.set_sri()
		self.process_response()

		# Report success
		return True

	def var_info(self):

		"""
		Give a list of dictionaries with variable descriptions

		Returns:
		A list of (name, description) tuples
		"""

		return item.item.var_info(self) + \
			generic_response.generic_response.var_info(self)

class qtport_reader(port_reader, qtplugin.qtplugin):

	"""GUI controls for port_reader plug-in"""

	def __init__(self, name, experiment, string=None):

		"""
		Constructor

		Arguments:
		name -- item name
		experiment -- experiment instance

		Keyword arguments:
		string -- definition string (default=None)
		"""

		# Pass the word on to the parents
		port_reader.__init__(self, name, experiment, string)
		qtplugin.qtplugin.__init__(self, __file__)

	def init_edit_widget(self):

		"""Initialize GUI controls"""

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

		self.add_combobox_control("dummy", \
			"Dummy mode (use keyboard instead)", ["yes", "no"], \
			tooltip="Enable dummy mode for testing purposes")
		self.add_spinbox_control("port", "Port number", 0, 1024, tooltip= \
			"Expecting a valid port number")
		self.add_spinbox_control("resting_value", "Resting state value", 0, \
			255, tooltip= \
			"A value that is read from the port when there is no input")
		self.add_line_edit_control("correct_response", "Correct response", \
			tooltip="Expecting response values (0 .. 255)")
		self.add_line_edit_control("timeout", "Timeout", tooltip= \
			"Expecting a value in milliseconds or 'infinite'", default= \
			"infinite")

		# Add a stretch to the edit_vbox, so that the controls do not
		# stretch to the bottom of the window.
		self.edit_vbox.addStretch()

		# Unlock
		self.lock = True

	def apply_edit_changes(self):

		"""Apply GUI controls"""

		# Abort if the parent reports failure of if the controls are locked
		if not qtplugin.qtplugin.apply_edit_changes(self) or self.lock:
			return False

		# Refresh the main window, so that changes become visible everywhere
		self.experiment.main_window.refresh(self.name)

		# Report success
		return True

	def edit_widget(self):

		"""Update GUI controls"""

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
