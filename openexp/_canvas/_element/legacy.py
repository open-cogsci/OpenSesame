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


class LegacyElement(object):

    """
    desc:
            Together with Element, LegacyElement is the base object for all legacy
            sketchpad elements.
    """

    @property
    def surface(self):
        return self._canvas.surface

    def _on_attribute_change(self, **kwargs):

        self._canvas.redraw()

    def copy(self, canvas):

        # We reinstantiate the Element from scratch, to avoid having to
        # deep-copy anything
        properties = {
            key: val.colorspec if hasattr(val, u'colorspec') else val
            for key, val in self._properties.items()
        }
        return self.__class__(canvas, **properties)
