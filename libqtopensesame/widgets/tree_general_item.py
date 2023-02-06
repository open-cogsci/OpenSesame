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
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'tree_general_item', category=u'core')


class TreeGeneralItem(TreeBaseItem):

    r"""Corresponds to the general widget in the overview area."""
    def __init__(self, main_window):
        r"""Constructor.

        Parameters
        ----------
        main_window : qtopensesame
            The main-window object.
        """
        super().__init__()
        self.setup(main_window)
        self.setText(0, safe_decode(self.experiment.var.title))
        self.setIcon(0, self.theme.qicon(u'os-experiment'))
        self.setToolTip(0, _(u'General options'))
        self._droppable = False
        self._draggable = False
        self.name = u'__general__'
        if self.experiment.var.start in self.experiment.items:
            try:
                self.experiment.items[self.experiment.var.start] \
                    .build_item_tree(self)
            except RecursionError:
                from libqtopensesame.widgets.tree_recursion_error_item import (
                    tree_recursion_error_item
                )
                self.addChild(
                    tree_recursion_error_item(self)
                )
            self.child(0).set_draggable(False)
        self.expand()

    def ancestry(self):

        return u'__general__', u'__general__'

    def open_tab(self):

        self.main_window.tabwidget.open_general()


# Alias for backwards compatibility
tree_general_item = TreeGeneralItem
