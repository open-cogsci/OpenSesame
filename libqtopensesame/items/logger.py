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
from libopensesame.logger import logger as logger_runtime
from libqtopensesame.items.qtplugin import qtplugin
from libqtopensesame.widgets.logger_widget import logger_widget

class logger(logger_runtime, qtplugin):

	"""
	desc:
		GUI controls for the logger item.
	"""

	def __init__(self, name, experiment, string=None):

		"""See item."""

		logger_runtime.__init__(self, name, experiment, string)
		qtplugin.__init__(self)

	def init_edit_widget(self):

		"""See qtitem."""

		super(logger, self).init_edit_widget(stretch=False)
		self.logger_widget = logger_widget(self)
		self.add_widget(self.logger_widget)
		self.auto_add_widget(self.logger_widget.ui.checkbox_auto_log,
			u'auto_log')
		self.auto_add_widget(self.logger_widget.ui.checkbox_ignore_missing,
			u'ignore_missing')
		self.auto_add_widget(self.logger_widget.ui.checkbox_use_quotes,
			u'use_quotes')

	def edit_widget(self):

		"""See qtitem."""

		super(logger, self).edit_widget()
		self.logger_widget.update()

	def apply_edit_changes(self):

		"""See qtitem."""

		self.logvars = self.logger_widget.var_selection()
		super(logger, self).apply_edit_changes()
		self.logger_widget.update()
