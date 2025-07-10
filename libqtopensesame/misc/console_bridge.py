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
from libqtopensesame.misc.base_subcomponent import BaseSubcomponent


class ConsoleBridge(BaseSubcomponent):
    """A base console for debug-window consoles."""
    
    def __init__(self, main_window):

        super(ConsoleBridge, self).__init__()
        self.setup(main_window)
        self._jupyter_console = None
        self._writing = False

    def write(self, s):

        oslogger.debug(s)
        if self._writing:
            oslogger.warning('recursive write() call')
            print(safe_decode(s, errors='ignore'))
            return
        self._writing = True
        if hasattr(self, 'extension_manager'):
            self.extension_manager.fire('jupyter_write', msg=s)
        else:
            oslogger.info(s)
        self._writing = False

    def set_workspace_globals(self, _globals={}):

        print('***** GLOBALS')
        print(_globals)
        self.extension_manager.fire(
            'set_workspace_globals',
            global_dict=_globals
        )

    def show_prompt(self):

        self.extension_manager.fire('jupyter_show_prompt')
