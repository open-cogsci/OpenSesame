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

from libopensesame import misc
from libqtopensesame.misc import config
from libqtopensesame.widgets.base_widget import base_widget
from PyQt4 import QtGui, QtCore

class loop_widget(base_widget):

	"""
	desc:
		A credits window, embedded in the start-new widget.
	"""

	def __init__(self, main_window):

		"""
		desc:
			Constructor.

		keywords:
			main_window:	A qtopensesame object.
		"""

		super(loop_widget, self).__init__(main_window,
			ui=u'widgets.loop_widget')
