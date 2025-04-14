"""This file is part of OpenSesame.

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
        self._log = safe_open(self._path, 'w')
        self._header_written = False

    def write(self, msg, newline=True):

        self._log.write(safe_decode(msg))
        if newline:
            self._log.write('\n')
        # Flush to avoid pending write operations
        self._log.flush()
        os.fsync(self._log)
        
    def _csv_escape_and_quote(self, val):
        """
        Takes a single value, which can be of any type, and returns it so that 
        it matches the CSV specification for a field. For consistency, we put 
        double quotes around all values, and escape any instances of a double quote 
        by doubling them.
        """
        s = safe_decode(val)
        s = s.replace('"', '""')
        return '"' + s + '"'

    def write_vars(self, var_list=None):

        if var_list is None:
            var_list = self.all_vars()
        if not self._header_written:
            self.write(
                ','.join(self._csv_escape_and_quote(var) for var in var_list))
            self._header_written = True
        values = []
        for var in var_list:
            val = self.experiment.var.get(var, _eval=False, default='NA')
            values.append(self._csv_escape_and_quote(val))
        self.write(','.join(values))


# Non PEP-8 alias for backwards compatibility
csv = Csv
