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
import uuid
import os
import ast
import time
import json
import inspect
import pickle
from libqtopensesame.misc.base_subcomponent import BaseSubcomponent
from qtpy.QtWidgets import QApplication
from qtpy.QtCore import QTimer
from libopensesame.oslogging import oslogger
from qtconsole.rich_jupyter_widget import RichJupyterWidget
try:
    from base64 import decodebytes
except ImportError:  # Python 2
    from base64 import decodestring as decodebytes
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'JupyterConsole', category=u'extension')


GLOBAL_EXPR = u'''{
key: (
    repr(val),
    val.__class__.__name__,
    (
        val.shape if hasattr(val, 'shape')
        else len(val) if hasattr(val, '__len__')
        else len(val.layers) if hasattr(val, 'layers') and hasattr(val.layers, '__len__')
        else None
    )
)
for key, val in globals().items()
if (
    hasattr(val, 'layers') and hasattr(val.layers, '__len__')
) or (
    not key.startswith(u'_') and
    key not in ('In', 'Out') and
    not callable(val) and
    not inspect.isclass(val) and
    not inspect.ismodule(val)
)
}'''

LIST_GLOBAL_EXPR = u'''[
key
for key, val in globals().items()
if (
    hasattr(val, 'layers') and hasattr(val.layers, '__len__')
) or (
    not key.startswith(u'_') and
    key not in ('In', 'Out') and
    not callable(val) and
    not inspect.isclass(val) and
    not inspect.ismodule(val)
)
]
'''


class FailedToGetWorkspaceVariable(Exception):
    
    def __repr__(self):
        
        return _('Failed to get workspace variable')


class TransparentJupyterWidget(RichJupyterWidget, BaseSubcomponent):

    def __init__(self, jupyter_console):

        self._name = jupyter_console.name
        self._jupyter_console = jupyter_console
        super(TransparentJupyterWidget, self).__init__(jupyter_console)
        self.setup(jupyter_console)
        self.executed.connect(self._on_executed)
        self.executing.connect(self._on_executing)
        self._last_executed = None
        # It is possible for _on_executing() to be called again, before
        # _on_executed() is called. We therefore keep track of how many times
        # _on_executing() has been called, and only release the busy status
        # when this counter is set back to 0.
        self._executing_counter = 0
        
    def execute(self, *args, **kwargs):
        
        self._last_executed = args[0] if args else kwargs.get('source', None)
        super(TransparentJupyterWidget, self).execute(*args, **kwargs)

    def _on_executing(self):

        self._executing_counter += 1
        self._jupyter_console.set_busy(True)
        self.extension_manager.fire('jupyter_execute_start')

    def _on_executed(self):
        """Is called when the kernel is done executing code. Oddly, this can
        happen just before the last bit of output is captured. Therefore, we
        don't react right away, but call the finish() function 100 ms later.
        """
        def finish():
            if self._executing_counter:
                self._executing_counter -= 1
            if self._executing_counter:
                return
            self._jupyter_console.set_busy(False)
            self.extension_manager.fire(
                u'workspace_update',
                name=self._name,
                workspace_func=self.get_workspace_globals
            )
            self.extension_manager.fire('jupyter_execute_finished')
        QTimer.singleShot(100, finish)
        
    def running(self):
        
        return self._executing_counter > 0
    
    def reset(self, clear=False):
        
        super(TransparentJupyterWidget, self).reset(clear=clear)
        self._executing_counter = 0
        self._jupyter_console.set_busy(False)
        
    def _handle_display_data(self, msg):
        """Reimplemented to handle communications between the figure explorer
        and the kernel. Inspired by Spyder's `figurebrowser.py`.
        """
        img = None
        data = msg['content']['data']
        if 'image/svg+xml' in data:
            fmt = 'image/svg+xml'
            img = data['image/svg+xml']
        elif 'image/png' in data:
            # PNG data is base64 encoded as it passes over the network
            # in a JSON structure so we decode it.
            fmt = 'image/png'
            img = decodebytes(data['image/png'].encode('ascii'))
        elif 'image/jpeg' in data and self._jpg_supported:
            fmt = 'image/jpeg'
            img = decodebytes(data['image/jpeg'].encode('ascii'))
        if img is not None:
            self.extension_manager.fire(
                'jupyter_execute_result_image',
                img=img,
                fmt=fmt,
                code=self._last_executed
            )
        return super(TransparentJupyterWidget, self)._handle_display_data(msg)
        
    def _append_plain_text(self, text, *args, **kwargs):
        
        super(TransparentJupyterWidget, self)._append_plain_text(
            text,
            *args,
            **kwargs
        )
        if not self._executing_counter:
            return
        self.extension_manager.fire('jupyter_execute_result_text', text=text)
        if 'Traceback (most recent call last)' in text:
            self.extension_manager.fire('jupyter_exception_occurred')


class OutprocessJupyterWidget(TransparentJupyterWidget):

    """Makes the Python workspace of a Jupyter console with a kernel running in
    a different process accessible.
    """

    def __init__(self, jupyter_console):

        self._user_expressions = {}
        super(OutprocessJupyterWidget, self).__init__(jupyter_console)

    def _handle_execute_reply(self, msg):

        self._user_expressions = msg.get(
            u'content',
            {}
        ).get(u'user_expressions', {})
        return super(OutprocessJupyterWidget, self)._handle_execute_reply(msg)
        
    def _silent_execute(self, expr):
        
        key = str(uuid.uuid4())
        self._kernel_client.execute(
            u'import os, inspect',
            silent=True,
            user_expressions={
                key: expr
            }
        )
        for _ in range(100):
            if key in self._user_expressions:
                break
            time.sleep(0.01)
            QApplication.processEvents()
        else:
            return {u'no reply': None}
        reply = self._user_expressions[key].get(u'data', {}).get(
            u'text/plain',
            u'{"invalid reply": None}'
        )
        try:
            return ast.literal_eval(reply)
        except (ValueError, SyntaxError):
            return {u'cannot eval reply': None}

    def get_workspace_globals(self):

        return self._silent_execute(GLOBAL_EXPR)

    def list_workspace_globals(self):

        return self._silent_execute(LIST_GLOBAL_EXPR)

    def set_workspace_globals(self, global_dict):

        code = ['from pickle import loads']
        for var, val in global_dict.items():
            if (
                var.startswith('_') or
                callable(val) or
                inspect.isclass(val) or
                inspect.ismodule(val)
            ):
                continue
            try:
                blob = pickle.dumps(val)
            except (pickle.PicklingError, TypeError):
                pass
            else:
                code.append('{} = loads({})'.format(var, repr(blob)))
        self._kernel_client.execute(';'.join(code), silent=True)

    def get_workspace_variable(self, name):

        key = str(uuid.uuid4())
        self._kernel_client.execute(
            u'import pickle',
            silent=True,
            user_expressions={
                key: u'pickle.dumps({})'.format(name)
            }
        )
        for _ in range(200):
            if key in self._user_expressions:
                break
            time.sleep(0.05)
            QApplication.processEvents()
        else:
            return FailedToGetWorkspaceVariable()
        reply = self._user_expressions[key].get(
            u'data',
            {}
        ).get(u'text/plain', None)
        if reply is None:
            return FailedToGetWorkspaceVariable()
        try:
            return pickle.loads(eval(reply))
        except (
            TypeError,
            pickle.UnpicklingError,
            RecursionError,
            ModuleNotFoundError
        ):
            return FailedToGetWorkspaceVariable()


class InprocessJupyterWidget(TransparentJupyterWidget):

    """Makes the Python workspace of a Jupyter console with a kernel running in
    the same process accessible.
    """

    def __init__(self, parent):

        self._jupyter_console = parent
        super(InprocessJupyterWidget, self).__init__(parent)

    def get_workspace_globals(self):

        return {
            key: (
                json.dumps(val, default=lambda x: u'<no preview>'),
                val.__class__.__name__,
                len(val) if hasattr(val, '__len__')
                else len(val.layers) if hasattr(val, 'layers') and hasattr(val.layers, '__len__')
                else '<na>'
            )
            for key, val
            in self._kernel_manager.kernel.shell.user_global_ns.copy().items()
            if (
                hasattr(val, 'layers') and hasattr(val.layers, '__len__')
            ) or (
                not key.startswith(u'_') and
                key not in ('In', 'Out') and
                not callable(val) and
                not inspect.isclass(val) and
                not inspect.ismodule(val)
            )
        }
        
    def list_workspace_globals(self):
        
        return [
            key
            for key, val
            in self._kernel_manager.kernel.shell.user_global_ns.copy().items()
            if (
                hasattr(val, 'layers') and hasattr(val.layers, '__len__')
            ) or (
                not key.startswith(u'_') and
                key not in ('In', 'Out') and
                not callable(val) and
                not inspect.isclass(val) and
                not inspect.ismodule(val)
            )
        ]

    def set_workspace_globals(self, global_dict):

        self._kernel_manager.kernel.shell.push(global_dict)

    def get_workspace_variable(self, name):

        return self._kernel_manager.kernel.shell.user_global_ns.get(name, None)
