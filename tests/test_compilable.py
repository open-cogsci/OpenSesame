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
from libopensesame.py3compat import *
import unittest
import os

class check_compilable(unittest.TestCase):

    """
    desc: |
        Checks whether all `.py` files can be compiled.
    """
    def checkFile(self, path):

        """
        desc:
            Checks the syntax of a single `.py` source file.

        arguments:
            path:
                desc:	The full path to the file.
                type:	[str, unicode]
        """
        print(u'- %s' % path)
        src = open(path).read()
        usrc = safe_decode(src)
        if u'\n# NO UNITTEST\n' in usrc:
            return
        compile(src, u'<string>', u'exec')
        if not path.endswith(u'py3compat.py') and \
                not path.endswith('__.py'):
            self.assertTrue(u'\nfrom libopensesame.py3compat import *\n' in usrc)

    def checkFolder(self, root):

        """
        desc:
            Checks the syntax of all `.py` source files within a folder.

        arguments:
            root:
                desc:	The directory to start from.
                type:	[str, unicode]
        """
        for dirpath, dirnames, filenames in os.walk(root):
            for dirname in dirnames:
                path = os.path.join(dirpath, dirname)
                self.checkFolder(path)
            for filename in filenames:
                if not filename.endswith(u'.py'):
                    continue
                path = os.path.join(dirpath, filename)
                self.checkFile(path)

    def runTest(self):

        """
        desc:
            Checks the syntax of all `.py` source files.

        """
        print(u'Checking whether all files are compilable and valid ...\n')
        for folder in [
            u'opensesame_plugins',
            u'opensesame_extensions',
            u'libqtopensesame',
            u'libopensesame',
            u'openexp'
            ]:
            self.checkFolder(folder)

if __name__ == '__main__':
    unittest.main()
