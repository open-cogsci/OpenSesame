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
from libopensesame.exceptions import osexception
from libqtopensesame.items.experiment import experiment
from libqtopensesame.widgets.base_widget import base_widget
from libqtopensesame.misc.config import cfg
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'general_script_editor', category=u'core')

class general_script_editor(base_widget):

	"""
	desc:
		The general script editor.
	"""

	def __init__(self, main_window):

		"""
		desc:
			Constructor.

		arguments:
			main_window:	A qtopensesame object.
		"""

		from QProgEdit import QTabManager
		super(general_script_editor, self).__init__(main_window,
			ui=u'widgets.general_script_editor')
		self.ui.qprogedit = QTabManager(handlerButtonText=u'Apply', cfg=cfg)
		self.ui.qprogedit.handlerButtonClicked.connect(self._apply)
		self.ui.qprogedit.addTab(u'General script').setLang(u'OpenSesame')
		self.ui.layout_vbox.addWidget(self.ui.qprogedit)
		self.tab_name = u'__general_script__'

	def _apply(self):

		"""
		desc:
			Confirms and applies the script changes.
		"""

		resp = QtWidgets.QMessageBox.question(self.main_window, _(u'Apply?'),
			_(u'Are you sure you want to apply the changes to the general script?'),
			QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
		if resp == QtWidgets.QMessageBox.No:
			return
		self.main_window.regenerate(self.ui.qprogedit.text())

	def on_activate(self):

		"""
		desc:
			Refreshes the tab when it is activated.
		"""

		self.refresh()

	def refresh(self):

		"""
		desc:
			Refreshes the contents of the general script.
		"""

		self.ui.qprogedit.setText(self.main_window.experiment.to_string())
