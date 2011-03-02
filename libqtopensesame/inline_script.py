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

import libopensesame.inline_script
import libqtopensesame.qtitem
import libqtopensesame.inline_editor
import random
import re
from PyQt4 import QtCore, QtGui
import libqtopensesame.syntax_highlighter

class inline_script(libopensesame.inline_script.inline_script, libqtopensesame.qtitem.qtitem):

	def __init__(self, name, experiment, string = None):
	
		"""
		Initialize the experiment		
		"""
		
		libopensesame.inline_script.inline_script.__init__(self, name, experiment, string)
		libqtopensesame.qtitem.qtitem.__init__(self)
		self.lock = False	
		self._var_info = None
		random.seed()
		
	def apply_edit_changes(self, dummy = None, dummy2 = None, catch = True):
	
		"""
		Read the logvar table
		"""	
				
		libqtopensesame.qtitem.qtitem.apply_edit_changes(self, False)
		
		sp = str(self.textedit_prepare.edit.toPlainText())
		sr = str(self.textedit_run.edit.toPlainText())				
		
		if "\"\"\"" in sp + sr:
			if catch:
				self.experiment.notify("You're not allowed to use the \"\"\" way to define strings. This confuses OpenSesame :$ Sorry!")
				return		
			else:
				raise libopensesame.exceptions.script_error("You're not allowed to use the \"\"\" way to define strings. This confuses OpenSesame :$ Sorry!")
				
		self.prepare_script = sp
		self.run_script = sr
		self.lock = True
		self._var_info = None		
		self.experiment.main_window.refresh(self.name)		
		self.lock = False
		
		self.textedit_prepare.setModified(False)
		self.textedit_run.setModified(False)
		
	def strip_script_line(self, s):
	
		"""
		Strips the unwanted characters from the script line
		"""
		
		return s + "\n"				
				
	def init_edit_widget(self):
	
		"""
		Build the edit widget
		"""
		
		libqtopensesame.qtitem.qtitem.init_edit_widget(self, False)
		
		tabwidget_script = QtGui.QTabWidget(self._edit_widget)
		
		self.textedit_prepare = libqtopensesame.inline_editor.inline_editor(self.experiment)
		self.textedit_prepare.apply.clicked.connect(self.apply_edit_changes)
		QtCore.QObject.connect(self.textedit_prepare.edit, QtCore.SIGNAL("focusLost"), self.apply_edit_changes)		
		libqtopensesame.syntax_highlighter.syntax_highlighter(self.textedit_prepare.edit.document(), libqtopensesame.syntax_highlighter.python_keywords)
		
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
						
		self.textedit_run = libqtopensesame.inline_editor.inline_editor(self.experiment)
		self.textedit_run.apply.clicked.connect(self.apply_edit_changes)	
		QtCore.QObject.connect(self.textedit_run.edit, QtCore.SIGNAL("focusLost"), self.apply_edit_changes)
		libqtopensesame.syntax_highlighter.syntax_highlighter(self.textedit_run.edit.document(), libqtopensesame.syntax_highlighter.python_keywords)
		
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
		
		self.edit_vbox.addWidget(tabwidget_script)
		
	def edit_widget(self):
	
		"""
		Refresh the edit widget
		with current information
		and return it
		"""	
		
		libqtopensesame.qtitem.qtitem.edit_widget(self, False)				
		
		if not self.lock:
			self.textedit_prepare.edit.clear()
			self.textedit_prepare.edit.insertPlainText(self.prepare_script)
			self.textedit_run.edit.clear()
			self.textedit_run.edit.insertPlainText(self.run_script)								
								
		return self._edit_widget		
		
				
	def get_ready(self):
	
		"""
		Apply pending script changes
		"""
		
		if self.textedit_prepare.isModified() or self.textedit_run.isModified():
			if self.experiment.debug:
				print "inline_script.finalize(): applying pending Python script changes"
			self.apply_edit_changes(catch = False)
			return True
			
		return libqtopensesame.qtitem.qtitem.get_ready(self)
			
