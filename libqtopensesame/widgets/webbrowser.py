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
import platform
from qtpy import QtCore
from libqtopensesame.widgets.base_widget import base_widget
from libopensesame import plugins, misc
from libqtopensesame.misc.markdown_parser import markdown_parser
import os.path

import os
if os.environ[u'QT_API'] == u'pyqt':
	from PyQt4 import QtWebKit
else:
	from PyQt5 import QtWebKitWidgets as QtWebKit

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
		# Touch events are enabled by default, and this has the effect that
		# touch events are broken for all other widgets once the webbrowser has
		# been used. This affects at least Ubuntu 15.05.
		self.ui.webview.setAttribute(QtCore.Qt.WA_AcceptTouchEvents, False)
		self.ui.webview.loadProgress.connect(self.update_progressbar)
		self.ui.webview.loadStarted.connect(self.load_started)
		self.ui.webview.loadFinished.connect(self.load_finished)
		self.ui.webview.urlChanged.connect(self.url_changed)
		self.ui.webview.linkClicked.connect(self.link_clicked)
		self.ui.layout_main.addWidget(self.ui.webview)
		self.ui.button_back.clicked.connect(self.ui.webview.back)
		self.ui.button_osdoc.clicked.connect(self.open_osdoc)
		self.ui.button_forum.clicked.connect(self.open_forum)
		self.main_window.theme.apply_theme(self)
		self.markdown_parser = markdown_parser(self)

	def load(self, url):

		"""
		desc:
			Loads a webpage.

		arguments:
			url:	The url to load.
		"""

		if isinstance(url, QtCore.QUrl):
			url = url.toString()
		if url.endswith(u'.md') and not url.startswith(u'http://') \
			and not url.startswith(u'https://'):
			self.ui.top_widget.hide()
			with open(url) as fd:
				md = safe_decode(fd.read(), errors=u'ignore')
			self.load_markdown(md)
			return
		self.ui.top_widget.show()
		self.ui.webview.load(QtCore.QUrl(url))
		self.ui.webview.page().setLinkDelegationPolicy(
			self.ui.webview.page().DelegateAllLinks)

	def load_markdown(self, md):

		"""
		desc:
			Loads a Markdown text string.

		arguments:
			md:		A Markdown text string.
		"""

		self.ui.top_widget.hide()
		self.ui.webview.setHtml(self.markdown_parser.to_html(md))
		self.ui.webview.page().setLinkDelegationPolicy(
			self.ui.webview.page().DelegateAllLinks)

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

	def link_clicked(self, url):

		"""
		desc:
			Process link-clicks to capture special URLs.

		arguments:
			url:
				type:	QUrl
		"""

		url = url.toString()
		if url.startswith(u'opensesame://'):
			self.command(url)
			return
		if url.startswith(u'new:'):
			wb = webbrowser(self.main_window)
			wb.load(url[4:])
			self.main_window.tabwidget.open_browser(url[4:])
			return
		if url.startswith(u'http://osdoc.cogsci.nl'):
			self.load(url)
			return
		misc.open_url(url)

	def command(self, cmd):

		"""
		desc:
			Processes commands that are embedded in urls to trigger actions and
			events.

		arguments:
			cmd:
				desc:	A command string, such as 'action.save'.
				type:	str
		"""

		cmd = cmd[13:]
		# This is quite a hacky workaround for Windows. The file paths are
		# automatically transformed into a Unix-like slashforward format.
		# Windows therefore cannot find the paths anymomre. To fix this, we
		# insert a colon, and normpath it.
		if platform.system() == u'Windows':
			_cmd = os.path.normpath(cmd[0] + u':' + cmd[1:])
		else:
			_cmd = cmd
		if os.path.exists(_cmd):
			self.main_window.open_file(path=_cmd, add_to_recent=False)
			return
		cmd = cmd.split(u'.')
		if len(cmd) == 2 and cmd[0] == u'action':
			try:
				action = getattr(self.main_window.ui, u'action_%s' % cmd[1])
			except:
				self.experiment.notify(u'Invalid action: %s' % cmd[1])
				return
			action.trigger()
			return
		if len(cmd) == 2 and cmd[0] == u'event':
			self.main_window.extension_manager.fire(cmd[1])
			return
		if len(cmd) > 1 and cmd[0] == u'help':
			if len(cmd) == 2:
				self.main_window.ui.tabwidget.open_help(cmd[1])
			elif len(cmd) == 3 and cmd[1] in [u'extension', u'plugin']:
				path = os.path.join(plugins.plugin_folder(cmd[2], _type=cmd[1]),
					cmd[2]+u'.md')
				self.load(path)
			return
