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

from libopensesame import debug, misc
import libopensesame.inline_script
from libqtopensesame.items import qtitem
from libqtopensesame.misc import _, config
import random
import re
import sys
from PyQt4 import QtCore, QtGui

class inline_script(libopensesame.inline_script.inline_script, qtitem.qtitem):

	"""The inline_script GUI controls"""

	def __init__(self, name, experiment, string=None):

		"""
		Constructor.

		Arguments:
		name 		--	The item name.
		experiment	--	The experiment object.

		Keywords arguments:
		string		--	A definition string. (default=None)
		"""

		libopensesame.inline_script.inline_script.__init__(self, name, \
			experiment, string)
		qtitem.qtitem.__init__(self)
		self.lock = False
		self._var_info = None

	def apply_edit_changes(self, **args):

		"""
		Applies the controls.

		Keywords arguments:
		args	--	A dictionary to accept unused keyword arguments.
		"""

		qtitem.qtitem.apply_edit_changes(self, False)
		sp = self.qprogedit.text(index=0)
		sr = self.qprogedit.text(index=1)
		self.set(u'_prepare', sp)
		self.set(u'_run', sr)
		self.lock = True
		self._var_info = None
		self.experiment.main_window.refresh(self.name)
		self.lock = False

	def init_edit_widget(self):

		"""Constructs the GUI controls."""
		
		from QProgEdit import QTabManager
		qtitem.qtitem.init_edit_widget(self, False)
		self.qprogedit = QTabManager(handler=self.apply_edit_changes, \
			defaultLang=u'Python')
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

		"""
		Updates the GUI controls.

		Returns:
		The control QWidget.
		"""

		qtitem.qtitem.edit_widget(self, False)
		if not self.lock:
			self.qprogedit.setText(self._prepare, index=0)
			self.qprogedit.setText(self._run, index=1)
		return self._edit_widget

	def get_ready(self):

		"""Applies pending script changes."""

		if self.qprogedit.isModified():
			debug.msg(u'applying pending script changes')
			self.apply_edit_changes(catch=False)
			return True
		return qtitem.qtitem.get_ready(self)

