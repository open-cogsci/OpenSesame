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
from openexp._canvas._ellipse.ellipse import Ellipse


class Circle(Ellipse):

    def __init__(self, canvas, x, y, r, **properties):

        properties = properties.copy()
        self._r = r
        properties.update({'x': x, 'y': y, 'w': 2*r, 'h': 2*r})
        self.prepare = self.circle_prepare(self.prepare)
        Ellipse.__init__(self, canvas, **properties)

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, val):
        self._r = val
        self.w = self.h = 2 * val

    @property
    def rect(self):
        return self.x-self.r, self.y-self.r, self.r*2, self.r*2

    def __contains__(self, xy):

        return ((xy[0]-self.x)**2+(xy[1]-self.y)**2)**0.5 <= self.r

    def circle_prepare(self, ellipse_prepare):
        """
        desc:
                A decorator that converts the center coordinates used by the circle
                to the top-left coordinates used by the ellipse.
        """

        def inner():

            r = self._properties[u'w'] // 2
            self._properties[u'x'] -= r
            self._properties[u'y'] -= r
            ellipse_prepare()
            self._properties[u'x'] += r
            self._properties[u'y'] += r

        return inner

    @staticmethod
    def _getter(key, self):

        if key == u'r':
            return self._properties[u'w'] // 2
        return Ellipse._getter(key, self)

    @staticmethod
    def _setter(key, self, val):

        if key == u'r':
            self._properties[u'w'] = val * 2
            self._properties[u'h'] = val * 2
            return
        Ellipse._setter(key, self, val)
