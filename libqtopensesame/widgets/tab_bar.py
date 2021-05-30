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
from qtpy.QtWidgets import QTabBar, QMenu, QAction
from qtpy.QtCore import Qt
from libqtopensesame.misc.base_subcomponent import BaseSubcomponent
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'tab_bar', category=u'core')


class TabBar(BaseSubcomponent, QTabBar):
	"""A tab-bar for the overview area, implementing a right-click context
	menu, and a close-on-middle-click.
	"""
	
	def __init__(self, tab_widget):
		
		QTabBar.__init__(self, tab_widget)
		BaseSubcomponent.setup(self, tab_widget)
		self._tab_widget = tab_widget
		self.setContextMenuPolicy(Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self._show_context_menu)
		
	def mousePressEvent(self, event):
		
		QTabBar.mousePressEvent(self, event)
		if event.button() == Qt.MiddleButton:
			self._tab_widget.removeTab(self.tabAt(event.pos()))
			
	def _show_context_menu(self, pos):
		
		tab_index = self.tabAt(pos)
		self._tab_widget.setCurrentIndex(tab_index)
		menu = QMenu(self)
		menu.addAction(self.main_window.ui.action_close_current_tab)
		menu.addAction(self.main_window.ui.action_close_all_tabs)
		menu.addAction(self.main_window.ui.action_close_other_tabs)
		if 'tab_to_dockwidget' in self.extension_manager:
			menu.addSeparator()
			menu.addAction(
				self.extension_manager['tab_to_dockwidget'].action
			)
		menu.exec_(self.mapToGlobal(pos))
