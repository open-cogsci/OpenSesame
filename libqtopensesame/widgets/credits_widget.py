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

from libopensesame import misc, metadata
from libqtopensesame.misc import config
from libqtopensesame.widgets.base_widget import base_widget
from libopensesame.py3compat import *
from qtpy import QtWidgets, QtCore

class credits_widget(base_widget):

	"""
	desc:
		A credits window, embedded in the start-new widget.
	"""

	def __init__(self, main_window):

		"""
		desc:
			Constructor.

		keywords:
			main_window:	A qtopensesame object.
		"""

		super(credits_widget, self).__init__(main_window,
			ui=u'widgets.credits_widget')
		self.ui.label_opensesame.setText(self.ui.label_opensesame.text() % {
			u'version' : metadata.__version__,
			u'codename' : metadata.codename,
			u'channel' : metadata.channel,
			u'python_version' : metadata.python_version
			})
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
