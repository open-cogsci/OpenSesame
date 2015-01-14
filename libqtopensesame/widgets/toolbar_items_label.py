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

from PyQt4 import QtCore, QtGui
from libqtopensesame.misc import _
from libqtopensesame.misc.base_subcomponent import base_subcomponent

class toolbar_items_label(base_subcomponent, QtGui.QFrame):

	"""
	desc:
		A label for the item toolbar.
	"""

	def __init__(self, parent, label):

		"""
		desc:
			Constructor

		arguments:
			parent:
				desc:	The parent.
				type:	QWidget
			label:
				desc:	Label text.
				type:	unicode
		"""

		super(toolbar_items_label, self).__init__(parent)
		self.setup(parent)
		l = QtGui.QLabel(_(label))
		l.setMaximumWidth(90)
		l.setIndent(5)
		l.setWordWrap(True)
		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(l)
		hbox.setMargin(0)
		self.setLayout(hbox)
