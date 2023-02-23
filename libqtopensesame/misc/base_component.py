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
import os
from qtpy import QtCore, QtWidgets, uic
from openexp import resources
from libopensesame.oslogging import oslogger


class BaseComponent:

    r"""A base class for all components, notably dialogs and widgets."""
    enc = u'utf-8'

    def setup(self, main_window, ui=None):
        r"""Constructor.

        Parameters
        ----------
        main_window
            A qtopensesame object.
        ui, optional
            An id for a user-interface file. For example
            'dialogs.quick_switcher' will correspond to the file
            'resources/ui/dialogs/quick_switcher.ui'.
        """
        self.main_window = self.get_main_window(main_window)
        self.load_ui(ui)
        if hasattr(self.main_window, u'theme'):
            self.main_window.theme.apply_theme(self)

    def load_ui(self, ui=None):
        r"""Dynamically loads the ui, if any.

        Parameters
        ----------
        ui, optional
            An id for a user-interface file, or None.
        """
        self.ui = None
        if ui is None:
            return
        # If the UI file has been explicitly registered, which is the case
        # for extensions
        try:
            ui_path = resources[ui]
        except FileNotFoundError:
            # Dot-split the ui id, append a `.ui` extension, and assume it's
            # relative to the resources/ui subfolder.
            path_list = [u'ui'] + ui.split(u'.')
            try:
                ui_path = resources[os.path.join(*path_list) + '.ui']
            except FileNotFoundError:
                return
        oslogger.debug(f'dynamically loading ui: {ui_path}')
        with safe_open(ui_path) as fd:
            self.ui = uic.loadUi(fd, self)

    def get_main_window(self, main_window):
        r"""If the main_window is actually not the main window, but a widget
        that has the main window somewhere above it in the hierarchy, we
        traverse upwards.

        Parameters
        ----------
        main_window
            An object that is the main window or a descendant of the main
            window.

        Returns
        -------
        qtopensesame
            The main window.
        """
        from libqtopensesame.qtopensesame import QtOpenSesame
        while not isinstance(main_window, QtOpenSesame):
            if hasattr(main_window, u'main_window'):
                _parent = main_window.main_window
            else:
                _parent = main_window.parent()
            main_window = _parent
        return main_window

    @staticmethod
    def quick_connect(slot, signals):
        r"""A convenience function to connect many signals to one slot.

        Parameters
        ----------
        slot
            a slot
        signals
            a list of signals
        """
        for signal in signals:
            signal.connect(slot)


# Alias for backwards compatibility
base_component = BaseComponent
