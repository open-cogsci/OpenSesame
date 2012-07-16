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

from libopensesame import misc
from libqtopensesame.misc import config
from libqtopensesame.ui.credits_widget_ui import Ui_widget_credits
from PyQt4 import QtGui, QtCore

class credits_widget(QtGui.QWidget):

	"""A widget with the opensesame credits"""

	def __init__(self, parent=None):
	
		"""
		Constructor

		Keywords arguments:
		parent -- the parent QWidget
		"""	
	
		QtGui.QTabWidget.__init__(self, parent)		
		self.ui = Ui_widget_credits()
		self.ui.setupUi(self)
		
	def initialize(self, main_window):
	
		self.main_window = main_window
		self.main_window.theme.apply_theme(self)
		self.ui.label_opensesame.setText(unicode( \
			self.ui.label_opensesame.text()).replace("[version]", \
			misc.version).replace("[codename]", misc.codename))			
		self.ui.label_website.mousePressEvent = self.open_website
		self.ui.label_facebook.mousePressEvent = self.open_facebook
		self.ui.label_twitter.mousePressEvent = self.open_twitter
			
	def open_website(self, dummy=None):
	
		"""Open the main website"""
		
		misc.open_url(config.get_config("url_website"))
		
	def open_facebook(self, dummy=None):
	
		"""Open Facebook page"""	

		misc.open_url(config.get_config("url_facebook"))

	def open_twitter(self, dummy=None):
	
		"""Open Twitter page"""	
	
		misc.open_url(config.get_config("url_twitter"))					
		
