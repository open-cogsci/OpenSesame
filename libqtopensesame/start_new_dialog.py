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
from libqtopensesame import start_new_dialog_ui, cowsay
import random
import os

class start_new_dialog(QtGui.QDialog):

	"""Start new dialog presented when starting with a clean experiment"""

	def __init__(self, main_window):
	
		"""
		Constructor

		Arguments:
		main_window -- a the main ui
		"""
	
		QtGui.QDialog.__init__(self, main_window)
	
		self.main_window = main_window
		self.ui = start_new_dialog_ui.Ui_Dialog()
		self.ui.setupUi(self)

		templates = ("default.opensesame", "Default template"), ("extended_template.opensesame", "Extended template")

		for f in self.main_window.recent_files:
			item = QtGui.QListWidgetItem(self.ui.list_recent)
			item.setText(os.path.basename(f))
			item.file = f
			item.setIcon(self.main_window.experiment.icon("experiment"))

		for f in templates:
			item = QtGui.QListWidgetItem(self.ui.list_templates)
			item.setText(f[1])
			item.file = self.main_window.experiment.resource(f[0])
			item.setIcon(self.main_window.experiment.icon("wizard"))
			self.ui.list_templates.addItem(item)

		self.ui.list_recent.setCurrentRow(0)
		self.ui.list_templates.setCurrentRow(0)

		self.ui.list_recent.itemDoubleClicked.connect(self.open_recent)
		self.ui.list_templates.itemDoubleClicked.connect(self.open_template)		
		self.ui.button_template.clicked.connect(self.open_template)
		self.ui.button_recent.clicked.connect(self.open_recent)
		self.ui.button_browse.clicked.connect(self.browse)

	def open_template(self):

		"""Open the selected template"""

		self.main_window.open_file(path = self.ui.list_templates.currentItem().file, add_to_recent = False)
		self.close()
		
	def open_recent(self):

		"""Open the selected file"""

		item = self.ui.list_recent.currentItem()
		if item == None:
			self.browse()
		else:
			self.main_window.open_file(path = self.ui.list_recent.currentItem().file)
		self.close()

	def browse(self):

		"""Browse for an experiment file"""

		self.main_window.open_file()
		self.close()

