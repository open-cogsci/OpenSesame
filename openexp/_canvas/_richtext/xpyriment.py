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
from openexp._canvas._richtext.richtext import RichText
from openexp._canvas._element.xpyriment import XpyrimentElement
from expyriment.stimuli._visual import Visual


class Xpyriment(XpyrimentElement, RichText):

    def prepare(self):

        im = self._to_pil()
        surface = pygame.image.fromstring(im.tobytes(), im.size, im.mode)
        x, y = self.to_xy(self.x, self.y)
        if not self.center:
            x += im.width // 2
            y -= im.height // 2
        self._stim = Visual(position=(x, y))
        self._stim.set_surface(surface)
        self._stim.preload()
