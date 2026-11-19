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
import sys

TESTS_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_PATH = os.path.dirname(TESTS_PATH)

# Make all project packages (libopensesame, libqtopensesame, openexp, etc.) as
# well as the shared test configuration in tests/config importable, regardless
# of the folder from which the tests are run.
for _path in (PROJECT_PATH, TESTS_PATH):
    if _path not in sys.path:
        sys.path.insert(0, _path)
