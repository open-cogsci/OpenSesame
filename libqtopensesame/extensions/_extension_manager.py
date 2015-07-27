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

import sys
from PyQt4 import QtGui, QtCore
from libopensesame import plugins
from libopensesame.exceptions import osexception
from libqtopensesame.misc import _
from libqtopensesame.misc.base_subcomponent import base_subcomponent

class extension_manager(base_subcomponent):

	"""
	desc:
		Initializes GUI extensions, and distributes signals (fires) to the
		relevant extensions.
	"""

	def __init__(self, main_window):

		"""
		desc:
			Constructor.

		arguments:
			main_window:	The main-window object.
		"""

		self.setup(main_window)
		self.main_window.set_busy()
		QtGui.QApplication.processEvents()
		self._extensions = []
		self.events = {}
		for ext_name in plugins.list_plugins(_type=u'extensions'):
			try:
				ext = plugins.load_extension(ext_name, self.main_window)
			except Exception as e:
				if not isinstance(e, osexception):
					e = osexception(msg=u'Extension error', exception=e)
				self.notify(
					u'Failed to load extension %s (see debug window for stack trace)' \
					% ext_name)
				self.console.write(e)
			self._extensions.append(ext)
			for event in ext.supported_events():
				if event not in self.events:
					self.events[event] = []
				self.events[event].append(ext)
		self.main_window.set_busy(False)

	def fire(self, event, **kwdict):

		"""
		desc:
			Fires an event to all extensions that support the event.

		arguments:
			event:		The event name.

		keyword-dict:
		kwdict:		A dictionary with keywords that are applicable to a
					particular event.
		"""

		if event == u'open_experiment':
			for ext in self._extensions:
				ext.register_ui_files()
		for ext in self.events.get(event, []):
			try:
				ext.fire(event, **kwdict)
			except Exception as e:
				if not isinstance(e, osexception):
					e = osexception(msg=u'Extension error', exception=e)
				self.notify(
					u'Extension %s misbehaved on event %s (see debug window for stack trace)' \
					% (ext.name(), event))
				self.console.write(e)
