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

__author__ = "Sebastiaan Mathot"
__license__ = "GPLv3"

from qtpy import QtWidgets
from libopensesame import plugins

class plugin_action(QtWidgets.QAction):

	"""Menu action for a plugin"""

	def __init__(self, main_window, menu, plugin):

		"""
		Constructor

		Arguments:
		main_window -- the main window
		menu -- the menu into which the action should be inserted
		plugin -- the name of the plugin
		"""

		self.main_window = main_window
		icon = QtGui.QIcon(plugins.plugin_icon_large(plugin))
		self.plugin = plugin
		QtWidgets.QAction.__init__(self, icon, "Add %s" % plugin, menu)
		self.triggered.connect(self.add_plugin)

	def add_plugin(self, dummy = None):

		"""
		Start a drag to add the plugin to the experiment

		Keyword arguments:
		dummy -- a dummy argument passed by the signal handler (default=None)
		"""

		self.main_window.drag_item(self.plugin)
