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
from PyQt4 import QtGui
from libqtopensesame.misc.base_subcomponent import base_subcomponent
from libqtopensesame.misc import _

class confirmation(QtGui.QMessageBox, base_subcomponent):

	"""
	desc:
		A simple yes/ confirmation dialog.
	"""

	def __init__(self, main_window, msg):

		"""
		desc:
			Constructor.

		arguments:
			main_window:
				desc:	The main-window object.
				type:	QWidget
			msg:
				desc:	The message.
				type:	[unicode, str]
		"""

		QtGui.QMessageBox.__init__(self, main_window)
		self.setup(main_window)
		self.yes = self.addButton(QtGui.QMessageBox.Yes)
		self.no = self.addButton(QtGui.QMessageBox.No)
		self.setDefaultButton(QtGui.QMessageBox.No)
		self.setWindowTitle(_(u'Please confirm'))
		self.setText(msg)

	def show(self):

		"""
		desc:
			Shows the confirmation dialog.

		returns:
			desc:	True if confirmed, False otherwise.
			type:	bool
		"""

		self.exec_()
		return self.clickedButton() == self.yes
