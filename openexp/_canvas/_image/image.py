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
from openexp._canvas._element.element import Element


class Image(Element):

    def __init__(self, canvas, fname, center=True, x=None, y=None, scale=None,
                 rotation=None, **properties):

        x, y = canvas.none_to_center(x, y)
        self._image_size = None
        self._shapely_polygon = None
        Element.__init__(
            self, canvas,
            fname=fname,
            center=center,
            x=x,
            y=y,
            scale=scale,
            rotation=rotation,
            **properties
        )

    def _size(self):

        if self._image_size is None:
            from PIL import Image
            w, h = Image.open(self.fname).size
            if self.scale is not None:
                w *= self.scale
                h *= self.scale
            self._image_size = w, h
        return self._image_size

    @property
    def rect(self):

        from PIL import Image

        im = Image.open(self.fname)
        w1, h1 = im.size
        if self.rotation is not None and self.rotation != 0:
            im = im.rotate(self.rotation, expand=True)
        w2, h2 = im.size
        im.close()
        dx = (w2-w1)/2
        dy = (h2-h1)/2
        if self.scale is not None:
            w2 *= self.scale
            h2 *= self.scale
            dx *= self.scale
            dy *= self.scale
        x, y = self.none_to_center(self.x, self.y)
        if self.center:
            return x-w2//2, y-h2//2, w2, h2
        return x-dx, y-dy, w2, h2

    def __contains__(self, xy):

        # Shapely is used to determine whether a point falls exactly within the
        # polygon. If shapely isn't available, we fall back to a simple bounding
        # box. The shapely polygon is stored for performance.
        try:
            from shapely.geometry import box, Point
            from shapely import affinity
        except ImportError:
            return Element.__contains__(self, xy)
        if self._shapely_polygon is None:
            w, h = self._size()
            x, y = self.none_to_center(self.x, self.y)
            if self.center:
                x -= w / 2
                y -= h / 2
            self._shapely_polygon = box(x, y, x + w, y + h)
            if self.rotation:
                self._shapely_polygon = affinity.rotate(
                    self._shapely_polygon,
                    self.rotation
                )
        return self._shapely_polygon.contains(Point(*xy))

    def _on_attribute_change(self, **kwargs):

        # When a change occurs the shapely line (if any) needs to be
        # redetermined in __contains__
        self._shapely_polygon = None
        Element._on_attribute_change(self, **kwargs)
