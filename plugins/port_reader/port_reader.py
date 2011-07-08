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
from PyQt4 import QtGui, QtCore
try:
	from ctypes import windll
except:
	print "port_reader: failed to load ctypes.windll mode (only dummy mode will be available)"
	pass

class port_reader(item.item, generic_response.generic_response):

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
		self.item_type = "port_reader"
		
		# Provide a short accurate description of the items functionality
		self.description = "Collects input from a port for the purpose of response collection"
		
		self.timeout = "infinite"
		self.port = 889
		self.resting_value = 127
		self.auto_response = 255 # 'a'
		self.duration = "portinput"
		self.dummy = "no"
		
		# The parent handles the rest of the contruction
		item.item.__init__(self, name, experiment, string)

	def get_portinput(self):

		"""Read port input"""

		while True:
			val = self._port.Inp32(self.port)
			time = self.time()
			if val != self.resting_value:
				break
			if self._timeout != None and time - self.sri > self._timeout:
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
				raise exceptions.runtime_error("Failed to load inpout32.dll in port_reader '%s'" % self.name)
			self._duration_func = self.get_portinput

	def process_response_portinput(self, retval):

		"""Process a portinput response"""

		self.experiment.start_response_interval = self.sri			
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

		return generic_response.generic_response.var_info(self)
					
class qtport_reader(port_reader, qtplugin.qtplugin):

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
		port_reader.__init__(self, name, experiment, string)		
		qtplugin.qtplugin.__init__(self, __file__)	
		
	def init_edit_widget(self):
	
		"""
		This function creates the controls for the edit
		widget.
		"""
		
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
		
		self.add_combobox_control("dummy", "Dummy mode (use keyboard instead)", ["yes", "no"], tooltip = "Enable dummy mode for testing purposes")
		self.add_spinbox_control("port", "Port number", 0, 1024, tooltip = "Expecting a valid port number", )
		self.add_spinbox_control("resting_value", "Resting state value", 0, 255, tooltip = "A value that is read from the port when there is no input")
		self.add_line_edit_control("correct_response", "Correct response", tooltip = "Expecting response values (0 .. 255)")
		self.add_line_edit_control("timeout", "Timeout", tooltip = "Expecting a value in milliseconds or 'infinite'", default = "infinite")

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
