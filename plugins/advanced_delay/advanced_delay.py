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
from PyQt4 import QtGui, QtCore
import os.path
import random

class advanced_delay(item.item):

	def __init__(self, name, experiment, string = None):
	
		"""
		Initialize the item
		"""
		
		self.item_type = "advanced_delay"
		self.description = "Waits for a specified duration"
		self.duration = 1000
		self.jitter = 0
		item.item.__init__(self, name, experiment, string)
				
	def prepare(self):
	
		"""
		Prepare the item
		"""
		
		item.item.prepare(self)		
		
		try:
			if self.get("jitter_mode") is "Uniform":
				self._duration = int(self.get("duration") + random.uniform(0, self.get("jitter")) - self.get("jitter")*0.5)
			else:
				self._duration = int(self.get("duration") + random.gauss(0, self.get("jitter")))
		except:
			raise exceptions.runtime_error("Invalid duration and/ or jitter in advanced_delay '%s'" % self.name)

		if self._duration < 0:
			self._duration = 0
			
		self.experiment.set("delay_%s" % self.name, self._duration)
		if self.experiment.debug:
			print "advanced_delay.prepare(): delay for %s ms" % self._duration
				
		return True
				
	def run(self):
	
		"""
		Run the item
		"""
		
		self.set_item_onset(self.time())
		self.sleep(self._duration)
		
		return True
		
	def var_info(self):
	
		"""
		Add 'response' to the variables
		"""
		
		return item.item.var_info(self) + [("delay_%s" % self.name, "[Determined at runtime]")]		
					
class qtadvanced_delay(advanced_delay, qtplugin.qtplugin):

	def __init__(self, name, experiment, string = None):
	
		"""
		Initialize the GUI part of the plugin
		"""
		
		# Pass the word on to the parents		
		advanced_delay.__init__(self, name, experiment, string)		
		qtplugin.qtplugin.__init__(self, __file__)

	def init_edit_widget(self):
	
		"""
		Build the edit widget
		"""
		
		self.lock = True
		qtplugin.qtplugin.init_edit_widget(self, False)
		
		self.add_spinbox_control("duration", "Duration", 0, 1000000, suffix = "ms", tooltip = "The averege duration in milliseconds")
		self.add_spinbox_control("jitter", "Jitter", 0, 1000000, suffix = "ms", tooltip = "The jitter of the actual duration in milliseconds (depends on Jitter mode)")
		self.add_combobox_control("jitter_mode", "Jitter mode", ["Std. Dev.", "Uniform"], tooltip = "The mode of determining the duration (see Help)")
		
		self.edit_vbox.addStretch()		
		self.lock = False
		
	def apply_edit_changes(self):
	
		"""
		Apply changes to the edit widget
		"""
		
		if not qtplugin.qtplugin.apply_edit_changes(self, False) or self.lock:
			return			
		
		self.experiment.main_window.refresh(self.name)		

	def edit_widget(self):
	
		"""
		Refresh and return the edit widget
		"""
		
		self.lock = True

		qtplugin.qtplugin.edit_widget(self)		
		
		self.lock = False
		
		return self._edit_widget
		
