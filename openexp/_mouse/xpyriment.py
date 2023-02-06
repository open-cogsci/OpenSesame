# -*- coding:utf-8 -*-

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
from pygame.locals import *
from openexp._mouse.mouse import Mouse
from openexp._mouse.legacy import Legacy
from openexp.backend import configurable
from libopensesame.exceptions import osexception
import pygame
from expyriment import stimuli
from expyriment.misc.geometry import coordinates2position as c2p
from openexp._coordinates.xpyriment import Xpyriment as XpyrimentCoordinates


class Xpyriment(XpyrimentCoordinates, Legacy):

    r"""This is a mouse backend built on top of PyGame, adapted for Expyriment.
    For function specifications and docstrings, see `openexp._mouse.mouse`.
    """
    settings = {}

    def __init__(self, experiment, **resp_args):

        Mouse.__init__(self, experiment, **resp_args)
        XpyrimentCoordinates.__init__(self)

    @configurable
    def get_click(self):

        buttonlist = self.buttonlist
        timeout = self.timeout
        pygame.mouse.set_visible(self.visible)
        start_time = pygame.time.get_ticks()
        time = start_time
        while True:
            time = pygame.time.get_ticks()
            # Process the input
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.experiment.pause()
                        continue
                    pygame.event.post(event)
                if event.type == MOUSEBUTTONDOWN:
                    if buttonlist is None or event.button in buttonlist:
                        pygame.mouse.set_visible(self._cursor_shown)
                        return event.button, self.from_xy(event.pos), time
            if timeout is not None and time - start_time >= timeout:
                break
        pygame.mouse.set_visible(self._cursor_shown)
        return None, None, time


# Non PEP-8 alias for backwards compatibility
xpyriment = Xpyriment
