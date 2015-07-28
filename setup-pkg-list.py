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

from stdlib_list import stdlib_list
import sys

python_version = "%d.%d" % (sys.version_info[0], sys.version_info[1])
print(u'Python version: %s' % python_version)
fd = open(u'pkg-list-py%s.txt' % python_version, u'w')
for pkg in stdlib_list(python_version):
    try:
        __import__(pkg)
        print('Imported %s' % pkg)
        fd.write(pkg + u'\n')
    except ImportError:
        print('Failed to import %s' % pkg)
fd.close()
