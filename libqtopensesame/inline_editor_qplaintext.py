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

This reimplementation of QPlainTextEdit is slightly adapted from
<http://john.nachtimwald.com/2009/08/19/better-qplaintextedit-with-line-numbers/>
and is available under the MIT license

The MIT License

Copyright (c) 2009 John Schember <john@nachtimwald.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE

NOTE
This editor will be replaced with the inline_editor_qscintilla. Right now, it
serves as a fallback only.
"""
 
from PyQt4.Qt import QFrame
from PyQt4.Qt import QHBoxLayout
from PyQt4.Qt import QPainter
from PyQt4.Qt import QPlainTextEdit
from PyQt4.Qt import QRect
from PyQt4.Qt import QTextEdit
from PyQt4.Qt import QTextFormat
from PyQt4.Qt import QVariant
from PyQt4.Qt import QWidget
from PyQt4.Qt import Qt
from PyQt4 import QtGui, QtCore
import os
from libqtopensesame import replace_dialog_ui
from libqtopensesame.syntax_highlighter import syntax_highlighter, opensesame_keywords, python_keywords

class replace_dialog(QtGui.QDialog):

	"""
	A search/ replace dialog
	"""

	def __init__(self, parent = None):
		
		"""
		Constructore
		"""
							
		QtGui.QDialog.__init__(self, parent)	
		self.edit = parent.edit
		self.ui = replace_dialog_ui.Ui_Dialog()
		self.ui.setupUi(self)	
		self.adjustSize()	
		
		self.ui.edit_search.setText(parent.search.text())
		
		self.ui.button_search.clicked.connect(self.search)
		self.ui.button_replace.clicked.connect(self.replace)
		self.ui.button_replace_all.clicked.connect(self.replace_all)
		
	def search(self):
	
		"""
		Select text matching the current selection. Returns True
		if the selection has been found, false otherwise
		"""
	
		if not self.edit.find(self.ui.edit_search.text()):
			self.edit.moveCursor(QtGui.QTextCursor.Start)
			return self.edit.find(self.ui.edit_search.text())
			
		return True

	def replace(self):
	
		"""
		Replace the current selection
		"""
	
		c = self.edit.textCursor()					
		p = c.position()	
			
		if c.hasSelection():
			c.beginEditBlock()										
			c.removeSelectedText()			
			c.insertText(self.ui.edit_replace.text())
			c.endEditBlock()
		else:
			QtGui.QMessageBox.information(self, "No selection", "No text has been selected. You can search and select text using the 'Search' button.")
		
	def replace_all(self):
	
		"""
		Iteratively replace all occurences
		"""
	
		i = 0
		while self.search():
			self.replace()
			i += 1
			
		QtGui.QMessageBox.information(self, "Replace all", "%d occurence(s) have been replaced" % i)
 
class inline_editor(QFrame):

	"""
	A wrapper class around several widgets, which
	together make up a full fledged text editor
	"""
 
	class NumberBar(QWidget):

		"""
		The line numbers
		"""

		def __init__(self, edit):
		
			"""
			The constructor of the line numbers
			"""
		
			QWidget.__init__(self, edit)
	 
			self.edit = edit
			self.adjustWidth(1)
	 
		def paintEvent(self, event):
		
			"""
			Paint the numberbar (handled by the editor)
			"""
		
			self.edit.numberbarPaint(self, event)
			QWidget.paintEvent(self, event)
	 
		def adjustWidth(self, count):
		
			"""
			Adjust the width based on the number of lines
			"""
		
			width = self.fontMetrics().width(unicode(count))
			if self.width() != width:
				self.setFixedWidth(width)
	 
		def updateContents(self, rect, scroll):
		
			"""
			Handle scrolling
			"""
		
			if scroll:
				self.scroll(0, scroll)
			else:
				self.update()
 
 
	class PlainTextEdit(QPlainTextEdit):
 
		def __init__(self, editor):
		
			"""
			The editor part
			"""
		
			QPlainTextEdit.__init__(self, editor)
	 
	 		self.editor = editor
			self.setFrameStyle(QFrame.NoFrame)
			self.highlight()
			
			# Set a monospace font with a tab indent of 4 characters
			if os.name == "posix":
				self.font = QtGui.QFont("mono")
			else:
				self.font = QtGui.QFont("courier")
			self.setFont(self.font)
			self.setTabStopWidth(self.fontMetrics().width(unicode("1234")))
			
			self.cursorPositionChanged.connect(self.highlight)
	 
		def highlight(self):
		
			"""
			Highlight the current line
			"""
		
			hi_selection = QTextEdit.ExtraSelection()
	 
			hi_selection.format.setBackground(self.palette().alternateBase())
			hi_selection.format.setProperty(QTextFormat.FullWidthSelection, QVariant(True))
			hi_selection.cursor = self.textCursor()
			hi_selection.cursor.clearSelection()
	 
			self.setExtraSelections([hi_selection])
			
		def indent(self):
		
			"""
			Indent the text one level
			"""
	
			c = self.textCursor()
			p = c.position()	
			c.beginEditBlock()									
			
			if c.hasSelection():			
				# Prepend a tab and replace all add a new tab after every newline
				s = "\t" + unicode(c.selection().toPlainText()).replace("\n", "\n\t")
				c.insertText(s)
				c.setPosition(c.position() - len(s))
				c.setPosition(c.position() + len(s), QtGui.QTextCursor.KeepAnchor)
				
			else:			
				# If there is no selection, simply insert a tab
				self.insertPlainText("\t")				
			
			c.endEditBlock()								
			self.setTextCursor(c)
			self.setFocus()
			self.editor.setModified(True)
		
		def unindent(self):
	
			"""
			Unindents selected text one level
			"""
	
			c = self.textCursor()
			p = c.position()
			c.beginEditBlock()					
			
			if c.hasSelection():

				# Remove the tabs at the beginning of each line and the tab leading the selection
				s = unicode(c.selection().toPlainText()).replace("\n\t", "\n")			
				if s[0] == "\t":
					s = s[1:]
				c.insertText(s)
				c.setPosition(c.position() - len(s))
				c.setPosition(c.position() + len(s), QtGui.QTextCursor.KeepAnchor)
				
			else:						
				# Delete a tab if it leads the current line
				block = c.block()
				c.movePosition(QtGui.QTextCursor.StartOfLine)
				s = unicode(c.block().text())
				if len(s) > 0 and s[0] == "\t":
					c.deleteChar()				
				c.setPosition(p)					
						
			c.endEditBlock()						
			self.setTextCursor(c)
			self.setFocus()
			self.editor.setModified(True)
						
		def keyPressEvent(self, e):
		
			"""
			Captures keypresses to implement selection indentation
			and auto indentation
			
			Arguments:
			e -- a keypress even
			"""			

			# Process the Alt + A shortcut to apply changes
			if e.key() == QtCore.Qt.Key_A and e.modifiers() == QtCore.Qt.AltModifier:
				self.editor.apply.clicked.emit(True)
				return
				
			if e.key() not in range(QtCore.Qt.Key_Home, QtCore.Qt.Key_Direction_R):		
				self.editor.setModified(True)

			c = self.textCursor()			
			if not c.hasSelection():
			
				# Auto indent after a return
				if e.key() == QtCore.Qt.Key_Return and c.block().length() > 0:					
					s = unicode(c.block().text())
					n_tab = 0
					self.insertPlainText("\n")
					if len(s) > 0:
						while len(s) > 0 and s[0] == "\t":
							s = s[1:]
							self.insertPlainText("\t")				
					e.ignore()
					self.setFocus()					
					return																									
																			
			# Selection indent/ unindent
			if e.key() == QtCore.Qt.Key_Tab:
				if e.modifiers() == QtCore.Qt.MetaModifier:
					self.unindent()
					e.ignore()
					self.setFocus()
					return					
				elif c.hasSelection():
					self.indent()
					e.ignore()
					self.setFocus()
					return
			
			self.setFocus()	
			QPlainTextEdit.keyPressEvent(self, e)
									
		def focusOutEvent(self, e):
		
			"""
			Tell the outside world that focus has been lost
			
			Arguments:
			e -- A focusout event
			"""
		
			self.emit(QtCore.SIGNAL("focusLost"))
			
		def currentLine(self):
		
			"""
			Returns the current line number
			"""
		
			return self.document().findBlock(self.textCursor().position()).blockNumber() + 1

		def numberbarPaint(self, number_bar, event):
		
			"""
			Paints the line numbers
			"""
		
			font_metrics = self.fontMetrics()
			current_line = self.document().findBlock(self.textCursor().position()).blockNumber() + 1
	 
			block = self.firstVisibleBlock()
			line_count = block.blockNumber()
			painter = QPainter(number_bar)
			
			fg_pen = QtGui.QPen(QtGui.QColor("gray"))
			
			painter.setFont(self.font)
			painter.setPen(fg_pen)
			painter.fillRect(event.rect(), self.palette().base())
	 
			# Iterate over all visible text blocks in the document.
			while block.isValid():
				line_count += 1
				block_top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
		 
				# Check if the position of the block is out side of the visible
				# area.
				if not block.isVisible() or block_top >= event.rect().bottom():
					break
		 
				# We want the line number for the selected line to be bold.
				if line_count == current_line:
					font = painter.font()
					font.setBold(True)
					painter.setFont(font)
				else:
					font = painter.font()
					font.setBold(False)
					painter.setFont(font)
		 
				# Draw the line number right justified at the position of the line.
				paint_rect = QRect(0, block_top, number_bar.width(), font_metrics.height())
				painter.drawText(paint_rect, Qt.AlignRight, unicode("x%.4d" % line_count))
		 
				block = block.next()
	 
			painter.end()
 
	def __init__(self, experiment, notification=None, syntax=None):

		"""
		Constructor of the main class, which wraps around
		the plaintextedit and the numberbar
		"""

		QFrame.__init__(self)
		
		self.experiment = experiment
	 
		self.setFrameStyle(QFrame.NoFrame)
	 
		self.edit = self.PlainTextEdit(self)
		self.number_bar = self.NumberBar(self.edit)
		
		self.search = QtGui.QLineEdit()
		self.search.setMaximumWidth(150)
		self.search.returnPressed.connect(self.perform_search)
		self.search.setToolTip("Enter a search term")
		
		self.search_button = QtGui.QPushButton(self.experiment.icon("search"), "")
		self.search_button.setIconSize(QtCore.QSize(16, 16))
		self.search_button.setToolTip("Search")
		self.search_button.clicked.connect(self.perform_search)
		
		self.replace_button = QtGui.QPushButton(self.experiment.icon("replace"), "")
		self.replace_button.setIconSize(QtCore.QSize(16, 16))
		self.replace_button.setToolTip("Replace")
		self.replace_button.clicked.connect(self.perform_replace)
		
		self.indent_button = QtGui.QPushButton(self.experiment.icon("indent"), "")
		self.indent_button.setIconSize(QtCore.QSize(16, 16))
		self.indent_button.setToolTip("Indent one level (tab)")
		self.indent_button.clicked.connect(self.edit.indent)
		
		self.unindent_button = QtGui.QPushButton(self.experiment.icon("unindent"), "")
		self.unindent_button.setIconSize(QtCore.QSize(16, 16))
		self.unindent_button.setToolTip("Unindent one level (super + tab)")
		self.unindent_button.clicked.connect(self.edit.unindent)		
		
		self.modified = self.experiment.label_image("unsaved_changes")
		self.modified.setToolTip("Press Alt + A to apply unsaved changes")
		self.modified.hide()
		
		self.apply = QtGui.QPushButton(self.experiment.icon("apply"), "Apply")
		self.apply.setToolTip("Press Alt + A to apply unsaved changes")
		self.apply.setIconSize(QtCore.QSize(16, 16))
						
		search_widget = QtGui.QWidget()
		search_hbox = QtGui.QHBoxLayout(search_widget)
		search_hbox.addWidget(self.search)
		search_hbox.addWidget(self.search_button)
		search_hbox.addWidget(self.replace_button)
		search_hbox.addWidget(self.indent_button)
		search_hbox.addWidget(self.unindent_button)
		if notification != None:
			search_hbox.addWidget(QtGui.QLabel("<small>%s</small>" % notification))				
		search_hbox.addStretch()						
		search_hbox.addWidget(self.modified)				
		search_hbox.addWidget(self.apply)
		search_hbox.setContentsMargins(0, 0, 0, 0)		
	 
	 	main_widget = QtGui.QFrame()
	 	main_widget.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken) 
		main_hbox = QtGui.QHBoxLayout(main_widget)
		main_hbox.setSpacing(0)
		main_hbox.setMargin(0)
		main_hbox.addWidget(self.number_bar)
		main_hbox.addWidget(self.edit)
		
		vbox = QtGui.QVBoxLayout(self)
		vbox.addWidget(main_widget)
		vbox.addWidget(search_widget)		
		vbox.setSpacing(4)
		vbox.setMargin(0)		
	 
		self.edit.blockCountChanged.connect(self.number_bar.adjustWidth)
		self.edit.updateRequest.connect(self.number_bar.updateContents)
		
		if syntax == "python":
			syntax_highlighter(self.edit.document(), python_keywords)
		elif syntax == "opensesame":
			syntax_highlighter(self.edit.document(), opensesame_keywords)
			
		self.toolbar_hbox = search_hbox
				
	def perform_search(self):
	
		"""
		Searches the text
		"""
		
		if not self.edit.find(self.search.text()):
			self.edit.moveCursor(QtGui.QTextCursor.Start)
			self.edit.find(self.search.text())
			
	def perform_replace(self):
	
		"""
		Performs a search/ replace
		"""
		
		replace_dialog(self).exec_()
		
	def getText(self):

		"""
		Return the contents of the editor
		"""

		return unicode(self.edit.toPlainText())

	def setText(self, text):

		"""
		Set the contents of the editor
		"""

		self.edit.setPlainText(text)

	def isModified(self):

		"""
		Check if the editor has been modified
		"""

		return self.edit.document().isModified()

	def setModified(self, modified):

		"""
		Set the modified status of the editor
		"""

		self.modified.setVisible(modified)
		self.edit.document().setModified(modified)

	def setLineWrapMode(self, mode):

		"""
		Turn line wrapping on/ off
		"""

		self.edit.setLineWrapMode(mode)
	
