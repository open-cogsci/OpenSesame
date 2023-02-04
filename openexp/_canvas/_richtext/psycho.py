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
import platform
from openexp._canvas._richtext.richtext import RichText
from openexp._canvas._element.psycho import PsychoElement
from psychopy import visual


class Psycho(PsychoElement, RichText):

    def prepare(self):

        im = self._to_pil()
        if platform.system() == 'Darwin':
            # When displaying on Mac retina screens, the resolutions reported
            # by psychopy's window object and OpenSesame's experiment object
            # may diverge. This results in incorrectly rendered text with
            # respect to scale and positioning. We correct for the discrepancy
            # between reported sizes by the ratios calculated below. If the
            # sizes reported by win and experiment are equal, the ratio values
            # should end up as 1, and nothing changes.
            x_ratio = int(self.win.size[0] / self.experiment.width)
            y_ratio = int(self.win.size[1] / self.experiment.height)
            # Only resize if necessary to prevent unnecessary operations
            if x_ratio != 1 or y_ratio != 1:
                im = im.resize((im.width * x_ratio, im.height * y_ratio))
            x, y = self.to_xy(self.x * x_ratio, self.y * y_ratio)
        else:
            x, y = self.to_xy(self.x, self.y)
        if not self.center:
            x += im.width // 2
            y -= im.height // 2
        self._stim = visual.SimpleImageStim(self.win, im, pos=(x, y))
