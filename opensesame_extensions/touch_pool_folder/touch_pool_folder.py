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
import os
from qtpy import QtCore
from libqtopensesame.misc.config import cfg
from libqtopensesame.extensions import base_extension


class touch_pool_folder(base_extension):

	"""
	desc:
		Touches the pool folder every once in a while so that Windows (and
		perhaps other operating systems) doesn't clear it up.
	"""

	def event_startup(self):

		self._timer = None
		self._start_timer()

	def _start_timer(self):

		print('Touching %s' % self.experiment.pool_folder)
		os.utime(self.experiment.pool_folder, None)
		self._timer = QtCore.QTimer()
		self._timer.setInterval(cfg.touch_interval)
		self._timer.setSingleShot(True)
		self._timer.timeout.connect(self._start_timer)
		self._timer.start()

	def event_run_experiment(self, fullscreen):

		if self._timer is not None:
			self._timer.stop()

	def event_end_experiment(self, ret_val):

		if self._timer is not None:
			self._timer.start()
