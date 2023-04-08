"""This file is part of OpenSesame.

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
from qtpy.QtWidgets import QStyledItemDelegate
from qtpy.QtGui import QColor, QFont, QPen
from qtpy.QtCore import Qt


class RunIfDelegate(QStyledItemDelegate):
    """Adds a comment next to run-if statements in the overview area to
    clarify that True means always run and False means never run.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self._font = QFont('Roboto Condensed')
        self._pen = QPen(QColor('#78909c'))
        self._margin = 48
        self._width = None
        self._flags = Qt.AlignLeft | Qt.AlignVCenter
    
    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        data = index.data()
        if data not in ('True', 'False'):
            return
        # The first time that we draw an annotation, we determine how far from
        # the left we need to draw it. This depends on the margin and the size
        # of the text
        if self._width is None:
            rect = painter.boundingRect(option.rect, 0, data)
            self._width = rect.right() + self._margin
        option.rect.setLeft(self._width)
        painter.setFont(self._font)
        painter.setPen(self._pen)
        painter.drawText(
            option.rect, self._flags,
            'Always run' if data == 'True' else 'Never run')
