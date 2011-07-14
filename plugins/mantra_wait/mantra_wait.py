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

from libopensesame import item, exceptions
from libqtopensesame import qtplugin
import os.path
from PyQt4 import QtGui, QtCore

class mantra_wait(item.item):

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
		self.item_type = "mantra_wait"		
		
		self._smov = "Movement start"
		self._emov = "Movement end"
		
		self.event = self._smov
		self.object = 0
		self.timeout = 0
		
		# Provide a short accurate description of the items functionality
		self.description = "Wait for event plugin for the Mantra object tracker"

		# The parent handles the rest of the contruction
		item.item.__init__(self, name, experiment, string)
								
	def prepare(self):
	
		"""
		Prepare the item. In this case this means drawing a fixation
		dot to an offline canvas.
		"""
		
		# Pass the word on to the parent
		item.item.prepare(self)		
		
		# Create an mantra instance if it doesn't exist yet. Libmantra is
		# dynamically loaded
		if not hasattr(self.experiment, "mantra"):
			raise exceptions.runtime_error("Please connect to the mantra using the the mantra_connect plugin before using any other mantra plugins")
		
		if self.event == self._smov:
			self._event_func = self.experiment.mantra.smov
		elif self.event == self._emov:
			self._event_func = self.experiment.mantra.emov
		else:
			raise exceptions.runtime_error("An unknown event was specified in mantra_wait item '%s'" % self.name)
			
		# Prepare the object nr
		try:
			self._object = int(self.object)
		except:
			raise exceptions.runtime_error("An incorrect object was specified in mantra_wait item '%s'. Expecting a numeric value." % self.name)
			
		# Prepare the timeout
		try:
			self._timeout = int(self.timeout)
		except:
			raise exceptions.runtime_error("An incorrect timeout was specified in mantra_wait item '%s'. Expecting a numeric value." % self.name)		
		if self._timeout <= 0:
			self._timeout = None
				
		# Report success
		return True
				
	def run(self):
	
		"""
		Run the item. In this case this means putting the offline canvas
		to the display and waiting for the specified duration.
		"""
		
		self.set_item_onset()		
		
		# If no start response interval has been set, set it to the onset of
		# the current response item
		if self.experiment.start_response_interval == None:
			self.experiment.start_response_interval = self.get("time_%s" % self.name)		
		
		resp = self._event_func(self._object, self._timeout)
		self.experiment.end_response_interval = self.time()		

		# Do some bookkeeping
		self.experiment.response_time = self.experiment.end_response_interval - self.experiment.start_response_interval		
		self.experiment.total_response_time += self.experiment.response_time
		self.experiment.total_responses += 1						
		self.experiment.start_response_interval = None					
		
		if self.event == self._smov:			
			self.experiment.set("smov_x", resp[0])
			self.experiment.set("smov_y", resp[1])
			self.experiment.set("smov_z", resp[2])
			self.experiment.set("emov_x", "na")
			self.experiment.set("emov_y", "na")
			self.experiment.set("emov_z", "na")						
		else:
			self.experiment.set("smov_x", resp[0][0])
			self.experiment.set("smov_y", resp[0][1])
			self.experiment.set("smov_z", resp[0][2])
			self.experiment.set("emov_x", resp[1][0])
			self.experiment.set("emov_y", resp[1][1])
			self.experiment.set("emov_z", resp[1][2])			
				
		# Report success
		return True
		
	def var_info(self):
	
		"""
		Give a list of dictionaries with variable descriptions
		"""
		
		l = item.item.var_info(self)
		l.append( ("response_time", "<i>Depends on response</i>") )		
		l.append( ("smov_x", "<i>Depends on response</i>") )
		l.append( ("smov_y", "<i>Depends on response</i>") )
		l.append( ("smov_z", "<i>Depends on response</i>") )
		l.append( ("emov_x", "<i>Depends on response</i>") )
		l.append( ("emov_y", "<i>Depends on response</i>") )
		l.append( ("emov_z", "<i>Depends on response</i>") )
		
		return l			
					
class qtmantra_wait(mantra_wait, qtplugin.qtplugin):

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
		mantra_wait.__init__(self, name, experiment, string)		
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
		self.add_combobox_control("event", "Event", [self._smov, self._emov], tooltip = "The mantra event to wait for")
		self.add_spinbox_control("object", "Object", 0, 100, prefix = "#", tooltip = "The nr of the object (0 = first)")
		self.add_spinbox_control("timeout", "Timeout", 0, 100000, suffix = "ms", tooltip = "The time to wait before declaring a timeout (0 = no timeout)")
		
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
		
		
