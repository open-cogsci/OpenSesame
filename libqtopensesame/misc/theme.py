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

import os.path
import imp
from libopensesame import debug, misc
from libqtopensesame.misc import config
from PyQt4 import QtGui, QtCore

available_themes = [u'default']

class theme:

	"""Handles the GUI theme"""

	default_icon_size = 32

	def __init__(self, main_window, theme=None):

		"""
		Constructor

		Arguments:
		main_window -- the main_window object

		Keyword arguments:
		theme -- the theme to be used or None to use config (default=None)
		"""

		self.main_window = main_window
		self.fallback_icon = QtGui.QIcon(os.path.join(misc.resource(u"theme"),
			u"fallback.png"))
		if theme == None:
			self.theme = config.get_config(u"theme")
		else:
			self.theme = theme
		self.theme_folder = misc.resource(os.path.join(u"theme", \
			self.theme))
		debug.msg(u"theme = '%s' (%s)" % (self.theme, self.theme_folder))
		if self.theme_folder == None or not os.path.exists(self.theme_folder):
			debug.msg(u"theme '%s' does not exist, using 'default'" % theme, \
				reason=u"warning")
			self.theme = u"default"
			self.theme_folder = misc.resource(os.path.join(u"theme", \
				self.theme))
		self.theme_info = os.path.join(self.theme_folder, u"__theme__.py")
		if os.path.exists(self.theme_info):
			info = imp.load_source(self.theme, self.theme_info)
			self._qss = path = \
				open(os.path.join(self.theme_folder, info.qss)).read()
			self._icon_map = info.icon_map
			self._icon_theme = info.icon_theme
		self.load_icon_map()
		self.apply_theme(self.main_window)

	@property
	def experiment(self):
		return self.main_window.experiment

	def apply_theme(self, widget):

		"""
		Apply the theme to a QWidget, i.e. load the stylesheet and the icons

		Arguments:
		widget -- a QWidget
		"""

		if hasattr(widget, u'setStyleSheet'):
			widget.setStyleSheet(self._qss)
		if hasattr(widget, u"ui"):
			self.load_icons(widget.ui)

	def qicon(self, icon):

		"""
		Get an icon from the theme

		Arguments:
		icon -- the icon name

		Returns:
		A QIcon
		"""

		if isinstance(icon, QtGui.QIcon):
			return icon
		if hasattr(self, u'experiment') and u'%s_large.png' % icon in \
			self.experiment.resources:
			return QtGui.QIcon(self.experiment.resource(u'%s_large.png' % icon))
		if icon in self.icon_map:
			name = self.icon_map[icon][0]
		else:
			name = icon
		icon = QtGui.QIcon.fromTheme(name, self.fallback_icon)
		if icon.name() != name:
			debug.msg(u'missing icon %s' % name, reason=u'warning')
		return icon

	def qpixmap(self, icon, size=None):

		"""
		Get an icon from the theme

		Arguments:
		icon -- the icon name

		Keyword arguments:
		size -- the size of the icon or None for default (default=None)

		Returns:
		A QPixmap
		"""

		if size == None:
			if icon in self.icon_map:
				size = self.icon_map[icon][1]
			else:
				size = self.default_icon_size
		icon = self.qicon(icon)
		return icon.pixmap(size)

	def qlabel(self, icon, size=None):

		"""
		Get an icon from the theme

		Arguments:
		icon -- the icon name

		Keyword arguments:
		size -- the size of the icon or None for default (default=None)

		Returns:
		A QLabel
		"""

		l = QtGui.QLabel()
		l.setPixmap(self.qpixmap(icon, size=size))
		return l

	def load_icon_map(self):

		"""Load the icon map"""

		self.original_theme = QtGui.QIcon.themeName()
		if os.path.exists(os.path.join(self.theme_folder, self._icon_theme)):
			debug.msg(u"using custom icon theme")
			QtGui.QIcon.setThemeSearchPaths(QtGui.QIcon.themeSearchPaths() \
				+ [self.theme_folder])
			QtGui.QIcon.setThemeName(self._icon_theme)
		else:
			debug.msg(u"using default icon theme, icons may be missing", \
				reason=u"warning")
		self.icon_map = {}
		path = os.path.join(self.theme_folder, self._icon_map)
		debug.msg(path)
		for l in open(path):
			l = l.split(",")
			if len(l) == 3:
				try:
					size = int(l[2])
				except:
					size = 32
				alias = l[0].strip()
				name = l[1].strip()
				if alias in self.icon_map:
					debug.msg(u"alias '%s' already in icon map, overwriting" % \
						alias, reason=u"warning")
				self.icon_map[alias] = name, size

	def load_icons(self, ui):

		"""
		Add icons to all icon supporting widgets in a ui object

		Arguments:
		ui -- the ui object to load icons into
		"""

		for i in dir(ui):
			# Oddly enough, it can happend that getattr() fails on items that
			# have been returned by dir(). That's why we need a hasattr() as
			# well.
			if i in self.icon_map and hasattr(ui, i):
				a = getattr(ui, i)
				if hasattr(a, u"setIcon"):
					a.setIcon(self.qicon(i))
				elif hasattr(a, u"setPixmap"):
					a.setPixmap(self.qpixmap(i))

	def set_toolbar_size(self, size):

		"""
		Control the size of the icons in the toolbar

		Arguments:
		size -- a size in pixels
		"""

		self.main_window.ui.toolbar_main.setIconSize(QtCore.QSize(size, size))
		self.main_window.ui.toolbar_items.setIconSize(QtCore.QSize(size, size))
		self.main_window.ui.toolbar_items.build()

	def resource(self, fname):

		"""
		Retrieves the path to a resource within the theme folder.

		Arguments:
		fname	--	The resource filename.

		Returns:
		The full path to the resource file in the theme folder.
		"""

		return os.path.join(self.theme_folder, fname)

