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
from libqtopensesame.misc.config import cfg
from libqtopensesame.extensions import base_extension
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'toolbar_menu', category=u'extension')

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

		self.menu = QtWidgets.QMenu()
		for action in self.menubar.actions():
			self.menu.addAction(action)
		self.stretch = QtWidgets.QWidget()
		self.stretch.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
			QtWidgets.QSizePolicy.Expanding)
		self.button = QtWidgets.QPushButton(self.theme.qicon(self.icon()),
			_(u'Menu'))
		self.button.setMenu(self.menu)
		self.button.setIconSize(QtCore.QSize(cfg.toolbar_size,
			cfg.toolbar_size))
		self.button.setFlat(True)
		self.toolbar.addWidget(self.stretch)
		self.menu_action = self.toolbar.addWidget(self.button)
		if cfg.toolbar_menu_active:
			self.activate_toolbar_menu()
			self.set_checked(True)
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
		self.menu_action.setVisible(True)
		self.stretch.setVisible(True)

	def deactivate_toolbar_menu(self):

		"""
		desc:
			Show the menu bar and hide the toolbar widget.
		"""

		cfg.toolbar_menu_active = False
		self.menubar.setVisible(True)
		self.menu_action.setVisible(False)
		self.stretch.setVisible(False)
