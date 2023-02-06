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
from qtpy import QtWidgets, QtCore
from libqtopensesame.misc.base_subcomponent import BaseSubcomponent
from libqtopensesame.widgets import pool_widget
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'pool_select', category=u'core')


class PoolSelect(QtWidgets.QWidget, BaseSubcomponent):

    r"""A widget that implements a file-pool selector. Partly emulates the
    QLineEdit API.
    """
    editingFinished = QtCore.Signal()
    textEdited = QtCore.Signal()

    def __init__(self, main_window):

        QtWidgets.QComboBox.__init__(self, main_window)
        self.setup(main_window)
        self.edit = QtWidgets.QLineEdit()
        self.edit.editingFinished.connect(self.editingFinished.emit)
        self.edit.textEdited.connect(self.textEdited.emit)
        self.edit.setMinimumWidth(200)
        self.button = QtWidgets.QPushButton(
            self.theme.qicon(u'browse'),
            _(u'Browse')
        )
        self.button.setIconSize(QtCore.QSize(16, 16))
        self.button.clicked.connect(self.browse)
        self.hbox = QtWidgets.QHBoxLayout(self)
        self.hbox.addWidget(self.edit)
        self.hbox.addWidget(self.button)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(6)
        self.setLayout(self.hbox)

    def text(self):

        return self.edit.text()

    def setText(self, value):

        return self.edit.setText(value)

    def browse(self):

        s = pool_widget.select_from_pool(self.main_window)
        if not s:
            return
        self.edit.setText(s)
        self.editingFinished.emit()


# Alias for backwards compatibility
pool_select = PoolSelect
