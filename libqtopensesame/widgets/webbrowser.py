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
from libqtopensesame.widgets.base_widget import base_widget
from libopensesame import debug
from libopensesame.py3compat import *
import os.path
import sys

class small_webview(QtWebKit.QWebView):

	"""
	desc:
		A wrapper around QWebView too override the sizeHint, which prevents the
		browser from resizing to small sizes.
	"""

	def sizeHint(self):

		"""
		desc:
			Gives a size hint.

		returns:
			A QSize
		"""

		return QtCore.QSize(100,100)

class webbrowser(base_widget):

	"""
	desc:
		A browser widget used to display online and offline help pages.
	"""

	def __init__(self, main_window):

		"""
		desc:
			Constructor.

		keywords:
			main_window:	A qtopensesame object.
		"""

		super(webbrowser, self).__init__(main_window,
			ui=u'widgets.webbrowser_widget')
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
		desc:
			Loads a webpage.

		arguments:
			url:	The url to load.
		"""

		if url.endswith(u'.md'):
			try:
				import markdown
				html = markdown.markdown(safe_decode(open(url),
					errors=u'ignore'))
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

		"""
		desc:
			Hides the statusbar to indicate that loading is finished.
		"""

		self.ui.label_load_progress.setText(u'Done')

	def update_progressbar(self, progress):

		"""
		desc:
			Updates the progressbar to indicate the load progress.

		arguments:
			progress:	The load progress.
		"""

		self.ui.label_load_progress.setText(u'%d%%' % progress)

	def load_started(self):

		"""
		desc:
			Shows the statusbar to indicate that loading has started.
		"""

		self.ui.label_load_progress.setText(u'Starting ...')

	def open_osdoc(self):

		"""
		desc:
			Opens osdoc.cogsci.nl.
		"""

		self.load(u'http://osdoc.cogsci.nl/')

	def open_forum(self):

		"""
		desc:
			Opens forum.cogsci.nl.
		"""

		self.load(u'http://forum.cogsci.nl/')

	def url_changed(self, url):

		"""
		desc:
			Updates the url bar.

		arguments:
			url:	A url string.
		"""

		self.ui.edit_url.setText(url.toString())
