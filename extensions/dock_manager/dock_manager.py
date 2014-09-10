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

from PyQt4 import QtGui
from libqtopensesame.extensions import base_extension
from libqtopensesame.misc.config import cfg

class dock_manager(base_extension):

	"""
	desc:
		Locks the dock widgets and sets the dock title orientation.
	"""

	def dock_widgets(self):

		"""
		returns:
			A list of QDockWidget items.
		"""

		return [
			self.main_window.ui.dock_stdout,
			self.main_window.ui.dock_pool,
			self.main_window.ui.dock_variable_inspector,
			self.main_window.ui.dock_overview
			]

	def event_startup(self):

		"""
		desc:
			Sets the dock title orientation and the initial lock status.
		"""

		if cfg.vertical_dock_titles:
			for dock in self.dock_widgets():
				dock.setFeatures(dock.features() \
					| QtGui.QDockWidget.DockWidgetVerticalTitleBar)
		if cfg.lock_dock_widgets:
			self.lock_dock_widgets()
			self.set_checked(True)
		else:
			self.unlock_dock_widgets()
			self.set_checked(False)

	def activate(self):

		"""
		desc:
			Toggles the locked status.
		"""

		if cfg.lock_dock_widgets:
			self.unlock_dock_widgets()
		else:
			self.lock_dock_widgets()

	def lock_dock_widgets(self):

		"""
		desc:
			Locks the dock widgets.
		"""

		cfg.lock_dock_widgets = True
		for dock in self.dock_widgets():
			dock.setFeatures(dock.features() \
				^ QtGui.QDockWidget.DockWidgetClosable \
				^ QtGui.QDockWidget.DockWidgetMovable \
				^ QtGui.QDockWidget.DockWidgetFloatable)

	def unlock_dock_widgets(self):

		"""
		desc:
			Unlocks the dock widgets.
		"""

		cfg.lock_dock_widgets = False
		for dock in self.dock_widgets():
			dock.setFeatures(dock.features() \
				| QtGui.QDockWidget.DockWidgetClosable \
				| QtGui.QDockWidget.DockWidgetMovable \
				| QtGui.QDockWidget.DockWidgetFloatable)
