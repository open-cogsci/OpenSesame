#!/usr/bin/env python
#-*- coding:utf-8 -*-

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
import unittest
from libopensesame.py3compat import *
from libqtopensesame.items.inline_script import InlineScript


test_script = '''

def fnc():
    global d
    d = 1
    x = 1

a = 1
var.b = 1
while True:
    c = 1
for i in range(10):
    e = 1
'''


class CheckInlineScript(unittest.TestCase):
    
    def runTest(self):
        assignments = InlineScript._extract_assignments(test_script)
        assert sorted(assignments) == ['a', 'b', 'c', 'd', 'e']
