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
import imp
from PyQt4 import QtGui, QtCore

class eyelink_calibrate(item.item):

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
		self.item_type = "eyelink_calibrate"
		
		self._text_attached = "Yes"
		self._text_not_attached = "No (dummy mode)"
		self.tracker_attached = self._text_attached
		self.sacc_vel_thresh = 35
		self.sacc_acc_thresh = 9500
		
		# This options makes OpenSesame restart automatically after each session,
		# but this is not neessary anymore
		self.restart = "No"
		
		# Provide a short accurate description of the items functionality
		self.description = "Calibration/ initialization plugin for the Eyelink series of eye trackers (SR-Research)"

		# The parent handles the rest of the contruction
		item.item.__init__(self, name, experiment, string)
						
	def prepare(self):
	
		"""
		Prepare the item. In this case this means drawing a fixation
		dot to an offline canvas.
		"""
		
		# Pass the word on to the parent
		item.item.prepare(self)		
		
		# Create an eyelink instance if it doesn't exist yet. Libeyelink is
		# dynamically loaded
		path = os.path.join(os.path.dirname(__file__), "libeyelink.py")						
		libeyelink = imp.load_source("libeyelink", path)			
										
		if self.get("tracker_attached") == self._text_attached:
					
			# The edf logfile has the same name as the opensesame log, but with a different extension
			# We also filter out characters that are not supported
			data_file = ""
			for c in os.path.splitext(os.path.basename(self.get("logfile")))[0]:
				if c.isalnum():
					data_file += c
			data_file += ".edf"
			
			print "eyelink_calibrate(): logging tracker data as %s" % data_file
			
		
			if self.experiment.debug:
				print "eyelink_calibrate(): loading libeyelink"
								
			self.experiment.eyelink = libeyelink.libeyelink( (self.get("width"), self.get("height")), data_file = data_file, saccade_velocity_threshold = self.get("sacc_vel_thresh"), saccade_acceleration_threshold = self.get("sacc_acc_thresh"))
			self.experiment.cleanup_functions.append(self.close)
			
			if self.get("restart") == "Yes":
				self.experiment.restart = True
		else:
		
			if self.experiment.debug:
				print "eyelink_calibrate.prepare(): loading libeyelink (dummy mode)"
		
			self.experiment.eyelink = libeyelink.libeyelink_dummy()
		
		# Report success
		return True
		
	def close(self):
	
		"""
		Perform some cleanup functions to make sure that we don't leave
		OpenSesame and the eyelink in a mess
		"""

		if self.experiment.debug:
			print "eyelink_calibrate.close(): starting eyelink deinitialisation"		
		self.sleep(100)
		self.experiment.eyelink.close()
		self.experiment.eyelink = None
		if self.experiment.debug:
			print "eyelink_calibrate.close(): finished eyelink deinitialisation"		
		self.sleep(100)
				
	def run(self):
	
		"""
		Run the item. In this case this means putting the offline canvas
		to the display and waiting for the specified duration.
		"""
		
		self.set_item_onset()
		
		self.experiment.eyelink.calibrate()
		
		# Report success
		return True
					
class qteyelink_calibrate(eyelink_calibrate, qtplugin.qtplugin):

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
		eyelink_calibrate.__init__(self, name, experiment, string)		
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
		self.add_combobox_control("tracker_attached", "Tracked attached", [self._text_attached, self._text_not_attached], tooltip = "Indicates if the tracker is attached")
		self.add_line_edit_control("sacc_vel_thresh", "Saccade velocity threshold", default = self.get("sacc_vel_thresh"), tooltip = "Saccade detection parameter")
		self.add_line_edit_control("sacc_acc_thresh", "Saccade acceleration threshold", default = self.get("sacc_acc_thresh"), tooltip = "Saccade detection parameter")
		#self.add_combobox_control("restart", "Restart OpenSesame after experiment", ["Yes", "No"], tooltip = "Restart OpenSesame after experiment")
		self.add_text("\nThis plug-in starts the Eyelink calibration/ tracker setup. If necessary, it also establishes a connection to the Eyelink.")		
		
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
		
		

