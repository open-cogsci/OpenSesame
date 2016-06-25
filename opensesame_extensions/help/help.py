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
from libopensesame import misc
from libqtopensesame.extensions import base_extension
from libqtopensesame.misc.base_subcomponent import base_subcomponent
from libqtopensesame.misc.config import cfg
from libopensesame.py3compat import *
if py3:
	from urllib.request import urlopen
else:
	from urllib2 import urlopen
import yaml
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

		self._urls = []
		self.menu = self.menubar.addMenu(_(u'Help'))
		menu = self.online_help_menu(
			sitemap_url=cfg.online_help_sitemap.replace(u'[version]',
				metadata.main_version),
			base_url=cfg.online_help_base_url, label=_(u'Online help'),
			local_sitemap=u'sitemap-osdoc.yaml')
		if menu is not None:
			self.action_online_help = self.menu.addMenu(menu)
		# menu = self.online_help_menu(
		# 	sitemap_url=u'http://docs.expyriment.org/0.8.0/sitemap.yml',
		# 	base_url=u'http://expyriment.org/', label=_(u'Expyriment API'),
		# 	local_sitemap=u'sitemap-expyriment.yaml')
		# if menu is not None:
		# 	self.action_online_help = self.menu.addMenu(menu)
		menu = self.psychopy_help_menu()
		if menu is not None:
			self.action_psychopy_help = self.menu.addMenu(menu)
		self.menu.addSeparator()

	def online_help_menu(self, sitemap_url, base_url, label,
		local_sitemap=None):

		"""
		desc:
			Build online help menu based on remote sitemap.
		"""

		try:
			fd = urlopen(sitemap_url)
			sitemap = fd.read()
			_dict = yaml.load(sitemap)
		except:
			if local_sitemap is None:
				return
			with open(self.ext_resource(local_sitemap)) as fd:
				sitemap = fd.read()
				_dict = yaml.load(sitemap)
		if not isinstance(_dict, dict):
			return
		menu = self.build_menu(self.menu, base_url, label, _dict)
		return menu

	def build_menu(self, parent_menu, base_url, title, _dict):

		"""
		desc:
			A helper function to build the online-help menu.

		arguments:
			parent_menu:	A parent QMenu for a submenu.
			base_url:		A prefix for relative urls.
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
				if not link.startswith(u'http://') and \
					not link.startswith(u'https://'):
					link = base_url+link
				self._urls.append(link)
				action = menu.addAction(
					action_page(self.main_window, safe_decode(name,
						enc=u'utf-8'), link, menu))
			else:
				self.build_menu(menu, base_url, name, link)
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
		menu = self.build_menu(self.menu, None, _(u'PsychoPy API'), _dict)
		return menu

	def build_cache(self):

		"""
		desc:
			Creates a webbrowser cache for all help pages. This is mostly a help
			function so that this cache can be bundled along with OpenSesame
			when it is distributed, so that help is also available offline.
		"""

		import pickle

		cache = {}
		for url in self._urls:
			try:
				fd = urlopen(url)
				page = fd.read()
			except:
				print('failed to cache %s' % url)
				continue
			cache[url] = page
			print('cached %s' % url)
		with open(u'help-cache.pkl', u'w') as fd:
			pickle.dump(cache, fd, protocol=2)
