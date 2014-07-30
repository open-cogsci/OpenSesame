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

import libopensesame.mouse_response
from libqtopensesame.items import qtplugin
from PyQt4 import QtCore, QtGui

class mouse_response(libopensesame.mouse_response.mouse_response, \
	qtplugin.qtplugin):

	"""mouse_response item GUI"""

	def __init__(self, name, experiment, string=None):

		"""
		Constructor

		Arguments:
		name -- item name
		experiment -- experiment instance

		Keywords arguments:
		string -- a definition string (default=None)
		"""
		libopensesame.mouse_response.mouse_response.__init__(self, name, \
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
			tooltip='Set the allowed responses seperated by a semi-colon, e.g., "left_button;right_button"' \
			)
		self.add_line_edit_control('timeout', 'Timeout',
			tooltip='Set the response timeout in milliseconds, or "infinite"')
		self.add_checkbox_control('show_cursor', 'Visible mouse cursor',
			tooltip='If checked, the mouse cursor will be visible')
		self.add_checkbox_control('flush', 'Flush pending mouse clicks',
			tooltip='Flush pending mouse clicks')
		self.add_text( \
			'<small><i><b>Note:</b> Change the "custom cursor" option in the backend settings to switch between the system cursor and the custom OpenSesame cursor</i></small>' \
			)
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

