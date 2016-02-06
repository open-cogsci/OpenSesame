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

from libopensesame.py3compat import *

from qtpy import QtCore, QtWidgets
from libqtopensesame.dialogs.base_dialog import base_dialog
from libqtopensesame.widgets import sketchpad_widget

class sketchpad_dialog(base_dialog):

	"""
	desc:
		The pop-out version of the sketchpad_widget.
	"""

	def __init__(self, main_window, sketchpad):

		"""
		desc:
			Constructor.

		arguments:
			main_window:	A qtopensesame object.
			sketchpad:		A sketchpad object.
		"""

		super(sketchpad_dialog, self).__init__(main_window, flags= \
			QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCloseButtonHint)
		self.sketchpad = sketchpad
		self.tools_widget = sketchpad_widget.sketchpad_widget(self.sketchpad,
			parent=self, embed=False)
		self.close_button = QtWidgets.QPushButton(self.theme.qicon(u"close"),
			u"Close")
		self.close_button.setIconSize(QtCore.QSize(16,16))
		self.close_button.clicked.connect(self.accept)
		self.hbox = QtWidgets.QHBoxLayout()
		self.hbox.addStretch()
		self.hbox.addWidget(self.close_button)
		self.hbox.setContentsMargins(0, 0, 0, 0)
		self.hbox_widget = QtWidgets.QWidget()
		self.hbox_widget.setLayout(self.hbox)
		self.vbox = QtWidgets.QVBoxLayout()
		self.vbox.addWidget(self.tools_widget)
		self.vbox.addWidget(self.hbox_widget)
		self.setLayout(self.vbox)
