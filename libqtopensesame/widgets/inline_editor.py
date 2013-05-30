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

import os
from PyQt4 import QtGui, QtCore
from PyQt4.Qsci import QsciScintilla, QsciScintillaBase, QsciLexerPython, \
	QSCINTILLA_VERSION
from libqtopensesame.misc import config, _
from libqtopensesame.dialogs.replace_dialog import replace_dialog
from libopensesame import debug

class python_lexer(QsciLexerPython):

	"""Handles Python syntax highlighting"""

	def __init__(self, font):

		"""
		Constructor

		Arguments:
		font -- a QFont
		"""

		QsciLexerPython.__init__(self)
		self.setDefaultFont(font)
		self.setIndentationWarning(self.Inconsistent)

class scintilla(QsciScintilla):

	"""The text editor"""

	focusLost = QtCore.pyqtSignal()

	def __init__(self, parent=None, syntax=None):

		"""
		Constructor

		Keywords arguments:
		parent -- parent QWidget
		syntax -- the syntax highlighter 'python', 'opensesame' or None
				  (default=None)
		"""

		self._parent = parent
		QsciScintilla.__init__(self, parent)
		self.syntax = syntax
		self.textChanged.connect(self._parent.setModified)
		self.refresh_layout = True
		self.cfg_ver = config.get_config("cfg_ver")
		self.setUtf8(True)
		self.setEolMode(self.EolUnix)

	def paintEvent(self, e):

		"""Optionally refresh the layout before a paint event"""

		if self.refresh_layout:
			self.set_layout()
			self.refresh_layout = False
		QsciScintilla.paintEvent(self, e)

	def set_layout(self):

		"""Initialize the editor layout"""
		
		if config.get_config("scintilla_custom_font"):
			font_family = config.get_config("scintilla_font_family")
		elif os.name == "posix":
			font_family = "mono"
		else:
			font_family = "courier"
		font = QtGui.QFont(font_family)
		font.setFixedPitch(True)
		if config.get_config("scintilla_custom_font"):
			font.setPointSize(config.get_config("scintilla_font_size"))		

		fm = QtGui.QFontMetrics(font)
		self.setFont(font)
		self.setMarginsFont(font)
		self.setTabWidth(4)

		# Set line numbers
		self.setMarginWidth(0, fm.width( "0000" ))
		self.setMarginLineNumbers(0, config.get_config( \
			"scintilla_line_numbers"))

		# Set the right margin
		self.setEdgeColumn(80)
		if config.get_config("scintilla_right_margin"):
			self.setEdgeMode(QsciScintilla.EdgeLine)
		else:
			self.setEdgeMode(QsciScintilla.EdgeNone)

		# Set EOL visibility
		self.setEolVisibility(config.get_config("scintilla_eol_visible"))

		# Set whitespace visibility
		if config.get_config("scintilla_whitespace_visible"):
			self.setWhitespaceVisibility(QsciScintilla.WsVisible)
		else:
			self.setWhitespaceVisibility(QsciScintilla.WsInvisible)

		# Set indentation guides
		self.setIndentationGuides(config.get_config( \
			"scintilla_indentation_guides"))

		# Set auto indent
		self.setAutoIndent(config.get_config("scintilla_auto_indent"))

		# Set folding
		if config.get_config("scintilla_folding"):
			self.setFolding(QsciScintilla.BoxedTreeFoldStyle)
		else:
			self.setFolding(QsciScintilla.NoFoldStyle)

		# Set brace matching
		if config.get_config("scintilla_brace_match"):
			self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
		else:
			self.setBraceMatching(QsciScintilla.NoBraceMatch)
			
		# Set syntax highlighting.
		if config.get_config("scintilla_syntax_highlighting") and \
			(self.syntax == "python" or self.syntax == "opensesame"):
			self.setLexer(python_lexer(font))
			for i in range(16): # There are properties that need to be forced
				# In Ubuntu 13.04, forcing the font actually causes the font
				# to be reset. This is an ugly hack to prevent that from
				# happening, assuming that this regression is due to the version
				# of Qscintilla.
				if QSCINTILLA_VERSION < 132865:
					self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, i, \
						font.family())
				self.SendScintilla(QsciScintilla.SCI_STYLESETSIZE, i, \
					font.pointSize())
		else:
			self.setLexer(None)
			self.SendScintilla(QsciScintilla.SCI_CLEARDOCUMENTSTYLE)				

	def toPlainText(self):

		"""
		Convenience function for compatibility with QPlainTextEdit

		Returns:
		A unicode string with the editor contents
		"""

		return unicode(self.text())

	def setPlainText(self, s, set_modified=False):

		"""
		(For compatibility with QPlainTextEdit)

		Arguments:
		s -- the new contents of the editor

		Keyword arguments:
		set_modified -- indicates whether the modified flag should be set
						(default=False)
		"""

		if not set_modified:
			_m = self.isModified()
			self.textChanged.disconnect()
		self.setText(self._parent.experiment.unistr(s))
		if not set_modified:
			self.textChanged.connect(self._parent.setModified)
			self._parent.setModified(_m)
		else:
			self._parent.setModified(True)

	def focusOutEvent(self, e):

		"""Send a focusLost signal if we lose focus"""

		self.emit(QtCore.SIGNAL("focusLost"))
		self.focusLost.emit()
		QsciScintilla.focusOutEvent(self, e)

	def focusInEvent(self, e):

		"""Refresh the layout on a focus in event"""

		# Only update the layout if the config is outdated
		if self.cfg_ver != config.get_config("cfg_ver"):
			self.set_layout()
			self.cfg_ver = config.get_config("cfg_ver")
		QsciScintilla.focusInEvent(self, e)

	def keyPressEvent(self, e):

		"""
		Captures keypresses to implement apply (Alt+A

		Arguments:
		e -- a keypress even
		"""

		# Process the Alt + A shortcut to apply changes
		if e.key() == QtCore.Qt.Key_A and \
			e.modifiers() == QtCore.Qt.AltModifier:
			self._parent.apply.clicked.emit(True)
			return
		if e.key() == QtCore.Qt.Key_F and \
			e.modifiers() == QtCore.Qt.ControlModifier:
			self._parent.perform_replace()
			return
		QsciScintilla.keyPressEvent(self, e)

class inline_editor(QtGui.QFrame):

	"""The wrapper containing the editor and additional controls"""

	changed = QtCore.pyqtSignal()
	applied = QtCore.pyqtSignal()

	def __init__(self, experiment, notification=None, syntax=None):

		"""
		Constructor

		Arguments:
		experiment -- the opensesame experiment

		Keywords arguments:
		notification -- a short notification message (default=None)
		syntax -- the syntax highlighter 'python', 'opensesame' or None
				  (default=None)
		main_window -- the QtOpenSesame main window
		"""

		QtGui.QFrame.__init__(self)

		self.experiment = experiment
		self.setFrameStyle(QtGui.QFrame.NoFrame)
		self.edit = scintilla(self, syntax=syntax)
		self.edit.focusLost.connect(self.changed.emit)

		self.search = QtGui.QLineEdit()
		self.search.setMaximumWidth(150)
		self.search.returnPressed.connect(self.perform_search)
		self.search.setToolTip(_("Enter a search term"))

		self.search_button = QtGui.QPushButton(self.experiment.icon("search"), \
			"")
		self.search_button.setIconSize(QtCore.QSize(16, 16))
		self.search_button.setToolTip(_("Search"))
		self.search_button.clicked.connect(self.perform_search)

		self.replace_button = QtGui.QPushButton( \
			self.experiment.icon("replace"), "")
		self.replace_button.setIconSize(QtCore.QSize(16, 16))
		self.replace_button.setToolTip(_("Replace"))
		self.replace_button.clicked.connect(self.perform_replace)

		self.indent_button = QtGui.QPushButton(self.experiment.icon("indent"), \
			"")
		self.indent_button.setIconSize(QtCore.QSize(16, 16))
		self.indent_button.setToolTip(_("Indent one level (tab)"))
		self.indent_button.clicked.connect(self.indent)

		self.unindent_button = QtGui.QPushButton( \
			self.experiment.icon("unindent"), "")
		self.unindent_button.setIconSize(QtCore.QSize(16, 16))
		self.unindent_button.setToolTip(_("Unindent one level (super + tab)"))
		self.unindent_button.clicked.connect(self.unindent)

		self.modified = self.experiment.label_image("unsaved_changes")
		self.modified.setToolTip(_("Press Alt + A to apply unsaved changes"))
		self.modified.hide()

		self.apply = QtGui.QPushButton(self.experiment.icon("apply"), \
			_("Apply"))
		self.apply.setToolTip(_("Press Alt + A to apply unsaved changes"))
		self.apply.setIconSize(QtCore.QSize(16, 16))
		self.apply.clicked.connect(self._apply)

		search_widget = QtGui.QWidget()
		search_hbox = QtGui.QHBoxLayout(search_widget)
		search_hbox.addWidget(self.search)
		search_hbox.addWidget(self.search_button)
		search_hbox.addWidget(self.replace_button)
		search_hbox.addWidget(self.indent_button)
		search_hbox.addWidget(self.unindent_button)
		if notification != None:
			search_hbox.addWidget(QtGui.QLabel("<small>%s</small>" % \
				notification))
		search_hbox.addStretch()
		search_hbox.addWidget(self.modified)
		search_hbox.addWidget(self.apply)
		search_hbox.setContentsMargins(0, 0, 0, 0)

	 	main_widget = QtGui.QFrame()
	 	main_widget.setFrameStyle(QtGui.QFrame.StyledPanel | \
			QtGui.QFrame.Sunken)
		main_hbox = QtGui.QHBoxLayout(main_widget)
		main_hbox.setSpacing(0)
		main_hbox.setMargin(0)
		main_hbox.addWidget(self.edit)

		vbox = QtGui.QVBoxLayout(self)
		vbox.addWidget(main_widget)
		vbox.addWidget(search_widget)
		vbox.setSpacing(4)
		vbox.setMargin(0)

		self.toolbar_hbox = search_hbox

	def _apply(self):

		"""When apply is clicked, two signals are sent"""

		self.changed.emit()
		self.applied.emit()

	def perform_search(self, event=None, term=None):

		"""
		Select the text based on the search term

		Keywords arguments:
		term -- the search term or None to use the search input (default=None)

		Returns:
		True if the term was found, False otherwise
		"""

		if term == None:
			term = self.search.text()
		return self.edit.findFirst(term, False, False, False, True)

	def perform_replace(self):

		"""Shows the search/replace dialog"""

		replace_dialog(self).exec_()

	def getText(self):

		"""
		Returns:
		The contents of the editor
		"""

		return self.edit.toPlainText()

	def setText(self, text):

		"""
		Sets the contents of the editor

		Arguments:
		text -- the new contents
		"""

		self.edit.setPlainText(text)

	def isModified(self):

		"""
		Check if the editor has been modified

		Returns:
		True if modified, False otherwise
		"""

		return self.edit.isModified()

	def setModified(self, modified=True):

		"""
		Set the modified status of the editor

		Keywords arguments:
		modified -- the modified status (default=True)
		"""

		self.modified.setVisible(modified)
		self.edit.setModified(modified)
		if modified and not self.experiment.main_window.unsaved_changes:
			self.experiment.main_window.set_unsaved()

	def indent(self):

		"""Indent the current line or selection by one level"""

		self.selection_do(self.edit.indent)

	def unindent(self):

		"""Indent the current line or selection by one level"""

		self.selection_do(self.edit.unindent)

	def selection_do(self, func):

		"""
		Call a function for the current line or each line from the selection

		Arguments:
		func -- the function to be called
		"""

		lf, _if, lt, it = self.edit.getSelection()
		if lf < 0:
			lf = self.edit.getCursorPosition()[0]
			lt = lf
		for i in range(lf, lt+1):
			func(i)
