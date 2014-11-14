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

from PyQt4 import QtCore, QtGui
from libopensesame import debug
from libqtopensesame.misc import _
from libqtopensesame.widgets.base_widget import base_widget

class header_widget(base_widget):

	"""
	desc:
		Editable labels for an item's name and description.
	"""

	def __init__(self, item):

		"""
		desc:
			Constructor.

		arguments:
			item: 			A qtitem object.
		"""

		super(header_widget, self).__init__(item.main_window)
		self.setCursor(QtCore.Qt.IBeamCursor)
		self.setToolTip(_(u"Click to edit"))
		self.item = item
		self.label_name = QtGui.QLabel()
		self.edit_name = QtGui.QLineEdit()
		self.edit_name.editingFinished.connect(self.apply_name)
		self.edit_name.hide()
		self.label_desc = QtGui.QLabel()
		self.edit_desc = QtGui.QLineEdit()
		self.edit_desc.editingFinished.connect(self.apply_desc)
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

		"""
		desc:
			Updates the header so that it's content match the item.
		"""

		self.set_name(self.item.name)
		self.set_desc(self.item.description)

	def set_name(self, name):

		"""
		desc:
			Sets the name.

		arguments:
			name:	A name.
			type:	unicode
		"""

		self.label_name.setText(
			(u"<font size='5'><b>%s</b> - %s</font>&nbsp;&nbsp;&nbsp;"
			u"<font color='gray'><i>Click to edit</i></font>") \
			% (name, self.item.item_type.replace(u"_", u" ").title()))
		self.edit_name.setText(name)

	def set_desc(self, desc):

		"""
		desc:
			Sets the description.

		arguments:
			name:	A description.
			type:	unicode
		"""

		self.edit_desc.setText(desc)
		self.label_desc.setText(desc)

	def apply_name(self):

		"""
		desc:
			Applies the name change and revert the edit control back to the
			static label.
		"""

		if self.label_name.isVisible():
			return
		debug.msg()
		self.label_name.show()
		self.edit_name.hide()
		self.item_store.rename(self.item.name, unicode(self.edit_name.text()))

	def apply_desc(self):

		"""
		desc:
			Applies the description change and revert the edit back to the
			label.
		"""

		if self.label_desc.isVisible():
			return
		debug.msg()
		self.label_desc.show()
		self.edit_desc.hide()
		self.item.apply_edit_changes()

	def mousePressEvent(self, event):

		"""
		Change the label into an edit for the name or
		the description, depending on where has been
		clicked

		Arguments:
		event -- the mouseClickEvent
		"""

		target = self.childAt(event.pos())
		if target == self.label_name:
			self.apply_desc()
			self.label_name.hide()
			self.edit_name.show()
			self.edit_name.selectAll()
			self.edit_name.setFocus()
		elif target == self.label_desc:
			self.apply_name()
			self.label_desc.hide()
			self.edit_desc.show()
			self.edit_desc.selectAll()
			self.edit_desc.setFocus()
