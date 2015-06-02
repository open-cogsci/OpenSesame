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

import os
import yamldoc
import unittest
from libopensesame.py3compat import *

class check_parsing(unittest.TestCase):

	"""
	desc:
		Checks whether all examples can be parsed.
	"""

	@yamldoc.validate
	def checkExample(self, expPath):

		"""
		desc:
			Checks whether a given experiment can be parsed.

		arguments:
			expPath:
				desc:	A path to an experiment
				type:	[unicode, str]
		"""

		# Quest is not Python 3 compatible
		if py3 and u'quest' in expPath:
			return
		print(u'Checking %s ...' % expPath)
		from libopensesame.experiment import experiment
		experiment(u'dummy', expPath, experiment_path=os.path.dirname(expPath))
		print(u'Done!')

	def runTest(self):

		"""
		desc:
			Walk through all examples
		"""

		for example in os.listdir(u'examples'):
			if example.endswith(u'.opensesame') or \
				example.endswith(u'.opensesame.tar.gz'):
				self.checkExample(os.path.join(u'examples', example))

if __name__ == '__main__':
	unittest.main()
