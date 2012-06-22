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

from libopensesame import item
from libqtopensesame import qtplugin
import openexp.canvas
import os.path
from PyQt4 import QtGui, QtCore

class notepad(item.item):

	"""Notepad plug-in"""

	def __init__(self, name, experiment, string=None):
	
		"""
		Constructor

		Arguments:
		name -- the name of the item
		experiment -- the experiment

		Keyword arguments:
		string -- an item definition string (default = None)
		"""
		
		self.item_type = "notepad"
		self.note = "Type your note here"
		self.description = \
			"A simple notepad to document your experiment. This plug-in does nothing."
		item.item.__init__(self, name, experiment, string)					
					
class qtnotepad(notepad, qtplugin.qtplugin):

	"""Notepad plug-in GUI"""

	def __init__(self, name, experiment, string=None):
	
		"""
		Constructor

		Arguments:
		name -- the name of the item
		experiment -- the experiment

		Keyword arguments:
		string -- an item definition string (default = None)
		"""
		
		notepad.__init__(self, name, experiment, string)		
		qtplugin.qtplugin.__init__(self, __file__)	
		
	def init_edit_widget(self):
	
		"""Initialize controls"""
		
		self.lock = True		
		qtplugin.qtplugin.init_edit_widget(self, False)		
		self.add_editor_control("note", "Note", tooltip = "Type your note here")				
		self.lock = True		
		
	def apply_edit_changes(self):
	
		"""
		Apply controls
		
		Returns:
		True on success, False on failure		
		"""
		
		if not qtplugin.qtplugin.apply_edit_changes(self, False) or self.lock:
			return False
		self.experiment.main_window.refresh(self.name)		
		return True

	def edit_widget(self):
	
		"""
		Update the controls
		
		Returns:
		The QWidget containing the controls
		"""
		
		self.lock = True
		qtplugin.qtplugin.edit_widget(self)				
		self.lock = False
		return self._edit_widget
