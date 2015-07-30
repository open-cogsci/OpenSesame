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

	def set_supported_drop_types(self, types=None):

		if not hasattr(self, u'setAcceptDrops'):
			raise osexception(u'Not a QWidget')
		if types is None:
			self.setAcceptDrops(False)
			self.supported_drop_types = None
			return
		self.setAcceptDrops(True)
		self.supported_drop_types = types

	def dragEnterEvent(self, e):

		"""
		desc:
			Handles drag-enter events to see if they are supported

		arguments:
			e:
				desc:	A drag-enter event.
				type:	QDragEnterEvent
		"""

		data = drag_and_drop.receive(e)
		if drag_and_drop.matches(data, self.supported_drop_types):
			e.accept()
		else:
			e.ignore()

	def dropEvent(self, e):

		"""
		desc:
			Handles drop events and accepts them if supported.

		arguments:
			e:
				desc:	A drop event.
				type:	QDropEvent
		"""

		data = drag_and_drop.receive(e)
		if drag_and_drop.matches(data, self.supported_drop_types):
			e.accept()
			self.accept_drop(data)
		else:
			e.ignore()

	def accept_drop(self, data):

		"""
		desc:
			Is called after a supported drop type. Should be re-implemented.

		arguments:
			data:
				desc:	The drop data.
				type:	dict
		"""

		pass

	# These properties allow for cleaner programming, without dot references.

	@property
	def experiment(self):
		return self.main_window.experiment

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
	def console(self):
		return self.main_window.console

	@property
	def pool(self):
		return self.main_window.experiment.pool
