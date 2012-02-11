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
from libqtopensesame import tip_dialog_ui, cowsay
import random
import os

class tip_dialog(QtGui.QDialog):

	"""
	The tip dialog reads the tips.txt from the resources and
	presents a simple tips dialog.
	"""

	def __init__(self, main_window):
	
		"""
		Constructor
		"""
	
		QtGui.QDialog.__init__(self, main_window)
	
		self.main_window = main_window
		self.ui = tip_dialog_ui.Ui_Dialog()
		self.ui.setupUi(self)
		self.main_window.theme.load_icons(self.ui)
		self.i = 0
		self.ui.checkbox_show_startup_tip.setChecked(self.main_window.show_startup_tip)		
		self.ui.button_next.clicked.connect(self.next_tip)
		self.ui.button_prev.clicked.connect(self.prev_tip)
		self.ui.checkbox_show_startup_tip.stateChanged.connect(self.set_startup_tip)		

		# Set a monospace font with a tab indent of 4 characters
		if os.name == "posix":
			font = QtGui.QFont("mono")
		else:
			font = QtGui.QFont("courier")
		self.ui.textedit_tip.setFont(font)
			
		self.tips = []
		for tip in open(self.main_window.experiment.resource("tips.txt"), "r").read().split("\n\n"):
			tip = tip.strip()
			if tip != "":
				self.tips.append(tip)
		random.shuffle(self.tips)
		
		if len(self.tips) == 0:
			self.tips.append("No tips available.")
		
		self.set_tip()						
		
	def set_startup_tip(self):
	
		"""
		Toggle showing tips on startu[
		"""
	
		self.main_window.show_startup_tip = self.ui.checkbox_show_startup_tip.isChecked()		
		self.main_window.update_preferences_tab()
		
	def set_tip(self):
	
		"""
		Randomly set a tip
		"""
	
		if random.choice( (True, False) ):
			s = cowsay.cowsay(self.tips[self.i], 55)
		else:
			s = cowsay.tuxsay(self.tips[self.i], 55)			
		self.ui.textedit_tip.setPlainText(s)			
		
	def next_tip(self):
	
		"""
		Advance to the next tip
		"""
	
		if self.i >= len(self.tips) - 1:
			self.i = 0
		else:
			self.i += 1
		self.set_tip()
		
	def prev_tip(self):
	
		"""
		Go to the previous tip
		"""
	
		if self.i <= 0:
			self.i = len(self.tips) - 1
		else:
			self.i -= 1
		self.set_tip()
	
		

