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
from libqtopensesame.extensions import base_extension


class quick_switcher(base_extension):

	"""
	desc:
		The quick-switcher allows you to quickly navigate to items and
		functions, and to quickly activate menu actions.
	"""

	# We need to update or fully refresh the dialog after several structural
	# changes.

	def event_startup(self):
		self.d = None

	def event_open_experiment(self, path):
		self.d = None

	def event_rename_item(self, from_name, to_name):
		if self.d is not None:
			self.d.rename_item(from_name, to_name)

	def event_new_item(self, name, _type):
		if self.d is not None:
			self.d.add_item(name)

	def event_delete_item(self, name):
		if self.d is not None:
			self.d.delete_item(name)

	def event_purge_unused_items(self):
		self.d = None

	def event_regenerate(self):
		self.d = None

	def event_change_item(self, name):
		if self.d is not None:
			if self.experiment.items._type(name) == u'inline_script':
				self.d.refresh_item(name)
				
	def event_open_item(self, name):
		if self.d is not None:
			self.d.bump_item(name)

	def init_dialog(self):

		"""
		desc:
			Re-init the dialog.
		"""

		self.set_busy()
		from quick_switcher_dialog.dialog import quick_switcher
		self.d = quick_switcher(self.main_window)
		self.set_busy(False)

	def activate(self):

		"""
		desc:
			Pops up the quick-switcher dialog.
		"""

		if not hasattr(self, u'd') or self.d is None:
			self.init_dialog()
		self.d.items_list_widget.sortItems()
		self.d.exec_()
