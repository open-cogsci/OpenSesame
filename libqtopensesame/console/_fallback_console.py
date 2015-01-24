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
import code
import sys
import time
from PyQt4 import QtGui, QtCore
from libopensesame import debug
from libqtopensesame.misc import _
from libqtopensesame.misc.config import cfg
from libqtopensesame.console._base_console import base_console

class pyterm(code.InteractiveConsole):

	"""
	desc:
		Custom Python interpreter.
	"""

	def __init__(self, textedit):

		"""
		desc:
			Constructor.

		arguments:
			textedit:
				type: fallback_console.
		"""

		self._locals = {}
		self.textedit = textedit
		code.InteractiveConsole.__init__(self, self._locals)

	def set_locals(self, _locals={}):

		"""
		desc:
			Updates the globals dictionary for the console's workspace.

		keywords:
			_globals:
				desc:	A globals dictionary
				type:	dict
		"""

		self._locals.clear()
		self._locals.update(_locals)

class fallback_console(base_console, QtGui.QPlainTextEdit):

	"""
	desc:
		A basic debug window.
	"""

	def __init__(self, main_window):

		"""
		desc:
			Constructor.

		arguments:
			main_window:	The main window object.
		"""

		super(fallback_console, self).__init__(main_window)
		self.collect_input = False
		self._input = u""
		self.history = []
		self.prompt = u">>> "
		self.pyterm = pyterm(self)
		self.setCursorWidth(8)
		self.setTheme()
		self.welcome()
		self.show_prompt()

	def setTheme(self):

		"""
		desc:
			Sets the theme, based on the QProgEdit settings.
		"""

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
		desc:
			Processes focus-in events to set the style of the debug window.

		arguments:
			e:
				type:	QFocusEvent
		"""

		self.setTheme()
		super(fallback_console, self).focusInEvent(e)

	def clear(self):

		"""See base_console."""

		QtGui.QPlainTextEdit.clear(self)
		self.show_prompt()

	def welcome(self):

		"""
		desc:
			Prints welcome information.
		"""

		s = u"Python %d.%d.%d" % (sys.version_info[0], sys.version_info[1], \
			sys.version_info[2]) \
			+ u"\nType \"help()\", \"copyright()\", \"credits()\" or \"license()\" for more information." \
			+ u"\nType \"modules()\" for details about installed modules and version information." \
			+ u"\nUse the \"print([msg])\" statement in inline_script items to print to this debug window."
		self.insertPlainText(s)

	def show_prompt(self, suffix=""):

		"""See base_console."""

		self.appendPlainText(self.prompt+suffix)

	def keyPressEvent(self, e):

		"""
		desc:
			Handles key presses.

		arguments:
			e:
				type:	QKeyEvent
		"""

		# Emulate the standard input
		if self.collect_input:
			if e.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:
				self._input += u"\n"
			else:
				self._input += str(e.text())
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

		"""
		desc:
			Executes a command.
		"""

		try:
			s = str(self.document().lastBlock().text())[len(self.prompt):]
		except:
			self.appendPlainText( \
				_(u"Error: Command contains invalid characters"))
			self.show_prompt()
			return
		if len(s) > 0:
			self.history.append(s)
		self.capture_stdout()
		self.pyterm.push(s)
		self.release_stdout()
		self.show_prompt()

	def jump_to_end(self):

		"""
		desc:
			Restore the cursor to the end of the textedit.
		"""

		c = self.textCursor()
		if not c.atEnd() and c.blockNumber()+1 < self.document().blockCount():
			c.movePosition(QtGui.QTextCursor.End)
			self.setTextCursor(c)

	def readline(self):

		"""
		desc:
			Implements text input.

		returns:
			The input text.
		"""

		self._input = u''
		self.collect_input = True
		while len(self._input) == 0 or self._input[-1] != u'\n':
			time.sleep(0.01)
			QtGui.QApplication.processEvents()
		self.collect_input = False
		return self._input

	def write(self, s):

		"""See base_console."""

		s = str(s)
		if s.strip() != u'':
			self.appendPlainText(s)
			QtGui.QApplication.processEvents()

	def set_workspace_globals(self, _globals={}):

		"""See base_console."""

		_globals = _globals.copy()
		_globals.update(self.default_globals())
		self.pyterm.set_locals(_globals)

	def setup(self, main_window):

		"""See base_subcomponent."""

		super(fallback_console, self).setup(main_window)
		self.set_workspace_globals()
