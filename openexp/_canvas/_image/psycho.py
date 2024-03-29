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
from openexp._canvas._image.image import Image
from openexp._canvas._element.psycho import PsychoElement, RotatingElement
from psychopy import visual


class Psycho(RotatingElement, PsychoElement, Image):

    def prepare(self):

        self._stim = visual.ImageStim(
            win=self.win,
            image=safe_decode(self.fname)
        )
        if self.rotation is not None and self.rotation != 0:
            self._stim.ori = self.rotation
        if self.scale is not None:
            w, h = self._stim.size
            w *= self.scale
            h *= self.scale
            self._stim.size = w, h
        x, y = self.to_xy(self.x, self.y)
        if not self.center:
            size = self._stim.size
            x += size[0] / 2
            y -= size[1] / 2
        self._stim.pos = x, y
