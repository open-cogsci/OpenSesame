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
from libqtopensesame.misc.base_subcomponent import BaseSubcomponent
from qtpy import QtWidgets


class BaseWidget(QtWidgets.QWidget, BaseSubcomponent):
    r"""A base class for widgets.

    Parameters
    -----------
    main_window : QtOpenSesame
    ui : str, optional
        An id for a user-interface file, for example 'dialogs.quick_switcher'.
    *arglist:
        passed onto parent constructors.
    *kwdict:
        passed onto parent constructors.
    """
    
    def __init__(self, parent, ui=None, *arglist, **kwdict):
        super().__init__(parent, *arglist, **kwdict)
        self.setup(parent, ui=ui)


# Alias for backwards compatibility
base_widget = BaseWidget
