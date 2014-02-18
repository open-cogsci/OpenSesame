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
from libqtopensesame.ui.general_script_editor_ui import \
	Ui_widget_general_script_editor
from libqtopensesame.misc.config import cfg

class general_script_editor(QtGui.QWidget):

	"""The general script editor"""

	def __init__(self, main_window):
	
		"""
		Constructor
		
		Arguments:
		main_window -- the main window
		"""	
	
		from QProgEdit import QTabManager
		
		self.main_window = main_window
		QtGui.QWidget.__init__(self, main_window)
		self.ui = Ui_widget_general_script_editor()
		self.ui.setupUi(self)
		self.ui.qprogedit = QTabManager(handler=self._apply, defaultLang= \
			u'OpenSesame', handlerButtonText=u'Apply', cfg=cfg)
		self.ui.qprogedit.addTab(u'General script')
		self.ui.layout_vbox.addWidget(self.ui.qprogedit)
		self.main_window.theme.apply_theme(self)
		self.tab_name = '__general_script__'
		
	def _apply(self):
	
		"""Confirm and apply the script changes"""
		
		resp = QtGui.QMessageBox.question(self.main_window, _('Apply?'), \
			_('Are you sure you want to apply the changes to the general script?'), \
			QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		if resp == QtGui.QMessageBox.No:
			return	
		self.main_window.dispatch.event_regenerate.emit( \
			self.ui.qprogedit.text())
				
	def on_activate(self):
		
		"""Refresh the tab when it is activated"""
	
		self.refresh()
		
	def refresh(self):
	
		"""Refresh the contents of the general script"""
		
		self.ui.qprogedit.setText(self.main_window.experiment.to_string())
