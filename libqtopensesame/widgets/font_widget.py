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

from PyQt4 import QtCore, QtGui
from libqtopensesame.ui import font_widget_ui

class font_widget(QtGui.QWidget):

	"""A font selection widget"""
	
	max_size = 64

	def __init__(self, parent=None):
	
		"""
		Constructor
		
		Arguments:
		experiment -- the experiment
		
		Keywords arguments:
		parent -- the parent QWidget (default=None)		
		"""
	
		QtGui.QWidget.__init__(self, parent)
		self.ui = font_widget_ui.Ui_font_widget()
		self.ui.setupUi(self)		
				
	def _apply(self):
	
		"""Apply the controls"""
	
		self.family = self.ui.combobox_family.currentText()
		self.size = self.ui.spinbox_size.value()
		self.italic = self.ui.checkbox_italic.isChecked()
		self.bold = self.ui.checkbox_bold.isChecked()
		self.ui.label_example.setFont(self.get_font())
		self.emit(QtCore.SIGNAL("font_changed"))
		
	def apply_family(self):
	
		"""
		Apply the controls and optionally present a full font selection dialog
		if the user has selected 'other ...'
		"""
	
		if self.ui.combobox_family.currentText() == 'other ...':
			font, ok = QtGui.QFontDialog.getFont(self.get_font())
			if ok:
				self.family = str(font.family())
				self.update_family_combobox()
		self._apply()
		
	def get_font(self):
	
		"""
		Make a QFont based on the settings
		
		Returns:
		A QFont
		"""

		if self.bold:
			weight = QtGui.QFont.Bold
		else:
			weight = QtGui.QFont.Normal	
		return QtGui.QFont(self.family, min(self.max_size, self.size), weight, \
			self.italic)		
		
	def initialize(self, experiment, family=None, italic=None, bold=None, \
		size=None):
		
		"""
		Initialize the widget
		
		Arguments:
		experiment -- an opensesame experiment
		
		Keyword arguments:
		family -- the font family or None to use experiment default
				  (default=None)
		italic -- the font italic state or None to use experiment default
				  (default=None)
		bold -- the font bold state or None to use experiment default
				(default=None)
		size -- the font size or None to use experiment default
				  (default=None)
		"""
	
		self.experiment = experiment
		if family == None:
			self.family = self.experiment.get('font_family')
		else:
			self.family = family
		if italic == None:
			self.italic = self.experiment.get('font_italic') == 'yes'		
		else:
			self.italic = italic
		if bold == None:
			self.bold = self.experiment.get('font_bold') == 'yes'
		else:
			self.bold = bold
		if size == None:
			self.size = self.experiment.get('font_size')
		else:
			self.size = size						
		self.ui.combobox_family.setCurrentIndex( \
			self.ui.combobox_family.findText(self.family))
		self.ui.checkbox_italic.setChecked(self.italic)
		self.ui.checkbox_bold.setChecked(self.bold)
		self.ui.spinbox_size.setValue(self.size)
		self._apply()
		self.ui.combobox_family.currentIndexChanged.connect( \
			self.apply_family)
		self.ui.checkbox_italic.toggled.connect(self._apply)
		self.ui.checkbox_bold.toggled.connect(self._apply)
		self.ui.spinbox_size.valueChanged.connect(self._apply)		
						
	def update_family_combobox(self):
	
		"""Update the family combobox to include a custom font"""

		self.ui.combobox_family.currentIndexChanged.disconnect()
		self.ui.combobox_family.clear()	
		l = ['mono', 'sans', 'serif', 'other ...']
		if self.family not in l:
			l += [self.family]
		self.ui.combobox_family.insertItems(0, l)
		self.ui.combobox_family.setCurrentIndex( \
			self.ui.combobox_family.findText(self.family))
		self.ui.combobox_family.currentIndexChanged.connect( \
			self.apply_family)		
						
			
