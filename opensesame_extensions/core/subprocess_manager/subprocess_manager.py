# coding=utf-8

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
import multiprocessing
from queue import Empty
import psutil
from qtpy.QtCore import Qt, QTimer
from qtpy.QtWidgets import QDockWidget
from datamatrix import DataMatrix
from qdatamatrix import QDataMatrix
from libqtopensesame.misc.config import cfg
from libopensesame.oslogging import oslogger
from libqtopensesame.extensions import BaseExtension
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'SubprocessManager', category=u'extension')

PARACHUTE_STOP = -1
PARACHUTE_HEARTBEAT = -2
PARACHUTE_HEARTBEAT_INTERVAL = 5


def parachute(queue, main_pid):
    
    """This function runs as a subprocess and receives the PIDs off all
    subprocesses. Whether the main process is alive is kept track of with a
    heartbeat. If no heartbeat comes in, then all subprocesses are killed to
    make sure that no runaway processes are left on shutdown.
    """

    oslogger.start('parachute')
    pids = [main_pid]
    oslogger.debug('main-process PID: {}'.format(main_pid))
    while True:
        try:
            pid = queue.get(True, 2 * PARACHUTE_HEARTBEAT_INTERVAL)
        except (Empty, ValueError, OSError):
            # If something is blocking the main process, the heartbeat stops.
            # This can happen for example if something is executed in an
            # in-process console. In that case we don't want to kill everything
            # off.
            if psutil.pid_exists(main_pid):
                oslogger.warning('main process is alive but unresponsive')
                continue
            oslogger.warning('main process appears to have died')
            break
        if pid == PARACHUTE_STOP:
            oslogger.debug('parchute stop')
            return
        if pid == PARACHUTE_HEARTBEAT:
            continue
        oslogger.debug('subprocess PID: {}'.format(pid))
        pids.append(pid)
    for pid in filter(psutil.pid_exists, pids):
        oslogger.warning('parachute killing PID: {}'.format(pid))
        p = psutil.Process(pid)
        p.kill()


class SubprocessDockWidget(QDockWidget):
    
    def __init__(self, subprocess_manager):
        
        QDockWidget.__init__(self, subprocess_manager.main_window)
        self._subprocess_manager = subprocess_manager
        self._qdm = QDataMatrix(self._subprocess_manager.dm(), read_only=True)
        self.setWidget(self._qdm)
        self.setWindowTitle(_('Subprocesses'))
        self.setObjectName('SubprocessManager')
        self.visibilityChanged.connect(self._refresh)
    
    def _refresh(self):

        if not self.isVisible():
            return
        self._qdm.dm = self._subprocess_manager.dm()
        self._qdm.refresh()
        QTimer.singleShot(2000, self._refresh)
    

class SubprocessManager(BaseExtension):
    
    def activate(self):

        if not hasattr(self, '_dock_widget'):
            self._dock_widget = SubprocessDockWidget(self)
            self.main_window.addDockWidget(
                Qt.RightDockWidgetArea,
                self._dock_widget
            )
        self._dock_widget.setVisible(True)

    def dm(self):
        
        died = []
        pids = [os.getpid()]
        states = ['running']
        descs = ['MainProcess']
        for pid, description in self._processes.items():
            if not psutil.pid_exists(pid):
                self._ended.append((pid, description))
                died.append(pid)
                continue
            pids.append(pid)
            states.append('running')
            descs.append(description)
        for pid in died:
            del self._processes[pid]
        if cfg.subprocess_manager_show_ended:
            for pid, description in self._ended:
                pids.append(pid)
                states.append('ended')
                descs.append(description)
        dm = DataMatrix(length=len(pids))
        dm.pid = pids
        dm.state = states
        dm.description = descs
        return dm

    def event_register_subprocess(self, pid, description):
        
        if not hasattr(self, '_parachute'):
            self._processes = {}
            self._parachute_start()
            self._ended = []
        oslogger.debug('{}: {}'.format(pid, description))
        self._processes[pid] = description
        self._queue.put(pid)

    def event_close(self):
        
        for pid in self._active_processes:
            oslogger.debug('killing process {} ({})'.format(
                pid, self._processes[pid]))
            p = psutil.Process(pid)
            p.kill()
            
    def event_run_experiment(self, fullscreen):
        
        self._parachute_stop()
        
    def event_end_experiment(self, ret_val):
        
        self._parachute_start()
        
    def provide_subprocess_pids(self):
        
        return list(self._processes.keys())
            
    def _parachute_start(self):
        
        self._queue = multiprocessing.Queue()
        self._parachute = multiprocessing.Process(
            target=parachute,
            args=(self._queue, os.getpid())
        )
        self._parachute.start()
        for pid in self._active_processes:
            self._queue.put(pid)
        QTimer.singleShot(
            1000 * PARACHUTE_HEARTBEAT_INTERVAL,
            self._pararchute_heartbeat
        )
        
    @property
    def _active_processes(self):
        
        return filter(psutil.pid_exists, self._processes)
        
    def _parachute_stop(self):
        
        self._queue.put(PARACHUTE_STOP)

    def _pararchute_heartbeat(self):
        
        self._queue.put(PARACHUTE_HEARTBEAT)
        QTimer.singleShot(
            1000 * PARACHUTE_HEARTBEAT_INTERVAL,
            self._pararchute_heartbeat
        )
