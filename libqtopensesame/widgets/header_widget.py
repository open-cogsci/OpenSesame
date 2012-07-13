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

__author__ = "Sebastiaan Mathot"
__license__ = "GPLv3"

from PyQt4 import QtCore, QtGui
from libopensesame import debug
from libqtopensesame.misc import _

class header_widget(QtGui.QWidget):

	"""Editable labels for the item's name and description"""

	def __init__(self, item):

		"""
		Constructor

		Arguments:
		item -- the item to provide a header for
		"""

		QtGui.QWidget.__init__(self)
		self.setCursor(QtCore.Qt.IBeamCursor)
		self.setToolTip(_("Click to edit"))
		self.item = item
		self.label_name = QtGui.QLabel()
		self.label_name.id = "name"
		self.edit_name = QtGui.QLineEdit()
		self.edit_name.editingFinished.connect(self.restore_name)
		self.edit_name.hide()
		self.label_desc = QtGui.QLabel()
		self.label_desc.id = "desc"
		self.edit_desc = QtGui.QLineEdit()
		self.edit_desc.editingFinished.connect(self.restore_desc)
		self.edit_desc.hide()
			
		vbox = QtGui.QVBoxLayout()
		vbox.setContentsMargins(8, 0, 0, 0)
		vbox.setSpacing(0)
		vbox.addWidget(self.label_name)
		vbox.addWidget(self.edit_name)
		vbox.addWidget(self.label_desc)
		vbox.addWidget(self.edit_desc)		
		self.refresh()
		self.setLayout(vbox)

	def refresh(self):

		"""Update the header"""

		self.edit_name.setText(self.item.name)
		self.label_name.setText( \
			"<font size='5'><b>%s</b> - %s</font>&nbsp;&nbsp;&nbsp;<font color='gray'><i>Click to edit</i></font>" \
			% (self.item.name, self.item.item_type.replace("_", " ").title()))
		self.edit_desc.setText(self.item.description)
		self.label_desc.setText(self.item.description)

	def restore_name(self, apply_name_change=True):

		"""
		Apply the name change and revert the edit control back to the static
		label

		Keywords arguments:
		apply_name_change -- indicates of the name change should be applied
							 (default=True)
		"""
		
		debug.msg("apply_name_change = %s" % apply_name_change)
		if apply_name_change:
			self.item.apply_name_change()			
		self.refresh()					
		self.label_name.show()
		self.edit_name.hide()

	def restore_desc(self):

		"""Apply the description change and revert the edit	back to the label"""
		
		self.item.apply_edit_changes()			
		self.refresh()
		self.label_desc.show()
		self.edit_desc.hide()

	def mousePressEvent(self, event):

		"""
		Change the label into an edit for the name or
		the description, depending on where has been
		clicked

		Arguments:
		event -- the mouseClickEvent
		"""

		target = self.childAt(event.pos())

		if target != None and hasattr(target, "id"):
			if target.id == "name":
				self.restore_desc()
				self.label_name.hide()
				self.edit_name.show()
				self.edit_name.selectAll()
				self.edit_name.setFocus()
			else:
				self.restore_name()
				self.label_desc.hide()
				self.edit_desc.show()
				self.edit_desc.selectAll()
				self.edit_desc.setFocus()
