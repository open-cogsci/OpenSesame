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
from libopensesame.exceptions import InvalidOpenSesameScript


class Logger(Item):

    r"""The logger item logs experimental data (i.e. variables)."""
    description = u'Logs experimental data'
    is_oneshot_coroutine = True

    def reset(self):
        """See item."""
        self.logvars = []
        self._logvars = None
        self.var.auto_log = u'yes'

    def run(self):
        """See item."""
        self.set_item_onset()
        if self._logvars is None:
            if self.var.auto_log == u'yes':
                self._logvars = self.experiment.log.all_vars()
            else:
                self._logvars = []
            for var in self.logvars:
                if var not in self._logvars:
                    self._logvars.append(var)
            self._logvars.sort()
        self.experiment.log.write_vars(self._logvars)

    def coroutine(self, coroutines):
        """See coroutines plug-in."""
        yield
        self.run()

    def from_string(self, string):
        """See item."""
        self.var.clear()
        self.comments = []
        self.reset()
        if string is None:
            return
        for line in string.split(u'\n'):
            self.parse_variable(line)
            cmd, arglist, kwdict = self.experiment.syntax.parse_cmd(line)
            if cmd == u'log' and len(arglist) > 0:
                for var in arglist:
                    if not self.experiment.syntax.valid_var_name(
                            safe_decode(var)):
                        raise InvalidOpenSesameScript(
                            '{var} is not a valid variable name')
                self.logvars += arglist

    def to_string(self):
        """See item."""
        s = super().to_string('logger')
        for logvar in self.logvars:
            s += u'\t' + self.experiment.syntax.create_cmd(
                u'log', [logvar]) + u'\n'
        return s


# Alias for backwards compatibility
logger = Logger
