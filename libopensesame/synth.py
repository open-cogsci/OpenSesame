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
from libopensesame.exceptions import OSException
from libopensesame.base_response_item import BaseResponseItem
from libopensesame.sampler import Sampler
from openexp.synth import Synth as OpenExpSynth


class Synth(Sampler):
    """An item for synthesized-sound playback."""
    
    description = 'A basic sound synthesizer'

    def reset(self):
        self.var.freq = 440
        self.var.length = 100
        self.var.osc = 'sine'
        self.var.pan = 0
        self.var.attack = 0
        self.var.decay = 5
        self.var.volume = 1.0
        self.var.duration = 'sound'
        self.block = False

    def prepare(self):
        BaseResponseItem.prepare(self)
        try:
            self.sampler = OpenExpSynth(self.experiment, osc=self.var.osc,
                                        freq=self.var.freq,
                                        length=self.var.length,
                                        attack=self.var.attack,
                                        decay=self.var.decay)
        except Exception as e:
            raise OSException(f'Failed to generate sound: {e}')
        pan = self.var.pan
        if pan == -20:
            pan = 'left'
        elif pan == 20:
            pan = 'right'
        self.sampler.pan = pan
        self.sampler.volume = self.var.volume
        self.sampler.block = self.var.duration == 'sound'


# Alias for backwards compatibility
synth = Synth
