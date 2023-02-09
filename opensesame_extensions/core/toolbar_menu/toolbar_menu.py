# -*- coding:utf-8 -*-

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
from libopensesame.oslogging import oslogger
from libqtopensesame.extensions import BaseExtension
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'toolbar_menu', category=u'extension')


class ToolbarMenu(BaseExtension):

    r"""Integrates the menu into the toolbar."""
    def event_startup(self):

        self._menu = None
        if not cfg.toolbar_menu_active:
            return
        cfg.toolbar_menu_active = False  # It will be toggled!
        self.activate()
        self.set_checked(True)

    def activate(self):
        r"""Toggle the menubar integration."""
        if self._menu is None:
            self._init_menu()
        if cfg.toolbar_menu_active:
            self._deactivate_toolbar_menu()
        else:
            self._activate_toolbar_menu()

    def _init_menu(self):
        r"""Creates a widget with a menu that copies all actions from the main
        menu bar.
        """
        self._menu = QtWidgets.QMenu()
        for action in self.menubar.actions():
            self._menu.addAction(action)
        self.stretch = QtWidgets.QWidget()
        self.stretch.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        self.button = QtWidgets.QPushButton(
            self.theme.qicon(self.icon()),
            _(u'Menu')
        )
        self.button.setMenu(self._menu)
        self.button.setIconSize(
            QtCore.QSize(cfg.toolbar_size, cfg.toolbar_size)
        )
        self.button.setFlat(True)
        self.toolbar.addWidget(self.stretch)
        self.menu_action = self.toolbar.addWidget(self.button)

    def _keep_toolbar_visible(self, visible):

        if visible:
            return
        oslogger.debug('keep toolbar visible')
        self.toolbar.setVisible(True)

    def _activate_toolbar_menu(self):
        r"""Hide the menu bar and show the toolbar widget."""
        cfg.toolbar_menu_active = True
        self.menubar.setVisible(False)
        self.menu_action.setVisible(True)
        self.stretch.setVisible(True)
        if not self.toolbar.isVisible():
            self.toolbar.setVisible(True)
        self.toolbar.visibilityChanged.connect(self._keep_toolbar_visible)

    def _deactivate_toolbar_menu(self):
        r"""Show the menu bar and hide the toolbar widget."""
        cfg.toolbar_menu_active = False
        self.menubar.setVisible(True)
        self.menu_action.setVisible(False)
        self.stretch.setVisible(False)
        self.toolbar.visibilityChanged.disconnect()
