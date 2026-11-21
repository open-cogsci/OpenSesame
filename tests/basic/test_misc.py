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
from libopensesame.misc import yes_no_to_bool


class CheckYesNoToBool(unittest.TestCase):

    """
    desc: |
        Checks whether yes/no experiment variables are correctly converted
        to booleans, including legacy Python booleans (True/False) that were
        incorrectly saved by the General tab.
    """
    def runTest(self):

        """
        desc:
            Checks various yes/no variable values.
        """
        for val, expected in [
            (u'yes', True),
            (u'no', False),
            (u'Yes', True),
            (u'NO', False),
            (u'true', True),
            (u'false', False),
            (True, True),
            (False, False),
            (u'True', True),
            (u'False', False),
            (u'1', False),
            (u'0', False),
            (None, False),
            (u'', False),
        ]:
            self.assertEqual(
                yes_no_to_bool(val),
                expected,
                msg=u'%r should convert to %s' % (val, expected)
            )
