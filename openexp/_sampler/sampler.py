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
from openexp.backend import Backend, configurable
from libopensesame.exceptions import InvalidValue


class Sampler(Backend):
    r"""The `Sampler` class provides functionality to play sound samples. You 
    generally create a `Sampler` object with the `Sampler()` factory function, 
    as described in the section [Creating a Sampler](#creating-a-sampler).
    
    __Example:__
    
    ~~~ .python
    src = pool['bark.ogg']
    my_sampler = Sampler(src, volume=.5)
    my_sampler.play()
    ~~~
    
    [TOC]
    
    ## Things to know
    
    ### Creating a Sampler
    
    You generally create a `Sampler` with the `Sampler()` factory function, which
    takes the full path to a sound file as the first argument.
    
    ~~~ .python
    src = pool['bark.ogg']
    my_sampler = Sampler(src)
    ~~~
    
    Optionally, you can pass [Playback keywords](#playback-keywords) to `Sampler()`
    to set the default behavior:
    
    ~~~ .python
    src = pool['bark.ogg']
    my_sampler = Sampler(src, volume=.5)
    ~~~
    
    ### Sampling rate
    
    If you find that your sample plays too slowly (low pitch) or too quickly (high
    pitch), make sure that the sampling rate of your sample matches the sampling
    rate of the sampler back-end as specified under backend settings.
    
    ### Supported file formats
    
    Sound files in `.wav`, `.mp3`, and `.ogg` format are supported. If you need to
    convert samples from a different format, you can use
    [Audacity](http://sourceforge.net/projects/audacity/).
    
    ### Playback keywords
    
    Functions that accept `**playback_args` take the following keyword arguments:
    
    - `volume` specifies a volume between `0.0` (silent) and `1.0` (maximum).
    - `pitch` specifies a pitch (or playback speed), where values > 1 indicate a
      higher pitch, and values < 1 indicate a lower pitch.
    - `pan` specifies a panning, where values < 0 indicate panning to the left, and
      values > 0 indicate panning to the right. Alternatively, you can set pan to
      'left' or 'right' to play only a single channel.
    - `duration` specifies the duration of the sound in milliseconds, or is set to
      `0` or `None` to play the full sound.
    - `fade_in` specifies the fade-in time (or attack) of the sound, or is set to
      `0` or `None` to disable fade-in.
    - `block` indicates whether the experiment should block (`True`) during
      playback or not (`False`).
    
    ~~~ .python
    src = pool['bark.ogg']
    my_sampler = Sampler(src)
    my_sampler.play(volume=.5, pan='left')
    ~~~
    
    Playback keywords only affect the current operation (except when passed to
    `Sampler()` when creating the object). To change the behavior for all
    subsequent operations, set the playback properties directly:
    
    ~~~ .python
    src = pool['bark.ogg']
    my_sampler = Sampler(src)
    my_sampler.volume = .5
    my_sampler.pan = 'left'
    my_sampler.play()
    ~~~
    
    Or pass the playback keywords to `Sampler()` when creating the object:
    
    ~~~ .python
    src = pool['bark.ogg']
    my_sampler = Sampler(src, volume=.5, pan='left')
    my_sampler.play()
    ~~~
    """
    def __init__(self, experiment, src, **playback_args):
        r"""Constructor to create a new SAMPLER object. You do not generally
        call this constructor directly, but use the `Sampler()` function,
        which
        is described here: [/python/sampler/]().

        Parameters
        ----------
        experiment : experiment
            The experiment object.
        src : unicode, str
            The full path to a `.wav` or `.ogg` file.
        **playback_args : dict
            Optional [playback keywords](#playback-keywords) that will be used
            as the default for this SAMPLER object.


        Examples
        --------
        >>> src = pool['my_sound.ogg']
        >>> my_sampler = Sampler(src, volume=.5)
        """
        self.experiment = experiment
        Backend.__init__(self, configurables={
            'volume': self.assert_numeric,
            'pan': self.assert_pan,
            'pitch': self.assert_numeric,
            'duration': self.assert_numeric_or_None,
            'fade_in': self.assert_numeric_or_None,
            'block': self.assert_bool,
        }, **playback_args)

    def default_config(self):

        return {
            'volume': 1.,
            'pan': 0.,
            'pitch': 1.,
            'duration': None,
            'fade_in': None,
            'block': False,
        }

    def assert_pan(self, key, val):

        if not isinstance(val, int) and not isinstance(val, float) \
                and val not in ['left', 'right']:
            raise InvalidValue(
                'pan should be numeric, \'left\', or \'right\', not %s' % val)

    @configurable
    def play(self, **playback_args):
        r"""Plays the sound.

        Parameters
        ----------
        **playback_args : dict
            Optional [playback keywords](#playback-keywords) that will be used
            for this call to `Sampler.play()`. This does not affect subsequent
            operations.


        Examples
        --------
        >>> src = pool['my_sound.ogg']
        >>> my_sampler = Sampler(src)
        >>> my_sampler.play(pitch=.5, block=True)
        """
        raise NotImplementedError()

    def stop(self):
        r"""Stops the currently playing sound (if any).

        Examples
        --------
        >>> src = pool['my_sound.ogg']
        >>> my_sampler = Sampler(src)
        >>> my_sampler.play()
        >>> sleep(100)
        >>> my_sampler.stop()
        """
        raise NotImplementedError()

    def pause(self):
        r"""Pauses playback (if any).

        Examples
        --------
        >>> src = pool['my_sound.ogg']
        >>> my_sampler = Sampler(src)
        >>> my_sampler.play()
        >>> sleep(100)
        >>> my_sampler.pause()
        >>> sleep(100)
        >>> my_sampler.resume()
        """
        raise NotImplementedError()

    def resume(self):
        r"""Resumes playback (if any).

        Examples
        --------
        >>> src = pool['my_sound.ogg']
        >>> my_sampler = Sampler(src)
        >>> my_sampler.play()
        >>> sleep(100)
        >>> my_sampler.pause()
        >>> sleep(100)
        >>> my_sampler.resume()
        """
        raise NotImplementedError()

    def is_playing(self):
        r"""Checks if a sound is currently playing.

        Returns
        -------
        bool
            True if a sound is playing, False if not.

        Examples
        --------
        >>> src = pool['my_sound.ogg']
        >>> my_sampler = Sampler(src)
        >>> my_sampler.play()
        >>> sleep(100)
        >>> if my_sampler.is_playing():
        >>>         print('The sampler is still playing!')
        """
        raise NotImplementedError()

    def wait(self):
        r"""Blocks until the sound has finished playing or returns right away
        if no sound is playing.

        Examples
        --------
        >>> src = pool['my_sound.ogg']
        >>> my_sampler = Sampler(src)
        >>> my_sampler.play()
        >>> my_sampler.wait()
        >>> print('The sampler is finished!')
        """
        raise NotImplementedError()

    @staticmethod
    def init_sound(experiment):
        r"""Initializes the pygame mixer before the experiment begins.

        Parameters
        ----------
        experiment : experiment
            The experiment object.
        """
        raise NotImplementedError()

    @staticmethod
    def close_sound(experiment):
        r"""Closes the mixer after the experiment is finished.

        Parameters
        ----------
        experiment : experiment
            The experiment object.
        """
        raise NotImplementedError()


# Non PEP-8 alias for backwards compatibility
sampler = Sampler
