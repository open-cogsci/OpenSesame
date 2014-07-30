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

import libopensesame.keyboard_response
from libqtopensesame.items import qtplugin
from libqtopensesame.misc import _
from openexp.keyboard import keyboard
from PyQt4 import QtCore, QtGui
import cgi

class keyboard_response(libopensesame.keyboard_response.keyboard_response, \
	qtplugin.qtplugin):

	"""keyboard_response item GUI"""

	def __init__(self, name, experiment, string=None):

		"""
		Constructor

		Arguments:
		name -- item name
		experiment -- experiment instance

		Keywords arguments:
		string -- a definition string (default=None)
		"""

		libopensesame.keyboard_response.keyboard_response.__init__(self, name, \
			experiment, string)
		qtplugin.qtplugin.__init__(self)

	def apply_edit_changes(self):

		"""Apply controls"""

		if not qtplugin.qtplugin.apply_edit_changes(self, False) or self.lock:
			return False
		return True

	def init_edit_widget(self):

		"""Initialize controls"""

		self.lock = True
		qtplugin.qtplugin.init_edit_widget(self, False)

		# Use auto-controls for most stuff
		self.add_line_edit_control('correct_response', 'Correct response',
			tooltip='Set the correct response')
		self.add_line_edit_control('allowed_responses', 'Allowed responses',
			tooltip='Set the allowed responses seperated by a semi-colon, e.g., "z;/"' \
			)
		self.add_line_edit_control('timeout', 'Timeout',
			tooltip='Set the response timeout in milliseconds, or "infinite"')
		self.add_checkbox_control('flush', 'Flush pending keypresses',
			tooltip='Flush pending keypresses')

		# List available keys
		button_list_keys = QtGui.QPushButton(self.experiment.icon("info"), \
			"List available keys")
		button_list_keys.setIconSize(QtCore.QSize(16,16))
		button_list_keys.clicked.connect(self.list_keys)
		self.add_control('', button_list_keys, 'List available keys')

		self.edit_vbox.addStretch()
		self.lock = True

	def edit_widget(self):

		"""
		Update controls

		Returns:
		Controls QWidget
		"""

		self.lock = True
		qtplugin.qtplugin.edit_widget(self)
		self.lock = False
		return self._edit_widget

	def list_keys(self):

		"""Show a dialog with available key names"""

		my_keyboard = keyboard(self.experiment)
		s = _('The following key names are valid:<br />') \
			+ '<br />'.join(my_keyboard.valid_keys())
		self.experiment.notify(s)

