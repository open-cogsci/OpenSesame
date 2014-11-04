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

import code
import sys
import os
import time
from PyQt4 import QtGui, QtCore
from libopensesame import debug
from libqtopensesame.misc import _
from libqtopensesame.misc.config import cfg

def modules():

	"""Print version info"""

	from libopensesame.misc import module_versions
	print(module_versions())

class output_buffer:

	"""Used to capture the standard output and reroute it to the debug window"""

	def __init__(self, plaintext):

		"""
		Constructor

		Keyword arguments:
		plaintext -- a QPlainTextEdit widget
		"""

		self.plaintext = plaintext

	def readline(self):

		"""Input is crudely supported through an input dialog"""

		self.plaintext._input = ""
		self.plaintext.collect_input = True
		while len(self.plaintext._input) == 0 or self.plaintext._input[-1] != \
			"\n":
			time.sleep(0.01)
			QtGui.QApplication.processEvents()
		self.plaintext.collect_input = False
		return self.plaintext._input

	def write(self, s):

		"""
		Write a string

		Arguments:
		s -- a string
		"""

		if isinstance(s, str):
			s = s.decode(u'utf-8', u'replace')
		if s.strip() != u'':
			self.plaintext.appendPlainText(s)
			QtGui.QApplication.processEvents()

	def flush(self):

		"""Dummy flush function for compatibility."""

		pass

class pyterm(code.InteractiveConsole):

	"""Custom Python interpreter"""

	def __init__(self, parent, textedit=None):

		"""Constructor"""

		self._locals = {}
		self.parent = parent
		self.set_workspace_globals()
		code.InteractiveConsole.__init__(self, self._locals)
		self.textedit = textedit

	def write(self, s):

		"""
		Simply redirect everything to the standard output.

		Arguments:
		s -- the output string
		"""

		if isinstance(s, str):
			s = s.decode(u'utf-8', u'replace')
		print(s.replace(u'\n', u''))

	def set_workspace_globals(self, _globals={}):

		"""
		desc:
			Updates the globals dictionary for the console's workspace.

		keywords:
			_globals:
				desc:	A globals dictionary
				type:	dict
		"""

		global modules
		self._locals.clear()
		self._locals[u'modules'] = modules
		self._locals[u'qtopensesame'] = self.get_qtopensesame
		self._locals[u'cfg'] = self.get_cfg
		self._locals.update(_globals)

	def get_qtopensesame(self):

		"""
		desc:
			A getter for the main window.

		returns:
			type:	qtopensesame
		"""

		return self.parent.parent().parent().parent()

	def get_cfg(self):

		"""
		desc:
			A getter for the config object.

		returns:
			type:	config
		"""

		from libqtopensesame.misc.config import cfg
		return cfg

class console(QtGui.QPlainTextEdit):

	"""A nice console widget"""

	def __init__(self, parent=None):

		"""
		Constructor

		Keywords arguments:
		parent -- parent QWidget
		"""

		QtGui.QPlainTextEdit.__init__(self, parent)
		self.collect_input = False
		self._input = u""
		self.history = []
		self.prompt = u">>> "
		self.pyterm = pyterm(parent)
		self.pyterm.textedit = self
		self.setCursorWidth(8)
		self.setTheme()
		self.welcome()
		self.show_prompt()

	def setTheme(self):

		"""Sets the theme, based on the QProgEdit settings."""

		self.setFont(QtGui.QFont(cfg.qProgEditFontFamily, \
			cfg.qProgEditFontSize))
		from QProgEdit import QColorScheme
		if not hasattr(QColorScheme, cfg.qProgEditColorScheme):
			debug.msg(u'Failed to set debug-output colorscheme')
			return
		cs = getattr(QColorScheme, cfg.qProgEditColorScheme)
		if u'Background' not in cs:
			background = u'white'
		else:
			background = cs[u'Background']
		if u'Default' not in cs:
			foreground = u'black'
		else:
			foreground = cs[u'Default']
		self.setStyleSheet(u'background-color: "%s"; color: "%s";' \
			% (background, foreground))

	def focusInEvent(self, e):

		"""
		Process focus-in events to set the style of the debug window.

		Arguments:
		e		--	A focus-in event.
		"""

		self.setTheme()
		super(console, self).focusInEvent(e)

	def clear(self):

		"""Clear and draw prompt"""

		QtGui.QPlainTextEdit.clear(self)
		self.show_prompt()

	def welcome(self):

		"""Print welcome information"""

		s = u"Python %d.%d.%d" % (sys.version_info[0], sys.version_info[1], \
			sys.version_info[2]) \
			+ u"\nType \"help()\", \"copyright()\", \"credits()\" or \"license()\" for more information." \
			+ u"\nType \"modules()\" for details about installed modules and version information." \
			+ u"\nUse the \"print([msg])\" statement in inline_script items to print to this debug window."
		self.insertPlainText(s)

	def show_prompt(self, suffix=""):

		"""Show a prompt"""

		self.appendPlainText(self.prompt+suffix)

	def keyPressEvent(self, e):

		"""
		Handle key presses

		Arguments:
		e -- a QKeyEvent
		"""

		# Emulate the standard input
		if self.collect_input:
			if e.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:
				self._input += u"\n"
			else:
				self._input += unicode(e.text())
				QtGui.QPlainTextEdit.keyPressEvent(self, e)

		# Emulate the console
		else:
			self.jump_to_end()
			if e.key() == QtCore.Qt.Key_Up:
				if len(self.history) > 0:
					cmd = self.history.pop()
					self.show_prompt(cmd)
					self.history.insert(0, cmd)
			elif e.key() == QtCore.Qt.Key_Home:
				cursor = self.textCursor()
				cursor.setPosition(self.textCursor().block().position() \
					+len(self.prompt))
				self.setTextCursor(cursor)
			elif e.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:
				self.execute()
			elif e.key() not in [QtCore.Qt.Key_Backspace, QtCore.Qt.Key_Home, \
				QtCore.Qt.Key_Up, QtCore.Qt.Key_Down] and e.key() != \
				QtCore.Qt.Key_Left or self.textCursor().positionInBlock() > \
				len(self.prompt):
				QtGui.QPlainTextEdit.keyPressEvent(self, e)

	def execute(self):

		"""Execute a command"""

		try:
			s = unicode(self.document().lastBlock().text())[len(self.prompt):]
		except:
			self.appendPlainText( \
				_(u"Error: Command contains invalid characters"))
			self.show_prompt()
			return
		if len(s) > 0:
			self.history.append(s)
		buf = output_buffer(self)
		sys.stdout = buf
		sys.stdin = buf
		self.pyterm.push(s)
		sys.stdout = sys.__stdout__
		sys.stdin = sys.__stdin__
		self.show_prompt()

	def jump_to_end(self):

		"""Restore the cursor to the end of the textedit"""

		c = self.textCursor()
		if not c.atEnd() and c.blockNumber()+1 < self.document().blockCount():
			c.movePosition(QtGui.QTextCursor.End)
			self.setTextCursor(c)

