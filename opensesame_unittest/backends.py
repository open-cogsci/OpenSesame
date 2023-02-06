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
from libopensesame.py3compat import *

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
				type:	type
			chk_cls:
				desc:	The implementation class.
				type:	type
		"""
		print(u'Starting new check ...')
		print(u'\tChecking whether %s inherits %s ...' % (chk_cls, ref_cls))
		self.assertTrue(issubclass(chk_cls, ref_cls))
		# Loop through all functions
		for name, ref_obj in ref_cls.__dict__.items():
			ref_df = yamldoc.DocFactory(ref_obj, types=[u'function'])
			if ref_df is None:
				continue
			chk_obj = getattr(chk_cls, name)
			chk_df = yamldoc.DocFactory(chk_obj, types=[u'function'])
			print(u'\tChecking %s ...' % chk_obj)
			# Remove keyword dictionaries from the argument specification,
			# because these can change because of the @configurable decorator.
			ref_argSpec = ref_df.argSpec()._replace(keywords = None)
			chk_argSpec = chk_df.argSpec()._replace(keywords = None)
			self.assertEqual(ref_argSpec, chk_argSpec)
			chk_src = safe_decode(inspect.getsource(chk_obj).strip())
			# Check whether the function has been implemented
			self.assertNotIn(u'raise NotImplementedError()', chk_src)
		print(u'Done!')

	@yamldoc.validate
	def checkBackendCategory(self, category, backends):

		"""
		desc:
			Checks a back-end category.

		arguments:
			category:
				desc:	A back-end category, such as 'canvas'.
				type:	[unicode, str]
			backends:
				desc:	A list of back-end names that should be checked.
				type:	list
		"""
		# Check sampler back-ends
		ref_mod = __import__(u'openexp._%s.%s' % (category, category),
			fromlist=[u'dummy'])
		ref_cls = getattr(ref_mod, category)
		for backend in backends:
			if backend == 'xpyriment':
				try:
					import expyriment
				except:
					print('Expyriment is not installed, skipping test')
					continue
			if backend == 'psycho':
				try:
					import psychopy
				except:
					print('PsychoPy is not installed, skipping test')
					continue
			chk_mod = __import__(u'openexp._%s.%s' % (category, backend),
				fromlist=[u'dummy'])
			chk_cls = getattr(chk_mod, backend)
			self.check(ref_cls, chk_cls)

	def runTest(self):

		"""
		desc:
			Checks the integrity of all back-ends.
		"""
		self.checkBackendCategory(u'canvas', ['legacy', 'xpyriment', 'psycho'])
		self.checkBackendCategory(u'keyboard', ['legacy', 'psycho'])
		self.checkBackendCategory(u'mouse', ['legacy', 'xpyriment', 'psycho'])
		self.checkBackendCategory(u'sampler', ['legacy'])
		self.checkBackendCategory(u'clock', ['legacy', 'psycho'])
		self.checkBackendCategory(u'log', ['csv'])

if __name__ == '__main__':
	unittest.main()
