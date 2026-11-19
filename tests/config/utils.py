#-*- coding:utf-8 -*-

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
import os

TESTS_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_PATH = os.path.dirname(TESTS_PATH)

# The data folder contains example experiments and other resource files that
# are used by the basic and headless test groups.
DATA_PATH = os.path.join(TESTS_PATH, u'data')


def data_path(basename):

    """
    desc:
        Returns the path to a file in the shared test-data folder.

    arguments:
        basename:   A filename in the tests/data folder.

    returns:
        The full path to the file.
    """

    return os.path.join(DATA_PATH, basename)
