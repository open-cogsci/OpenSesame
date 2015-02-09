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
from libopensesame import debug
from libqtopensesame.widgets.base_widget import base_widget

class color_edit(base_widget):

	"""
	desc:
		A colorpicker widget that emulates a QLineEdit.
	"""

	textChanged = QtCore.pyqtSignal('QString')
	textEdited = QtCore.pyqtSignal('QString')

	def __init__(self, main_window):

		"""
		desc:
			Constructor.

		arguments:
			main_window:
				desc:	The main-window object.
				type:	qtopensesame
		"""

		super(color_edit, self).__init__(main_window)
		self.edit = QtGui.QLineEdit()
		self.edit.setSizePolicy(QtGui.QSizePolicy.Minimum,
			QtGui.QSizePolicy.Minimum)
		self.edit.editingFinished.connect(self.apply)
		self.editingFinished = self.edit.editingFinished
		self.button = QtGui.QPushButton()
		self.button.setIconSize(QtCore.QSize(16,16))
		self.button.clicked.connect(self.colorpicker)
		layout = QtGui.QHBoxLayout()
		layout.setContentsMargins(0,0,0,0)
		layout.addWidget(self.edit)
		layout.addWidget(self.button)
		self.setLayout(layout)

	def colorpicker(self):

		"""
		desc:
			Picks a color with the colorpicker dialog.
		"""

		color = self.experiment.colorpicker(self.experiment.sanitize(
			self.text()))
		if color == None:
			return
		self.setText(color)
		self.apply()

	def text(self):

		"""
		desc:
			Gets text (emulate QLineEdit behavior).

		returns:
			desc:	A color text.
			type:	QString
		"""

		return self.edit.text()

	def setText(self, s):

		"""
		dsc:
			Sets text (emulate QLineEdit behavior).

		arguments:
			s:
				desc:	Text.
				type:	unicode
		"""

		self.edit.setText(s)

	def apply(self):

		"""
		desc:
			Emits a 'set_color' signal to indicate that a color has been picked.
		"""

		self.emit(QtCore.SIGNAL(u'set_color'))
		self.textChanged.emit(self.text())
		self.textEdited.emit(self.text())

	def initialize(self, experiment=None, color=None):

		"""
		desc:
			Initializes the widget. This is necessary to apply the theme and
			give the fields initial values.

		keywords:
			experiment:
				desc:	The experiment object or None if it is already available
						via the base_component property.
				type:	[experiment, NoneType]
			color:
				color:	An initial color or None to start with experiment
						foreground.
				type:	[unicode, NoneType]
		"""

		debug.msg(u'color = %s' % color)
		if experiment == None:
			experiment = self.experiment
		if color == None:
			color = experiment.get(u'foreground', _eval=False)
		self.setText(color)
		self.button.setIcon(self.theme.qicon(u'os-color-picker'))
