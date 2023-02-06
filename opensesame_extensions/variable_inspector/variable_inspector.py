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
from libqtopensesame.extensions import base_extension
from libqtopensesame.misc.config import cfg
from variable_inspector_dockwidget import variable_inspector_dockwidget
from qtpy import QtCore, QtGui, QtWidgets
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'variable_inspector', category=u'extension')


class variable_inspector(base_extension):

    r"""A variable inspector."""
    def event_startup(self):
        r"""Initializes the variable inspector dock widget."""
        self.need_refresh = False
        self.dock_widget = variable_inspector_dockwidget(
            self.main_window, self)
        self.dock_widget.visibilityChanged.connect(self.set_visible)
        self.main_window.addDockWidget(
            QtCore.Qt.RightDockWidgetArea,
            self.dock_widget
        )
        self.set_visible(cfg.variable_inspector_visible)
        self.shortcut_focus = QtWidgets.QShortcut(QtGui.QKeySequence(
            cfg.variable_inspector_focus_shortcut), self.main_window,
            self.focus, context=QtCore.Qt.ApplicationShortcut)

    def focus(self):
        r"""Makes the dock visible and sets the focus to the filter box."""
        self.set_visible(True)
        self.dock_widget.widget().focus()

    def open_help(self):
        r"""Opens the help tab."""
        self.tabwidget.open_osdoc('manual/variables')

    def set_visible(self, visible):
        r"""Sets the visibility of the dock widget.

        Parameters
        ----------
        visible : bool
        """
        cfg.variable_inspector_visible = visible
        self.set_checked(visible)
        if visible:
            if self.need_refresh:
                self.dock_widget.widget().refresh()
                self.need_refresh = False
            self.dock_widget.show()
            self.dock_widget.widget().focus()
        else:
            self.dock_widget.hide()

    def activate(self):
        r"""Toggles the visibility of the dock widget."""
        self.set_visible(not cfg.variable_inspector_visible)

    def refresh(self):
        r"""Refreshes the variable inspector."""
        if self.dock_widget.isVisible():
            self.dock_widget.widget().refresh()
            self.need_refresh = False
        else:
            self.need_refresh = True

    # The following events all refresh the variable inspector

    def event_heartbeat(self):
        self.refresh()

    def event_change_item(self, name):
        self.refresh()

    def event_pause_experiment(self):
        self.refresh()

    def event_set_workspace_globals(self, global_dict):
        self.dock_widget.widget().set_workspace_globals(global_dict)
        self.refresh()

    def event_open_experiment(self, path):
        self.dock_widget.widget().set_workspace_globals({})
        self.refresh()
