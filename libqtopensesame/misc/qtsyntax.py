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
from libopensesame.syntax import Syntax
import re

FIX_CURLY_BRACES = re.compile(r'\{([a-zA-Z_][a-zA-Z0-9_]*)\}')


class QtSyntax(Syntax):

    def eval_text(self, txt, round_float=False):
        return txt
    
    def fix_conditional_expression(self, cond):
        return FIX_CURLY_BRACES.sub(r'\1', cond)
    

# Alias for backwards compatibility
qtsyntax = QtSyntax
