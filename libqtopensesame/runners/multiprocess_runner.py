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
import sys
import time
from libqtopensesame.runners import BaseRunner
from qtpy import QtWidgets
from libopensesame.exceptions import UserKilled, ExperimentProcessDied
from libopensesame.oslogging import oslogger

JOIN_TIMEOUT = 3  # Seconds to wait for the process to end cleanly


class MultiprocessRunner(BaseRunner):

    """Runs an experiment in another process using multiprocessing."""
    supports_kill = True

    def execute(self):
        """See base_runner.execute()."""
        import platform
        import multiprocessing
        from libqtopensesame.misc import process, _

        self._workspace_globals = {}
        self.channel = multiprocessing.Queue()
        try:
            self.exp_process = process.ExperimentProcess(
                self.experiment,
                self.channel
            )
        except Exception as e:
            return e
        self.console.set_workspace_globals({u'process': self.exp_process})
        # Start process!
        self.exp_process.start()
        # Wait for experiment to finish.
        # Listen for incoming messages in the meantime.
        finished = False
        while self.exp_process.is_alive() or not self.channel.empty():
            # We need to process the GUI. To make the GUI feel more responsive
            # during pauses, we refresh the GUI more often when paused.
            QtWidgets.QApplication.processEvents()
            if self.paused:
                for i in range(25):
                    time.sleep(.01)
                    QtWidgets.QApplication.processEvents()
            # Wait for messages. Will throw Exception if no message is received
            # before timeout.
            try:
                msg = self.channel.get(True, 0.05)
            except Exception:
                continue
            if isinstance(msg, str):
                sys.stdout.write(safe_decode(msg, errors=u'ignore'))
                continue
            # Capture exceptions
            if isinstance(msg, Exception):
                self.exp_process.join(JOIN_TIMEOUT)
                try:
                    self.exp_process.close()
                except AttributeError:
                    # Process.close() was introduced only in Python 3.7
                    pass
                except ValueError:
                    # This happens when the join times out. Then we forcibly
                    # terminate the process.
                    self.exp_process.terminate()
                    oslogger.warning(
                        'experiment process was forcibly terminated')
                return msg
            # The workspace globals are sent as a dict. A special __pause__ key
            # indicates whether the experiment should be paused or resumed.
            if isinstance(msg, dict):
                self._workspace_globals = msg
                if u'__kill__' in msg:
                    self.exp_process.kill()
                if u'__heartbeat__' in msg:
                    self.main_window.extension_manager.fire(
                        u'set_workspace_globals',
                        global_dict=msg
                    )
                    self.main_window.extension_manager.fire(u'heartbeat')
                elif u'__pause__' in msg:
                    if msg[u'__pause__']:
                        self.pause()
                    else:
                        self.resume()
                elif u'__finished__' in msg:
                    finished = True
                continue
            # Anything that is not a string, not an Exception, and not None is
            # unexpected
            return ValueError(
                f'Illegal message type received from child process: {msg} '
                f'({type(msg)})')
        self.exp_process.join(JOIN_TIMEOUT)
        try:
            self.exp_process.close()
        except AttributeError:
            # Process.close() was introduced only in Python 3.7
            pass
        except ValueError:
            # This happens when the join times out. Then we forcibly
            # terminate the process.
            self.exp_process.terminate()
            oslogger.warning('experiment process was forcibly terminated')
        if finished:
            return
        if self.exp_process.killed:
            return UserKilled('The experiment process was killed.')
        return ExperimentProcessDied(
            'The experiment process seems to have died as the result of an '
            'unknown problem. This should not happen!')

    def kill(self):
        """See base_runner."""
        self.exp_process.kill()

    def workspace_globals(self):
        """See base_runner."""
        return self._workspace_globals

    @staticmethod
    def has_heartbeat():
        """See base_runner."""
        return True
