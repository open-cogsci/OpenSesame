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

from libopensesame import debug
import libopensesame.inline_script
from libqtopensesame.items import qtitem
from libqtopensesame.misc import _
from libqtopensesame.widgets import inline_editor
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

	def apply_edit_changes(self, dummy=None, dummy2=None, catch=True):

		"""
		Applies the controls.

		Keywords arguments:
		dummy	--	A dummy argument. (default=None)
		dummy2	--	A dummy argument. (default=None)
		catch	--	A deprecated argument. (default=True)
		"""

		qtitem.qtitem.apply_edit_changes(self, False)
		sp = self.textedit_prepare.edit.toPlainText()
		sr = self.textedit_run.edit.toPlainText()
		self.set(u'_prepare', sp)
		self.set(u'_run', sr)
		self.lock = True
		self._var_info = None
		self.experiment.main_window.refresh(self.name)
		self.lock = False
		self.textedit_prepare.setModified(False)
		self.textedit_run.setModified(False)

	def init_edit_widget(self):

		"""Constructs the GUI controls."""

		qtitem.qtitem.init_edit_widget(self, False)

		tabwidget_script = QtGui.QTabWidget(self._edit_widget)
		py_ver = u'Python %d.%d.%d' % (sys.version_info[0], \
			sys.version_info[1], sys.version_info[2])
			
		# Construct prepare editor
		self.textedit_prepare = inline_editor.inline_editor(self.experiment, \
			notification=py_ver, syntax=u'python')
		self.textedit_prepare.apply.clicked.connect(self.apply_edit_changes)
		QtCore.QObject.connect(self.textedit_prepare.edit, QtCore.SIGNAL( \
			"focusLost"), self.apply_edit_changes)
		hbox = QtGui.QHBoxLayout()
		hbox.addStretch()
		hbox.setContentsMargins(0, 0, 0, 0)
		hbox_widget = QtGui.QWidget()
		hbox_widget.setLayout(hbox)
		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(self.textedit_prepare)
		vbox.addWidget(hbox_widget)
		widget = QtGui.QWidget()
		widget.setLayout(vbox)
		tabwidget_script.addTab(widget, self.experiment.icon( \
			u'inline_script'), _(u'Prepare phase'))

		# Construct run editor
		self.textedit_run = inline_editor.inline_editor(self.experiment, \
			notification=py_ver, syntax=u'python')
		self.textedit_run.apply.clicked.connect(self.apply_edit_changes)
		QtCore.QObject.connect(self.textedit_run.edit, QtCore.SIGNAL( \
			"focusLost"), self.apply_edit_changes)
		hbox = QtGui.QHBoxLayout()
		hbox.addStretch()
		hbox.setContentsMargins(0, 0, 0, 0)
		hbox_widget = QtGui.QWidget()
		hbox_widget.setLayout(hbox)
		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(self.textedit_run)
		vbox.addWidget(hbox_widget)
		widget = QtGui.QWidget()
		widget.setLayout(vbox)
		tabwidget_script.addTab(widget, self.experiment.icon( \
			u'inline_script'), _(u'Run phase'))

		# Switch to the run script by default, unless there is only content for
		# the prepare script.
		if self._run == u'' and self._prepare != u'':
			tabwidget_script.setCurrentIndex(0)
		else:
			tabwidget_script.setCurrentIndex(1)
			
		# Add all widgets to the edit_vbox
		self.edit_vbox.addWidget(tabwidget_script)

	def edit_widget(self):

		"""
		Updates the GUI controls.

		Returns:
		The control QWidget.
		"""

		qtitem.qtitem.edit_widget(self, False)
		if not self.lock:
			self.textedit_prepare.edit.setPlainText(	self._prepare)
			self.textedit_run.edit.setPlainText(self._run)
		return self._edit_widget

	def get_ready(self):

		"""Applies pending script changes."""

		if self.textedit_prepare.isModified() or self.textedit_run.isModified():
			debug.msg(u'applying pending script changes')
			self.apply_edit_changes(catch = False)
			return True
		return qtitem.qtitem.get_ready(self)

