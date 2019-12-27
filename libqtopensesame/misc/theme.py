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
import os.path
import imp
from libopensesame import misc
from libopensesame.oslogging import oslogger
from libqtopensesame.misc.config import cfg
from qtpy import QtGui, QtWidgets, QtCore

available_themes = [u'default', u'monokai']


class theme(object):

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
		self.fallback_icon = QtGui.QIcon(
			os.path.join(misc.resource(u"theme"), u"fallback.png")
		)
		self.theme = cfg.theme if theme is None else theme
		self.theme_folder = misc.resource(os.path.join(u"theme", self.theme))
		oslogger.debug(u"theme = '%s' (%s)" % (self.theme, self.theme_folder))
		# The theme folder must exist, and contain a file called __theme__.py,
		# if not, we fall back to the default theme, which is assumed to always
		# exist.
		if self.theme_folder is None or not os.path.exists(
			os.path.join(self.theme_folder, u'__theme__.py')):
			oslogger.warning(
				u"theme '%s' does not exist, using 'default'" % theme,
			)
			self.theme = u"default"
			self.theme_folder = misc.resource(
				os.path.join(u"theme", self.theme))
		self.theme_info = os.path.join(self.theme_folder, u"__theme__.py")
		if os.path.exists(self.theme_info):
			info = imp.load_source(
				self.theme,
				safe_str(self.theme_info, enc=misc.filesystem_encoding())
			)
			with safe_open(os.path.join(self.theme_folder, info.qss)) as fd:
				self._qss = fd.read()
			self._icon_map = info.icon_map
			self._icon_theme = info.icon_theme
			if hasattr(info, 'qdatamatrix'):
				from qdatamatrix import _qcell
				for key, color in info.qdatamatrix.items():
					setattr(_qcell, key, color)
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

	def qfileicon(self, path):

		"""
		desc:
			Gets an filetype icon for a file.

		arguments:
			path:	The full path to the file. The file must exist.

		returns:
			type:	QIcon
		"""

		try:
			import fileinspector
		except ImportError:
			return QtWidgets.QFileIconProvider().icon(QtCore.QFileInfo(path))
		filetype = fileinspector.determine_type(path, output='xdg')
		if filetype is None:
			filetype = u'text-x-generic'
		category = fileinspector.determine_category(filetype)
		if category is None:
			fallback = u'text-x-generic'
		else:
			fallback = category + u'-x-generic'
		return QtGui.QIcon.fromTheme(
			filetype,
			QtGui.QIcon.fromTheme(fallback)
		)

	def qicon(self, icon):

		"""
		desc:
			Gets an icon from the theme.

		arguments:
			icon:	One of the following:
					- A QIcon, which returned as is
					- The name of an image file
					- The name of a plug-in with a hardcoded icon
					- The name of an entry in the icon map
					- A theme icon name.

		returns:
			desc:	An icon, or a fallback icon if the specified wasn't found.
			type:	QIcon
		"""

		if isinstance(icon, QtGui.QIcon):
			return icon
		if os.path.isfile(icon):
			qicon = QtGui.QIcon()
			if icon.endswith(u'_large.png'):
				size = 32
			else:
				size = 16
			qicon.addFile(icon, size=QtCore.QSize(size, size))
			return qicon
		if (
			hasattr(self, u'experiment') and
			(
				u'%s_large.png' % icon in self.experiment.resources or
				'%s.png' in self.experiment.resources
			)
		):
			qicon = QtGui.QIcon()
			if u'%s_large.png' % icon in self.experiment.resources:
				qicon.addFile(
					self.experiment.resource(u'%s_large.png' % icon),
					size=QtCore.QSize(32, 32)
				)
			if u'%s.png' % icon in self.experiment.resources:
				qicon.addFile(
					self.experiment.resource(u'%s.png' % icon),
					size=QtCore.QSize(16, 16)
				)
			return qicon
		if icon in self.icon_map:
			name = self.icon_map[icon][0]
		else:
			name = icon
		icon = QtGui.QIcon.fromTheme(name, self.fallback_icon)
		if icon.name() != name:
			oslogger.warning(u'missing icon %s' % name)
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

		if isinstance(icon, basestring) and os.path.exists(icon):
			return QtGui.QPixmap(icon)
		if size is None:
			if icon in self.icon_map:
				size = self.icon_map[icon][1]
			else:
				size = self.default_icon_size
		size = QtCore.QSize(size, size)
		# Pixmap should never return a pixmap larger than the requested size.
		# However, this does happen on some versions of Qt4. Therefore, we check
		# the size, and scale if necessary.
		pixmap = self.qicon(icon).pixmap(size)
		if pixmap.size() != size:
			pixmap = pixmap.scaled(size)
		return pixmap

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

		label = QtWidgets.QLabel()
		label.setPixmap(self.qpixmap(icon, size=size))
		return label

	def load_icon_map(self):

		"""Load the icon map"""

		self.original_theme = QtGui.QIcon.themeName()
		if os.path.exists(os.path.join(self.theme_folder, self._icon_theme)):
			oslogger.debug(u"using custom icon theme")
			QtGui.QIcon.setThemeSearchPaths(
				QtGui.QIcon.themeSearchPaths() + [self.theme_folder]
			)
			QtGui.QIcon.setThemeName(self._icon_theme)
		else:
			oslogger.warning(u"using default icon theme, icons may be missing")
		self.icon_map = {}
		path = os.path.join(self.theme_folder, self._icon_map)
		with safe_open(path) as fd:
			for line in fd:
				line = line.split(u',')
				if len(line) != 3:
					continue
				try:
					size = int(line[2])
				except ValueError:
					size = 32
				alias = line[0].strip()
				name = line[1].strip()
				if alias in self.icon_map:
					oslogger.debug(
						u"alias '%s' already in icon map, overwriting" % alias,
						reason=u"warning"
					)
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
