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
from openexp._color.color import color
from libopensesame.exceptions import OSException


class CheckColor(unittest.TestCase):

    """
    desc: |
        Checks whether color specifications are correct.
    """
    def runTest(self):

        """
        desc:
            Checks various correct and incorrect color specifications.
        """
        for colorspec, colorref in [
            ('green', '#008000'),
            (255, '#ffffff'),
            ('255', '#ffffff'),
            ('#00FF00', '#00ff00'),
            ('#00ff00', '#00ff00'),
            ('#0F0', '#00ff00'),
            ('#0f0', '#00ff00'),
            ((0, 255, 0), '#00ff00'),
            ('rgb(0,255,0)', '#00ff00'),
            ('rgb( 0 , 255 , 0 )', '#00ff00'),
            ('rgb(0%,100%,0%)', '#00ff00'),
            ('rgb( +0.0% , 100% , -0.0% )', '#00ff00'),
            ('hsl(120,100%,50%)', '#00ff00'),
            ('hsl( +120.0 , 100% , 50% )', '#00ff00'),
            ('hsv(120,100%,100%)', '#00ff00'),
            ('hsv( +120.0 , 100% , 100% )', '#00ff00'),
            ('lab(70, -127, 65)', '#00d412'),
            ('lab(37, -91, 34)', '#006f17'),
            ('lab( +41. , 8 , -59.0 )', '#0062c2'),
        ]:
            if isinstance(colorspec, str) and colorspec.startswith('lab'):
                try:
                    import psychopy
                except ImportError:
                    print('PsychoPy is not installed, skipping CIElab test')
                    continue
            print(
                'Checking correct {} ({}) -> {}'.format(
                    str(colorspec),
                    type(colorspec),
                    colorref
                )
            )
            self.assertEqual(color.to_hex(colorspec), colorref)

        for colorspec in [
            'wihte',
            '#FFFFF',
            '#FFFFG',
            (255, 255, 255.0),
            (255, 255, 255, 255),
            'rgb(255,255)',
            'rgb(255,255,255,255)',
            'rgb(100%,100%,100)',
            'rgb(100 %,100%,100)',
            'hsl(120,100,50)',
            'hsl(- 120,100,50)',
            'hsl(120 .0,100,50)',
            'hsv(120,100,50)',
        ]:
            print(
                'Checking incorrect %s (%s)'
                % (str(colorspec), type(colorspec))
            )
            self.assertRaises(OSException, color.to_hex, colorspec)


if __name__ == '__main__':

    unittest.main()
