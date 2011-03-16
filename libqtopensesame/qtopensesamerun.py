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

from PyQt4 import QtCore, QtGui
from libqtopensesame import opensesamerun_ui

class qtopensesamerun(QtGui.QMainWindow):

	"""
	The main class of the OpenSesame Run GUI.
	"""
	
	def __init__(self, options, parent = None):
		
		"""
		Constructor
		"""
			
		# Construct the parent
		QtGui.QMainWindow.__init__(self, parent)
														
		# Setup the UI
		self.ui = opensesamerun_ui.Ui_MainWindow()
		self.ui.setupUi(self)		
		self.ui.button_run.clicked.connect(self.run)
		
		self.ui.button_browse_experiment.clicked.connect(self.browse_experiment)
		self.ui.button_browse_logfile.clicked.connect(self.browse_logfile)
		
		self.options = options
		
		# Fill the GUI controls based on the options				
		self.ui.edit_experiment.setText(self.options.experiment)		
		self.ui.checkbox_fullscreen.setChecked(self.options.fullscreen)
		self.ui.checkbox_pylink.setChecked(self.options.pylink)				
		self.ui.spinbox_subject_nr.setValue(int(self.options.subject))
		self.ui.edit_logfile.setText(self.options.logfile)
		
	def browse_experiment(self):
	
		"""
		Locate the experiment file
		"""
		
		file_type_filter = "OpenSesame files (*.opensesame.tar.gz *.opensesame);;OpenSesame script and file pool (*.opensesame.tar.gz);;OpenSesame script (*.opensesame)"				
		path = QtGui.QFileDialog.getOpenFileName(self, "Open experiment file", filter = file_type_filter)
		if path == "":
			return
			
		self.ui.edit_experiment.setText(path)
		
	def browse_logfile(self):
	
		"""
		Locate the logfile
		"""
			
		path = QtGui.QFileDialog.getSaveFileName(self, "Choose a location for the logfile")
		if path == "":
			return
			
		self.ui.edit_logfile.setText(path)		
		
	def show(self):
	
		"""
		Set the run flag to false
		"""
	
		self.run = False
		QtGui.QMainWindow.show(self)
			
	def run(self):
	
		"""
		Does not actual run the experiment, but marks the application for
		running later
		"""
	
		self.run = True
		
		self.options.experiment = str(self.ui.edit_experiment.text())
		self.options.subject = self.ui.spinbox_subject_nr.value()
		self.options.logfile = str(self.ui.edit_logfile.text())
		
		self.options.fullscreen = self.ui.checkbox_fullscreen.isChecked()
		self.options.custom_resolution = self.ui.checkbox_custom_resolution.isChecked()
		self.options.width = self.ui.spinbox_width.value()
		self.options.height = self.ui.spinbox_height.value()		
		
		self.options.pylink = self.ui.checkbox_pylink.isChecked()
		
		self.close()

