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
from libopensesame.item import Item
import re
from libopensesame.exceptions import InvalidOpenSesameScript


class Logger(Item):
    """The logger item logs experimental data (i.e. variables)."""
    
    description = 'Logs experimental data'
    is_oneshot_coroutine = True

    def reset(self):
        self.logvars = []
        self._logvars = None
        self.var.auto_log = 'yes'
        self.exclude_vars = []

    def run(self):
        self.set_item_onset()
        if self._logvars is None:
            if self.var.auto_log == 'yes':
                self._logvars = self.experiment.log.all_vars()
            else:
                self._logvars = []
            for var in self.logvars:
                if var not in self._logvars:
                    self._logvars.append(var)
            excludes = []
            for ref_var in self.exclude_vars:
                for test_var in self._logvars:
                    if re.fullmatch(ref_var, test_var):
                        excludes.append(test_var)
            for exclude in excludes:
                self._logvars.remove(exclude)
            self._logvars.sort()
        self.experiment.log.write_vars(self._logvars)

    def coroutine(self, coroutines):
        yield
        self.run()

    def from_string(self, string):
        self.var.clear()
        self.comments = []
        self.reset()
        if string is None:
            return
        for line in string.split('\n'):
            self.parse_variable(line)
            cmd, arglist, kwdict = self.experiment.syntax.parse_cmd(line)
            if cmd in ('log', 'exclude') and len(arglist) > 0:
                if cmd == 'log':
                    for var in arglist:
                        if not self.experiment.syntax.valid_var_name(
                                safe_decode(var)):
                            raise InvalidOpenSesameScript(
                                '{var} is not a valid variable name')
                    self.logvars += arglist
                else:
                    self.exclude_vars += arglist

    def to_string(self):
        s = super().to_string('logger')
        for var in self.logvars:
            s += '\t' + self.experiment.syntax.create_cmd(
                'log', [var]) + '\n'
        for var in self.exclude_vars:
            s += '\t' + self.experiment.syntax.create_cmd(
                'exclude', [var]) + '\n'
        return s


# Alias for backwards compatibility
logger = Logger
