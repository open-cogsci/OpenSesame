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
import os
import unittest
from libopensesame.experiment import experiment
from libopensesame.osexpfile import osexpreader, osexpwriter


class check_readandwrite(unittest.TestCase):
	
	"""
	desc:
		Checks whether experiment files can written and read properly in all
		supported formats.
	"""
	
	def path(self, basename):
		
		"""
		returns:
			The path to the basename file in the data subfolder.
		"""
		
		return os.path.join(os.path.dirname(__file__), u'data', basename)
	
	def checkRead(self, path, fmt, pool=[]):
		
		"""
		desc:
			Checks whether a single experiment can be read, written, and then
			read again.
			
		arguments:
			path:	The path to the experiment file, or script of the experiment
					file.
			fmt:	The expected format of the experiment file when re-opening
					it.
		
		keywords:
			pool:	A list of filenames that should be in the file pool.
		"""
		
		e = experiment(string=path)
		self.assertEqual(e.var.title, u'New experiment')
		for basename in pool:
			self.assertIn(basename, e.pool)
		osexpwriter(e, 'tmp.osexp')
		r = osexpreader(e, 'tmp.osexp')
		self.assertEqual(r.format, fmt)
	
	def runTest(self):
		
		"""
		desc:
			Runs the full test.
		"""
		
		self.checkRead(self.path(u'targzfile.osexp'), fmt='targz',
			pool=[u'tést.txt'])
		self.checkRead(self.path(u'tarfile.osexp'), fmt='targz',
			pool=[u'tést.txt'])
		self.checkRead(self.path(u'scriptfile.osexp'), fmt='scriptfile')
		with open(self.path(u'scriptfile.osexp')) as fd:
			self.checkRead(fd.read(), fmt='scriptfile')

	
if __name__ == '__main__':
	unittest.main()
