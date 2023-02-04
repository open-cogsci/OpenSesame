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
import os
import pygame
from libopensesame.exceptions import osexception
from openexp._canvas._image.image import Image
from openexp._canvas._element.legacy import LegacyElement


class Legacy(LegacyElement, Image):

    def prepare(self):

        if not hasattr(self, '_image_surface') or self._dirty:
            self._dirty = False
            fname = safe_decode(self.fname)
            if not os.path.isfile(fname):
                raise osexception(u'"%s" does not exist' % fname)
            with open(fname, u'rb') as fd:
                try:
                    self._image_surface = pygame.image.load(fd)
                except pygame.error:
                    raise osexception(
                        u"'%s' is not a supported image format" % fname)
            # After rotation, the figure gets bigger. We therefore need to
            # compensate by moving it a bit
            if self.rotation is not None and self.rotation != 0:
                w1, h1 = self._image_surface.get_size()
                self._image_surface = pygame.transform.rotate(
                    self._image_surface.convert_alpha(), -self.rotation
                )
                w2, h2 = self._image_surface.get_size()
                self._dx = (w2-w1)/2
                self._dy = (h2-h1)/2
            else:
                self._dx = self._dy = 0
            if self.scale is not None:
                try:
                    self._image_surface = pygame.transform.smoothscale(
                        self._image_surfacesurface,
                        (int(self._image_surface.get_width()*self.scale),
                         int(self._image_surface.get_height()*self.scale))
                    )
                except:
                    self._image_surface = pygame.transform.scale(
                        self._image_surface,
                        (int(self._image_surface.get_width()*self.scale),
                         int(self._image_surface.get_height()*self.scale))
                    )
                self._dx *= self.scale
                self._dy *= self.scale
        size = self._image_surface.get_size()
        x, y = self.to_xy(self.x, self.y)
        if self.center:
            x -= size[0] / 2
            y -= size[1] / 2
        else:
            x -= self._dx
            y -= self._dy
        self.surface.blit(self._image_surface, (x, y))

    @staticmethod
    def _setter(key, self, val):

        self._dirty = True
        Image._setter(key, self, val)
