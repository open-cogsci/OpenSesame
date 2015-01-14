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

from libopensesame.py3compat import *

import sys
if '--catch-translatables' in sys.argv:

	# Automatically catches all strings that require translation
	from libopensesame import misc
	import os.path
	path = misc.resource(os.path.join(u'ts', u'translatables.txt'))
	def _(s):
		l = open(path).read().split(u'\n')
		if s not in l:
			f = open(path, u'a')
			f.write(s + u'\n')
			print(u'New translatable: '+s)
			f.close()
		return s

else:
	from PyQt4.QtCore import QCoreApplication
	def _(s, context=u'script'):

		"""
		Translates a string of text.

		Arguments:
		s			--	The string to translate.

		Keyword arguments:
		context		--	The translation context. (default=u'script')

		Returns:
		The translated string.
		"""

		return str(QCoreApplication.translate(context, s,
			encoding=QCoreApplication.UnicodeUTF8))
