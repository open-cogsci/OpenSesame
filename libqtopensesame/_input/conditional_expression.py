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
from qtpy.QtWidgets import QLineEdit
from qtpy.QtGui import QColor, QBrush, QPainter, QPen, QFont
from qtpy.QtCore import Qt
from libqtopensesame.misc.base_subcomponent import BaseSubcomponent
from libqtopensesame.misc.translate import translation_context
_ = translation_context('conditional_expression', category='core')


class ConditionalExpression(QLineEdit, BaseSubcomponent):
    """A line-edit widget for conditional expressions. Automatically rewrites
    False and True expressions to be more readable, and adds a color hit.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup(parent)
        self.textChanged.connect(self._set_conditional_expression)
        self._verb = ''
        self._font = QFont('Roboto Condensed')
        self._pen = QPen(QColor('#78909c'))
        self._margin = 16
        self._width = None
        self._flags = Qt.AlignLeft | Qt.AlignVCenter
        self._annotations = {'True': 'Always', 'False': 'Never'}
        
    @property
    def verb(self):
        return self._verb
    
    @verb.setter
    def verb(self, value):
        self._verb = value
        self._annotations = {'True': f'Always {value}',
                             'False': f'Never {value}'}
    
    def _set_conditional_expression(self, cond):
        self.textChanged.disconnect(self._set_conditional_expression)
        fixed_cond = self.experiment.syntax.fix_conditional_expression(cond)
        if cond != fixed_cond:
            self.setText(fixed_cond)
        else:
            clean_cond = cond.strip().lower()
            color = None
            if clean_cond in ('always', 'true'):
                self.setText('True')
                color = 'green'
            elif clean_cond in ('never', 'false'):
                self.setText('False')
            if color is not None:
                self.setStyleSheet(f'color: {color}')
            else:
                self.setStyleSheet(None)
        self.textChanged.connect(self._set_conditional_expression)

    def paintEvent(self, event):
        """Draws annotations to describe the conditional expressions for the
        user.
        """
        super().paintEvent(event)
        painter = QPainter(self)
        data = self.text()
        annotation = self._annotations.get(data, None)
        if annotation is None:
            return
        # The first time that we draw an annotation, we determine how far from
        # the left we need to draw it. This depends on the margin and the size
        # of the text
        event_rect = event.rect()
        if self._width is None:
            rect = painter.boundingRect(event_rect, 0, data)
            self._width = rect.right() + self._margin
        event_rect.setLeft(self._width)
        painter.setFont(self._font)
        painter.setPen(self._pen)
        painter.drawText(event_rect, self._flags, annotation)
