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
from distutils.version import StrictVersion
import sys

__version__ = u'3.0.0a20'
strict_version = StrictVersion(__version__)
# The version without the prerelease (if any)
main_version = u'.'.join([str(i) for i in strict_version.version])
python_version = u'%d.%d.%d' % (sys.version_info[0], sys.version_info[1], \
	sys.version_info[2])
codename = u'Interactive Ising'
channel = u'dev'
platform = sys.platform
