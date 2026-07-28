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
from libopensesame.oslogging import oslogger
from libopensesame.exceptions import PythonError, PythonSyntaxError, \
    AbortCoroutines


class InlineScript(Item):
    """Allows users to use Python code in their experiments."""

    description = 'Executes Python code'

    def reset(self):
        """See item."""
        self.var._prepare = ''
        self.var._run = ''
        self._var_info = None

    @property
    def workspace(self):

        return self.experiment.python_workspace        

    def from_string(self, string):
        super().from_string(string)
        self.var.set('_prepare', self._ensure_space_indent(
            self.var.get('_prepare', _eval=False)))
        self.var.set('_run', self._ensure_space_indent(
            self.var.get('_run', _eval=False)))

    def prepare(self):
        """Executes the prepare script. The code that you enter in the
        'prepare' tab of an inline_script item in the GUI is used as a body for
        this function.
        """
        super().prepare()
        # 'self' must always be registered, otherwise we get confusions between
        # the various inline_script items.
        self.workspace['self'] = self
        prepare_script = self.var.get('_prepare', _eval=False)
        run_script = self.var.get('_run', _eval=False)
        # Compile prepare script
        try:
            self.cprepare = self.workspace._compile(prepare_script)
        except SyntaxError as e:
            raise PythonSyntaxError(
                'Syntax error in inline script (prepare phase)',
                line_nr=e.lineno)
        # Compile run script
        try:
            self.crun = self.workspace._compile(run_script)
        except SyntaxError as e:
            raise PythonSyntaxError(
                'Syntax error in inline script (run phase)',
                line_nr=e.lineno)
        # Run prepare script
        try:
            self.workspace._exec(self.cprepare)
        except Exception as e:
            raise PythonError(
                'Error while executing inline script (prepare phase)')

    def run(self):
        """Executes the run script. The code that you enter in the 'run' tab
        of an inline_script item in the GUI is used as a body for this
        function.
        """
        self.set_item_onset()
        # 'self' must always be registered, otherwise we get confusions between
        # the various inline_script items.
        self.workspace['self'] = self
        try:
            self.workspace._exec(self.crun)
        except Exception as e:
            raise PythonError(
                'Error while executing inline script (run phase)')

    def coroutine(self, coroutines):
        """See coroutines plug-in"""
        yield
        self.set_item_onset()
        while True:
            self.workspace['self'] = self
            try:
                self.workspace._exec(self.crun)
            except AbortCoroutines as e:
                # If the inline_script is part of a coroutines, this signals
                # that the coroutines should be aborted, so we don't wrap it
                # into a PythonError.
                raise
            except Exception as e:
                raise PythonError(
                    'Error while executing inline script (coroutines)')
            yield

    @staticmethod
    def _ensure_space_indent(script):
        """Takes a Python script that may have mixed space and tab indentation,
        and fixes it to pure space indentation. The number of spaces per indent
        should be autodetected and default to 4 if autodetection failed. If any
        indentations were converted, use oslogger.warning().
        """
        lines = script.splitlines()

        # --- Autodetect indent width from space-only indented lines ---
        indent_widths = []
        for line in lines:
            leading = line[:len(line) - len(line.lstrip(' \t'))]
            if leading and '\t' not in leading:
                indent_widths.append(len(leading))

        if indent_widths:
            # The indent width is the GCD of all observed space indentation
            # widths, so that every indentation level is a clean multiple.
            indent_width = indent_widths[0]
            for w in indent_widths[1:]:
                while w:
                    indent_width, w = w, indent_width % w
            # A GCD below 2 is unrealistic and likely indicates messy code;
            # fall back to the default.
            if indent_width < 2:
                indent_width = 4
        else:
            indent_width = 4

        # --- Convert tabs to spaces in leading whitespace only ---
        converted = False
        new_lines = []
        for line in lines:
            stripped = line.lstrip(' \t')
            leading = line[:len(line) - len(stripped)]
            if '\t' in leading:
                converted = True
                new_lines.append(leading.expandtabs(indent_width) + stripped)
            else:
                new_lines.append(line)

        if converted:
            oslogger.warning(
                'Converted tab indentation to {}-space indentation '
                'in inline script'.format(indent_width)
            )

        return '\n'.join(new_lines)


# Alias for backwards compatibility
inline_script = InlineScript
