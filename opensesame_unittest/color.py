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

class check_color(unittest.TestCase):

	"""
	desc: |
		Checks whether color specifications are correct.
	"""

	def runTest(self):

		"""
		desc:
			Checks various correct and incorrect color specifications.
		"""

		for colorspec in [
			u'white',
			u'#FFFFFF',
			u'#ffffff',
			u'#FFF',
			u'#fff',
			(255, 255, 255),
			255,
			u'rgb(255,255,255)',
			u'rgb( 255 , 255 , 255 )',
			u'rgb(100%,100%,100%)',
			u'rgb( 100% , 100% , 100% )',
			]:
			print(u'Checking correct %s (%s)' % (str(colorspec), type(colorspec)))
			self.assertEqual(u'#ffffff', color.to_hex(colorspec))

		for colorspec in [
			u'wihte',
			u'#FFFFF',
			u'#FFFFG',
			(255,255,255.0),
			(255, 255, 255, 255),
			255.0,
			u'rgb(255,255)',
			u'rgb(255,255,255,255)',
			u'rgb(100%,100%,100)',
			]:
			print(u'Checking incorrect %s (%s)' \
				% (str(colorspec), type(colorspec)))
			self.assertRaises(osexception, color.to_hex, colorspec)

if __name__ == '__main__':
	unittest.main()
