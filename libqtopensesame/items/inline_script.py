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
from libqtopensesame.widgets import inline_editor
import random
import re
import sys
from PyQt4 import QtCore, QtGui

class inline_script(libopensesame.inline_script.inline_script, qtitem.qtitem):

	"""The inline_script GUI controls"""

	def __init__(self, name, experiment, string=None):

		"""
		Constructor

		Arguments:
		name -- the item name
		experiment -- the experiment

		Keywords arguments:
		string -- definition string
		"""

		libopensesame.inline_script.inline_script.__init__(self, name, experiment, string)
		qtitem.qtitem.__init__(self)
		self.lock = False
		self._var_info = None
		random.seed()

	def apply_edit_changes(self, dummy=None, dummy2=None, catch=True):

		"""
		Apply the controls

		Keywords arguments:
		dummy -- dummy argument
		dummy2 -- dummy argument
		catch -- deprecated argument
		"""

		qtitem.qtitem.apply_edit_changes(self, False)

		sp = str(self.textedit_prepare.edit.toPlainText())
		sr = str(self.textedit_run.edit.toPlainText())

		self.set("_prepare", sp)
		self.set("_run", sr)
		self.lock = True
		self._var_info = None
		self.experiment.main_window.refresh(self.name)
		self.lock = False

		self.textedit_prepare.setModified(False)
		self.textedit_run.setModified(False)

	def init_edit_widget(self):

		"""Construct the GUI controls"""

		qtitem.qtitem.init_edit_widget(self, False)

		tabwidget_script = QtGui.QTabWidget(self._edit_widget)
		py_ver = "Python %d.%d.%d" % (sys.version_info[0], sys.version_info[1], sys.version_info[2])

		self.textedit_prepare = inline_editor.inline_editor(self.experiment, notification=py_ver, syntax="python")
		self.textedit_prepare.apply.clicked.connect(self.apply_edit_changes)
		QtCore.QObject.connect(self.textedit_prepare.edit, QtCore.SIGNAL("focusLost"), self.apply_edit_changes)

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

		tabwidget_script.addTab(widget, self.experiment.icon("inline_script"), "Prepare phase")

		self.textedit_run = inline_editor.inline_editor(self.experiment, notification=py_ver, syntax="python")
		self.textedit_run.apply.clicked.connect(self.apply_edit_changes)
		QtCore.QObject.connect(self.textedit_run.edit, QtCore.SIGNAL("focusLost"), self.apply_edit_changes)

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

		tabwidget_script.addTab(widget, self.experiment.icon("inline_script"), "Run phase")

		# Switch to the run script by default, unless there is only content for
		# the prepare script.
		if self._run == "" and self._prepare != "":
			tabwidget_script.setCurrentIndex(0)
		else:
			tabwidget_script.setCurrentIndex(1)

		self.edit_vbox.addWidget(tabwidget_script)

	def edit_widget(self):

		"""
		Update the GUI controls

		Returns:
		The control QWidget
		"""

		qtitem.qtitem.edit_widget(self, False)
		if not self.lock:
			self.textedit_prepare.edit.setPlainText(self.unsanitize(str(self._prepare)))
			self.textedit_run.edit.setPlainText(self.unsanitize(str(self._run)))
		return self._edit_widget

	def get_ready(self):

		"""Apply pending script changes"""

		if self.textedit_prepare.isModified() or self.textedit_run.isModified():
			debug.msg("applying pending script changes")
			self.apply_edit_changes(catch = False)
			return True
		return qtitem.qtitem.get_ready(self)

