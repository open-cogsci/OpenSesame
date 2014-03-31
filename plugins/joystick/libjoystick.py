#-*- coding:utf-8 -*-

"""
This file is part of openexp.

openexp is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

openexp is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with openexp.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import imp
from libopensesame import debug

class libjoystick:

	"""Morphs into the appropriate class form the _libjoystick module."""

	def __init__(self, experiment, joybuttonlist=None, timeout=None):
	
		backend = u'legacy'
		debug.msg(u'morphing into %s' % backend)
		mod_path = os.path.join(os.path.dirname(__file__), u'_libjoystick', \
			u'%s.py' % backend)
		debug.msg(u'loading %s' % mod_path)
		mod = imp.load_source(backend, mod_path)
		cls = getattr(mod, backend)
		self.__class__ = cls
		cls.__init__(self, experiment, joybuttonlist=joybuttonlist, timeout= \
			timeout)
