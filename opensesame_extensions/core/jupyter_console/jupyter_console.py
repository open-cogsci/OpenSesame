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
from libqtopensesame.misc.config import cfg
from libqtopensesame.extensions import BaseExtension
from libopensesame.oslogging import oslogger
from qtpy.QtWidgets import QDockWidget, QShortcut
from qtpy.QtCore import Qt
from qtpy.QtGui import QKeySequence
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'JupyterConsole', category=u'extension')


class JupyterConsole(BaseExtension):
    
    preferences_ui = 'extensions.jupyter_console.preferences'

    @BaseExtension.as_thread(wait=500)
    def event_startup(self):

        from .jupyter_tabwidget import ConsoleTabWidget

        self.set_busy(True)
        self._jupyter_console = ConsoleTabWidget(self.main_window)
        self._dock_widget = QDockWidget(u'Console', self.main_window)
        self._dock_widget.setObjectName(u'JupyterConsole')
        self._dock_widget.setWidget(self._jupyter_console)
        self._dock_widget.closeEvent = self._on_close_event
        self.main_window.addDockWidget(
            Qt.BottomDockWidgetArea,
            self._dock_widget
        )
        self._set_visible(cfg.jupyter_visible)
        self._shortcut_focus = QShortcut(
            QKeySequence(cfg.jupyter_focus_shortcut),
            self.main_window,
            self._focus,
            context=Qt.ApplicationShortcut
        )
        self.set_busy(False)
        
    def fire(self, event, **kwdict):
        
        if event != 'startup':
            oslogger.debug('ignoring events until after startup')
            return
        JupyterConsole.fire = BaseExtension.fire
        self.fire(event, **kwdict)

    def activate(self):

        if not hasattr(self, '_jupyter_console'):
            oslogger.debug('ignoring activate until after startup')
            return
        self._set_visible(not cfg.jupyter_visible)

    def event_run_experiment(self, fullscreen):

        oslogger.debug(u'capturing stdout')
        self._jupyter_console.current.capture_stdout()

    def event_end_experiment(self, ret_val):

        self._jupyter_console.current.release_stdout()
        self._jupyter_console.current.show_prompt()
        oslogger.debug(u'releasing stdout')

    def event_jupyter_start_kernel(self, kernel):

        self._jupyter_console.add(kernel=kernel)

    def event_jupyter_run_file(self, path, debug=False):

        self._set_visible(True)
        if not os.path.isfile(path):
            return
        self._jupyter_console.current.change_dir(os.path.dirname(path))
        if debug:
            self._jupyter_console.current.run_debug(
                path,
                breakpoints=self.extension_manager.provide(
                    'pyqode_breakpoints'
                )
            )
        else:
            self._jupyter_console.current.run_file(path)

    def event_jupyter_change_dir(self, path):

        self._jupyter_console.current.change_dir(path)

    def event_jupyter_run_code(self, code, editor=None):

        self._set_visible(True)
        self._jupyter_console.current.execute(code)
    
    def event_jupyter_run_silent(self, code):

        self._jupyter_console.current.execute(code)
        
    def event_jupyter_run_system_command(self, cmd):

        self._jupyter_console.current.run_system_command(cmd)

    def event_jupyter_write(self, msg):

        try:
            self._jupyter_console.current.write(msg)
        except AttributeError:
            oslogger.error(safe_decode(msg))

    def event_jupyter_focus(self):

        self._jupyter_console.current.focus()

    def event_jupyter_show_prompt(self):

        self._jupyter_console.current.show_prompt()

    def event_jupyter_restart(self):

        self._jupyter_console.current.restart()

    def event_jupyter_interrupt(self):

        self._jupyter_console.current.interrupt()

    def event_set_workspace_globals(self, global_dict):

        self._jupyter_console.current.set_workspace_globals(global_dict)

    def provide_jupyter_workspace_name(self):

        try:
            return self._jupyter_console.current.name
        except AttributeError:
            return None
        
    def provide_workspace_kernel(self):
        
        try:
            return self._jupyter_console.current._kernel
        except AttributeError:
            return None
        
    def provide_workspace_language(self):

        try:
            return self._jupyter_console.current.language
        except AttributeError:
            return None
        
    def provide_workspace_logging_commands(self):

        from .jupyter_tabwidget.constants import LOGGING_LEVEL_CMD
        try:
            kernel = self._jupyter_console.current.language
        except AttributeError:
            return None
        return LOGGING_LEVEL_CMD.get(kernel, None)

    def provide_jupyter_workspace_globals(self):

        return self.get_workspace_globals()

    def provide_jupyter_list_workspace_globals(self):

        return self.list_workspace_globals()

    def provide_jupyter_workspace_variable(self, name):

        return self._jupyter_console.current.get_workspace_variable(name)
        
    def provide_jupyter_kernel_running(self):
        
        try:
            return self._jupyter_console.current.running()
        except AttributeError:
            return False

    def provide_jupyter_check_syntax(self, code):

        return self._jupyter_console.current.check_syntax(code)

    def get_workspace_globals(self):

        try:
            return self._jupyter_console.current.get_workspace_globals()
        except AttributeError:
            return {u'no reply': None}

    def list_workspace_globals(self):

        try:
            return self._jupyter_console.current.list_workspace_globals()
        except Exception as e:
            print(e)
            return []

    def event_close(self):

        if not hasattr(self, '_jupyter_console'):
            oslogger.debug('ignoring close all')
            return
        self._jupyter_console.close_all()

    def _set_visible(self, visible):

        cfg.jupyter_visible = visible
        self.set_checked(visible)
        if visible:
            self._dock_widget.show()
            self._jupyter_console.current.focus()
        else:
            self._dock_widget.hide()

    def _focus(self):

        self._set_visible(True)
        self._jupyter_console.current.focus()

    def _on_close_event(self, e):

        self._set_visible(False)
