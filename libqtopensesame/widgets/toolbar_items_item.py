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
from libopensesame import debug
from libqtopensesame.misc import _
from libqtopensesame.misc.base_subcomponent import base_subcomponent
from libqtopensesame.misc import drag_and_drop

class toolbar_items_item(base_subcomponent, QtGui.QLabel):

	"""
	desc:
		A draggable toolbar icon.
	"""

	def __init__(self, parent, item, pixmap):

		"""
		desc:
			Constructor.

		arguments:
			parent:
				desc:	The parent.
				type:	QWidget
			item:
				desc:	An item.
				type:	qtitem
			pixmap:
				desc:	A pixmap for the icon.
				type:	QPixmap
		"""

		super(toolbar_items_item, self).__init__(parent)
		self.setup(parent)
		self.item = item
		self.pixmap = pixmap
		# self.setMargin(6)
		self.setToolTip(_(
			"Drag this <b>%s</b> item to the intended location in the overview "
			"area or into the item list of a sequence tab") % self.item)
		self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
		self.setPixmap(self.pixmap)

	def mousePressEvent(self, e):

		"""
		desc:
			Initiates a drag event after a mouse press.

		arguments:
			e:
				desc:	A mouse event.
				type:	QMouseEvent
		"""

		if e.buttons() != QtCore.Qt.LeftButton:
			return
		data = {
			u'type'			: u'item-new',
			u'item-type'	: self.item,
			u'item-name'	: self.item,
			u'script'		: u'',
			}
		drag_and_drop.send(self, data)
