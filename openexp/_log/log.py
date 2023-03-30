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
from libopensesame.oslogging import oslogger
import warnings


class Log:

    r"""The `log` object provides data logging. A `log` object is created
    automatically when the experiment starts.

    __Example__:

    ~~~ .python
    #
    Write one line of text
    log.write(u'My custom log message')
    # Write all
    variables
    log.write_vars()
    ~~~

    [TOC]
    """
    def __init__(self, experiment, path):
        r"""Constructor to create a new `log` object. You do not generally call
        this constructor directly, because a `log` object is created
        automatically when the experiment is launched.

        Parameters
        ----------
        experiment : experiment
            The experiment object.
        """
        self.experiment = experiment
        self.experiment.var.logfile = path
        self._all_vars = None
        self.open(path)

    def __call__(self, msg):

        self.write(msg)

    def close(self):
        r"""Closes the current log.

        Examples
        --------
        >>> log.close()
        """
        pass

    def all_vars(self):
        """
        visible: False

        returns:
                A list of all variables that exist in the experiment.
        """
        if self._all_vars is None:
            self._all_vars = []
            for key in self.experiment.var.inspect().keys():
                try:
                    key = self.experiment.syntax.eval_text(key)
                except Exception:
                    oslogger.warning(f'cannot evaluate variable name {key}')
                else:
                    self._all_vars.append(key)
        return self._all_vars

    def open(self, path):
        r"""Opens the current log. If a log was already open, it is closed
        automatically, and re-opened.

        Parameters
        ----------
        path : str, unicode
            The path to the current logfile. In most cases (unless) a custom
            log back-end is used, this will be a filename.

        Examples
        --------
        >>> # Open a new log
        >>> log.open(u'/path/to/new/logfile.csv')
        """
        pass

    def write(self, msg, newline=True):
        r"""Write one message to the log.

        Parameters
        ----------
        msg : str, unicode
            A text message. When using Python 2, this should be either
            `unicode` or a utf-8-encoded `str`. When using Python 3, this
            should be either `str` or a utf-8-encoded `bytes`.
        newline : bool, optional
            Indicates whether a newline should be written after the message.

        Examples
        --------
        >>> # Write a single string of text
        >>> log.write(u'time = %s' % clock.time())
        """
        pass

    def write_vars(self, var_list=None):
        r"""Writes variables to the log.

        Parameters
        ----------
        var_list : list, NoneType, optional
            A list of variable names to write, or None to write all variables
            that exist in the experiment.

        Examples
        --------
        >>> # Write all variables to the logfile
        >>> log.write_vars()
        """
        pass


# Non PEP-8 alias for backwards compatibility
log = Log
