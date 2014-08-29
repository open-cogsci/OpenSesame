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

import sys
from libopensesame import plugins
from libqtopensesame.misc.base_subcomponent import base_subcomponent

class extension_manager(base_subcomponent):

	def __init__(self, main_window):

		self.setup(main_window)
		self._extensions = []
		self.events = {}
		for ext_name in plugins.list_plugins(_type=u'extensions'):
			ext = plugins.load_extension(ext_name, self.main_window)
			self._extensions.append(ext)
			for event in ext.supported_events():
				if event not in self.events:
					self.events[event] = []
				self.events[event].append(ext)

	def fire(self, event, **kwdict):

		for ext in self.events.get(event, []):
			ext.fire(event, **kwdict)
