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
from openexp._canvas._element.xpyriment import XpyrimentElement
from expyriment.stimuli import Ellipse as ExpyrimentEllipse


class Xpyriment(XpyrimentElement, Ellipse):

    def prepare(self):

        self._stim = ExpyrimentEllipse(
            radii=(self.w//2, self.h//2),
            position=self.to_xy(self.x+self.w//2, self.y+self.h//2),
            colour=self.color.backend_color,
            line_width=0 if self.fill else self.penwidth
        )
        self._stim.preload()
