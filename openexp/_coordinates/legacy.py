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
from openexp._coordinates.coordinates import Coordinates


class Legacy(Coordinates):

    r"""For function specifications and docstrings, see
    `openexp._coordinates.coordinates`.
    """
    def to_xy(self, x, y=None):

        if isinstance(x, tuple):
            x, y = x
        x, y = self.none_to_center(x, y)
        if not self.uniform_coordinates:
            return x, y
        return x + self._xcenter, y + self._ycenter

    def from_xy(self, x, y=None):

        if isinstance(x, tuple):
            x, y = x
        if not self.uniform_coordinates:
            return x, y
        return x - self._xcenter, y - self._ycenter


# Non PEP-8 alias for backwards compatibility
legacy = Legacy
