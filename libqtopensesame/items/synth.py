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

import libopensesame.synth
from libqtopensesame.misc import _
from libqtopensesame.items import qtitem
from libqtopensesame.widgets.synth_widget import synth_widget
from PyQt4 import QtCore, QtGui

class synth(libopensesame.synth.synth, qtitem.qtitem):

	"""GUI controls for the synth item"""

	def __init__(self, name, experiment, string = None):
	
		"""
		Constructor
		
		Arguments:
		name -- the item name
		experiment -- the experiment
		
		Keywords arguments:
		string -- definition string (default=None)
		"""
		
		libopensesame.synth.synth.__init__(self, name, experiment, string)
		qtitem.qtitem.__init__(self)					
		self.lock = False
						
	def init_edit_widget(self):
	
		"""Build the GUI controls"""
		
		qtitem.qtitem.init_edit_widget(self, False)				
		self.synth_widget = synth_widget(self.main_window)
		self.synth_widget.ui.spin_attack.valueChanged.connect( \
			self.apply_edit_changes)
		self.synth_widget.ui.spin_decay.valueChanged.connect( \
			self.apply_edit_changes)
		self.synth_widget.ui.spin_pan.valueChanged.connect( \
			self.apply_edit_changes)
		self.synth_widget.ui.spin_volume.valueChanged.connect( \
			self.apply_edit_changes)
		self.synth_widget.ui.spin_length.valueChanged.connect( \
			self.apply_edit_changes)				
		self.synth_widget.ui.edit_freq.editingFinished.connect( \
			self.apply_edit_changes)		
		self.synth_widget.ui.edit_duration.editingFinished.connect( \
			self.apply_edit_changes)		
		self.synth_widget.ui.dial_attack.valueChanged.connect(self.apply_dials)
		self.synth_widget.ui.dial_decay.valueChanged.connect(self.apply_dials)	
		self.synth_widget.ui.dial_pan.valueChanged.connect(self.apply_dials)
		self.synth_widget.ui.dial_volume.valueChanged.connect(self.apply_dials)		
		self.synth_widget.ui.button_sine.clicked.connect(self.set_sine)
		self.synth_widget.ui.button_saw.clicked.connect(self.set_saw)
		self.synth_widget.ui.button_square.clicked.connect(self.set_square)
		self.synth_widget.ui.button_white_noise.clicked.connect( \
			self.set_white_noise)							
		self.edit_vbox.addWidget(self.synth_widget)
		self.edit_vbox.addStretch()
		
	def set_sine(self):
	
		"""Select the sine oscillator"""
		
		self.synth_widget.ui.button_sine.setChecked(True)
		self.synth_widget.ui.button_saw.setChecked(False)
		self.synth_widget.ui.button_square.setChecked(False)
		self.synth_widget.ui.button_white_noise.setChecked(False)
		
		self.set("osc", "sine")
		self.apply_edit_changes()
		
	def set_saw(self):
	
		"""Select the saw oscillator"""

		self.synth_widget.ui.button_sine.setChecked(False)
		self.synth_widget.ui.button_saw.setChecked(True)
		self.synth_widget.ui.button_square.setChecked(False)
		self.synth_widget.ui.button_white_noise.setChecked(False)
		
		self.set("osc", "saw")
		self.apply_edit_changes()
		
	def set_square(self):
	
		"""Select the square oscillator"""

		self.synth_widget.ui.button_sine.setChecked(False)
		self.synth_widget.ui.button_saw.setChecked(False)
		self.synth_widget.ui.button_square.setChecked(True)
		self.synth_widget.ui.button_white_noise.setChecked(False)
		
		self.set("osc", "square")
		self.apply_edit_changes()
		
	def set_white_noise(self):
	
		"""Select the white noise oscillator"""

		self.synth_widget.ui.button_sine.setChecked(False)
		self.synth_widget.ui.button_saw.setChecked(False)
		self.synth_widget.ui.button_square.setChecked(False)
		self.synth_widget.ui.button_white_noise.setChecked(True)
		
		self.set("osc", "white_noise")
		self.apply_edit_changes()
						
	def edit_widget(self):
	
		"""Refresh the GUI controls"""	
		
		self.lock = True		
		
		qtitem.qtitem.edit_widget(self, False)		
				
		if self.variable_vars(["duration", "freq"]):			
			self.synth_widget.ui.frame_controls.setVisible(False)
			self.user_hint_widget.add_user_hint(_( \
				'The controls are disabled, because one of the settings is defined using variables.'))
			self.user_hint_widget.refresh()			
		else:
		
			self.synth_widget.ui.frame_controls.setVisible(True)				
			self.synth_widget.ui.edit_freq.setText(self.unistr(self.get( \
				'freq', _eval=False)))		
			self.synth_widget.ui.edit_duration.setText(self.unistr(self.get( \
				'duration', _eval=False)))
			self.synth_widget.ui.spin_attack.setValue(self.get("attack", \
				_eval=False))
			self.synth_widget.ui.spin_decay.setValue(self.get("decay", _eval= \
				False))		
			self.synth_widget.ui.spin_pan.setValue(self.get("pan", _eval=False))
			self.synth_widget.ui.spin_volume.setValue(100.0 * self.get( \
				"volume", _eval=False))
			self.synth_widget.ui.spin_length.setValue(self.get("length", \
				_eval=False))
			self.synth_widget.ui.dial_attack.setValue(self.get("attack", \
				_eval=False))
			self.synth_widget.ui.dial_decay.setValue(self.get("decay", \
				_eval=False))
			self.synth_widget.ui.dial_pan.setValue(self.get("pan", _eval= \
				False))
			self.synth_widget.ui.dial_volume.setValue(100.0 * self.get( \
				"volume", _eval=False))									
			self.synth_widget.ui.button_sine.setChecked(self.get("osc", \
				_eval=False) == "sine")
			self.synth_widget.ui.button_saw.setChecked(self.get("osc", _eval= \
				False) == "saw")
			self.synth_widget.ui.button_square.setChecked(self.get("osc", \
				_eval=False) == "square")
			self.synth_widget.ui.button_white_noise.setChecked(self.get( \
				"osc", _eval=False) == "white_noise")
			
		self.lock = False
			
		return self._edit_widget


	def apply_edit_changes(self, dummy1=None, dummy2=None):
	
		"""
		Apply the GUI controls
		
		Keywords arguments:
		dummy1 -- a dummy argument (default=None)
		dummy2 -- a dummy argument (default=None)
		"""	
		
		if not qtitem.qtitem.apply_edit_changes(self) or self.lock:
			return
			
		self.set("freq", self.sanitize(self.synth_widget.ui.edit_freq.text(), \
			strict=True))		
		dur = self.sanitize(self.synth_widget.ui.edit_duration.text(), \
			strict=True)
		if dur == "":
			dur = "sound"
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
						
	def apply_dials(self, dummy=None):
	
		"""
		Set the spinbox values based on the dials
		
		Keywords arguments:
		dummy -- a dummy argument (default=None)
		"""
		
		if self.lock:
			return		
		self.set("attack", self.synth_widget.ui.dial_attack.value())
		self.set("decay", self.synth_widget.ui.dial_decay.value())
		self.set("pan", self.synth_widget.ui.dial_pan.value())
		self.set("volume", .01 * self.synth_widget.ui.dial_volume.value())		
		self.edit_widget()
