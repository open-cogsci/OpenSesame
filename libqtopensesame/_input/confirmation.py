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
from qtpy import QtWidgets
from libqtopensesame.misc.base_subcomponent import base_subcomponent
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'confirmation', category=u'core')

class confirmation(QtWidgets.QMessageBox, base_subcomponent):

	"""
	desc:
		A simple yes/ no/ cancel confirmation dialog.
	"""

	def __init__(self, main_window, msg, title=None, allow_cancel=False,
		default=u'no'):

		"""
		desc:
			Constructor.

		arguments:
			main_window:
				desc:	The main-window object.
				type:	QWidget
			msg:
				desc:	The message.
				type:	[unicode, str]
			title:
				desc:	A Window title or None for a default title.
				type:	[str, NoneType]
			allow_cancel:
				desc:	Indicates whether a cancel button should be included,
						in addition to the yes and no buttons.
				type:	bool
			default:
				desc:	The button that is active by default, 'no', 'yes', or
						'cancel'
				type:	str
		"""

		QtWidgets.QMessageBox.__init__(self, main_window)
		self.setup(main_window)
		self.yes = self.addButton(QtWidgets.QMessageBox.Yes)
		self.no = self.addButton(QtWidgets.QMessageBox.No)
		if allow_cancel:
			self.cancel = self.addButton(QtWidgets.QMessageBox.Cancel)
		else:
			self.cancel = None
		if default == u'no':
			self.setDefaultButton(QtWidgets.QMessageBox.No)
		elif default == u'yes':
			self.setDefaultButton(QtWidgets.QMessageBox.Yes)
		elif default == u'cancel' and allow_cancel:
			self.setDefaultButton(QtWidgets.QMessageBox.Cancel)
		if title is None:
			title = _(u'Please confirm')
		self.setWindowTitle(title)
		self.setText(msg)

	def show(self):

		"""
		desc:
			Shows the confirmation dialog.

		returns:
			desc:	True if confirmed, False disconfirmed, and None if
					cancelled.
			type:	[bool, NoneType]
		"""

		self.exec_()
		button = self.clickedButton()
		if self.cancel is not None and button is self.cancel:
			return None
		return button == self.yes
