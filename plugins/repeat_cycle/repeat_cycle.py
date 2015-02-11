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

# Optional: Indicate contact and license information
__author__ = 'Sebastiaan Mathot'
__license__ = 'GPLv3'

# Import the base class from which all items are derived
from libopensesame import item

# Import the base class for the plug-in GUI
from libqtopensesame import qtplugin

class repeat_cycle(item.item):

	"""		
	This class (the class with the same name as the module) handles the basic
	runtime functionality of the item. The GUI controls are handled by the
	class qt_[plugin_name], which is defined later on in the same script.		
	"""

	def __init__(self, name, experiment, string=None):
	
		"""
		Constructor. The constructor is automatically called with the proper
		name, a reference to the experiment, etc.
		
		Arguments:
		name -- the name of the item
		experiment -- an experiment instance, as described here:
					  http://osdoc.cogsci.nl/python-inline-code/experiment-functions
		
		Keyword arguments:
		string -- a definition string, which contains the OpenSesame script
				  which is used to construct the plug-in. This is handled
				  automatically (default=None)
		"""
		
		# The item_typeshould match the name of the module
		self.item_type = "repeat_cycle"
		
		# Provide a short accurate description of the items functionality
		self.description = "Optionally repeat a cycle from a loop"		
		
		# Initialize variables
		self.condition = 'never'
		
		# The parent handles the rest of the contruction
		item.item.__init__(self, name, experiment, string)
						
	def prepare(self):
	
		"""Prepare the item"""
		
		item.item.prepare(self)		
		self._condition = self.compile_cond(self.condition)
		return True
				
	def run(self):
	
		"""Run the item"""
		
		if eval(self._condition):
			self.experiment.set('repeat_cycle', 1)
		return True
					
class qtrepeat_cycle(repeat_cycle, qtplugin.qtplugin):

	"""
	This class (the class named qt[name of module] handles the GUI part of the
	plugin. There are a number of convenience functions to construct controls.	
	For more information about GUI programming using PyQt4, see:
	<http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/classes.html>
	"""

	def __init__(self, name, experiment, string=None):
	
		"""
		Constructor. The constructor is automatically called with the proper
		name, a reference to the experiment, etc.
		
		Arguments:
		name -- the name of the item
		experiment -- an experiment instance
		
		Keyword arguments:
		string -- a definition string (default=None)
		"""
		
		# Pass the word on to the parents		
		repeat_cycle.__init__(self, name, experiment, string)		
		qtplugin.qtplugin.__init__(self, __file__)	
		
	def init_edit_widget(self):
	
		"""Set up the GUI controls for the plugin"""
		
		self.lock = True
		qtplugin.qtplugin.init_edit_widget(self, False)		
		self.add_line_edit_control("condition", "Repeat if", tooltip= \
			"Conditional statement to specify when a cycle should be repeated")			
		self.add_stretch()
		self.lock = True
		
	def apply_edit_changes(self):
	
		"""
		Apply the controls (controls -> variables). Unless you have used custom
		controls, you will not need to modify this function.		
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
		Update the controls (variables -> controls). Unless you have used custom
		controls, you will not need to modify this function.		
		"""
		
		# Lock the controls, otherwise a recursive loop might arise
		# in which updating the controls causes the variables to be
		# updated, which causes the controls to be updated, etc...
		self.lock = True
		
		# Let the parent handle everything
		qtplugin.qtplugin.edit_widget(self)				
		
		# Unlock
		self.lock = False
		
		# Return the _edit_widget
		return self._edit_widget
