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

__author__ = "Sebastiaan Mathot"
__license__ = "GPLv3"

import os.path
import imp
from libopensesame import debug, misc
from libqtopensesame.misc import config
from PyQt4 import QtGui, QtCore

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
		if theme == None:
			self.theme = config.get_config("theme")
		else:
			self.theme = theme
		self.theme_folder = misc.resource(os.path.join("theme", \
			self.theme))
		debug.msg("theme = '%s' (%s)" % (self.theme, self.theme_folder))			
		if self.theme_folder == None or not os.path.exists(self.theme_folder):			
			debug.msg("theme '%s' does not exist, using 'default'" % theme, \
				reason="warning")
			self.theme = "default"
			self.theme_folder = misc.resource(os.path.join("theme", \
				self.theme))						
		self.theme_info = os.path.join(self.theme_folder, "__theme__.py")
		if os.path.exists(self.theme_info):						
			info = imp.load_source(self.theme, self.theme_info)
			self._qss = path = \
				open(os.path.join(self.theme_folder, info.qss)).read()
			self._icon_map = info.icon_map
			self._icon_theme = info.icon_theme									
		self.load_icon_map()
		self.apply_theme(self.main_window)
		
	def apply_theme(self, widget):
	
		"""
		Apply the theme to a QWidget, i.e. load the stylesheet and the icons
		
		Arguments:
		widget -- a QWidget
		"""
				
		widget.setStyleSheet(self._qss)
		if hasattr(widget, "ui"):
			self.load_icons(widget.ui)
				
	def qicon(self, icon):
	
		"""
		Get an icon from the theme
		
		Arguments:
		icon -- the icon name
		
		Returns:
		A QIcon
		"""	
	
		if icon in self.icon_map:
			name, size = self.icon_map[icon]
		else:
			name = icon
		return QtGui.QIcon.fromTheme(name, QtGui.QIcon(os.path.join( \
			misc.resource("theme"), "fallback.png")))
			
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
				name, size = self.icon_map[icon]
			else:
				name = icon
				size = self.default_icon_size			
		else:
			if icon in self.icon_map:
				name = self.icon_map[icon][0]
			else:
				name = icon					
		return QtGui.QIcon.fromTheme(name, QtGui.QIcon(os.path.join( \
			misc.resource("theme"), "fallback.png"))).pixmap(size)
			
	def qlabel(self, icon):
	
		"""
		Get an icon from the theme
		
		Arguments:
		icon -- the icon name
		
		Returns:
		A QLabel		
		"""
	
		l = QtGui.QLabel()
		l.setPixmap(self.qpixmap(icon))
		return l
		
	def load_icon_map(self):
	
		"""Load the icon map"""
	
		if os.path.exists(os.path.join(self.theme_folder, self._icon_theme)):
			debug.msg("using custom icon theme")
			QtGui.QIcon.setThemeSearchPaths(QtGui.QIcon.themeSearchPaths() \
				+ [self.theme_folder])
			QtGui.QIcon.setThemeName(self._icon_theme)
		else:
			debug.msg("using default icon theme, icons may be missing", \
				reason="warning")
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
					debug.msg("alias '%s' already in icon map, overwriting" % \
						alias, reason="warning")
				self.icon_map[alias] = name, size
		
	def load_icons(self, ui):
	
		"""
		Add icons to all icon supporting widgets in a ui object
				
		Arguments:
		ui -- the ui object to load icons into
		"""
		
		debug.msg()
		for i in dir(ui):
			if i in self.icon_map:			
				a = getattr(ui, i)
				if hasattr(a, "setIcon"):
					a.setIcon(self.qicon(i))
				elif hasattr(a, "setPixmap"):
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

