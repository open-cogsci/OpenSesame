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
from libqtopensesame.dialogs.base_dialog import base_dialog
from libqtopensesame.misc import _
from libopensesame.py3compat import *

class new_loop_sequence_dialog(base_dialog):

	"""
	desc:
		A dialog to select an item-to-run for a new sequence or loop item.
	"""

	def __init__(self, main_window, item_type, _parent):

		"""
		desc:
			Constructor.

		arguments:
			main_window:	A qtopensesame object.
			item_type:		'sequence' or 'loop'
			_parent:
							The parent item, i.e. the item above the current
							item in the experiment hierarchy.
		"""

		super(new_loop_sequence_dialog, self).__init__(main_window,
			ui=u'dialogs.new_loop_sequence')
		self._parent = _parent
		self.ui.label_icon.setPixmap(self.theme.qpixmap(item_type))
		self.action = u"cancel"
		self.ui.button_new.clicked.connect(self.new_item)
		self.ui.button_select.clicked.connect(self.select_item)
		if item_type == u"loop":
			s = _(
				u"A loop needs another item to run, usually a sequence. You "
				u"can create a new item or select an existing item to add to "
				u"the loop.")
			select = u"sequence"
		else:
			s = _(
				u"A sequence needs at least one other item to run, such as a "
				u"sketchpad. You can create a new item or select an existing "
				u"item to add to the sequence.")
			select = u"sketchpad"
		self.ui.label_explanation.setText(s)
		self.experiment.item_type_combobox(True, True, self.ui.combobox_new,
			select)
		# The parents list is excluded from the list of possible children, but
		# this list if empty if there are no parents or the parent is the main
		# experiment sequence
		if self._parent == None or _parent not in self.experiment.items:
			parents = []
		else:
			parents = self.experiment.items[_parent].parents()
		self.experiment.item_combobox(None, parents, self.ui.combobox_select)

	def new_item(self):

		"""
		desc:
			Accepts the dialog and indicates that an item should be newly
			created.
		"""

		self.action = u'new'
		self.item_type = str(self.ui.combobox_new.currentText())
		self.accept()

	def select_item(self):

		"""
		desc:
			Accepts the dialog and indicates that an existing item should be
			used.
		"""

		self.action = u'select'
		self.item_name = str(self.ui.combobox_select.currentText())
		self.accept()
