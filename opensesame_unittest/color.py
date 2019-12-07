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
from openexp._color.color import color
from libopensesame.exceptions import osexception


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
			(u'green', u'#008000'),
			(255, u'#ffffff'),
			(u'#00FF00', u'#00ff00'),
			(u'#00ff00', u'#00ff00'),
			(u'#0F0', u'#00ff00'),
			(u'#0F0', u'#00ff00'),
			((0, 255, 0), u'#00ff00'),
			(u'rgb(0,255,0)', u'#00ff00'),
			(u'rgb( 0 , 255 , 0 )', u'#00ff00'),
			(u'rgb(0%,100%,0%)', u'#00ff00'),
			(u'rgb( 0% , 100% , 0% )', u'#00ff00'),
			(u'hsl(120,100%,50%)', u'#00ff00'),
			(u'hsl( 120 , 100% , 50% )', u'#00ff00'),
			(u'hsv(120,100%,100%)', u'#00ff00'),
			(u'hsv( 120 , 100% , 100% )', u'#00ff00'),
			(u'lab(53,-20,0)', '#163e35'),
			(u'lab( 53 , -20 , 0 )', '#163e35')
		]:
			print(
				u'Checking correct {} ({}) -> {}'.format(
					str(colorspec),
					type(colorspec),
					colorref
				)
			)
			self.assertEqual(color.to_hex(colorspec), colorref)

		for colorspec in [
			u'wihte',
			u'#FFFFF',
			u'#FFFFG',
			(255, 255, 255.0),
			(255, 255, 255, 255),
			255.0,
			u'rgb(255,255)',
			u'rgb(255,255,255,255)',
			u'rgb(100%,100%,100)',
			u'hsl(120,100,50)',
			u'hsv(120,100,50)'
		]:
			print(
				u'Checking incorrect %s (%s)'
				% (str(colorspec), type(colorspec))
			)
			self.assertRaises(osexception, color.to_hex, colorspec)


if __name__ == '__main__':

	unittest.main()
