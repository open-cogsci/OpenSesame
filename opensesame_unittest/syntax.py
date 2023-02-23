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
from libopensesame.experiment import experiment
from libopensesame.exceptions import OSException

class check_syntax(unittest.TestCase):

	"""
	desc:
		Checks whether OpenSesame syntax is correctly parsed
	"""
	def checkCmd(self, s, cmd, arglist, kwdict):

		print(u'Checking: %s' % s)
		_cmd, _arglist, _kwdict = self.exp.syntax.parse_cmd(s)
		print(_cmd, _arglist, _kwdict)
		self.assertEqual(cmd, _cmd)
		self.assertEqual(arglist, _arglist)
		self.assertEqual(kwdict, _kwdict)
		self.assertEqual(
			s,
			self.exp.syntax.create_cmd(_cmd, _arglist, _kwdict)
		)

	def checkEvalText(self, sIn, sOut):

		print(u'Checking: %s -> %s' % (sIn, sOut))
		self.assertEqual(self.exp.syntax.eval_text(sIn), sOut)

	def checkCnd(self, sIn, sOut):

		print(u'Checking: %s -> %s' % (sIn, sOut))
		self.assertEqual(
			self.exp.syntax.compile_cond(sIn, bytecode=False),
			sOut
		)

	def runTest(self):

		"""
		desc:
			Walk through the test
		"""
		self.exp = experiment()
		self.checkCmd(u'widget 0 0 1 1 label text="Tést 123"',
			u'widget', [0, 0, 1, 1, u'label'],
			{u'text' : u'Tést 123'})
		self.checkCmd(u'test', u'test',	[], {})
		self.checkCmd(u'set test "c:\\\\" x="d:\\\\"',
			u'set', [u'test', u'c:\\'], {u'x' : u'd:\\'})
		self.checkCmd(u'test "\\"quoted\\""',
			u'test', [u'\"quoted\"'], {})
		self.checkCmd(u'test test="\\"quoted\\""', u'test', [],
			{u'test' : u'\"quoted\"'},)
		self.checkCmd(
			u'draw textline text=" 1 "',
			u'draw',
			[u'textline'],
			{u'text': ' 1 '}
		)
		with self.assertRaises(OSException):
			print(u'Testing exception ...')
			self.checkCmd(u'widget 0 0 1 1 label text="Tést 123',
				u'widget', [0, 0, 1, 1, u'label'],
				{u'text' : u'Tést 123'})
		self.checkEvalText(r'\\[width] = \[width] = [width]',
			r'\1024 = [width] = 1024')
		self.checkEvalText(u'[no var]', u'[no var]')
		self.checkEvalText(u'[nóvar]', u'[nóvar]')
		self.checkEvalText(u'\[width]', u'[width]')
		self.checkEvalText(r'\\[width]', r'\1024')
		self.checkEvalText(u'[width] x [height]', u'1024 x 768')
		self.checkEvalText(u'[=10*10]', u'100')
		self.checkEvalText(r'\[=10*10]', u'[=10*10]')
		self.checkEvalText(r'\\[=10*10]', r'\100')
		self.checkEvalText(u'[=u"tést"]', u'tést')
		self.checkEvalText(u'[="\[test\]"]', u'[test]')
		self.checkCnd(u'[width] > 100', u'var.width > 100')
		self.checkCnd(u'[width] >= 100', u'var.width >= 100')
		self.checkCnd(u'[width] <= 100', u'var.width <= 100')
		self.checkCnd(u'always', u'True')
		self.checkCnd(u'ALWAYS', u'True')
		self.checkCnd(u'never', u'False')
		self.checkCnd(u'NEVER', u'False')
		self.checkCnd(u'[width] = 1024', u'var.width == 1024')
		self.checkCnd(u'[width] = 1024 and [height] == 768',
			u'var.width == 1024 and var.height == 768')
		self.checkCnd(u'=var.width > 100', u'var.width > 100')
		self.checkCnd(u'"yes" = yes', u'"yes" == "yes"')
		self.checkCnd(u'yes = \'yes\'', u'"yes" == \'yes\'')
		self.checkCnd(u'"y\'es" = \'y"es\'', u'"y\'es" == \'y"es\'')
		self.checkCnd(u'("a b c" = abc) or (x != 10) and ([width] == 100)',
			u'("a b c" == "abc") or ("x" != 10) and (var.width == 100)')
		self.checkCnd(
			u'[text] = has_underscore',
			'var.text == "has_underscore"'
		)

if __name__ == '__main__':
	unittest.main()