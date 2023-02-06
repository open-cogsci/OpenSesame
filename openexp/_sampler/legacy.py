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
import pygame
from openexp._sampler.sampler import Sampler
from libopensesame.exceptions import osexception
from libopensesame.oslogging import oslogger
from libopensesame import misc
from openexp.keyboard import Keyboard
from openexp.backend import configurable
import os.path
try:
    import numpy
except:
    numpy = None
try:
    import pygame.mixer as mixer
except ImportError:
    import android.mixer as mixer


class Legacy(Sampler):

    r"""This is a sampler backend built on top of PyGame. For function
    specifications and docstrings, see `openexp._sampler.sampler`.
    """
    # The settings variable is used by the GUI to provide a list of back-end
    # settings
    settings = {
        u"sound_buf_size": {
            u"name": u"Sound buffer size",
            u"description": u"Size of the sound buffer (increase if playback is choppy)",
            u"default": 1024
        },
        u"sound_freq": {
            u"name": u"Sampling frequency",
            u"description": u"Determines the sampling rate",
            u"default": 48000
        },
        u"sound_sample_size": {
            u"name": u"Sample size",
            u"description": u"Determines the bith depth (negative = signed)",
            u"default": -16
        },
        "sound_channels": {
            u"name": u"The number of sound channels",
            u"description": u"1 = mono, 2 = stereo",
            u"default": 2
        },
    }

    def __init__(self, experiment, src, **playback_args):

        if src is not None:
            if isinstance(src, str):
                if not os.path.exists(src):
                    raise osexception(
                        u"openexp._sampler.legacy.__init__() the file '%s' does not exist"
                        % src)
                if os.path.splitext(src)[1].lower() not in (".ogg", ".wav"):
                    raise osexception(
                        u"openexp._sampler.legacy.__init__() the file '%s' is not an .ogg or .wav file"
                        % src)
                # The mixer chokes on unicode pathnames that contain special
                # characters. To avoid this we convert to str with the
                # filesystem encoding. (Python 2 only).
                if not py3 and isinstance(src, str):
                    import sys
                    src = src.encode(misc.filesystem_encoding())
            self.sound = mixer.Sound(src)
        Sampler.__init__(self, experiment, src, **playback_args)
        self.keyboard = Keyboard(experiment)

    def set_config(self, **cfg):

        if u'duration' in cfg and cfg[u'duration'] is None:
            cfg[u'duration'] = 0
        if u'fade_in' in cfg and cfg[u'fade_in'] is None:
            cfg[u'fade_in'] = 0
        Sampler.set_config(self, **cfg)
        if u'volume' in cfg:
            self.sound.set_volume(cfg[u'volume'])
        if u'pitch' in cfg:
            self.adjust_pitch(cfg[u'pitch'])
        if u'pan' in cfg:
            self.adjust_pan(cfg[u'pan'])

    def adjust_pitch(self, p):

        # On Android, numpy does not exist and this is not supported
        if numpy is None:
            return
        if type(p) not in (int, float) or p <= 0:
            raise osexception(
                u"openexp._sampler.legacy.pitch should be a positive number")
        if p == 1:
            return
        buf = pygame.sndarray.array(self.sound)
        _buf = []
        for i in range(int(float(len(buf)) / p)):
            _buf.append(buf[int(float(i) * p)])
        self.sound = pygame.sndarray.make_sound(
            numpy.array(_buf, dtype=u"int16"))

    def adjust_pan(self, p):

        # On Android, numpy does not exist and this is not supported
        if numpy is None:
            return
        if type(p) not in (int, float) and p not in (u"left", u"right"):
            raise osexception(
                u"openexp._sampler.legacy.pan should be a number or 'left', 'right'")
        if p == 0:
            return
        buf = pygame.sndarray.array(self.sound)
        for i in range(len(buf)):
            l = buf[i][0]
            r = buf[i][1]
            if p == "left":
                r = 0
            elif p == "right":
                l = 0
            elif p < 0:
                r = int(float(r) / abs(p))
            else:
                l = int(float(l) / p)
            buf[i][0] = l
            buf[i][1] = r
        self.sound = pygame.sndarray.make_sound(numpy.array(buf))

    @configurable
    def play(self, **playback_args):

        self.sound.play(maxtime=self.duration, fade_ms=self.fade_in)
        if self.block:
            self.wait()

    def stop(self):

        mixer.stop()

    def pause(self):

        mixer.pause()

    def resume(self):

        mixer.unpause()

    def is_playing(self):

        return bool(mixer.get_busy())

    def wait(self):

        while mixer.get_busy():
            self.keyboard.flush()

    @staticmethod
    def init_sound(experiment):

        oslogger.info(
            u"sampling freq = %d, buffer size = %d"
            % (experiment.var.sound_freq, experiment.var.sound_buf_size)
        )
        if hasattr(mixer, u'get_init') and mixer.get_init():
            oslogger.warning(u'mixer already initialized, closing')
            pygame.mixer.quit()
        mixer.pre_init(
            experiment.var.sound_freq,
            experiment.var.sound_sample_size,
            experiment.var.sound_channels,
            experiment.var.sound_buf_size
        )
        try:
            mixer.init()
        except pygame.error:
            oslogger.error(u'failed to initialize mixer')

    @staticmethod
    def close_sound(experiment):

        mixer.quit()


# Non PEP-8 alias for backwards compatibility
legacy = Legacy
