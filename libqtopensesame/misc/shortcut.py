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
from qtpy import QtGui, QtCore, QtWidgets
from qtpy.QtWidgets import QShortcut
from qtpy.QtCore import Qt
from qtpy.QtGui import QKeySequence


class Shortcut(QShortcut):

    def __init__(self, parent, key_sequence, target,
                 _global=False):
        if _global:
            context = Qt.ApplicationShortcut
        else:
            context = Qt.WidgetWithChildrenShortcut
        super().__init__(QKeySequence(key_sequence), parent, target,
                         context=context)


# Alias for backwards compatibility
shortcut = Shortcut
