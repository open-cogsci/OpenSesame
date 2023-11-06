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
import numpy as np
from openexp._canvas import canvas
from libopensesame.oslogging import oslogger


class PsychoElement:

    r"""Together with Element, PsychoElement is the base object for all psycho
    sketchpad elements.
    """
    @property
    def win(self):
        return self._canvas.experiment.window

    def show(self):

        if self.visible:
            self._stim.draw()

    def _on_attribute_change(self, **kwargs):

        if self._canvas.auto_prepare:
            self.prepare()
            
    @staticmethod
    def _power_of_two(n):
        n = int(n)
        # A power of two always has exactly one bit set and does not have any
        # bitwise overlap with one number lower:
        # 4: 100
        # 3: 011
        # &: 000
        if (n & (n - 1) == 0) and n != 0:
            return n
        # The bit_length is the number of bits necessary to represent a number
        # so for 3 this would be 2: 11. The bit_length for one number lower in
        # this case is still 2: 10. The next power of two is 2 raised by this
        # number, so 2 ** 2 = 4.
        rounded_up = 2 ** ((n - 1).bit_length())
        oslogger.warning(
            f"Warning: {n} is not a power of two, rounding up to {rounded_up}.")
        return rounded_up

    def _mask(self, env, size, stdev):
        r"""Generates a PsychoPy mask for Gabor and NoisePatch stimuli.

        Parameters
        ----------
        env : str
            The envelope.
        size : int
            The stimulus size.
        stdev : int
            The standard deviation of the mask if the envelope is gaussian.

        Returns
        -------
        ndarray
            A PsychoPy mask, which is a numpy array.
        """
        # Create a PsychoPy mask
        env = canvas._match_env(env)
        if env == u'c':
            return u'circle', size
        if env == u'g':
            return u'gauss', 6 * stdev
        if env == u'r':
            return u'None', size
        if env == u'l':
            # Get the smallest power-of-two that is larger than or equal to 
            # the given size
            size = self._power_of_two(size)
            _env = np.zeros([size, size])
            for x in range(size):
                for y in range(size):
                    r = np.sqrt((x-size/2)**2+(y-size/2)**2)
                    _env[x, y] = (max(0, (0.5*size-r) / (0.5*size))-0.5)*2
            return _env, size
        raise ValueError('Invalid mask')


class RotatingElement:

    def _on_attribute_change(self, **kwargs):

        if u'rotation' in kwargs:
            self._stim.ori = kwargs.pop(u'rotation')
        if kwargs:
            super(RotatingElement, self)._on_attribute_change(**kwargs)
