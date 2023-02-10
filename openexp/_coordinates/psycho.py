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


class Psycho(Coordinates):

    r"""For function specifications and docstrings, see
    `openexp._coordinates.coordinates`.
    """
    def to_xy(self, x, y=None):

        if isinstance(x, tuple):
            x, y = x
        x, y = self.none_to_center(x, y)
        # For PsychoPy, 0,0 is the display center and positive y
        # coordinates are down.
        return x, -y

    def from_xy(self, x, y=None):

        if y is None:
            x, y = x
        return x, -y


# Non PEP-8 alias for backwards compatibility
psycho = Psycho
