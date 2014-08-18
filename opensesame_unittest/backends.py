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
		-	Checks whether all functions that should be overridden in thebackends
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

	@yamldoc.validate
	def checkBackendCategory(self, category, backends):

		"""
		desc:
			Checks a back-end category.

		arguments:
			category:
				desc:	A back-end category, such as 'canvas'.
				type:	unicode
			backends:
				desc:	A list of back-end names that should be checked.
				type:	list
		"""

		# Check sampler back-ends
		ref_mod = __import__(u'openexp._%s.%s' % (category, category),
			fromlist=[u'dummy'])
		ref_cls = getattr(ref_mod, category)
		for backend in backends:
			chk_mod = __import__(u'openexp._%s.%s' % (category, backend),
				fromlist=[u'dummy'])
			chk_cls = getattr(chk_mod, backend)
			self.check(ref_cls, chk_cls)

	def runTest(self):

		"""
		desc:
			Checks the integrity of all back-ends.
		"""

		self.checkBackendCategory(u'canvas', ['legacy', 'droid', 'xpyriment',
			'psycho'])
		self.checkBackendCategory(u'keyboard', ['legacy', 'droid', 'psycho'])
		self.checkBackendCategory(u'mouse', ['legacy', 'droid', 'xpyriment',
			'psycho'])
		self.checkBackendCategory(u'sampler', ['legacy', 'gstreamer'])
		self.checkBackendCategory(u'synth', ['legacy', 'droid'])


if __name__ == '__main__':
	unittest.main()
