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

__author__ = "Sebastiaan Mathot"
__license__ = "GPLv3"

from qtpy import QtWidgets
import os.path


class recent_action(QtWidgets.QAction):

    """Menu action for a recently opened file"""

    def __init__(self, path, main_window, menu):
        """
        Constructor

        Arguments:
        path -- path to the recent file
        main_window -- the main window
        menu -- the menu into which the action should be inserted
        """

        QtWidgets.QAction.__init__(self, os.path.basename(path), menu)
        self.main_window = main_window
        self.triggered.connect(self.open_file)
        self.path = path

    def open_file(self, dummy=None):
        """
        Open the file

        Keyword arguments:
        dummy -- a dummy argument passed by the signal handler (default=None)
        """

        self.main_window.open_file(path=self.path)
