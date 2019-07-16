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
from libqtopensesame.misc import drag_and_drop
from libqtopensesame.misc.base_component import base_component

class base_subcomponent(base_component):

	"""
	desc:
		A base class for all components that require an experiment and theme
		property.
	"""

	# These properties allow for cleaner programming, without dot references.

	@property
	def experiment(self):
		return self.main_window.experiment

	@property
	def tabwidget(self):
		return self.main_window.ui.tabwidget

	@property
	def theme(self):
		return self.main_window.theme

	@property
	def notify(self):
		return self.main_window.experiment.notify

	@property
	def text_input(self):
		return self.main_window.experiment.text_input

	@property
	def item_store(self):
		return self.experiment.items

	@property
	def extensions(self):
		return self.main_window.extension_manager._extensions

	@property
	def extension_manager(self):
		return self.main_window.extension_manager

	@property
	def overview_area(self):
		return self.main_window.ui.itemtree

	@property
	def console(self):
		return self.main_window.console

	@property
	def pool(self):
		return self.main_window.experiment.pool

	@property
	def locale(self):
		return self.main_window._locale

	@property
	def item_toolbar(self):
		return self.main_window.ui.toolbar_items

	@property
	def main_toolbar(self):
		return self.main_window.ui.toolbar_main


# PEP8 alias
BaseSubcomponent = base_subcomponent
