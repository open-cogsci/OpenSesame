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

from PyQt4 import QtCore, QtGui, QtWebKit
from libopensesame import debug
from libqtopensesame.ui import webbrowser_widget_ui
import os.path
import sys

class webbrowser(QtGui.QWidget):

	"""
	A very basic wrapper around QWebView, which currently adds nothing. This is
	used to add a browser tab to opensesame
	"""

	def __init__(self, parent):
	
		"""
		Constructor
		
		Keyword arguments:
		parent -- the parent QWidget (default=None)		
		"""
	
		QtGui.QWidget.__init__(self, parent)							
		self.main_window = parent
		self.history = []
		self.webview = QtWebKit.QWebView(self)
		self.webview.loadProgress.connect(self.update_progressbar)
		self.webview.loadStarted.connect(self.load_started)
		self.webview.loadFinished.connect(self.load_finished)
		self.webview.urlChanged.connect(self.url_changed)
		self.ui = webbrowser_widget_ui.Ui_webbrowser_widget()
		self.ui.setupUi(self)
		self.ui.button_back.clicked.connect(self.webview.back)
		self.ui.button_osdoc.clicked.connect(self.open_osdoc)
		self.ui.button_forum.clicked.connect(self.open_forum)
		self.ui.layout_main.addWidget(self.webview)
		self.main_window.theme.apply_theme(self)	
						
	def load(self, url):
	
		"""
		Load a webpage
		
		Arguments:
		url -- the webpage to load
		"""
	
		self.webview.load(QtCore.QUrl(url))
		
	def load_finished(self):
	
		"""Hide the statusbar to indicate that loading is finished"""

		self.ui.label_load_progress.setText('Done')
		
	def update_progressbar(self, progress):
	
		"""
		Update the progressbar to indicate the load progress
		
		Arguments:
		progress -- the load progress
		"""
	
		self.ui.label_load_progress.setText('%d%%' % progress)
		
	def load_started(self):
	
		"""Show the statusbar to indicate that loading has started"""

		self.ui.label_load_progress.setText('Starting ...')
		
	def open_osdoc(self):
	
		"""Open osdoc.cogsci.nl"""
	
		self.load('http://osdoc.cogsci.nl/')

	def open_forum(self):
	
		"""Open forum.cogsci.nl"""	
	
		self.load('http://forum.cogsci.nl/')

	def url_changed(self, url):

		"""Update the url bat"""	

		self.ui.edit_url.setText(url.toString())
