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
from qtpy import QtWidgets
from variable_inspector_widget import variable_inspector_widget
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'variable_inspector', category=u'extension')


class variable_inspector_dockwidget(QtWidgets.QDockWidget):

    """
    desc:
            A QDocktWidget that holds the variable inspector.
    """

    def __init__(self, main_window, ext):

        super(variable_inspector_dockwidget, self).__init__(
            _(u'Variable inspector'), main_window)
        self.setWidget(variable_inspector_widget(main_window, ext))
        self.setObjectName(u'variable_inspector')
