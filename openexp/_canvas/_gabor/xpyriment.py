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
from openexp._canvas import canvas
from openexp._canvas._gabor.gabor import Gabor
from openexp._canvas._element.xpyriment import XpyrimentElement
from expyriment.stimuli._visual import Visual


class Xpyriment(XpyrimentElement, Gabor):

    def prepare(self):

        im = canvas._gabor(
            self.orient,
            self.freq,
            self.env,
            self.size,
            self.stdev,
            self.phase,
            self.col1,
            self.col2,
            self.bgmode
        )
        surface = pygame.image.fromstring(im.tobytes(), im.size, u'RGB')
        self._stim = Visual(position=self.to_xy(self.x, self.y))
        self._stim.set_surface(surface)
        self._stim.preload()
