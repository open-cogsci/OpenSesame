# coding=utf-8

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
from qtpy import QtCore

# The DPI of the browser appears to be hard-set to 96, so we need adjust the
# zooom of QWebView to correct for this.
STANDARD_DPI = 96
system_dpi = QtCore.QCoreApplication.instance().desktop().screen().logicalDpiX()
display_scaling = 1.*STANDARD_DPI/system_dpi
