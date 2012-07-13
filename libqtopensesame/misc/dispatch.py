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

DISPATCH LOGIC
==============

The following elements can be affected by a change in an item

+ Item tree
	+ Affected by name changes
	+ Affected by sequence and loop changes

- Loop items
	+ Affected by name changes (only if parent)
	
- Sequence items
	+ Affected by name changes (only if parent)
		
To handle this, we have the following events

+ name_change
	Refresh item tree
	Refresh loops
	Refresh sequences

+ script_change

"""

class dispatch:

	"""
	The dispatch is informed of changes and passes theses on to the various
	parts of the GUI
	"""
		
	def __init__(self, main_window):
	
		"""
		Constructor
		
		Arguments:
		main_window -- the main window
		"""
	
		self.main_window = main_window
		
	def edit_changed(self, name):
	
		"""
		Handles simple changes to an item
		
		Arguments:
		name -- the name of an item
		"""
	
		self.main_window.refresh_variable_inspector()
		
	def name_changed(self, from_name, to_name):
	
		"""
		Handles the name change of an item
		
		Arguments:
		from_name -- the previous name
		to_name -- the new name		
		"""
	
		from_name = str(from_name)
		to_name = str(to_name)
		# Rename the item in the experiment item list
		item = self.main_window.experiment.items[from_name]
		del self.main_window.experiment.items[from_name]
		self.main_window.experiment.items[to_name] = item		
		# Give all items the chance to process the name change
		for item in self.main_window.experiment.items:
			self.main_window.experiment.items[item].rename(from_name, to_name)
		# Rebuild the item tree
		self.main_window.experiment.build_item_tree()		
		# Rename the item tab
		i = self.main_window.ui.tabwidget.get_item(to_name)
		if i != None:		
			self.main_window.ui.tabwidget.setTabText(i, to_name)
		# Pass on to the edit changed phase
		self.edit_changed(to_name)
