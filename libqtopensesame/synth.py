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

import libopensesame.synth
import libqtopensesame.qtitem
import libqtopensesame.synth_widget_ui
from PyQt4 import QtCore, QtGui

class synth(libopensesame.synth.synth, libqtopensesame.qtitem.qtitem):

	def __init__(self, name, experiment, string = None):
	
		"""
		Initialize the experiment		
		"""
		
		libopensesame.synth.synth.__init__(self, name, experiment, string)
		libqtopensesame.qtitem.qtitem.__init__(self)					
		self.lock = False
						
	def init_edit_widget(self):
	
		"""
		Build the edit widget
		"""
		
		libqtopensesame.qtitem.qtitem.init_edit_widget(self, False)
				
		self.synth_widget = QtGui.QWidget()
		self.synth_widget.ui = libqtopensesame.synth_widget_ui.Ui_Form()
		self.synth_widget.ui.setupUi(self.synth_widget)

		self.synth_widget.ui.spin_attack.valueChanged.connect(self.apply_edit_changes)
		self.synth_widget.ui.spin_decay.valueChanged.connect(self.apply_edit_changes)
		self.synth_widget.ui.spin_pan.valueChanged.connect(self.apply_edit_changes)
		self.synth_widget.ui.spin_volume.valueChanged.connect(self.apply_edit_changes)
		self.synth_widget.ui.spin_length.valueChanged.connect(self.apply_edit_changes)		
		
		self.synth_widget.ui.edit_freq.editingFinished.connect(self.apply_edit_changes)		
		self.synth_widget.ui.edit_duration.editingFinished.connect(self.apply_edit_changes)		

		self.synth_widget.ui.dial_attack.valueChanged.connect(self.apply_dials)
		self.synth_widget.ui.dial_decay.valueChanged.connect(self.apply_dials)	
		self.synth_widget.ui.dial_pan.valueChanged.connect(self.apply_dials)
		self.synth_widget.ui.dial_volume.valueChanged.connect(self.apply_dials)
		
		self.synth_widget.ui.button_script.clicked.connect(self.open_script_tab)		
		self.synth_widget.ui.button_sine.clicked.connect(self.set_sine)
		self.synth_widget.ui.button_saw.clicked.connect(self.set_saw)
		self.synth_widget.ui.button_square.clicked.connect(self.set_square)
		self.synth_widget.ui.button_white_noise.clicked.connect(self.set_white_noise)
							
		self.edit_vbox.addWidget(self.synth_widget)
		self.edit_vbox.addStretch()
		
	def set_sine(self):
	
		"""
		Set the oscillator
		"""
		
		self.synth_widget.ui.button_sine.setChecked(True)
		self.synth_widget.ui.button_saw.setChecked(False)
		self.synth_widget.ui.button_square.setChecked(False)
		self.synth_widget.ui.button_white_noise.setChecked(False)
		
		self.set("osc", "sine")
		self.apply_edit_changes()
		
	def set_saw(self):
	
		"""
		Set the oscillator
		"""

		self.synth_widget.ui.button_sine.setChecked(False)
		self.synth_widget.ui.button_saw.setChecked(True)
		self.synth_widget.ui.button_square.setChecked(False)
		self.synth_widget.ui.button_white_noise.setChecked(False)
		
		self.set("osc", "saw")
		self.apply_edit_changes()
		
	def set_square(self):
	
		"""
		Set the oscillator
		"""

		self.synth_widget.ui.button_sine.setChecked(False)
		self.synth_widget.ui.button_saw.setChecked(False)
		self.synth_widget.ui.button_square.setChecked(True)
		self.synth_widget.ui.button_white_noise.setChecked(False)
		
		self.set("osc", "square")
		self.apply_edit_changes()
		
	def set_white_noise(self):
	
		"""
		Set the oscillator
		"""

		self.synth_widget.ui.button_sine.setChecked(False)
		self.synth_widget.ui.button_saw.setChecked(False)
		self.synth_widget.ui.button_square.setChecked(False)
		self.synth_widget.ui.button_white_noise.setChecked(True)
		
		self.set("osc", "white_noise")
		self.apply_edit_changes()
						
	def edit_widget(self):
	
		"""
		Refresh the edit widget
		with current information
		and return it
		"""	
		
		self.lock = True		
		
		libqtopensesame.qtitem.qtitem.edit_widget(self, False)		
				
		if self.variable_vars(["duration", "freq"]):
			
			self.synth_widget.ui.frame_notification.setVisible(True)
			self.synth_widget.ui.frame_controls.setVisible(False)
			
		else:
		
			self.synth_widget.ui.frame_notification.setVisible(False)
			self.synth_widget.ui.frame_controls.setVisible(True)		
		
			self.synth_widget.ui.edit_freq.setText(str(self.get("freq")))		
			self.synth_widget.ui.edit_duration.setText(str(self.get("duration")))		

			self.synth_widget.ui.spin_attack.setValue(self.get("attack"))
			self.synth_widget.ui.spin_decay.setValue(self.get("decay"))		
			self.synth_widget.ui.spin_pan.setValue(self.get("pan"))
			self.synth_widget.ui.spin_volume.setValue(100.0 * self.get("volume"))
			self.synth_widget.ui.spin_length.setValue(self.get("length"))

			self.synth_widget.ui.dial_attack.setValue(self.get("attack"))
			self.synth_widget.ui.dial_decay.setValue(self.get("decay"))
			self.synth_widget.ui.dial_pan.setValue(self.get("pan"))
			self.synth_widget.ui.dial_volume.setValue(100.0 * self.get("volume"))			
						
			self.synth_widget.ui.button_sine.setChecked(self.get("osc") == "sine")
			self.synth_widget.ui.button_saw.setChecked(self.get("osc") == "saw")
			self.synth_widget.ui.button_square.setChecked(self.get("osc") == "square")
			self.synth_widget.ui.button_white_noise.setChecked(self.get("osc") == "white_noise")
			
		self.lock = False
			
		return self._edit_widget


	def apply_edit_changes(self, i = None, j = None):
	
		"""
		Apply the changes to the synth controls
		"""	
		
		if not libqtopensesame.qtitem.qtitem.apply_edit_changes(self) or self.lock:
			return
			
		self.set("freq", str(self.synth_widget.ui.edit_freq.text()))
		
		dur = str(self.synth_widget.ui.edit_duration.text())
		if type(self.auto_type(dur)) not in (int, float) and dur not in ("keypress", "mouseclick", "sound"):
			self.experiment.notify("'%s' is not a valid duration. Exception a positive number (duration in ms) or 'keypress', 'mouseclick', or 'sound'" % dur)
			self.synth_widget.ui.edit_duration.setText(self.get("duration"))
		else:
			self.set("duration", dur)			

		self.set("attack", self.synth_widget.ui.spin_attack.value())
		self.set("decay", self.synth_widget.ui.spin_decay.value())		
		self.set("pan", self.synth_widget.ui.spin_pan.value())
		self.set("volume", .01 * self.synth_widget.ui.spin_volume.value())
		self.set("length", self.synth_widget.ui.spin_length.value())
		
		if self.synth_widget.ui.button_sine.isChecked():
			self.set("osc", "sine")
		elif self.synth_widget.ui.button_saw.isChecked():
			self.set("osc", "saw")
		elif self.synth_widget.ui.button_square.isChecked():
			self.set("osc", "square")
		else:
			self.set("osc", "white_noise")
		
		self.experiment.main_window.refresh(self.name)			
						
	def apply_dials(self, i = None):
	
		"""
		Read the dials and use those to set the spinboxes
		"""
		
		if self.lock:
			return
		
		self.set("attack", self.synth_widget.ui.dial_attack.value())
		self.set("decay", self.synth_widget.ui.dial_decay.value())
		self.set("pan", self.synth_widget.ui.dial_pan.value())
		self.set("volume", .01 * self.synth_widget.ui.dial_volume.value())
		
		self.edit_widget()
