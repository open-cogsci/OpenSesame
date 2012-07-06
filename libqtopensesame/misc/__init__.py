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

__author__ = "Sebastiaan Mathot"
__license__ = "GPLv3"

import sys
if '--catch-translatables' in sys.argv:

	# Automatically catches all strings that require translation
	from libopensesame import misc
	import os.path
	path = misc.resource(os.path.join('ts', 'translatables.txt'))
	def _(s):
		l = open(path).read().split('\n')
		if s not in l:
			f = open(path, 'a')
			f.write(s+'\n')
			print 'New translatable: '+s
			f.close()
		return s
	
else:
	# A simple wrapper arround the translate function
	from PyQt4.QtCore import QCoreApplication
	_ = lambda s: QCoreApplication.translate('script', s)
