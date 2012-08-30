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

from PyQt4 import QtCore, QtGui
from libqtopensesame.ui import new_loop_sequence_ui

class new_loop_sequence_dialog(QtGui.QDialog):

	"""Dialog to select an item-to-run for a new sequence or loop item"""

	def __init__(self, parent, experiment, item_type, _parent):

		"""
		Constructor
		
		Arguments:
		parent -- the parent QWidget
		experiment -- the experiment object
		item_type -- 'sequence' or 'loop'
		_parent -- the parent item, i.e. the item above the current item in the
				   experiment hierarchy		
		"""	
	
		QtGui.QDialog.__init__(self, parent)
		self.experiment = experiment
		self._parent = _parent
		self.ui = new_loop_sequence_ui.Ui_new_loop_sequence_dialog()
		self.ui.setupUi(self)
		self.experiment.main_window.theme.apply_theme(self)		
		self.ui.label_icon.setPixmap( \
			self.experiment.main_window.theme.qpixmap(item_type))
		self.action = "cancel"		
		QtCore.QObject.connect(self.ui.button_new, QtCore.SIGNAL("clicked()"), \
			self.new_item)
		QtCore.QObject.connect(self.ui.button_select, \
			QtCore.SIGNAL("clicked()"), self.select_item)
		
		if item_type == "loop":
			s = "A loop needs another item to run, usually a sequence. You can create a new item or select an existing item to add to the loop."
			select = "sequence"
		else:
			s = "A sequence needs at least one other item to run, such as a sketchpad. You can create a new item or select an existing item to add to the sequence."
			select = "sketchpad"
			
		self.ui.label_explanation.setText(s)
		
		self.experiment.item_type_combobox(True, True, self.ui.combobox_new, \
			select)
		
		# The parents list is excluded from the list of possible children, but
		# this list if empty if there are no parents or the parent is the main
		# experiment sequence
		if self._parent == None or _parent not in self.experiment.items:
			parents = []
		else:
			parents = self.experiment.items[_parent].parents()
		self.experiment.item_combobox(None, parents, self.ui.combobox_select)		
					
	def new_item(self):
	
		self.action = "new"
		self.item_type = unicode(self.ui.combobox_new.currentText())		
		self.accept()

	def select_item(self):
	
		self.action = "select"
		self.item_name = unicode(self.ui.combobox_select.currentText())		
		self.accept()

