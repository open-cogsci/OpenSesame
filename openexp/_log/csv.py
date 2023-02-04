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
from openexp._log.log import Log
import os


class Csv(Log):

    """
    desc:
            For docstrings, see openexp._log.log.
    """

    def __init__(self, experiment, path):

        self._log = None
        Log.__init__(self, experiment, path)

    def close(self):

        if self._log is not None:
            self._log.close()

    def open(self, path):

        if self._log is not None:
            self.close()
        # If only a filename is present, we interpret this filename as relative
        # to the experiment folder, instead of relative to the current working
        # directory.
        if (
                os.path.basename(path) == path and
                self.experiment.experiment_path is not None
        ):
            self._path = os.path.join(self.experiment.experiment_path, path)
        else:
            self._path = path
        # Open the logfile
        self.experiment.var.logfile = self._path
        if self._path not in self.experiment.data_files:
            self.experiment.data_files.append(self._path)
        self._log = safe_open(self._path, u'w')
        self._header_written = False

    def write(self, msg, newline=True):

        self._log.write(safe_decode(msg))
        if newline:
            self._log.write(u'\n')
        # Flush to avoid pending write operations
        self._log.flush()
        os.fsync(self._log)

    def write_vars(self, var_list=None):

        if var_list is None:
            var_list = self.all_vars()
        if not self._header_written:
            l = [u'"%s"' % var.replace(u'"', u'\\"') for var in var_list]
            self.write(u','.join(l))
            self._header_written = True
        l = []
        for var in var_list:
            val = self.experiment.var.get(var, _eval=False, default=u'NA')
            val = safe_decode(val)
            l.append(u'"%s"' % val.replace(u'"', u'\\"'))
        self.write(u','.join(l))


# Non PEP-8 alias for backwards compatibility
csv = Csv
