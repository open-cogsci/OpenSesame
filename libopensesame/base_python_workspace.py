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
import warnings


class BasePythonWorkspace:

    r"""Provides a basic Python workspace for use in the GUI. This avoids
    unnecessarily importing the entire runtime API.
    """
    def __init__(self, experiment):
        r"""Constructor.

        Parameters
        ----------
        experiment : experiment
            The experiment object.
        """
        self.experiment = experiment
        self._globals = {}

    def check_syntax(self, script):
        r"""Checks whether a Python script is syntactically correct.

        Parameters
        ----------
        script : unicode
            A Python script.

        Returns
        -------
        int
            0 if script is correct, 1 if there is a syntax warning, and 2 if
            there is a syntax error.
        """
        with warnings.catch_warnings(record=True) as warning_list:
            try:
                self._compile(safe_decode(script))
            except:
                return 2
        if warning_list:
            return 1
        return 0

    def run_file(self, path):
        r"""Reads and executes a files.

        Parameters
        ----------
        path : str
            The full path to a Python file.
        """
        with safe_open(path) as fd:
            script = fd.read()
        bytecode = self._compile(script)
        self._exec(bytecode)

    def _compile(self, script):
        r"""Compiles a script into bytecode.

        Parameters
        ----------
        script : unicode
            A Python script.

        Returns
        -------
        code
            The compiled script.
        """
        return compile(script, u'<string>', u'exec')

    def _exec(self, bytecode):
        r"""Executes bytecode.

        Parameters
        ----------
        bytecode : code
            A chunk of bytecode.
        """
        exec(bytecode, self._globals)

    def _eval(self, bytecode):
        r"""Evaluates bytecode.

        Parameters
        ----------
        bytecode : code
            A chunk of bytecode.

        Returns
        -------
        The evaluated value of the bytecode
        """
        return eval(bytecode, self._globals)

    # The properties below emulate a dict interface.

    @property
    def __setitem__(self):
        return self._globals.__setitem__

    @property
    def __delitem__(self):
        return self._globals.__delitem__

    @property
    def __getitem__(self):
        return self._globals.__getitem__

    @property
    def __len__(self):
        return self._globals.__len__

    @property
    def __iter__(self):
        return self._globals.__iter__

    @property
    def items(self):
        return self._globals.items

    @property
    def keys(self):
        return self._globals.keys

    @property
    def values(self):
        return self._globals.values

    @property
    def copy(self):
        return self._globals.copy


# Alias for backwards compatibility
base_python_workspace = BasePythonWorkspace
