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
from libqtopensesame.misc import _
from libopensesame.exceptions import osexception
from libqtopensesame.items.experiment import experiment
from libqtopensesame.widgets.base_widget import base_widget
from libqtopensesame.misc.config import cfg

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

		resp = QtGui.QMessageBox.question(self.main_window, _(u'Apply?'),
			_(u'Are you sure you want to apply the changes to the general script?'),
			QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		if resp == QtGui.QMessageBox.No:
			return
		try:
			exp = experiment(self.main_window, name=self.experiment.title,
				string=self.ui.qprogedit.text(),
				pool_folder=self.experiment.pool_folder,
				experiment_path=self.experiment.experiment_path,
				resources=self.experiment.resources)
		except osexception as e:
			self.notify(e.html())
			self.main_window.print_debug_window(e)
			return
		self.main_window.experiment = exp
		self.main_window.tabwidget.close_all()
		self.main_window.tabwidget.open_general()
		self.experiment.build_item_tree()
		self.extension_manager.fire(u'regenerate')

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
