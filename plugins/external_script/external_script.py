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
from libopensesame import item
from libqtopensesame import qtplugin, pool_widget
import openexp.canvas
import os.path
from PyQt4 import QtGui, QtCore
import imp

class external_script(item.item):

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
		self.item_type = "external_script"
		self.file = ""
		self.module = None
		self.prepare_func = "prepare"
		self.run_func = "run"
		
		# Provide a short accurate description of the items functionality
		self.description = "An alternative way of running Python code, directly from a script file"
				
		# The parent handles the rest of the contruction
		item.item.__init__(self, name, experiment, string)
						
	def prepare(self):
	
		"""
		Prepare the item. In this case this means drawing a fixation
		dot to an offline canvas.
		"""
		
		# Pass the word on to the parent
		item.item.prepare(self)
		
		if self.module is None:
			try:
				self.module = imp.load_source("file", os.path.join( \
					self.experiment.pool_folder, self.file))
			except Exception as e:
				raise osexception( \
					"Failed to import '%s' in the prepare phase of external_script item '%s': %s" \
					% (self.file, self.name, e))
			
		try:
			getattr(self.module, self.prepare_func)(self)
		except Exception as e:
			raise osexception( \
				"Failed to run function '%s(item)' in the prepare phase of external_script item '%s': %s" \
				% (self.prepare_func, self.name, e))				
		
		# Report success
		return True
				
	def run(self):
	
		"""
		Run the item. In this case this means putting the offline canvas
		to the display and waiting for the specified duration.
		"""
		
		# Show the canvas
		self.set_item_onset()
			
		try:
			getattr(self.module, self.run_func)(self)
		except Exception as e:
			raise osexception( \
				"Failed to run function '%s(item)' in the run phase of external_script item '%s': %s" \
				% (self.run_func, self.name, e))
								
		# Report success
		return True
					
class qtexternal_script(external_script, qtplugin.qtplugin):

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
		external_script.__init__(self, name, experiment, string)		
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
		
		self.add_filepool_control("file", "Script file", self.browse_script, default = "", tooltip = "A Python (.py) script")	
		self.add_line_edit_control("prepare_func", "Prepare function in script", default = "prepare", tooltip = "A function with a single parameter, e.g., 'def run(item)'")		
		self.add_line_edit_control("run_func", "Run function in script", default = "run", tooltip = "A function with a single parameter, e.g., 'def run(item)'")		
		
		# Add a stretch to the edit_vbox, so that the controls do not
		# stretch to the bottom of the window.
		self.edit_vbox.addStretch()		
		
		# Unlock
		self.lock = True		
		
	def browse_script(self):
	
		"""
		Browse the filepool
		"""
		
		s = pool_widget.select_from_pool(self.experiment.main_window)
		if s == "":
			return
			
		self.auto_line_edit["file"].setText(s)			
		self.apply_edit_changes()							
		
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
