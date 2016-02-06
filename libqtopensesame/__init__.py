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
from libopensesame.metadata import __version__

from qtpy import QtCore
if QtCore.QCoreApplication is not None:
	# Redirect certain things so that the old way of from libqtopensesame import
	# qtplugin still works.
	from libqtopensesame.items import qtplugin
	from libqtopensesame.widgets import pool_widget
else:
	# Load dummy modules to avoid dependency on qtpy
	from libqtopensesame.misc import dummy as qtplugin
	from libqtopensesame.misc import dummy as qtautoplugin
