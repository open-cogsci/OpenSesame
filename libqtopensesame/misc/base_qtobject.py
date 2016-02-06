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

import sys
from libopensesame.py3compat import *

if '--debug' in sys.argv:

	from qtpy.QtCore import pyqtWrapperType
	import types
	import time
	from decorator import decorator
	from libopensesame import debug

	i = 0
	lvl = 0

	def debug_decorator(cls, name, fnc):

		"""
		desc:
			A decorator that prints the function-call flow plus timing to the
			standard output.
		"""

		def inner(fnc, *args, **kwargs):
			debug.msg(u'call %s.%s()' % (cls, name))
			debug.indent(1)
			t0 = time.time()
			retval = fnc(*args, **kwargs)
			t1 = time.time()
			debug.indent(-1)
			dur = 1000.*(t1-t0)
			debug.msg(u'done %s.%s() in %.2f ms' % (cls, name, dur))
			return retval

		return decorator(inner, fnc)

	class base_qtmetaclass(pyqtWrapperType):

		"""
		desc:
			A custom metaclass that applies a debug decorator to all functions.
		"""

		def __new__(cls, name, bases, dict):
			debug.msg(u'new  %s' % name)
			cls = pyqtWrapperType.__new__(cls, name, bases, dict)
			# Don't decorate the console objects, because it leads to infinite
			# recursion: They generate a write call everytime their write
			# function is called.
			if u'console' not in name:
				for key, val in cls.__dict__.items():
					if isinstance(val, types.FunctionType):
						setattr(cls, key, debug_decorator(name, key, val))
			return cls

	# Use the base_qtmetaclass in a way that is compatible with Python 2 and 3.
	base_qtobject = base_qtmetaclass('base_qtobject', (), {})
else:
	# Don't use a special metaclass
	base_qtobject = object
