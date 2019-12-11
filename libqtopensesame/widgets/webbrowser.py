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
import os
import platform
from qtpy import QtCore
from libqtopensesame.widgets.base_widget import base_widget
from libopensesame import plugins, misc
from libqtopensesame.misc.markdown_parser import markdown_parser
from libqtopensesame.misc import display
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'webbrowser', category=u'core')

if os.environ[u'QT_API'] == u'pyqt':
	from PyQt4.QtWebKit import QWebView as WebView
	from PyQt4.QtWebKit import QWebPage as WebPage
else:
	# QtWebKit is dropped in favour of QtWebEngine from Qt 5.6 on
	try:
		from PyQt5.QtWebKitWidgets import QWebView as WebView
		from PyQt5.QtWebKitWidgets import QWebPage as WebPage
	except ImportError as e:
		from PyQt5.QtWebEngineWidgets import QWebEngineView as WebView
		from PyQt5.QtWebEngineWidgets import QWebEnginePage as WebPage

# These urls are viewed internally in the browser component. All other urls are
# opened in an external browser.
INTERNAL_URLS = [
	u'http://osdoc.cogsci.nl/',
	u'https://osdoc.cogsci.nl/',
	u'http://www.psychopy.org/',
	u'https://www.psychopy.org/',
	u'http://psychopy.org/',
	u'https://psychopy.org/',
	u'http://www.expyriment.org/',
	u'https://www.expyriment.org/',
	u'http://expyriment.org/',
	u'https://expyriment.org/',
	u'http://docs.expyriment.org/',
	u'https://docs.expyriment.org/',
	]


class small_webview(WebView):

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


class small_webpage(WebPage):

	"""
	desc:
		A wrapper around QWeb(Engine)Page, to overload the acceptNavigationRequest
		function, which determines what needs to be done after a link is clicked.
	"""

	def acceptNavigationRequest(self, *args):

		"""
		desc:
			Handles navigation requests to the browser, which can originate from
			link clicks, or other sources. the arguments and their order differ
			with the web browser backend being used, which can be QtWebKit or the
			newer QtWebEngine.

			Arguments (when used by QtWebKit):
				frame:
					desc: 	The frame that has to be changed depending on the
							request
					type: 	QtWebKit.QWebFrame
				request:
					desc:	request containing information about the
							navigation request, among which the url to change the
							frame to.
					type: 	QtWebKit.QNetworkRequest
				navtype:
					desc: 	type of request has been received (such as link
							clicked, form submitted)
					type: 	QtWebKit.NavigationType

			Arguments (when used by QtWebEngine):
				url:
					desc: 	url to navigate to
					type: 	QtCore.QUrl
				navtype:
					desc: 	type of request has been received (such as link
							clicked, form submitted)
					type: 	QtWebEngine.NavigationType
				isMainFrame:
					desc: 	indicating whether the request corresponds
							to the main frame or a child frame.
					type: 	boolean
		"""

		# Check if the first argument is a QUrl. If so, then
		# QWebEngine is used, if not, then QWebKit must be used. This way, the order
		# of received arguments can be determined.
		if isinstance(args[0], QtCore.QUrl):
			url, navtype, isMainFrame = args
		else:
			frame, request, navtype = args
			url = request.url()

		if navtype == self.NavigationTypeLinkClicked:
			url = url.toString()
			if url.startswith(u'opensesame://'):
				self.parent().command(url)
				return False
			if url.startswith(u'new:'):
				self.parent().main_window.tabwidget.open_browser(url[4:])
				return False
			for internal_url in INTERNAL_URLS:
				if url.startswith(internal_url):
					self.parent().load(url)
					return False
			misc.open_url(url)
			return False
		return super(small_webpage, self).acceptNavigationRequest(*args)


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
		self._current_url = u''
		self._cache = None
		self.ui.webview = small_webview(self)
		# Set webpage which handles link clicks
		webpage = small_webpage(self)
		self.ui.webview.setPage(webpage)
		# Touch events are enabled by default, and this has the effect that
		# touch events are broken for all other widgets once the webbrowser has
		# been used. This affects at least Ubuntu 15.05.
		self.ui.webview.setAttribute(QtCore.Qt.WA_AcceptTouchEvents, False)
		self.ui.webview.loadProgress.connect(self.update_progressbar)
		self.ui.webview.loadStarted.connect(self.load_started)
		self.ui.webview.loadFinished.connect(self.load_finished)
		self.ui.webview.urlChanged.connect(self.url_changed)
		self.ui.layout_main.addWidget(self.ui.webview)
		self.ui.button_back.clicked.connect(self.ui.webview.back)
		self.ui.button_osdoc.clicked.connect(self.open_osdoc)
		self.ui.button_forum.clicked.connect(self.open_forum)
		self.main_window.theme.apply_theme(self)
		self.markdown_parser = markdown_parser(self)

	def load(self, url, tmpl=None):

		"""
		desc:
			Loads a webpage.

		arguments:
			url:	The url to load.
			tmpl:	A template to be wrapped around the html in the case of
					Markdown files.
		"""

		if isinstance(url, QtCore.QUrl):
			url = url.toString()
		if url.endswith(u'.md') and not url.startswith(u'http://') \
			and not url.startswith(u'https://'):
			self.ui.top_widget.hide()
			self.load_markdown(
				safe_read(url), url=os.path.basename(url),
				tmpl=tmpl
			)
			return
		self.ui.top_widget.show()
		self._current_url = url
		self.ui.webview.load(QtCore.QUrl(url))

	def load_markdown(self, md, url=None, tmpl=None):

		"""
		desc:
			Loads a Markdown text string.

		arguments:
			md:		A Markdown text string.
			url:	The url to load.
			tmpl:	A template to be wrapped around the html.
		"""

		if url is None:
			url = u'untitled'
		url = QtCore.QUrl(u'http://opensesame.app.cogsci.nl/%s' % url)
		self.ui.top_widget.hide()
		html = self.markdown_parser.to_html(md)
		if tmpl is not None:
			html = tmpl % {u'body': html}
		self.ui.webview.setHtml(html, baseUrl=url)
		self.ui.webview.setZoomFactor(display.display_scaling)

	def init_cache(self):

		"""
		desc:
			Initializes the webbrowser cache, if available.
		"""

		import pickle

		cache_file = misc.resource(u'webbrowser-cache.pkl')
		if cache_file is None:
			self.extension_manager.fire(u'notify',
				message=_(u'No webbrowser cache available'),
				category=u'info')
			self._cache = {}
			return
		with open(cache_file) as fd:
			try:
				self._cache = pickle.load(fd)
			except:
				self._cache = {}
				return
		if not isinstance(self._cache, dict):
			self.extension_manager.fire(u'notify',
				message=_(u'Webbrowser cache is corrupt'),
				category=u'warning')
			self._cache = {}
			return

	def try_cache(self):

		"""
		desc:
			Checks if the current page, after a failed load, is available in the
			cache, and if so, loads it from the cache.
		"""

		# On some versions of Qt, the load_finished signal is also sent when
		# displaying pages that have been set programmatically. In this case,
		# the current_url is '', so we ignore those.
		if self._current_url in (None, u''):
			return
		if self._cache is None:
			self.init_cache()
		if self._current_url not in self._cache:
			self.extension_manager.fire(u'notify',
				message=_(u'Failed to load page: ') + self._current_url,
				category=u'warning')
			return
		self.extension_manager.fire(u'notify',
			message=_(u'Displaying cached version of: %s. For a better viewing experience, connect to the internet.') \
			% self._current_url, category=u'info')
		self.ui.webview.setHtml(self._cache[self._current_url])
		self.ui.webview.setZoomFactor(display.display_scaling)

	def load_finished(self, ok):

		"""
		desc:
			Hides the statusbar to indicate that loading is finished.
		"""

		if not ok:
			self.try_cache()
		self.ui.label_load_progress.setText(_(u'Done'))
		self.ui.webview.setZoomFactor(display.display_scaling)

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

		self.ui.label_load_progress.setText(_(u'Loading …'))

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
