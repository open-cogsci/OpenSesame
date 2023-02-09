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
from libqtopensesame.misc.base_subcomponent import BaseSubcomponent
from qtpy.QtWidgets import QTabWidget
from libqtopensesame.misc.config import cfg
from .jupyter_console import JupyterConsole
from .console_cornerwidget import ConsoleCornerWidget
from .constants import KERNEL_NAMES


class ConsoleTabWidget(QTabWidget, BaseSubcomponent):

    def __init__(self, parent, kwargs={}):

        super(ConsoleTabWidget, self).__init__(parent)
        self.setup(parent)
        self._console_count = 1
        self._kwargs = kwargs
        self.setCornerWidget(ConsoleCornerWidget(self, kwargs))
        if cfg.jupyter_inprocess:
            # Also start a single inprocess console, mostly for debugging
            # purposes
            self.add(inprocess=True)
        self.tabCloseRequested.connect(self.close)
        self.currentChanged.connect(self._on_switch)
        self.add()

    def add(self, inprocess=False, **kwargs):

        merged_kwargs = self._kwargs.copy()
        merged_kwargs.update(kwargs)
        kernel = merged_kwargs.get('kernel', cfg.jupyter_default_kernel)
        name = u'{} ({})'.format(
            KERNEL_NAMES.get(kernel, kernel),
            self._console_count
        )
        jupyter_console = JupyterConsole(
            self,
            name=name,
            inprocess=inprocess,
            **merged_kwargs
        )
        self.addTab(
            jupyter_console,
            self.main_window.theme.qicon(
                'utilities-terminal'
                if inprocess
                else 'os-debug'
            ),
            name
        )
        if inprocess:
            global_dict = {
                ext.name(): ext
                for ext in self.extension_manager.extensions
            }
            global_dict['opensesame'] = self.main_window
            global_dict['event_durations'] = self._event_durations
            jupyter_console.set_workspace_globals(global_dict)
        else:
            self.extension_manager.fire(
                'register_subprocess',
                pid=jupyter_console.pid,
                description='jupyter_console:{}'.format(name)
            )
        self.setTabsClosable(self.count() > 1)
        self.setCurrentIndex(self.count() - 1)
        self._console_count += 1
        self.extension_manager.fire(
            'workspace_new',
            name=name,
            workspace_func=jupyter_console.get_workspace_globals
        )

    def close(self, index):

        console = self.widget(index)
        console.shutdown()
        self.removeTab(index)
        self.setTabsClosable(self.count() > 1)
        self.extension_manager.fire(
            'workspace_close',
            name=console.name
        )

    def close_all(self):

        while self.count():
            self.close(0)

    @property
    def current(self):

        return self.currentWidget()

    def _on_switch(self, index):

        if self.widget(index) is None:
            return
        self.extension_manager.fire(
            'workspace_switch',
            name=self.widget(index).name,
            workspace_func=self.widget(index).get_workspace_globals
        )

    def _event_durations(self):
        
        """Registered as a global function in the Python workspace to get an
        overview of event durations for development purposes.
        """
        
        if not self.main_window.options.profile:
            print('Start with --performance-profile to see event durations')
            return
        event_durations = []
        for ext in self.extension_manager._extensions:
            for event, durations in ext._event_durations.items():
                event_durations.append(
                    (ext, event, sum(durations) / len(durations))
                )
        for ext, event, duration in sorted(
            event_durations, key=lambda e: -e[2]
        ):
            print('{}({}): {:.2f} ms'.format(event, ext.name(), duration))
