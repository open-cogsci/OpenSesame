# coding=utf-8

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
import os
import sys
import time
from libopensesame.oslogging import oslogger
from libqtopensesame.misc.config import cfg
from libqtopensesame.widgets.base_widget import BaseWidget
from qtpy.QtWidgets import QHBoxLayout
from qtpy.QtGui import QFont
from qtconsole import styles
from .constants import (
    CHANGE_DIR_CMD,
    DEFAULT_CHANGE_DIR_CMD,
    RUN_FILE_CMD,
    DEFAULT_RUN_FILE_CMD,
    RUN_SYSTEM_CMD,
    DEFAULT_RUN_SYSTEM_CMD,
    TRANSPARENT_KERNELS,
    PID_CMD
)
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'JupyterConsole', category=u'extension')


class JupyterConsole(BaseWidget):

    def __init__(
        self,
        parent=None,
        name=None,
        kernel=None,
        inprocess=False
    ):

        super(JupyterConsole, self).__init__(parent)
        if kernel is None:
            kernel = cfg.jupyter_default_kernel
        self._console_tabwidget = parent
        self.name = name
        # Initialize Jupyter Widget
        if inprocess:
            from qtconsole.inprocess import (
                QtInProcessKernelManager as QtKernelManager
            )
            from .transparent_jupyter_widget import (
                InprocessJupyterWidget as JupyterWidget
            )
        else:
            from qtconsole.manager import QtKernelManager
            from .transparent_jupyter_widget import (
                OutprocessJupyterWidget as JupyterWidget
            )
        self._inprocess = inprocess
        self._kernel = kernel
        self._kernel_manager = QtKernelManager(kernel_name=kernel)
        self._kernel_manager.start_kernel()
        self._kernel_client = self._kernel_manager.client()
        self._kernel_client.start_channels()
        self._jupyter_widget = JupyterWidget(self)
        self._jupyter_widget.kernel_manager = self._kernel_manager
        self._jupyter_widget.kernel_client = self._kernel_client
        # Set theme
        self._jupyter_widget._control.setFont(
            QFont(
                cfg.pyqode_font_name,
                cfg.pyqode_font_size
            )
        )
        self._jupyter_widget.style_sheet = styles.sheet_from_template(
            cfg.pyqode_color_scheme,
            u'linux' if styles.dark_style(cfg.pyqode_color_scheme)
            else 'lightbg'
        )
        self._jupyter_widget.syntax_style = cfg.pyqode_color_scheme
        self._jupyter_widget._syntax_style_changed()
        self._jupyter_widget._style_sheet_changed()
        # Add to layout
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(6, 6, 6, 6)
        self._layout.addWidget(self._jupyter_widget)
        self.setLayout(self._layout)

    def capture_stdout(self):

        sys.stdout = self
        sys.stderr = self

    def release_stdout(self):

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def isatty(self):

        return False
    
    @property
    def language(self):
        
        return self._kernel_manager.kernel_spec.language
    
    @property
    def pid(self):
        
        if self.language:
            return os.getpid()
        if self._kernel not in PID_CMD:
            return -1
        for i in range(10):
            pid = self._jupyter_widget._silent_execute(PID_CMD[self._kernel])
            if isinstance(pid, int):
                return pid
            time.sleep(0.1)
        oslogger.warning('failed to get pid')
        return -1

    def flush(self):

        pass

    def execute(self, code):

        self._jupyter_widget.execute(code)

    def write(self, msg):

        self._jupyter_widget._control.insertPlainText(
            safe_decode(msg, errors=u'ignore')
        )
        self._jupyter_widget._control.ensureCursorVisible()

    def focus(self):

        self._jupyter_widget._control.setFocus()

    def set_busy(self, busy=True):

        if busy:
            icon = u'os-run'
        else:
            icon = 'utilities-terminal' if self._inprocess else 'os-debug'
        self._set_icon(icon)

    def _set_icon(self, icon):

        self._console_tabwidget.setTabIcon(
            self._console_tabwidget.indexOf(self),
            self.main_window.theme.qicon(icon)
        )

    def restart(self):

        oslogger.debug(u'restarting kernel')
        self._jupyter_widget.request_restart_kernel()
        self._jupyter_widget.reset(clear=True)
        self.extension_manager.fire(
            'workspace_restart',
            name=self.name,
            workspace_func=self.get_workspace_globals
        )
        self.extension_manager.fire(
            'register_subprocess',
            pid=self.pid,
            description='jupyter_console:{}'.format(self.name)
        )

    def interrupt(self):

        oslogger.debug(u'interrupting kernel')
        self._jupyter_widget.request_interrupt_kernel()

    def shutdown(self):

        oslogger.debug(u'shutting down kernel')
        self._jupyter_widget.kernel_client.stop_channels()
        self._jupyter_widget.kernel_manager.shutdown_kernel()

    def show_prompt(self):

        self._jupyter_widget._show_interpreter_prompt()

    def get_workspace_globals(self):

        if self.language in TRANSPARENT_KERNELS:
            return self._jupyter_widget.get_workspace_globals()
        return {'not supported': None}

    def list_workspace_globals(self):

        if self.language in TRANSPARENT_KERNELS:
            return self._jupyter_widget.list_workspace_globals()
        return []

    def get_workspace_variable(self, name):

        if self.language in TRANSPARENT_KERNELS:
            return self._jupyter_widget.get_workspace_variable(name)
        return None
    
    def running(self):
        
        return self._jupyter_widget.running()

    def set_workspace_globals(self, global_dict):

        self._jupyter_widget.set_workspace_globals(global_dict)

    def change_dir(self, path):

        self.execute(
            CHANGE_DIR_CMD.get(
                self._kernel,
                DEFAULT_CHANGE_DIR_CMD
            ).format(path=path.replace(u'\\', u'\\\\'))
        )

    def run_file(self, path):

        self.execute(
            RUN_FILE_CMD.get(
                self._kernel,
                DEFAULT_RUN_FILE_CMD
            ).format(path=path.replace(u'\\', u'\\\\'))
        )
        
    def run_system_command(self, cmd):
        
        tmpl = RUN_SYSTEM_CMD.get(self._kernel, DEFAULT_RUN_SYSTEM_CMD)
        cmd = cmd.replace(u'\\', u'\\\\')
        # If the command has double quotes itself, such as for the R system()
        # command, then we need to escape any quotes in the cmd string.
        if u'"' in tmpl:
            cmd = cmd.replace(u'"', u'\\"')
        self.execute(tmpl.format(cmd=cmd))
        
    def run_debug(self, path, breakpoints):

        # This should be changed into a kernel-agnostic implementation
        if (
            self.language not in ('python', 'python2', 'python3') or
            self._inprocess
        ):
            self.extension_manager.fire(
                'notify',
                message=_(u'The {} (inprocess={}) kernel does not support debugging').format(
                    self._kernel,
                    self._inprocess
                )
            )
            return
        code = self.extension_manager.provide(
            'python_debugger_code',
            path=path,
            breakpoints=breakpoints
        )
        if not code:
            oslogger.warning('no Python debugger code received')
            return
        silent_code, nonsilent_code = code
        # RapunzelPDB and debugfile() are silently loaded into the workspace,
        # and then the debugger is callend in a nonsilent way.`
        self._jupyter_widget._kernel_client.execute(silent_code, silent=True)
        self.execute(nonsilent_code)

    def check_syntax(self, code):

        if 'python' not in self._kernel:
            return True
        try:
            compile(code, 'dummy', 'exec')
        except SyntaxError:
            return False
        return True
