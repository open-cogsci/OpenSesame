# -*- coding:utf-8 -*-

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
from qtpy.QtCore import QAbstractEventDispatcher, QTime


class preload_items(base_extension):

    """
    desc:
            Silently preloads items in the background to improve usability.
    """

    def event_startup(self):

        self._monitoring_idle = False
        self._interval = cfg.preload_items_interval
        self._threshold = cfg.preload_items_idle_threshold
        self._start_idle_monitor()

    def _start_idle_monitor(self):

        if self._monitoring_idle:
            return
        self._idle = False
        self._monitoring_idle = True
        self._aed = QAbstractEventDispatcher.instance()
        self._aed.awake.connect(self._on_awake)
        self._n_events = 0
        self._last_update = QTime.currentTime()
        oslogger.debug('starting idle monitor')

    def _stop_idle_monitor(self):

        if not self._monitoring_idle:
            return
        self._aed.awake.disconnect()
        self._monitoring_idle = False
        oslogger.debug('stopping idle monitor')

    def _on_awake(self):

        self._n_events += 1
        self._last_awake = QTime.currentTime()
        time_past = self._last_update.msecsTo(self._last_awake)
        if time_past < self._interval:
            return
        event_rate = self._n_events / time_past
        if event_rate < self._threshold:
            self._idle = True
            oslogger.debug('idle {:4f}'.format(event_rate))
            self._preload_one_item()
        else:
            self._idle = False
            oslogger.debug('busy {:4f}'.format(event_rate))
        self._last_update = self._last_awake
        self._n_events = 0

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
            break
        else:
            self._stop_idle_monitor()

    def event_run_experiment(self, fullscreen):

        self._stop_idle_monitor()

    def event_end_experiment(self, ret_val):

        self._start_idle_monitor()

    def event_regenerate(self):

        self._start_idle_monitor()

    def event_open_experiment(self, path):

        self._start_idle_monitor()
