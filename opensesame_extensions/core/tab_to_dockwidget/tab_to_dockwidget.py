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
from libqtopensesame.extensions import BaseExtension
from .tab_to_dockwidget_docktab import DockTab
from qtpy import QtCore


class TabToDockwidget(BaseExtension):

    r"""This extensions turns tabs into standalone dockwidgets, so that you can
    see multiple things side by side.
    """
    def event_startup(self):
        r"""During initialization we monkey-patch the tabwidget so that it also
        manages dockwidgets.
        """
        self._docktabs = {}
        self.overview_area.structure_change.connect(self.update_all)
        self.tabwidget.add = self._add_tab(self.tabwidget.add)
        self.tabwidget.remove = self._remove_tab(self.tabwidget.remove)
        self.tabwidget.close_all = self._close_all_tabs(
            self.tabwidget.close_all)

    def event_run_experiment(self, fullscreen):
        r"""Disable all docked item controls when running the experiment."""
        for docktab in self._docktabs.values():
            docktab.setEnabled(False)

    def event_end_experiment(self, ret_val):
        r"""Re-enable all docked item controls when the experiment is done."""
        for docktab in self._docktabs.values():
            docktab.setEnabled(True)

    def update_all(self):
        r"""Update all item controls."""
        for docktab in self._docktabs.values():
            docktab.update()

    def event_rename_item(self, from_name, to_name):
        r"""Change the dockwidget titles on item rename, and allow items to
        update in response to renames.
        """
        for docktab in self._docktabs.values():
            docktab.rename(from_name, to_name)

    def event_new_item(self, name, _type):
        r"""Allow items to update in response to new items."""
        self.update_all()

    def event_delete_item(self, name):
        r"""Allow items to update in response to item deletions."""
        for docktab in self._docktabs.values():
            docktab.delete(name)

    def provide_item_in_dockwidget(self, name):
        r"""Checks whether an item (by name) is currently shown as a
        dockwidget.
        """
        if name not in self.item_store:
            return False
        return self.item_store[name].widget() in self._docktabs

    def activate(self):
        r"""Turns the currently visible tab (if any) into a dockwidget."""
        widget = self.tabwidget.currentWidget()
        if widget is None:
            return
        name = self.tabwidget.tabText(self.tabwidget.currentIndex())
        self.tabwidget.remove(widget)
        docktab = DockTab(self, widget, name)
        self._docktabs[widget] = docktab
        self.main_window.addDockWidget(QtCore.Qt.RightDockWidgetArea, docktab)

    def remove_widget(self, widget):
        r"""Removes a docked widget."""
        if widget in self._docktabs:
            del self._docktabs[widget]

    def _close_all_tabs(self, fnc):
        r"""Decorates tabwidget.close_all()"""
        def inner(*args, **kwargs):

            while self._docktabs:
                widget, docktab = self._docktabs.popitem()
                docktab.close()
            return fnc(*args, **kwargs)

        return inner

    def _add_tab(self, fnc):
        r"""Decorates tabwidget.add()"""
        def inner(widget, *args, **kwargs):

            if widget in self._docktabs:
                if hasattr(widget, u'set_focus'):
                    widget.set_focus()
                return
            return fnc(widget, *args, **kwargs)

        return inner

    def _remove_tab(self, fnc):
        r"""Decorates tabwidget.remove()"""
        def inner(widget, *args, **kwargs):

            if widget in self._docktabs:
                docktab = self._docktabs.pop(widget)
                docktab.close()
                return
            return fnc(widget, *args, **kwargs)

        return inner
