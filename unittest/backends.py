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

import types
import yamldoc
import unittest
import inspect

class check_backend_argspec(unittest.TestCase):

	"""
	desc: |
		-	Checks whether the argument specifications of the back-ends match
			those of the reference classes.
		-	Checks whether all functions that should be overridden in the
			back-ends have in fact been overridden.
	"""


	@yamldoc.validate
	def check(self, ref_cls, chk_cls):

		"""
		desc:
			Checks whether chk_cls is a valid back-end implementation of
			ref_cls.

		arguments:
			ref_cls:
				desc:	The reference class.
				type:	inherit
			chk_cls:
				desc:	The implementation class.
				type:	inherit
		"""

		print(u'Starting new check ...')
		print(u'\tChecking whether %s inherits %s ...' % (chk_cls, ref_cls))
		self.assertTrue(issubclass(chk_cls, ref_cls))
		# Loop through all functions
		for name, ref_obj in ref_cls.__dict__.items():
			ref_df = yamldoc.DocFactory(ref_obj, types=[u'function'])
			if ref_df == None:
				continue
			chk_obj = getattr(chk_cls, name)
			chk_df = yamldoc.DocFactory(chk_obj, types=[u'function'])
			print(u'\tChecking %s ...' % chk_obj)
			self.assertEqual(ref_df.argSpec(), chk_df.argSpec())
			chk_src = inspect.getsource(chk_obj).strip().decode(u'utf-8')
			# Check whether the function has been implemented
			self.assertNotIn(u'raise NotImplementedError()', chk_src)
			# Check whether docstrings match
			self.assertEqual(unicode(chk_df), unicode(ref_df))
		print(u'Done!')

	def runTest(self):

		"""
		desc:
			Checks the integrity of all back-ends.
		"""

		# Check canvas back-ends
		from openexp._canvas.canvas import canvas
		for backend in ['legacy', 'droid', 'xpyriment', 'psycho']:
			mod = __import__('openexp._canvas.%s' % backend, fromlist=['dummy'])
			cls = getattr(mod, backend)
			self.check(canvas, cls)

		# Check keyboard back-ends
		from openexp._keyboard.keyboard import keyboard
		for backend in ['legacy', 'droid', 'psycho']:
			mod = __import__('openexp._keyboard.%s' % backend,
				fromlist=['dummy'])
			cls = getattr(mod, backend)
			self.check(keyboard, cls)

		# Check mouse back-ends
		from openexp._mouse.mouse import mouse
		for backend in ['legacy', 'droid', 'xpyriment', 'psycho']:
			mod = __import__('openexp._mouse.%s' % backend, fromlist=['dummy'])
			cls = getattr(mod, backend)
			self.check(mouse, cls)

if __name__ == '__main__':
	unittest.main()
