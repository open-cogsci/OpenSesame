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
import functools
from jupyter_client import kernelspec
from libqtopensesame.misc.config import cfg
from libqtopensesame.widgets.base_widget import BaseWidget
from libopensesame.oslogging import oslogger
from qtpy.QtWidgets import QHBoxLayout, QPushButton, QMenu
from libqtopensesame.misc.translate import translation_context
from .constants import KERNEL_NAMES
_ = translation_context(u'JupyterConsole', category=u'extension')


class ConsoleCornerWidget(BaseWidget):

    def __init__(self, console_tabwidget, kwargs):

        super(ConsoleCornerWidget, self).__init__(console_tabwidget)
        self._console_tabwidget = console_tabwidget
        self._add_button = QPushButton()
        self._add_button.setIcon(self.main_window.theme.qicon(u'list-add'))
        self._add_button.setFlat(True)
        self._add_button.setMenu(self._kernel_menu())
        self._add_button.setToolTip(_(u'Start new console'))
        self._restart_button = QPushButton()
        self._restart_button.setIcon(
            self.main_window.theme.qicon(u'view-refresh')
        )
        self._restart_button.setFlat(True)
        self._restart_button.clicked.connect(self._restart)
        self._restart_button.setToolTip(_(u'Restart kernel'))
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._restart_button)
        self._layout.addWidget(self._add_button)
        self.setLayout(self._layout)

    def _add(self, kernel):

        self._console_tabwidget.add(kernel=kernel)

    def _installed_kernels(self):

        if cfg.jupyter_kernels:
            return safe_decode(cfg.jupyter_kernels).split(u';')
        kernelspec_manager = kernelspec.KernelSpecManager()
        kernels = list(kernelspec_manager.find_kernel_specs().keys())
        # Python 2 and 3 kernels apparently just start the same kernel that
        # corresponds to the active Python kernel. So if they are both
        # installed, we expose only one.
        if 'python2' in kernels and 'python3' in kernels:
            kernels.remove('python2')
        oslogger.debug('installed kernels: {}'.format(str(kernels)))
        return kernels

    def _kernel_menu(self):

        menu = QMenu(self.main_window)
        for kernel in self._installed_kernels():
            action = menu.addAction(KERNEL_NAMES.get(kernel, kernel))
            action.triggered.connect(
                functools.partial(self._add, kernel=kernel)
            )
        return menu

    def _restart(self):

        self._console_tabwidget.current.restart()
