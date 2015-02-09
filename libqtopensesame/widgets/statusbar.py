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
from libqtopensesame.misc import _
from libqtopensesame.widgets.base_widget import base_widget

class statusbar(QtGui.QStatusBar, base_widget):

	"""A fancy statusbar with icons"""

	def __init__(self, main_window):

		"""
		Constructor

		Keywords arguments:
		parent -- the parent QWidget
		"""

		super(statusbar, self).__init__(main_window)
		self.initialized = False

	def init(self):

		"""Initialize the statusbar"""

		self.ready_icon = self.experiment.label_image("status_ready")
		self.busy_icon = self.experiment.label_image("status_busy")
		self.message = QtGui.QLabel()
		self.addWidget(self.ready_icon)
		self.addWidget(self.busy_icon)
		self.addWidget(self.message)
		self.initialized = True

	def set_status(self, msg, timeout=5000, status="ready"):

		"""
		Set a statusbar message

		Arguments:
		msg -- the message

		Keywords arguments:
		timeout -- the timeout of the message (default=5000)
		status -- the message status (ready/busy) (default='ready')
		"""

		if not self.initialized:
			self.init()
		if status == "ready":
			self.ready_icon.show()
			self.busy_icon.hide()
			QtGui.QApplication.restoreOverrideCursor()
		else:
			QtGui.QApplication.setOverrideCursor(
				QtGui.QCursor(QtCore.Qt.WaitCursor))			
			self.ready_icon.hide()
			self.busy_icon.show()
		self.message.setText("<small>%s</small>" % msg)		
		if timeout != None:
			QtCore.QTimer.singleShot(timeout, self.clear_status)
		QtGui.QApplication.processEvents()

	def clear_status(self):

		"""Clear the statusbar to a default ready message"""

		self.set_status(_("Ready"), timeout=None)

