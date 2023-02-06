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
import pygame
from openexp._canvas import legacy
from openexp._canvas._text.text import Text
from openexp._canvas._element.legacy import LegacyElement
from openexp import resources


class Legacy(LegacyElement, Text):

    def __init__(self, canvas, text, x, y, **properties):

        self._antialias = True
        Text.__init__(self, canvas, text, x, y, **properties)
        self._set_font()

    def prepare(self):

        self._set_font()
        surface = self._font.render(self.text, self._antialias,
                                    self.color.backend_color)
        self.surface.blit(surface, self.to_xy(self.x, self.y))

    @property
    def size(self):

        return self._font.size(self.text)

    def _set_font(self):

        self._font = self._pygame_font(self.experiment, self.font_family,
                                       self.font_size)
        self._font.set_bold(self.font_bold)
        self._font.set_italic(self.font_italic)
        self._font.set_underline(self.font_underline)

    @staticmethod
    def _pygame_font(experiment, family, size):

        if (family, size) in legacy.fonts:
            return legacy.fonts[(family, size)]
        try:
            path = resource[f'{family}.ttf']
        except:
            # If the family cannot be found in the filepool, assume that it is
            # a system font.
            font = pygame.font.SysFont(family, size)
        else:
            fd = open(path, u'rb')
            legacy.fileobjects.append(fd)
            font = pygame.font.Font(fd, size)
        legacy.fonts[(family, size)] = font
        return font
