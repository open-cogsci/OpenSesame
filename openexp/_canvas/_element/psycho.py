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
        # Get the smallest power-of-two that is larger than or equal to the
        # given size
        size = int(np.ceil(np.sqrt(size))**2)
        # Create a PsychoPy mask
        env = canvas._match_env(env)
        if env == u'c':
            return u'circle', size
        if env == u'g':
            return u'gauss', 6 * stdev
        if env == u'r':
            return u'None', size
        if env == u'l':
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
