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
			(u'255', u'#ffffff'),
			(u'#00FF00', u'#00ff00'),
			(u'#00ff00', u'#00ff00'),
			(u'#0F0', u'#00ff00'),
			(u'#0f0', u'#00ff00'),
			((0, 255, 0), u'#00ff00'),
			(u'rgb(0,255,0)', u'#00ff00'),
			(u'rgb( 0 , 255 , 0 )', u'#00ff00'),
			(u'rgb(0%,100%,0%)', u'#00ff00'),
			(u'rgb( +0.0% , 100% , -0.0% )', u'#00ff00'),
			(u'hsl(120,100%,50%)', u'#00ff00'),
			(u'hsl( +120.0 , 100% , 50% )', u'#00ff00'),
			(u'hsv(120,100%,100%)', u'#00ff00'),
			(u'hsv( +120.0 , 100% , 100% )', u'#00ff00'),
			(u'lab(70, -127, 65)', u'#00d412'),
			(u'lab(37, -91, 34)', u'#006f17'),
			(u'lab( +41. , 8 , -59.0 )', u'#0062c2'),
		]:
			if isinstance(colorspec, str) and colorspec.startswith('lab'):
				try:
					import psychopy
				except ImportError:
					print('PsychoPy is not installed, skipping CIElab test')
					continue
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
			u'rgb(100 %,100%,100)',
			u'hsl(120,100,50)',
			u'hsl(- 120,100,50)',
			u'hsl(120 .0,100,50)',
			u'hsv(120,100,50)',
		]:
			print(
				u'Checking incorrect %s (%s)'
				% (str(colorspec), type(colorspec))
			)
			self.assertRaises(osexception, color.to_hex, colorspec)


if __name__ == '__main__':

	unittest.main()
