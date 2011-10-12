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

class good_looking_table(QtGui.QTableWidget):

	"""Extended the QTableWidget for copy-pasting, etc."""
	
	def __init__(self, rows, columns=None, icons={}, parent=None):
	
		"""
		Constructor
		
		Arguments:
		rows -- the number of rows
		
		Keywords arguments:
		columns -- the number of columns or None for no columns (default=None)
		icons -- a dictionary with QIcons for the various actions (default={})
		parent -- the parent QWidget (default=None)
		"""
	
		self.clipboard = QtGui.QApplication.clipboard	
		
		# Set-up the context menu
		self.menu = QtGui.QMenu()		
		if "cut" in icons:
			self.menu.addAction(icons["cut"], "Cut", self.cut)
		else:		
			self.menu.addAction("Cut", self.cut)							
		if "copy" in icons:
			self.menu.addAction(icons["copy"], "Copy", self.copy)
		else:
			self.menu.addAction("Copy", self.copy)					
		if "paste" in icons:
			self.menu.addAction(icons["paste"], "Paste", self.paste)
		else:		
			self.menu.addAction("Paste", self.paste)
		if "clear" in icons:
			self.menu.addAction(icons["clear"], "Clear", self._clear)
		else:		
			self.menu.addAction("Clear", self._clear)
		
		# If there is only one parameter, this is the parent
		if columns == None:
			QtGui.QTableWidget.__init__(self, rows)
		else:
			QtGui.QTableWidget.__init__(self, rows, columns, parent)
			
		self.setGridStyle(QtCore.Qt.DotLine)
		self.setAlternatingRowColors(True)
		
	def contextMenuEvent(self, e):
	
		"""
		Present the context menu
		
		Arguments:
		e -- a QContentMenuEvent
		"""
	
		self.pos = e.globalPos()
		self.menu.exec_(self.pos)
		
	def keyPressEvent(self, e):
	
		"""
		Capture keypresses to handle copy, cut, and paste
		
		Arguments:
		e -- a QKeyEvent
		"""
		
		if e.key() == QtCore.Qt.Key_Delete:
			self._clear()
			e.ignore()		
		elif e.modifiers() == QtCore.Qt.ControlModifier and e.key() == QtCore.Qt.Key_X:
			self.cut()
			e.ignore()			
		elif e.modifiers() == QtCore.Qt.ControlModifier and e.key() == QtCore.Qt.Key_C:
			self.copy()
			e.ignore()
		elif e.modifiers() == QtCore.Qt.ControlModifier and e.key() == QtCore.Qt.Key_V:
			self.paste()
			e.ignore()
		else:
			QtGui.QTableWidget.keyPressEvent(self, e)
			
	def cut(self):
	
		"""Cuts text from the table into the clipboard (copy + clear = cut)"""
	
		self.copy()
		self._clear()																		

	def copy(self):
	
		"""Copies data from the table into the clipboard"""

		selected_range = self.selectedRanges()[0]		
		rows = QtCore.QStringList()
		for row in range(selected_range.topRow(), selected_range.bottomRow() + 1):		
			columns = QtCore.QStringList()
			for column in range(selected_range.leftColumn(), selected_range.rightColumn() + 1):	
				item = self.item(row, column)
				if item != None:
					value = item.text()
				else:
					value = ""
				columns.append(value)
			rows.append(columns.join("\t"))					
		selection = rows.join("\n")		 	
		self.clipboard().setText(selection)
		
	def paste(self):
	
		"""Paste text from the clipboard into the table"""
			
		selection = self.clipboard().mimeData().text()		
		rows = selection.split("\n")			
		current_row = self.currentRow()		
		for row in rows:
			cells = row.split("\t")			
			current_column = self.currentColumn()
			for cell in cells:
				if current_column >= self.columnCount():
					break
				item = QtGui.QTableWidgetItem()
				item.setText(cell)
				self.setItem(current_row, current_column, item)
				current_column += 1				
			current_row += 1		
			
	def _clear(self):
	
		"""Clear the selected cells"""
	
		selected_range = self.selectedRanges()[0]
		for row in range(selected_range.topRow(), selected_range.bottomRow() + 1):		
			for column in range(selected_range.leftColumn(), selected_range.rightColumn() + 1):	
				item = self.item(row, column)
				if item != None:
					item.setText("")
		
if __name__ == "__main__":

	"""If called standalone, this class shows a demo table"""

	import sys
	app = QtGui.QApplication(sys.argv)
	widget = good_looking_table(10, 10)
	widget.setWindowTitle("Good looking table")
	widget.show()
	sys.exit(app.exec_())

