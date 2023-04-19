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
from openexp._sampler.sampler import Sampler
from libopensesame.oslogging import oslogger
from openexp.backend import configurable
from openexp.keyboard import Keyboard
import sys
import soundfile as sf
import numpy as np

DEFAULT_SOUND_FREQ = 48000
DEFAULT_BLOCK_SIZE = 256
NEEDS_BLOCK_SIZE = 'sounddevice', 'PTB'
# Due to issues with sounddevice/ portaudio on Mac OS, we fall back to
# pygame on that platform
DEFAULT_AUDIOLIB = 'pygame' if sys.platform == 'darwin' else 'sounddevice'
# Will be intialized during init_sound()
Sound = None
PLAYING = None



class Psycho(Sampler):
    """This is a sampler backend built on top of PsychoPy. For function
    specifications and docstrings, see `openexp._sampler.sampler`.
    """
    # The settings variable is used by the GUI to provide a list of back-end
    # settings
    settings = {
        'psycho_audiolib': {
            'name': 'Sound library',
            'description': 'Can be sounddevice, pyo, pygame, or PTB',
            'default': DEFAULT_AUDIOLIB},
        'sound_freq': {
            'name': 'Sampling frequency for synth',
            'description': 'Determines the sampling rate of synthesized sounds',
            'default': DEFAULT_SOUND_FREQ},
        'block_size': {
            'name': 'Buffer size',
            'description': 'Low values for low latency. High values for stability.',
            'default': DEFAULT_BLOCK_SIZE}}

    def __init__(self, experiment, src, **playback_args):

        if (isinstance(src, np.ndarray) and src.dtype == np.int16 and
                src.ndim == 1):
            # The Synth provides the data as a 1D array with int values between
            # 0 and 32767. The signal is stereo but flattened into a single
            # trace, so we expand it here.
            self._data = np.array(src, dtype=np.float64) / 32767
            self._data = self._data.reshape((self._data.shape[0] // 2, 2))
            self._samplerate = experiment.var.get('sound_freq',
                                                  DEFAULT_SOUND_FREQ)
        else:
            self._data, self._samplerate = sf.read(src)
        # Create keyword arguments, which depend on the sound backend
        kwargs = {}
        if (experiment.var.get('psycho_audiolib', DEFAULT_AUDIOLIB)
                in NEEDS_BLOCK_SIZE):
            kwargs['blockSize'] = experiment.var.get('block_size',
                                                     DEFAULT_BLOCK_SIZE)
        # Make sure that the data is a [samples, 2] array for stereo data
        if self._data.ndim == 1:
            self._data.shape = [len(self._data), 1]
        if self._data.shape[1] == 1:
            self._data = self._data.repeat(2, axis=1)
        self._sound = Sound(self._data, sampleRate=self._samplerate, **kwargs)
        # isPlaying() was introduced recently. For older versions of psychopy
        # we monkeypatch this function into existence using the older status
        # property
        # - https://github.com/psychopy/psychopy/commit/\
        #   50a730b7be0bb1a219d5666d657bad4c8cc121d1
        if not hasattr(self._sound, 'isPlaying'):
            self._sound.isPlaying = lambda self: self.status == PLAYING
        self._keyboard = Keyboard(experiment)
        Sampler.__init__(self, experiment, src, **playback_args)

    def set_config(self, **cfg):

        Sampler.set_config(self, **cfg)
        if not cfg:
            return
        if 'volume' in cfg:
            self._set_volume(cfg['volume'])
        if 'pitch' in cfg:
            self._set_pitch(cfg['pitch'])
        if 'pan' in cfg:
            self._set_pan(cfg['pan'])
        if 'duration' in cfg:
            self._set_duration(cfg['duration'])
        if 'fade_in' in cfg:
            self._set_fade_in(cfg['fade_in'])
        self._sound.stopTime = -1  # Fixes a bug in PsychoPy 3.2.4
        self._sound.setSound(self._data)

    def _set_volume(self, volume):

        if volume == 1:
            return
        self._data *= volume

    def _set_pitch(self, pitch):

        from scipy.signal import resample
        if pitch == 1:
            return
        self._data = resample(self._data, int(self._data.shape[0] / pitch))

    def _set_pan(self, pan):

        if pan == 'left':
            right_volume = 0.
            left_volume = 1.
        elif pan == 'right':
            right_volume = 1.
            left_volume = 0.
        elif pan < 0:
            right_volume = -1. / pan
            left_volume = 1.
        elif pan > 0:
            right_volume = 1.
            left_volume = 1. / pan
        else:
            return
        self._data[:, 0] *= left_volume
        self._data[:, 1] *= right_volume

    def _ms_to_samples(self, ms):

        return int(self._samplerate * (ms / 1000))

    def _set_duration(self, duration):

        if not duration:
            return
        self._data = self._data[:self._ms_to_samples(duration), :]

    def _set_fade_in(self, fade_in):

        if fade_in is None:
            return
        ramp = np.linspace(
            0, 1, self._ms_to_samples(fade_in)
        )[:self._data.shape[0]]
        self._data[:len(ramp), 0] *= ramp
        self._data[:len(ramp), 1] *= ramp

    @configurable
    def play(self, **playback_args):

        self._sound.stop()
        self._sound.play()
        if self.block:
            self.wait()

    def stop(self):

        self._sound.stop()

    def pause(self):

        self._sound.pause()

    def resume(self):

        self._sound.play()

    def is_playing(self):

        return self._sound.isPlaying

    def wait(self):

        while self._sound.isPlaying:
            self._keyboard.flush()

    @staticmethod
    def init_sound(experiment):

        global Sound, PLAYING

        from psychopy import prefs
        prefs.hardware['audioLib'] = [
            experiment.var.get('psycho_audiolib', DEFAULT_AUDIOLIB)]
        from psychopy import constants
        PLAYING = constants.PLAYING
        # Fixes a regression in psychopy introduced in
        # - https://github.com/psychopy/psychopy/commit/\
        #   45ed546b8e0a25ddb87156ef400687aaf31baf39
        # Should be removed as soon as this is fixed upstream
        import psychopy.sound._base
        psychopy.sound._base.defaultStim = []
        from psychopy.sound import Sound

    @staticmethod
    def close_sound(experiment):

        pass


# Non PEP-8 alias for backwards compatibility
psycho = Psycho
