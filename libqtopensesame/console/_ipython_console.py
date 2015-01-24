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
from IPython.qt.console.rich_ipython_widget import IPythonWidget
from IPython.qt.inprocess import QtInProcessKernelManager
from libqtopensesame.console._base_console import base_console

class ipython_console(base_console, QtGui.QWidget):

	"""
	desc:
		An IPython-based debug window.
	"""

	def __init__(self, main_window):

		"""
		desc:
			Constructor.

		arguments:
			main_window:	The main window object.
		"""

		super(ipython_console, self).__init__(main_window)
		kernel_manager = QtInProcessKernelManager()
		kernel_manager.start_kernel()
		self.kernel = kernel_manager.kernel
		self.kernel.gui = 'qt4'
		kernel_client = kernel_manager.client()
		kernel_client.start_channels()
		self.control = IPythonWidget()
		self.control.kernel_manager = kernel_manager
		self.control.kernel_client = kernel_client
		self.verticalLayout = QtGui.QVBoxLayout(self)
		self.verticalLayout.setContentsMargins(0,0,0,0)
		self.setLayout(self.verticalLayout)
		self.verticalLayout.addWidget(self.control)

	def clear(self):

		"""See base_console."""

		self.control.reset(clear=True)

	def focus(self):

		"""See base_console."""

		self.control._control.setFocus()

	def show_prompt(self):

		"""See base_console."""

		self.control._show_interpreter_prompt()

	def write(self, s):

		"""See base_console."""

		self.control._append_plain_text(str(s))

	def set_workspace_globals(self, _globals={}):

		"""See base_console."""

		self.kernel.shell.push(_globals)

	def setup(self, main_window):

		"""See base_subcomponent."""

		super(ipython_console, self).setup(main_window)
		self.kernel.shell.push(self.default_globals())
