# -*- coding: utf-8 -*-
"""
@author: Daniel Schreij

This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

This module is distributed under the Apache v2.0 License.
You should have received a copy of the Apache v2.0 License
along with this module. If not, see <http://www.apache.org/licenses/>.
"""
# Python3 compatibility
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from qtpy import QtWidgets, QtCore, QtGui

import QNotifications

from libopensesame import debug
from libopensesame.exceptions import osexception
from libopensesame.py3compat import *
from libqtopensesame.extensions import base_extension
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'notifications', category=u'extension')

__author__ = u"Daniel Schreij"
__license__ = u"GPLv3"

import os

class notifications(base_extension):
	### OpenSesame events
	def event_startup(self):
		self.notification_area = QNotifications.QNotificationArea(self.tabwidget)
		self.notification_area.setEntryEffect(u'fadeIn', 200)
		self.notification_area.setExitEffect(u'fadeOut', 200)
	
	def event_save_experiment(self, path):
		""" Displays a notification after an experiment has been saved. """
		self.event_notify(_(u"Experiment has been saved"), u"info")

	def event_notify(self, message, kind='primary', timeout=5000):
		""" Show a notification 'message' in the style 'notification type' for
		'timeout' milliseconds (where 0 milliseconds displays the notification 
		indefinitely, until the user removes it)."""
		self.notification_area.display(message, kind, timeout)
		
	
	