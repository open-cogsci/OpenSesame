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

from libopensesame import debug
from libqtopensesame.misc import config, _
from PyQt4 import QtGui, QtCore

class unused_widget(QtGui.QWidget):

	"""The unused items widget"""

	def __init__(self, parent=None):

		"""
		Constructor.

		Keywords arguments:
		parent	--	The parent QWidget. (default=None)
		"""
				
		self.main_window = parent
		self.experiment = self.main_window.experiment
		QtGui.QWidget.__init__(self, parent)

		# Set the header, with the icon, label and script button
		header_hbox = QtGui.QHBoxLayout()
		header_hbox.addWidget(self.experiment.label_image(u"unused"))
		header_label = QtGui.QLabel()
		header_label.setText(_(u"<b><font size='5'>Unused</font></b>"))
		header_hbox.addWidget(header_label)
		header_hbox.addStretch()
		header_widget = QtGui.QWidget()
		header_widget.setLayout(header_hbox)

		purge_button = QtGui.QPushButton(self.experiment.icon(u"purge"), \
			_(u"Permanently delete unused items"))
		purge_button.setIconSize(QtCore.QSize(16, 16))
		QtCore.QObject.connect(purge_button, QtCore.SIGNAL(u"clicked()"), \
			self.purge_unused)

		purge_hbox = QtGui.QHBoxLayout()
		purge_hbox.addWidget(purge_button)
		purge_hbox.addStretch()
		purge_widget = QtGui.QWidget()
		purge_widget.setLayout(purge_hbox)

		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(header_widget)
		vbox.addWidget(purge_widget)
		vbox.addStretch()
		
		self.setLayout(vbox)
		self.__unused_tab__ = True

	def purge_unused(self):

		"""Remove all unused items from the items list"""

		# Ask confirmation
		resp = QtGui.QMessageBox.question(self.main_window.ui.centralwidget, \
			_(u"Permanently delete items?"), \
			_(u"Are you sure you want to permanently delete all unused items? This action cannot be undone."), \
			QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		if resp == QtGui.QMessageBox.No:
			return
		
		# We need a loop, because items may become unused
		# by deletion of their unused parent items
		while len(self.main_window.experiment.unused_items) > 0:
			for item in self.main_window.experiment.unused_items:
				if item in self.main_window.experiment.items:
					del self.main_window.experiment.items[item]
			self.main_window.experiment.build_item_tree()
						
		# Notify dispatch
		self.main_window.dispatch.event_structure_change.emit(u'')		
		self.main_window.ui.tabwidget.close_all()
		self.main_window.ui.tabwidget.open_general()