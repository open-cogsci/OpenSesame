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
from qtpy.QtGui import QColor, QBrush
from libqtopensesame.misc.base_subcomponent import BaseSubcomponent
from libqtopensesame.misc.translate import translation_context
_ = translation_context('conditional_expression', category='core')


class ConditionalExpression(QLineEdit, BaseSubcomponent):
    """A line-edit widget for conditional expressions. Automatically rewrites
    False and True expressions to be more readable, and adds a color hit.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.textChanged.connect(self._set_conditional_expression)
        self.verb = ''
    
    def _set_conditional_expression(self, cond):
        self.textChanged.disconnect(self._set_conditional_expression)
        print('setting text')
        clean_cond = cond.strip().lower()
        color = None
        if clean_cond in ('always', '', 'true'):
            self.setText('True  # always' + self.verb)
            color = 'green'
        elif clean_cond in ('never', 'false'):
            self.setText('False  # never' + self.verb)
        if color is not None:
            self.setStyleSheet(f'color: {color}')
        else:
            self.setStyleSheet(None)
        self.textChanged.connect(self._set_conditional_expression)
