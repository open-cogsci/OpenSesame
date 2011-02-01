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

import libopensesame.keyboard_response
import libqtopensesame.qtitem
from PyQt4 import QtCore, QtGui

class keyboard_response(libopensesame.keyboard_response.keyboard_response, libqtopensesame.qtitem.qtitem):

	def __init__(self, name, experiment, string = None):
	
		"""
		Initialize the experiment		
		"""
		
		libopensesame.keyboard_response.keyboard_response.__init__(self, name, experiment, string)
		libqtopensesame.qtitem.qtitem.__init__(self)		

	def apply_edit_changes(self):
	
		"""
		Apply changes to the edit widget
		"""
		
		libqtopensesame.qtitem.qtitem.apply_edit_changes(self)
		
		cr = str(self.edit_correct_response.text()).strip()
		if cr.strip() != "":
			self.set("correct_response", cr)
		else:
			self.unset("allowed_responses")
		
		ar = str(self.edit_allowed_responses.text()).strip()
		if ar.strip() != "":
			self.set("allowed_responses", ar)
		else:
			self.unset("allowed_responses")
			
		to = str(self.edit_timeout.text()).strip()
		if to.strip() != "":
			self.set("timeout", to)
		else:
			self.set("timeout", "infinite")		
			
		self.experiment.main_window.refresh(self.name)			

	def init_edit_widget(self):
	
		"""
		Build the edit widget
		"""
		
		libqtopensesame.qtitem.qtitem.init_edit_widget(self, False)
		
		row = 3
		
		self.edit_grid.addWidget(QtGui.QLabel("Correct response"), row, 0)
		self.edit_correct_response = QtGui.QLineEdit()
		self.edit_correct_response.setToolTip("Set the correct response, e.g., 'z', '/', or 'space'")		
		QtCore.QObject.connect(self.edit_correct_response, QtCore.SIGNAL("editingFinished()"), self.apply_edit_changes)
		self.edit_grid.addWidget(self.edit_correct_response, row, 1)
		
		row += 1		
		
		self.edit_grid.addWidget(QtGui.QLabel("Allowed responses"), row, 0)
		self.edit_allowed_responses = QtGui.QLineEdit()
		self.edit_allowed_responses.setToolTip("Set the allowed responses seperated by a semi-colon, e.g., 'z;/'")		
		QtCore.QObject.connect(self.edit_allowed_responses, QtCore.SIGNAL("editingFinished()"), self.apply_edit_changes)
		self.edit_grid.addWidget(self.edit_allowed_responses, row, 1)		

		row += 1		
		
		self.edit_grid.addWidget(QtGui.QLabel("Timeout"), row, 0)
		self.edit_timeout = QtGui.QLineEdit()
		self.edit_timeout.setToolTip("Set the response timeout in milliseconds, or 'infinite'")		
		QtCore.QObject.connect(self.edit_timeout, QtCore.SIGNAL("editingFinished()"), self.apply_edit_changes)
		self.edit_grid.addWidget(self.edit_timeout, row, 1)		
		
		self.edit_vbox.addStretch()
							
	def edit_widget(self):
	
		"""
		Refresh and return the edit widget
		"""

		libqtopensesame.qtitem.qtitem.edit_widget(self)

		if hasattr(self, "correct_response"):
			cr = self.get("correct_response")
		else:
			cr = ""		
		self.edit_correct_response.setText(str(cr))		
		
		if hasattr(self, "allowed_responses"):
			ar = self.get("allowed_responses")
		else:
			ar = ""		
		self.edit_allowed_responses.setText(str(ar))
		
		if hasattr(self, "timeout"):
			to = self.get("timeout")
		else:
			to = ""		
		self.edit_timeout.setText(str(to))
		
		return self._edit_widget
		
	
