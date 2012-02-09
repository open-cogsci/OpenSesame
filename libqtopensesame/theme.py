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
from libopensesame import debug, misc
from libqtopensesame import config
from PyQt4 import QtGui, QtCore

class theme:

	def __init__(self, main_window):
	
		"""
		Constructor
		"""

		self.main_window = main_window
		self.theme = config.get_config("theme")
		self.theme_folder = misc.resource(os.path.join("theme", \
			self.theme))
		debug.msg("theme folder = '%s'" % self.theme_folder)
		
		self.load_qss()
		self.load_icon_map()
		self.load_icons()
				
	def qicon(self, icon):
	
		if icon in self.icon_map:
			name, size = self.icon_map[icon]
		else:
			name = icon
		return QtGui.QIcon.fromTheme(name, QtGui.QIcon(os.path.join( \
			misc.resource("theme"), "fallback.png")))
			
	def qpixmap(self, icon):
		
		if icon in self.icon_map:
			name, size = self.icon_map[icon]
		else:
			name = icon
			size = 32
		return QtGui.QIcon.fromTheme(name, QtGui.QIcon(os.path.join( \
			misc.resource("theme"), "fallback.png"))).pixmap(size)
			
	def qlabel(self, icon):
	
		l = QtGui.QLabel()
		l.setPixmap(self.qpixmap(icon))
		return l
		
	def load_icon_map(self):
	
		QtGui.QIcon.setThemeSearchPaths(QtGui.QIcon.themeSearchPaths() \
			+ [self.theme_folder])
		QtGui.QIcon.setThemeName("oscustom")
		self.icon_map = {}
		for l in open(os.path.join(self.theme_folder, "icon_map.csv")):
			l = l.split(",")			
			if len(l) == 3:
				try:
					size = int(l[2])
				except:
					size = 32
				self.icon_map[l[0].strip()] = l[1].strip(), size
		
	def load_icons(self):
	
		for i in dir(self.main_window.ui):
			if i in self.icon_map:			
				a = getattr(self.main_window.ui, i)
				if hasattr(a, "setIcon"):
					a.setIcon(self.qicon(self.icon_map[i][0]))
				elif hasattr(a, "setPixmap"):
					a.setPixmap(self.qpixmap(self.icon_map[i][0]))
						
	def load_qss(self):
	
		path = os.path.join(self.theme_folder, "stylesheet.qss")
		debug.msg("reading '%s'" % path)
		self.main_window.setStyleSheet(open(path).read())
		
		
