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
import os.path
import sys

class webbrowser(QtWebKit.QWebView):

	"""
	A very basic wrapper around QWebView, which currently adds nothing. This is
	used to add a browser tab to opensesame
	"""

	def __init(self, parent=None):
	
		"""
		Constructor
		
		Keyword arguments:
		parent -- the parent QWidget (default=None)		
		"""
	
		QtGui.QWebView.__init__(self, parent)						
				
