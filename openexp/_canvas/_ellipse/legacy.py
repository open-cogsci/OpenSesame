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
from openexp._canvas._element.legacy import LegacyElement
import pygame


class Legacy(LegacyElement, Ellipse):

    def prepare(self):

        x = int(self.x)
        y = int(self.y)
        w = int(self.w)
        h = int(self.h)
        x, y = self.to_xy(x, y)
        if self.fill:
            pygame.draw.ellipse(self.surface, self.color.backend_color,
                                (x, y, w, h), 0)
            return
        # Use experyiment's method to draw ellipses with a transparent
        # interior by using the transparent colorkey method. This involves
        # some trickery by making a separate surface of which a certain color
        # is designated as transparent and draw the ellipse on there first.
        # When being blit onto another surface, this transparent color
        # (e.g. the ellipses interior is not blitted with the rest.
        line_width = self.penwidth
        size = (w, h)
        surface = pygame.surface.Surface(
            [p + line_width for p in size],
            pygame.SRCALPHA).convert_alpha()
        pygame.draw.ellipse(surface, (0, 0, 0), pygame.Rect(
            (0, 0),
            [p + line_width for p in size]))
        tmp = pygame.surface.Surface(
            [p - line_width for p in size])
        tmp.fill([0, 0, 0])
        tmp.set_colorkey([255, 255, 255])
        hole = pygame.surface.Surface(
            [p - line_width for p in size],
            pygame.SRCALPHA).convert_alpha()
        pygame.draw.ellipse(tmp, (255, 255, 255), pygame.Rect(
            (0, 0), [p - line_width for p in size]))
        hole.blit(tmp, (0, 0))
        surface.blit(hole, (line_width, line_width),
                     special_flags=pygame.BLEND_RGBA_MIN)
        surface.fill(self.color.backend_color,
                     special_flags=pygame.BLEND_RGB_MAX)
        # The line_width affects the temp's surface size, so use it to correct the
        # positioning when blitting.
        self.surface.blit(surface, (x-line_width/2, y-line_width/2))
