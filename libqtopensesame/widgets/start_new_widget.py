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

from PyQt4 import QtCore, QtGui
from libqtopensesame.widgets.base_widget import base_widget
from libqtopensesame.misc import template_info
import random
import os

class start_new_widget(base_widget):

	"""Start new dialog presented when starting with a clean experiment"""

	def __init__(self, main_window, start=False):

		"""
		Constructor

		Arguments:
		main_window -- a the main ui

		Keyword arguments:
		start -- indicates whether the widget is opened because OpenSesame has
				 started (True) or because the new button has been clicked
				 (False) (default=True)
		"""

		super(start_new_widget, self).__init__(main_window,
			ui=u'widgets.start_new_widget')
		if start:
			self.tab_name = u'__start_wizard__'
		else:
			self.tab_name = u'__new_wizard__'
		# Initialize templates
		for path, desc in template_info.templates:
			try:
				path = self.experiment.resource(path)
			except:
				continue
			item = QtGui.QListWidgetItem(self.ui.list_templates)
			item.setText(desc)
			item.file = path
			item.setIcon(self.experiment.icon(u"document-open-recent"))
			self.ui.list_templates.addItem(item)
		self.ui.list_templates.setCurrentRow(0)
		self.ui.list_templates.itemDoubleClicked.connect(self.open_template)

		# Initialize recent
		if len(self.main_window.recent_files) == 0:
			self.ui.list_recent.hide()
			self.ui._label_recent.hide()
		else:
			for f in self.main_window.recent_files:
				item = QtGui.QListWidgetItem(self.ui.list_recent)
				item.setText(os.path.basename(f))
				item.file = f
				item.setIcon(self.experiment.icon(u"experiment"))
			self.ui.list_recent.setCurrentRow(0)
			self.ui.list_recent.itemDoubleClicked.connect(self.open_recent)

		# Connect buttons
		self.ui.button_browse.clicked.connect(self.main_window.open_file)
		self.ui.button_osdoc.clicked.connect( \
			self.main_window.ui.tabwidget.open_osdoc)
		self.ui.button_forum.clicked.connect( \
			self.main_window.ui.tabwidget.open_forum)
		self.ui.button_cancel.clicked.connect(self.cancel)

		# Show the correct header
		if start:
			self.ui.widget_header_new.hide()
		else:
			self.ui.widget_header_start.hide()

	def cancel(self):

		"""Cancel the start_new_wizard"""

		self.main_window.ui.tabwidget.close_current()
		self.main_window.ui.tabwidget.open_general()

	def open_template(self):

		"""Open the selected template"""

		self.main_window.open_file(path= \
			self.ui.list_templates.currentItem().file, add_to_recent=False)
		self.close()

	def open_recent(self):

		"""Open the selected file"""

		item = self.ui.list_recent.currentItem()
		if item != None:
			self.main_window.open_file(path= \
				self.ui.list_recent.currentItem().file)
			self.close()

