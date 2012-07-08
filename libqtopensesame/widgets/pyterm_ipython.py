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

import sys
from IPython.frontend.qt.console.ipython_widget import IPythonWidget
from IPython.frontend.qt.kernelmanager import QtKernelManager
from IPython.utils.localinterfaces import LOCALHOST
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtGui

class output_buffer:

	"""Used to capture the standard output and reroute it to the debug window"""

	def __init__(self, console):

		"""
		Constructor

		Keyword arguments:
		console -- a console widget
		"""

		self.console = console

	def write(self, s):

		"""
		Write a string

		Arguments:
		s -- a string
		"""

		self.console.console._append_plain_text(s)

class console(QWidget):

	"""A QWidget that serves as a debug window"""

	def __init__(self, parent=None):

		QDialog.__init__(self, parent)

		self.main_window = parent
		self.kernel_manager = QtKernelManager()
		self.kernel_manager.start_kernel()
		self.kernel_manager.start_channels()
		self.console = IPythonWidget(local_kernel=LOCALHOST)
		self.console.kernel_manager = self.kernel_manager
		self.verticalLayout = QVBoxLayout(self)
		self.verticalLayout.setContentsMargins(0,0,0,0)
		self.setLayout(self.verticalLayout)
		self.verticalLayout.addWidget(self.console)

	def setReadOnly(self, state):

		"""
		Dummy function

		Arguments:
		state -- dummy argument
		"""

		pass

	def clear(self):

		"""Clears the console"""

		self.console.reset()

	def show_prompt(self):

		"""Shows a new prompt"""

		self.console._show_interpreter_prompt()
