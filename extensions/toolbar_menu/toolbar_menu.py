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
from libqtopensesame.misc.config import cfg
from libqtopensesame.extensions import base_extension

class toolbar_menu(base_extension):

	"""
	desc:
		Integrates the menu into the toolbar.
	"""

	def event_startup(self):

		"""
		desc:
			On startup, a widget is created with a menu that copies all actions
			from the main menu bar.
		"""

		self.menu = QtGui.QMenu()
		for action in self.menubar.actions():
			self.menu.addAction(action)
		self.stretch = QtGui.QWidget()
		self.stretch.setSizePolicy(QtGui.QSizePolicy.Expanding,
			QtGui.QSizePolicy.Expanding)
		self.button = QtGui.QPushButton(self.theme.qicon(self.icon()),
			_(u'Menu'))
		self.button.setMenu(self.menu)
		self.button.setIconSize(QtCore.QSize(cfg.toolbar_size,
			cfg.toolbar_size))
		self.button.setFlat(True)
		self.toolbar.addWidget(self.stretch)
		self.action = self.toolbar.addWidget(self.button)
		if cfg.toolbar_menu_active:
			self.activate_toolbar_menu()
		else:
			self.deactivate_toolbar_menu()
	
	def activate(self):

		"""
		desc:
			Toggle the menubar integration.
		"""

		if cfg.toolbar_menu_active:
			self.deactivate_toolbar_menu()
		else:
			self.activate_toolbar_menu()

	def activate_toolbar_menu(self):

		"""
		desc:
			Hide the menu bar and show the toolbar widget.
		"""

		cfg.toolbar_menu_active = True
		self.menubar.setVisible(False)
		self.action.setVisible(True)
		self.stretch.setVisible(True)

	def deactivate_toolbar_menu(self):

		"""
		desc:
			Show the menu bar and hide the toolbar widget.
		"""

		cfg.toolbar_menu_active = False
		self.menubar.setVisible(True)
		self.action.setVisible(False)
		self.stretch.setVisible(False)
