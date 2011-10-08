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

import libopensesame.sampler
import libqtopensesame.qtitem
import libqtopensesame.sampler_widget_ui
import libqtopensesame.pool_widget
from PyQt4 import QtCore, QtGui

class sampler(libopensesame.sampler.sampler, libqtopensesame.qtitem.qtitem):

	"""GUI controls for the sampler item"""

	def __init__(self, name, experiment, string=None):
	
		"""
		Constructor
		
		Arguments:
		name -- the item name
		experiment -- the experiment
		
		Keywords arguments:
		string -- definition string (default=None)
		"""
		
		libopensesame.sampler.sampler.__init__(self, name, experiment, string)
		libqtopensesame.qtitem.qtitem.__init__(self)	
		self.lock = False			
				
	def init_edit_widget(self):
	
		"""Build the GUI controls"""
		
		libqtopensesame.qtitem.qtitem.init_edit_widget(self, False)
				
		self.sampler_widget = QtGui.QWidget()
		self.sampler_widget.ui = libqtopensesame.sampler_widget_ui.Ui_Form()
		self.sampler_widget.ui.setupUi(self.sampler_widget)
		
		self.sampler_widget.ui.spin_pan.valueChanged.connect(self.apply_edit_changes)
		self.sampler_widget.ui.spin_volume.valueChanged.connect(self.apply_edit_changes)
		self.sampler_widget.ui.spin_pitch.valueChanged.connect(self.apply_edit_changes)
		self.sampler_widget.ui.spin_stop_after.valueChanged.connect(self.apply_edit_changes)		
		self.sampler_widget.ui.spin_fade_in.valueChanged.connect(self.apply_edit_changes)		
		self.sampler_widget.ui.edit_duration.editingFinished.connect(self.apply_edit_changes)		
		self.sampler_widget.ui.edit_sample.editingFinished.connect(self.apply_edit_changes)		
	
		self.sampler_widget.ui.button_browse_sample.clicked.connect(self.browse_sample)
		self.sampler_widget.ui.button_script.clicked.connect(self.open_script_tab)
		
		self.sampler_widget.ui.dial_pan.valueChanged.connect(self.apply_dials)
		self.sampler_widget.ui.dial_volume.valueChanged.connect(self.apply_dials)
		self.sampler_widget.ui.dial_pitch.valueChanged.connect(self.apply_dials)
							
		self.edit_vbox.addWidget(self.sampler_widget)
		self.edit_vbox.addStretch()
					
	def browse_sample(self):
	
		"""Present a file dialog to browse for the sample"""
		
		s = libqtopensesame.pool_widget.select_from_pool(self.experiment.main_window)
		if str(s) == "":
			return			
		self.sampler_widget.ui.edit_sample.setText(s)
		self.apply_edit_changes()
		
	def edit_widget(self):
	
		"""
		Refresh the GUI controls
		
		Returns:
		A QWidget with the controls
		"""	
		
		self.lock = True		
		libqtopensesame.qtitem.qtitem.edit_widget(self)						
		if self.variable_vars(["sample", "duration"]):			
			self.sampler_widget.ui.frame_notification.setVisible(True)
			self.sampler_widget.ui.frame_controls.setVisible(False)
			
		else:		
			self.sampler_widget.ui.frame_notification.setVisible(False)
			self.sampler_widget.ui.frame_controls.setVisible(True)					
			self.sampler_widget.ui.edit_sample.setText(self.get("sample"))
			self.sampler_widget.ui.edit_duration.setText(str(self.get("duration")))		
			self.sampler_widget.ui.spin_pan.setValue(self.get("pan"))
			self.sampler_widget.ui.spin_volume.setValue(100.0 * self.get("volume"))
			self.sampler_widget.ui.spin_pitch.setValue(100.0 * self.get("pitch"))
			self.sampler_widget.ui.spin_fade_in.setValue(self.get("fade_in"))
			self.sampler_widget.ui.spin_stop_after.setValue(self.get("stop_after"))
			self.sampler_widget.ui.dial_pan.setValue(self.get("pan"))
			self.sampler_widget.ui.dial_volume.setValue(100.0 * self.get("volume"))
			self.sampler_widget.ui.dial_pitch.setValue(100.0 * self.get("pitch"))			
		self.lock = False		
		return self._edit_widget

	def apply_edit_changes(self, dummy1=None, dummy2=None):
	
		"""
		Apply the GUI controls
		
		Keywords arguments:
		dummy1 -- a dummy argument (default=None)
		dummy2 -- a dummy argument (default=None)
		"""	
		
		if not libqtopensesame.qtitem.qtitem.apply_edit_changes(self, False) or self.lock:
			return		
		self.set("sample", self.usanitize(self.sampler_widget.ui.edit_sample.text()))		
		dur = self.sanitize(self.sampler_widget.ui.edit_duration.text(), strict=True)
		if dur == "":
			dur = "sound"
		self.set("duration", dur)					
		self.set("pan", self.sampler_widget.ui.spin_pan.value())
		self.set("pitch", .01 * self.sampler_widget.ui.spin_pitch.value())
		self.set("volume", .01 * self.sampler_widget.ui.spin_volume.value())
		self.set("fade_in", self.sampler_widget.ui.spin_fade_in.value())
		self.set("stop_after", self.sampler_widget.ui.spin_stop_after.value())
		
		self.experiment.main_window.refresh(self.name)			
						
	def apply_dials(self, dummy=None):
	
		"""
		Set the spinbox values based on the dials
		
		Keywords arguments:
		dummy -- a dummy argument (default=None)
		"""
		
		if self.lock:
			return
		self.set("pan", self.sampler_widget.ui.dial_pan.value())
		self.set("pitch", .01 * self.sampler_widget.ui.dial_pitch.value())
		self.set("volume", .01 * self.sampler_widget.ui.dial_volume.value())		
		self.edit_widget()
