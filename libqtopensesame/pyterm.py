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

def modules():

	"""Print version info"""

	import libqtopensesame.qtopensesame
	from libopensesame.misc import version as osversion
	s = "OpenSesame %s" % osversion
	s += "\nPython %d.%d.%d" % (sys.version_info[0], sys.version_info[1], sys.version_info[2])
	s += "\nPyQt %s" % QtCore.PYQT_VERSION_STR		
	try:
		import pygame
		s += "\nPyGame %s" % pygame.ver
	except:
		s += "\nPyGame not available"
	try:
		import OpenGL
		s += "\nPyOpenGL %s" % OpenGL.__version__
	except:
		s += "\nPyOpenGL not available"			
	try:
		import psychopy
		s += "\nPsychoPy %s" % psychopy.__version__
	except:
		s += "\nPsychoPy not available"						
	try:
		import pyglet
		s += "\nPyglet %s" % pyglet.version
	except:
		s += "\nPyglet not available"
	print s

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
		while len(self.plaintext._input) == 0 or self.plaintext._input[-1] != "\n":
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

		if s.strip() != "":
			self.plaintext.appendPlainText(s)
			QtGui.QApplication.processEvents()

class pyterm(code.InteractiveConsole):

	"""Custom Python interpreter"""

	def __init__(self, textedit=None):
	
		"""Constructor"""	
		
		global modules
	
		self._locals = {"modules" : modules}
		code.InteractiveConsole.__init__(self, self._locals)
		self.textedit = textedit
				
	def write(self, s):
	
		"""
		Simply redirect everything to the standard output
		
		Arguments:
		s -- the output string
		"""
	
		print s.replace("\n", "")

class console(QtGui.QPlainTextEdit):

	"""A nice console widget"""

	def __init__(self, parent=None):			
	
		"""
		Constructor
		
		Keywords arguments:
		parent -- parent QWidget
		"""
	
		QtGui.QPlainTextEdit.__init__(self, parent)	
		if os.name == "posix":
			font = QtGui.QFont("mono")
		else:
			font = QtGui.QFont("courier")
		self.setFont(font)		
		self.collect_input = False
		self._input = ""
		self.history = []		
		self.prompt = ">>> "
		self.pyterm = pyterm()
		self.pyterm.textedit = self
		self.setCursorWidth(8)
		self.welcome()
		self.show_prompt()
		
	def clear(self):
	
		"""Clear and draw prompt"""
	
		QtGui.QPlainTextEdit.clear(self)
		self.show_prompt()		
		
	def welcome(self):
		
		"""Print welcome information"""
	
		s = "Python %d.%d.%d" % (sys.version_info[0], sys.version_info[1], sys.version_info[2]) \
			+ "\nType \"help()\", \"copyright()\", \"credits()\" or \"license()\" for more information." \
			+ "\nType \"modules()\" for details about installed modules and version information." \
			+ "\nUse the \"print [msg]\" statement in inline_script items to print to this debug window."
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
				self._input += "\n"
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
			elif e.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:		
				self.execute()			
			elif e.key() not in [QtCore.Qt.Key_Left, QtCore.Qt.Key_Backspace]\
				or self.textCursor().positionInBlock() > len(self.prompt):
				QtGui.QPlainTextEdit.keyPressEvent(self, e)			
		
	def execute(self):
	
		"""Execute a command"""
	
		try:
			s = unicode(self.document().lastBlock().text())[len(self.prompt):]
		except:
			self.appendPlainText("Error: Command contains invalid characters")
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
						
