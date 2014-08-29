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

from PyQt4 import QtGui
from libopensesame import debug
from libopensesame import misc
from libqtopensesame.misc import _
from libqtopensesame.extensions import base_extension
from libqtopensesame.misc.base_subcomponent import base_subcomponent
from libqtopensesame.misc.config import cfg

class action_page(QtGui.QAction, base_subcomponent):

	def __init__(self, main_window, title, link, menu):

		self.setup(main_window)
		QtGui.QAction.__init__(self, self.theme.qicon(u'applications-internet'),
			title, menu)
		self.title = title
		self.link = link
		self.triggered.connect(self.open_page)

	def open_page(self):

		self.main_window.tabwidget.open_browser(self.link)

class help(base_extension):
	
	def event_startup(self):

		self.menu = self.menubar.addMenu(_(u'Help'))
		self.action_online_help = self.menu.addMenu(self.online_help_menu())
		self.action_offline_help = self.menu.addAction(
			self.theme.qicon(u'help-contents'), _(u'Offline help'))
		self.action_offline_help.triggered.connect(self.open_offline_help)
		self.menu.addSeparator()

	def open_offline_help(self):

		self.tabwidget.open_browser(self.ext_resource(u'offline_help.md'))

	def online_help_menu(self):

		import urllib2
		import yaml
		version = misc.version
		if u'~' in version:
			version = version[:version.find(u'~')]
		sitemap_url = cfg.online_help_sitemap.replace(u'[version]', version)
		try:
			fd = urllib2.urlopen(sitemap_url)
			sitemap = fd.read()
			_dict = yaml.load(sitemap)
		except:
			return self.menu.addMenu(
				self.theme.qicon(u'network-error'),
				_('Online help (failed to load)'))
		menu = self.build_menu(self.menu, _(u'Online help'), _dict)
		return menu

	def build_menu(self, parent_menu, title, _dict):

		menu = parent_menu.addMenu(self.theme.qicon(u'applications-internet'),
			title)
		for name, link in _dict.items():
			if isinstance(link, basestring):
				action = menu.addAction(
					action_page(self.main_window, name,
						cfg.online_help_base_url+link, menu))
			else:
				self.build_menu(menu, name, link)
		return menu
