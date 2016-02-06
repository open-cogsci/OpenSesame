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

from qtpy import QtCore, QtWidgets
from libqtopensesame.misc.base_subcomponent import base_subcomponent

class qtitem_splitter(base_subcomponent, QtWidgets.QSplitter):

	"""
	desc:
		Implements a splitter for the edit and script view in an item tab. This
		custom is mostly necessary, because the default QSplitter.sizeHint()
		is too large.
	"""

	def __init__(self, item):

		"""
		desc:
			Constructor.

		item:
			desc:	The item.
			type:	qtitem
		"""

		super(qtitem_splitter, self).__init__(QtCore.Qt.Vertical,
			item.main_window)
		self.item = item
		self.setup(item.main_window)
		self.addWidget(self.item._edit_widget)
		self.addWidget(self.item._script_widget)

	def minimumSizeHint(self):

		"""
		returns:
			type:	QSize
		"""

		return QtCore.QSize(100, 100)

	def sizeHint(self):

		"""
		returns:
			type:	QSize
		"""

		return QtCore.QSize(100, 100)
