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
from libopensesame.exceptions import FStringError, FStringSyntaxError
from libopensesame.item_stack import item_stack_singleton
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
        
    @property
    def _globals(self):
        return self.experiment.var.__vars__

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
        return compile(script, '<string>', 'exec')  # __ignore_traceback__

    def _exec(self, bytecode):
        r"""Executes bytecode.

        Parameters
        ----------
        bytecode : code
            A chunk of bytecode.
        """
        exec(bytecode, self._globals)  # __ignore_traceback__

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
        return eval(bytecode, self._globals)  # __ignore_traceback__
        
    def eval_fstring(self, fs, include_local=False):
        """Evaluates an f-string.

        Parameters
        ----------
        fs : str
            An f-string
        include_local : bool, optional
            If True, the variable store of the current item is merged into the
            Python workspace. This allows items to evaluate f-strings that
            take into account the item's local variables.

        Returns
        -------
        A string corresponding to the evaluated f-string.
        """
        if include_local:
            item_name, phase = item_stack_singleton[-1]
            _globals = self._globals.copy()
            _globals.update(self.experiment.items[item_name].var.__vars__)
        else:
            _globals = self._globals
        fs_escaped = fs.replace(r"'''", r"\'\'\'")
        try:
            return eval(f"f'''{fs_escaped}'''", _globals)  # __ignore_traceback__
        except SyntaxError:
            raise FStringSyntaxError(
                f'The following text contains invalid f-string expression:\n\n~~~ .text\n{fs}\n~~~\n\n')
        except Exception:
            raise FStringError(
                f'Failed to evaluate f-string expression in the following text:\n\n~~~ .text\n{fs}\n~~~\n\n')

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
