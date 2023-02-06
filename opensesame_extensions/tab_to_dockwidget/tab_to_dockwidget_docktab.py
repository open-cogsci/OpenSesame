# coding=utf-8

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
from qtpy.QtWidgets import QDockWidget
from libqtopensesame.items.qtitem import qtitem


class DockTab(QDockWidget):

    r"""A dockwidget that holds a tab."""
    def __init__(self, tab_to_dockwidget, widget, name):

        QDockWidget.__init__(self, name, tab_to_dockwidget.main_window)
        self._tab_to_dockwidget = tab_to_dockwidget
        self.setWidget(widget)
        self.setObjectName(str(widget))
        if hasattr(widget, u'__item__'):
            self._item = tab_to_dockwidget.experiment.items[widget.__item__]
        else:
            self._item = None

    def update(self):

        if self._item is None:
            return
        self._item.update_script()
        self._item.edit_widget()

    def closeEvent(self, event):

        self._tab_to_dockwidget.remove_widget(self.widget())

    def rename(self, from_name, to_name):

        if self._item is None:
            return
        if self._item.name == to_name:
            self.setWindowTitle(to_name)
        self._item.rename(from_name, to_name)
        self.update()

    def delete(self, name):

        if self._item is None:
            return
        self._item.delete(name)
        self.update()
