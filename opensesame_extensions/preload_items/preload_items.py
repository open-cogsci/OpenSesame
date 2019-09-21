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
import time
from libqtopensesame.misc.config import cfg
from libqtopensesame.extensions import base_extension
from libopensesame.oslogging import oslogger
from qtpy.QtCore import QTimer


class preload_items(base_extension):

	"""
	desc:
		Silently preloads items in the background to improve usability.
	"""

	def event_startup(self):

		self._timer = QTimer()
		self._timer.setSingleShot(True)
		self._timer.setInterval(cfg.preload_items_interval)
		self._timer.timeout.connect(self._preload_one_item)
		self._timer.start()

	def _preload_one_item(self):

		for name, item in self.item_store.items():
			if item.container_widget is not None:
				continue
			t = time.time()
			self.extension_manager.fire(u'notify_suspend')
			item.init_edit_widget()
			item.edit_widget()
			item.first_refresh = True
			self.extension_manager.fire(u'notify_resume')
			oslogger.debug('preloaded {} in {:.2f} ms\n'.format(
				name,
				1000 * (time.time() - t))
			)
			self._timer.start()
			break

	def event_run_experiment(self, fullscreen):

		self._timer.stop()

	def event_end_experiment(self, ret_val):

		self._timer.start()

	def event_regenerate(self):

		self._timer.start()

	def event_open_experiment(self, path):

		self._timer.start()
