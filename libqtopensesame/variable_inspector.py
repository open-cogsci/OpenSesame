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

class sortable(QtGui.QTableWidgetItem):

	"""A sortable tablewidget"""

	def __init__(self, text, sort_key):
	
		"""
		Constructor
		
		Arguments:
		text -- the cell text
		sort_key -- the key to use for sorting
		"""
	
		QtGui.QTableWidgetItem.__init__(self, str(text), QtGui.QTableWidgetItem.UserType)
		self.sort_key = sort_key

	def __lt__(self, other):
	
		"""
		Sort operator (less than)
		
		Arguments:
		other -- the other sortable
		"""
	
		return self.sort_key < other.sort_key

class variable_inspector(QtGui.QTableWidget):

	"""The table for the variable inspector"""

	def __init__(self, parent=None):
	
		"""
		Constructor
		
		Keywords arguments:
		parent -- the parent QWidget
		"""
	
		QtGui.QTableWidget.__init__(self, parent)
		self.unsorted = True
		
	def refresh(self):
	
		"""Updates and restores the variable inspector"""
		
		if self.main_window.experiment.debug:
			print "variable_inspector.refresh()"
		
		if self.unsorted:
			self.sortItems(0, QtCore.Qt.AscendingOrder)
			self.unsorted = False
		scrollpos = self.verticalScrollBar().sliderPosition()
		col = self.currentColumn()
		row = self.currentRow()
		filt = str(self.main_window.ui.edit_variable_filter.text())
		self.setSortingEnabled(False)
		i = 0
		for var, val, item in self.main_window.experiment.var_list(filt):
			self.insertRow(i)
			self.setItem(i, 0, sortable(var, "%s_%s_%s" % (var,val,item)))
			self.setItem(i, 1, sortable(val, "%s_%s_%s" % (val,var,item)))
			self.setItem(i, 2, sortable(item, "%s_%s_%s" % (item,var,val)))
			i += 1
		self.setRowCount(i)					
		self.setSortingEnabled(True)					
		self.setCurrentCell(row, col)
		self.verticalScrollBar().setSliderPosition(scrollpos)	

