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

class small_webview(QtWebKit.QWebView):

	"""
	A wrapper around QWebView too override the sizeHint, which prevents the
	browser from resizing to small sizes
	"""

	def sizeHint(self):
	
		"""
		Give size hint
		
		Returns:
		A QSize
		"""
	
		return QtCore.QSize(100,100)

class webbrowser(QtGui.QWidget):

	"""A simple browser tab"""

	def __init__(self, parent):
	
		"""
		Constructor
		
		Keyword arguments:
		parent -- the parent QWidget (default=None)		
		"""
	
		QtGui.QWidget.__init__(self, parent)							
		self.main_window = parent
		self.ui = webbrowser_widget_ui.Ui_webbrowser_widget()
		self.ui.setupUi(self)		
		
		self.ui.webview = small_webview(self)		
		self.ui.webview.loadProgress.connect(self.update_progressbar)
		self.ui.webview.loadStarted.connect(self.load_started)
		self.ui.webview.loadFinished.connect(self.load_finished)
		self.ui.webview.urlChanged.connect(self.url_changed)
		self.ui.layout_main.addWidget(self.ui.webview)
		self.ui.button_back.clicked.connect(self.ui.webview.back)
		self.ui.button_osdoc.clicked.connect(self.open_osdoc)
		self.ui.button_forum.clicked.connect(self.open_forum)
		self.main_window.theme.apply_theme(self)	
						
	def load(self, url):
	
		"""
		Load a webpage
		
		Arguments:
		url -- the webpage to load
		"""
	
		if url.endswith(u'.md'):
			try:
				import markdown				
				html = markdown.markdown(open(url).read())
				html += u'<style type="text/css">%s</style>' % \
					open(self.main_window.theme.resource( \
					u'markdown.css')).read()
			except Exception as e:
				debug.msg(self.main_window.experiment.unistr(e))
				html = \
					u'<p>Python markdown must be installed to view this page. Sorry!</p>'
			self.ui.webview.setHtml(html, QtCore.QUrl(url))
		else:
			self.ui.webview.load(QtCore.QUrl(url))
		
	def load_finished(self):
	
		"""Hide the statusbar to indicate that loading is finished"""

		self.ui.label_load_progress.setText(u'Done')
		
	def update_progressbar(self, progress):
	
		"""
		Update the progressbar to indicate the load progress
		
		Arguments:
		progress -- the load progress
		"""
	
		self.ui.label_load_progress.setText(u'%d%%' % progress)
		
	def load_started(self):
	
		"""Show the statusbar to indicate that loading has started"""

		self.ui.label_load_progress.setText(u'Starting ...')
		
	def open_osdoc(self):
	
		"""Open osdoc.cogsci.nl"""
	
		self.load(u'http://osdoc.cogsci.nl/')

	def open_forum(self):
	
		"""Open forum.cogsci.nl"""	
	
		self.load(u'http://forum.cogsci.nl/')

	def url_changed(self, url):

		"""Update the url bat"""	

		self.ui.edit_url.setText(url.toString())
