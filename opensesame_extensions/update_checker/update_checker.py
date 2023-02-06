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
from qtpy.QtCore import QTimer
import multiprocessing
from distutils.version import StrictVersion
from libopensesame import metadata
from libopensesame.oslogging import oslogger
from libqtopensesame.extensions import base_extension
from libqtopensesame.misc.config import cfg
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'update_checker', category=u'extension')

POLL_MAX_ATTEMPT = 5
POLL_DELAY = 5000


class update_checker(base_extension):

    def activate(self):

        self._check_for_updates()

    def event_startup(self):

        self._checking = False
        self._check_for_updates(always=False)

    def _check_for_updates(self, always=True):

        self._always = always
        if not always and not cfg.auto_update_check:
            oslogger.debug(u'skipping update check')
            return
        if self._checking:
            oslogger.debug(u'update check already in progress')
            return
        self._checking = True
        self._queue = multiprocessing.Queue()
        self._update_checker = multiprocessing.Process(
            target=_update_checker,
            args=(self._queue, cfg.remote_metadata_url)
        )
        self._update_checker.start()
        self.extension_manager.fire(
            'register_subprocess',
            pid=self._update_checker.pid,
            description='update_checker'
        )
        oslogger.debug(u'checking (PID={})'.format(self._update_checker.pid))
        self._attempt = 1
        QTimer.singleShot(1000, self._poll_update_process)

    def _error_notify(self):

        self.extension_manager.fire(
            u'notify',
            message=_(u'Failed to check for updates'),
            category=u'warning',
            always_show=True,
        )

    def _poll_update_process(self):

        if self._queue.empty():
            if self._attempt > POLL_MAX_ATTEMPT:
                oslogger.debug(u'giving up')
                if self._update_checker.is_alive():
                    oslogger.debug(u'terminating update-checker process')
                    self._update_checker.terminate()
                self._checking = False
            else:
                oslogger.debug(u'queue still empty ({})'.format(self._attempt))
                self._attempt += 1
                QTimer.singleShot(POLL_DELAY, self._poll_update_process)
            return
        content = self._queue.get()
        self._update_checker.join()
        try:
            self._update_checker.close()
        except AttributeError:
            # Process.close() was introduced only in Python 3.7
            pass
        self._checking = False
        if content is None:
            self._error_notify()
            return
        try:
            remote_metadata = safe_yaml_load(content)
            remote_strict_version = StrictVersion(
                remote_metadata[u'stable_version'])
        except Exception as e:
            self._error_notify()
            oslogger.error(u"failed to parse metadata: {}".format(e))
            return
        if remote_strict_version > metadata.strict_version:
            oslogger.debug(u"new version available")
            s = safe_read(self.ext_resource(u'update-available.md'))
            self.tabwidget.open_markdown(
                s % remote_metadata,
                title=u'Update available!'
            )
            return
        oslogger.debug(u"up to date")
        if not self._always:
            return
        self.tabwidget.open_markdown(
            self.ext_resource(u'up-to-date.md'),
            title=_(u'Up to date!')
        )


def _update_checker(queue, metadata_url):

    from urllib.request import urlopen
    try:
        fd = urlopen(metadata_url, timeout=1)
        content = fd.read()
        fd.close()
    except Exception as e:
        print('failed to check for updates: {}'.format(e))
        queue.put(None)
    else:
        queue.put(content)
    queue.close()
    queue.join_thread()
