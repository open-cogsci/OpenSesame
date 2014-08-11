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

import random
import re
import sys
from libopensesame import debug, misc
from libopensesame.inline_script import inline_script as inline_script_runtime
from libqtopensesame.items.qtplugin import qtplugin
from libqtopensesame.misc import _
from libqtopensesame.misc.config import cfg
from PyQt4 import QtCore, QtGui

class inline_script(inline_script_runtime, qtplugin):

	"""The inline_script GUI controls"""

	def __init__(self, name, experiment, string=None):

		"""See item."""

		inline_script_runtime.__init__(self, name, experiment, string)
		qtplugin.__init__(self)

	def apply_edit_changes(self):

		"""See qtitem."""

		super(inline_script, self).apply_edit_changes(self)
		sp = self.qprogedit.text(index=0)
		sr = self.qprogedit.text(index=1)
		self.set(u'_prepare', sp)
		self.set(u'_run', sr)
		self.update_item_icon()

	def item_icon(self):

		"""
		desc:
			Determines the icon, based on whether the scripts are syntactically
			correct.

		returns:
			desc:	An icon name.
			type:	unicode
		"""

		if self.experiment.python_workspace.check_syntax(self.get(u'_prepare'))\
			and self.experiment.python_workspace.check_syntax(
			self.get(u'_run')):
			return u'os-inline_script'
		return u'os-inline_script-syntax-error'

	def init_edit_widget(self):

		"""See qtitem."""

		from QProgEdit import QTabManager
		super(inline_script, self).init_edit_widget(stretch=False)
		self.qprogedit = QTabManager(handler=self.apply_edit_changes,
			defaultLang=u'Python', cfg=cfg,
			focusOutHandler=self.apply_edit_changes)
		self.qprogedit.addTab(u'Prepare')
		self.qprogedit.addTab(u'Run')
		# Switch to the run phase, unless there is only content for the prepare
		# phase.
		if self._run == u'' and self._prepare != u'':
			self.qprogedit.setCurrentIndex(0)
		else:
			self.qprogedit.setCurrentIndex(1)
		self.edit_vbox.addWidget(self.qprogedit)

	def edit_widget(self):

		"""See qtitem."""

		super(inline_script, self).edit_widget()
		self.qprogedit.setText(self._prepare, index=0)
		self.qprogedit.setText(self._run, index=1)

	def get_ready(self):

		"""See qtitem."""

		if self.qprogedit.isModified():
			debug.msg(u'applying pending script changes')
			self.apply_edit_changes()
			return True
		return super(inline_script, self).get_ready()
