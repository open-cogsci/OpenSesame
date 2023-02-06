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
from libqtopensesame.misc.base_subcomponent import BaseSubcomponent
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'item_category', category=u'core')


class ToolbarItemsLabel(BaseSubcomponent, QtWidgets.QFrame):

    r"""A label for the item toolbar."""
    def __init__(self, parent, label):
        r"""Constructor

        Parameters
        ----------
        parent : QWidget
            The parent.
        label : unicode
            Label text.
        """
        super().__init__(parent)
        self.setup(parent)
        l = QtWidgets.QLabel(_(label))
        l.setMaximumWidth(90)
        l.setIndent(6)
        l.setWordWrap(True)
        hbox = QtWidgets.QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(l)
        self.setLayout(hbox)


# Alias for backwards compatibility
toolbar_items_label = ToolbarItemsLabel
