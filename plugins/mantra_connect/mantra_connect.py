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
import openexp.canvas
import os.path
import imp
from PyQt4 import QtGui, QtCore

class mantra_connect(item.item):

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
		self.item_type = "mantra_connect"
		
		self.version = 0.10
		
		self._text_attached = "Yes"
		self._text_not_attached = "No (dummy mode)"
		self.tracker_attached = self._text_attached
		
		self.mantra_logfile = "[logfile]"
		self.host = "localhost"
		self.port = 40007
		
		# Provide a short accurate description of the items functionality
		self.description = "Connects to the Mantra server"
				
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
		path = os.path.join(os.path.dirname(__file__), "libmantra.py")						
		libmantra = imp.load_source("libmantra", path)			
										
		if self.get("tracker_attached") == self._text_attached:
		
			if self.experiment.debug:
				print "mantra_connect.prepare(): connecting to %s:%s" % (self.get("host"), self.get("port"))
		
			err_msg = "Failed to connect to the Mantra server at %s:%s. Perhaps Mantra is not running or the host or port has been specified incorrectly." % (self.get("host"), self.get("port"))
		
			try:			
				self.experiment.mantra = libmantra.libmantra(self.get("host"), self.get("port"))
			except:
				raise exceptions.runtime_error(err_msg)
				
			if not self.experiment.mantra.connected:
				raise exceptions.runtime_error(err_msg)
				
			self.experiment.mantra.set_fname(os.path.basename(self.get("mantra_logfile")))	
			
			self.experiment.cleanup_functions.append(self.cleanup)
			
		else:
			if self.experiment.debug:
				print "mantra_connect.prepare(): running in dummy mode"
						
			self.experiment.mantra = libmantra.libmantra_dummy()
		
		# Report success
		return True
				
	def run(self):
	
		"""
		Run the item. In this case this means putting the offline canvas
		to the display and waiting for the specified duration.
		"""
		
		# Show the canvas
		self.set_item_onset()
				
		# Report success
		return True
		
	def cleanup(self):
	
		"""
		Clean up the connection to Mantra, otherwise
		we'll need to restart OpenSesame for a new
		connection
		"""
		
		if self.experiment.debug:
			print "mantra_connect.cleanup(): closing connection to Mantra"
	
		self.experiment.mantra.close()
					
class qtmantra_connect(mantra_connect, qtplugin.qtplugin):

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
		mantra_connect.__init__(self, name, experiment, string)		
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
		
		self.add_combobox_control("tracker_attached", "Tracked attached", [self._text_attached, self._text_not_attached], tooltip = "Indicates if the tracker is attached")		
		self.add_line_edit_control("mantra_logfile", "Logfile", tooltip = "The name of the logfile on the Mantra server side")
		self.add_line_edit_control("host", "Host", tooltip = "The IP-address or hostname of the server on which Mantra is running")
		self.add_line_edit_control("port", "Port", tooltip = "The port at which the Mantra server is listening")		
		self.add_text("<small><b>Mantra OpenSesame plug-in v%.2f</b></small>" % self.version)
		
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
