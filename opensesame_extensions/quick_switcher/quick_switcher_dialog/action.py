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
from libqtopensesame.widgets.base_widget import base_widget

class quick_open_element_action(base_widget):

	"""
	desc:
		An action element for the quick switcher.
	"""

	def __init__(self, dialog, action, path_to_action):

		"""
		desc:
			Constructor.

		arguments:
			dialog:
				desc:	The parent dialog.
				type:	quick_switcher
			action:
				desc:	An action.
				type:	QAction
			path_to_action:
				desc:	A list of parent actions, to represent the path to
						the action in the menu.
				type:	list
		"""

		super(quick_open_element_action, self).__init__(dialog)
		self.dialog = dialog
		self.action = action
		self.text = str(action.text())
		self.path_to_action = u' : '.join(path_to_action)
		if self.action.icon().isNull():
			self.icon = self.theme.qlabel(u'system-run')
		else:
			self.icon = self.theme.qlabel(self.action.icon())
		self.label = QtWidgets.QLabel(u'action <b>%s</b><br /><i>%s</i>' \
			% (self.text, self.path_to_action))
		self.layout = QtWidgets.QHBoxLayout(self)
		self.layout.addWidget(self.icon)
		self.layout.addWidget(self.label)
		self.layout.addStretch()
		self.setLayout(self.layout)

	def match(self, query):

		"""
		returns:
			desc:	True if the action matches the query, False otherwise.
			type:	bool
		"""

		_text = self.text.lower()
		_path = self.path_to_action.lower()
		for term in query.lower().split():
			if term not in _text and term not in _path:
				return False
		return True

	def activate(self):

		"""
		desc:
			Triggers the action.
		"""

		self.dialog.show_wait()
		self.action.trigger()
