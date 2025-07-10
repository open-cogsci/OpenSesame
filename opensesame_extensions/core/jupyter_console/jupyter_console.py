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
from libqtopensesame.misc.config import cfg
from libqtopensesame.extensions import BaseExtension
from libopensesame.oslogging import oslogger
from qtpy.QtWidgets import QShortcut
from qtpy.QtCore import Qt
from qtpy.QtGui import QKeySequence
from libqtopensesame.misc.translate import translation_context
from pyqt_code_editor.components.jupyter_console import JupyterConsole as JupyterDock
import sys
_ = translation_context(u'JupyterConsole', category=u'extension')


class JupyterConsole(BaseExtension):

    @BaseExtension.as_thread(wait=500)
    def event_startup(self):
            
        self.set_busy(True)
        self._jupyter_console = JupyterDock(self.main_window)
        self.main_window.addDockWidget(
            Qt.BottomDockWidgetArea,
            self._jupyter_console
        )
        self._set_visible(cfg.jupyter_visible)
        self._shortcut_focus = QShortcut(
            QKeySequence(cfg.jupyter_focus_shortcut),
            self.main_window,
            self._focus,
            context=Qt.ApplicationShortcut
        )
        # Store original stdout and stderr
        self._original_stdout = None
        self._original_stderr = None
        self.set_busy(False)
        
    @property
    def jupyter_widget(self):
        return self._jupyter_console.get_current_console().jupyter_widget
    
    def activate(self):

        self._set_visible(not cfg.jupyter_visible)        

    def event_run_experiment(self, fullscreen):

        oslogger.debug('capturing stdout')
        # Store the original stdout and stderr
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        # Redirect stdout and stderr to this console
        sys.stdout = self
        sys.stderr = self

    def event_end_experiment(self, ret_val):

        oslogger.debug('releasing stdout')
        # Restore original stdout and stderr
        if self._original_stdout is not None:
            sys.stdout = self._original_stdout
            self._original_stdout = None
        if self._original_stderr is not None:
            sys.stderr = self._original_stderr
            self._original_stderr = None        
        self.jupyter_widget._show_interpreter_prompt()

    def event_jupyter_write(self, msg):
        self.write(msg)

    def write(self, text):
        """Write text to the Jupyter console widget"""
        self.jupyter_widget._append_plain_text(str(text))

    def flush(self):
        """Flush method required for file-like objects"""
        pass
            
    def _set_visible(self, visible):

        cfg.jupyter_visible = visible
        self.set_checked(visible)
        self._jupyter_console.setVisible(visible)
            
    def _focus(self):
        
        self._set_visible(True)
