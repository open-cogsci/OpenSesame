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
from libopensesame.experiment import experiment

class check_response(unittest.TestCase):

	"""
	desc: |
		Checks whether response logging is sane
	"""
	def assertState(self, response, response_time, correct, total_responses,
		total_response_time, total_correct):

		self.assertEqual(self.exp.var.response, response)
		self.assertEqual(self.exp.var.response_time, response_time)
		self.assertEqual(self.exp.var.correct, correct)
		self.assertEqual(self.exp.var.total_responses, total_responses)
		self.assertEqual(self.exp.var.total_response_time, total_response_time)
		self.assertEqual(self.exp.var.total_correct, total_correct)

	def runTest(self):

		"""
		desc:
			Runs the response test.
		"""
		print(u'Checking response handling')
		self.exp = experiment()
		with self.assertRaises(osexception) as cm:
			self.exp.set_response(correct=u'A')
		with self.assertRaises(osexception) as cm:
			self.exp.set_response(response_time=u'A')
		for i in range(2):
			self.exp.reset_feedback()
			self.exp.set_response()
			self.assertState(u'None', None, u'undefined', 1, 0, 0)
			self.exp.set_response(response=u'A')
			self.assertState(u'A', None, u'undefined', 2, 0, 0)
			self.exp.set_response(response=u'B', response_time=1000)
			self.assertState(u'B', 1000, u'undefined', 3, 1000, 0)
			self.exp.set_response(response=u'C', response_time=1000, correct=1)
			self.assertState(u'C', 1000, 1, 4, 2000, 1)
			self.exp.set_response(response=u'D', response_time=1, correct=0)
			self.assertState(u'D', 1, 0, 5, 2001, 1)

if __name__ == '__main__':
	unittest.main()
