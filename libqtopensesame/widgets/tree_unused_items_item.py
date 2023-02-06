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
from libqtopensesame.widgets.tree_base_item import TreeBaseItem
from libqtopensesame.misc import drag_and_drop
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'tree_unused_items_item', category=u'core')


class TreeUnusedItemsItem(TreeBaseItem):

    r"""Corresponds to the unused-items widget in the overview area."""
    def __init__(self, main_window):
        r"""Constructor.

        Parameters
        ----------
        main_window : qtopensesame
            The main-window object.
        """
        super().__init__()
        self.setup(main_window)
        self.setIcon(0, self.theme.qicon(u'unused'))
        self.setToolTip(0, _(u'Unused items'))
        self._droppable = True
        self._draggable = False
        self.name = u'__unused__'
        i = 0
        for item_name in self.experiment.items.unused():
            self.experiment.items[item_name].build_item_tree(self, max_depth=1)
            i += 1
        self.setText(0, _(u'Unused items') + u' (%s)' % i)

    def droppable(self, data):

        return drag_and_drop.matches(data, [u'item-existing']) and \
            data[u'application-id'] == self.main_window._id()

    def drop_hint(self):

        return _(u'Move to unused items')

    def open_tab(self):

        self.main_window.tabwidget.open_unused()

    def ancestry(self):

        return u'__unused__', u'__unused__:0'

    def show_context_menu(self, pos):

        from libqtopensesame.widgets.unused_items_context_menu import \
            UnusedItemsContextMenu
        menu = UnusedItemsContextMenu(self.main_window, self)
        menu.popup(pos)


# Alias for backwards compatibility
tree_unused_items_item = TreeUnusedItemsItem
