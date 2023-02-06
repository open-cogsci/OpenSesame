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
from qtpy import QtGui
from libqtopensesame.misc.base_subcomponent import BaseSubcomponent


class BaseValidator(BaseSubcomponent, QtGui.QValidator):

    """
    desc:
            A base class for input validators.
    """

    def __init__(self, main_window, default):

        self.default = default
        main_window = self.get_main_window(main_window)
        super().__init__(main_window)
        self.setup(main_window)

    def is_valid(self, val):

        return True

    def validate(self, val, pos):

        if self.is_valid(val):
            return self.Acceptable, val, pos
        return self.Intermediate, val, pos

    def fixup(self, val):

        if not self.is_valid(val):
            return self.default
        return val
