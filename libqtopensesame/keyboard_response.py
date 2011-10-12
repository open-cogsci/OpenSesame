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
from openexp.keyboard import keyboard
from PyQt4 import QtCore, QtGui
import cgi

class keyboard_response(libopensesame.keyboard_response.keyboard_response, libqtopensesame.qtitem.qtitem):

	"""keyboard_response item GUI"""

	def __init__(self, name, experiment, string=None):
	
		"""
		Constructor
		
		Arguments:
		name -- item name
		experiment -- experiment instance	
		
		Keywords arguments:
		string -- a definition string (default=None)	
		"""
		
		libopensesame.keyboard_response.keyboard_response.__init__(self, name, experiment, string)
		libqtopensesame.qtitem.qtitem.__init__(self)		

	def apply_edit_changes(self):
	
		"""Apply controls"""
		
		libqtopensesame.qtitem.qtitem.apply_edit_changes(self)
		
		cr = self.usanitize(self.edit_correct_response.text())
		if cr.strip() != "":
			self.set("correct_response", cr)
		else:
			self.unset("correct_response")
		
		ar = self.usanitize(self.edit_allowed_responses.text())
		if ar.strip() != "":
			self.set("allowed_responses", ar)
		else:
			self.unset("allowed_responses")
			
		to = self.sanitize(self.edit_timeout.text(), strict=True)
		if to.strip() != "":
			self.set("timeout", to)
		else:
			self.set("timeout", "infinite")		
			
		if self.checkbox_flush.isChecked():
			self.set("flush", "yes")
		else:
			self.set("flush", "no")
			
		self.experiment.main_window.refresh(self.name)			

	def init_edit_widget(self):
	
		"""Initialize controls"""
		
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
		
		row += 1							
		
		self.checkbox_flush = QtGui.QCheckBox("Flush pending key presses")
		self.checkbox_flush.toggled.connect(self.apply_edit_changes)
		self.edit_grid.addWidget(self.checkbox_flush, row, 1)
		
		row += 1							
		
		button_list_keys = QtGui.QPushButton(self.experiment.icon("info"), "List available keys")
		button_list_keys.clicked.connect(self.list_keys)
		self.edit_grid.addWidget(button_list_keys, row, 1)
				
		self.edit_vbox.addStretch()
							
	def edit_widget(self):
	
		"""
		Update controls
		
		Returns:
		Controls QWidget
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
		
		self.checkbox_flush.setChecked(self.get("flush") == "yes")
		
		return self._edit_widget
		
	def list_keys(self):
	
		"""Show a dialog with available key names"""
		
		my_keyboard = keyboard(self.experiment)
		s = "The following keys have been detected. Note that different backends may use slightly different names.<br /><br />"
		s += "Keyboard backend: %s<br/><br />" % self.get("keyboard_backend")
		for name in sorted(my_keyboard.valid_keys()):			
			s += "Key: <b>%s</b><br />" % cgi.escape(str(name))
			syn = my_keyboard.synonyms(name)
			if syn != [name]:
				s += "(or %s)<br />" % (", ".join([cgi.escape(str(x)) for x in syn]))
		self.experiment.notify(s)
	
