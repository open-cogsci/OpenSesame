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

from qtpy import QtWidgets
from libopensesame import debug
from libopensesame import metadata
from libqtopensesame.extensions import base_extension
from libqtopensesame.misc.base_subcomponent import base_subcomponent
from libqtopensesame.misc.config import cfg
from libopensesame.py3compat import *
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'help', category=u'extension')

class action_page(QtWidgets.QAction, base_subcomponent):

	"""
	desc:
		A menu entry for a single help page.
	"""

	def __init__(self, main_window, title, link, menu):

		"""
		desc:
			Constructor.

		arguments:
			main_window:	The main-window object.
			title:			The menu title.
			link:			The URL to open.
			menu:			The menu for the action.
		"""

		QtWidgets.QAction.__init__(self, main_window.theme.qicon(
			u'applications-internet'), title, menu)
		self.setup(main_window)
		self.title = title
		self.link = link
		self.triggered.connect(self.open_page)

	def open_page(self):

		"""
		desc:
			Opens the page URL.
		"""

		self.main_window.tabwidget.open_browser(self.link)

class help(base_extension):

	"""
	desc:
		An extension that implements the help menu.
	"""

	def event_startup(self):

		"""
		desc:
			Build the menu on startup.
		"""

		self.menu = self.menubar.addMenu(_(u'Help'))
		menu = self.online_help_menu()
		if menu is not None:
			self.action_online_help = self.menu.addMenu(menu)
		menu = self.psychopy_help_menu()
		if menu is not None:
			self.action_psychopy_help = self.menu.addMenu(menu)
		self.action_offline_help = self.menu.addAction(
			self.theme.qicon(u'help-contents'), _(u'Offline help'))
		self.action_offline_help.triggered.connect(self.open_offline_help)
		self.menu.addSeparator()

	def open_offline_help(self):

		"""
		desc:
			Open offline help in browser.
		"""

		self.tabwidget.open_browser(self.ext_resource(u'offline_help.md'))

	def online_help_menu(self):

		"""
		desc:
			Build online help menu based on remote sitemap.
		"""

		if py3:
			from urllib.request import urlopen
		else:
			from urllib2 import urlopen
		import yaml
		sitemap_url = cfg.online_help_sitemap.replace(u'[version]',
			metadata.main_version)
		try:
			fd = urlopen(sitemap_url)
			sitemap = fd.read()
			_dict = yaml.load(sitemap)
		except:
			return
		if not isinstance(_dict, dict):
			return
		menu = self.build_menu(self.menu, _(u'Online help'), _dict)
		return menu

	def build_menu(self, parent_menu, title, _dict):

		"""
		desc:
			A helper function to build the online-help menu.

		arguments:
			parent_menu:	A parent QMenu for a submenu.
			title:			A menu title.
			_dict:			A dict extracted from the sitemap with page names
							and contents.

		returns:
			A QMenu.
		"""

		menu = parent_menu.addMenu(self.theme.qicon(u'applications-internet'),
			title)
		for name, link in _dict.items():
			if isinstance(link, basestring):
				if not link.startswith(u'http://'):
					link = cfg.online_help_base_url+link
				action = menu.addAction(
					action_page(self.main_window, safe_decode(name,
						enc=u'utf-8'), link, menu))
			else:
				self.build_menu(menu, name, link)
		return menu

	def psychopy_help_menu(self):

		"""
		desc:
			Builds a PsychoPy help menu.

		returns:
			A QMenu.
		"""

		import yaml
		with open(self.ext_resource(u'psychopy_sitemap.yaml')) as fd:
			sitemap = fd.read()
		_dict = yaml.load(sitemap)
		menu = self.build_menu(self.menu, _(u'PsychoPy API'), _dict)
		return menu
