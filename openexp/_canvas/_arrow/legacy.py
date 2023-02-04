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
from openexp._canvas._arrow.arrow import Arrow
from openexp._canvas._polygon.legacy import Legacy as LegacyPolygon


class Legacy(LegacyPolygon, Arrow):

    def copy(self, canvas):

        vertices = self._properties['vertices']
        del self._properties['vertices']
        arrow_copy = LegacyPolygon.copy(self, canvas)
        self._properties['vertices'] = vertices
        return arrow_copy

    def _on_attribute_change(self, **kwargs):

        # When a change occurs the shapely line (if any) needs to be
        # redetermined in __contains__
        self._properties['vertices'] = self._shape(
            self.sx,
            self.sy,
            self.ex,
            self.ey,
            self.body_length,
            self.body_width,
            self.head_width
        )
        Arrow._on_attribute_change(self, **kwargs)
