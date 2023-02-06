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
from qtpy import QtCore, QtGui, QtWidgets


class variable_inspector_cell(QtWidgets.QTableWidgetItem):

    """
    desc:
            A cell for the variable-inspector table.
    """

    def __init__(self, text, info):
        """
        desc:
                Constructor.

        arguments:
                text:
                        desc:	The cell text.
                        type:	str
                info:
                        desc:	Variable info as returned by var_store.inspect().
                        type:	dict
        """

        a = QtCore.Qt.AlignLeft
        f = QtGui.QFont()
        if info[u'alive']:
            f.setBold(True)
        if not isinstance(text, str):
            try:
                len(text)
            except TypeError:
                if text is None:
                    text = u''
                elif isinstance(text, int) or isinstance(text, float):
                    text = str(text)
                    a = QtCore.Qt.AlignRight
                else:
                    text = safe_decode(text, errors=u'ignore')
            else:
                text = u','.join([safe_decode(s) for s in text])
        QtWidgets.QTableWidgetItem.__init__(self, text)
        self.setFont(f)
        self.setTextAlignment(a)
