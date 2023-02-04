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
from collections import OrderedDict
from libopensesame.oslogging import oslogger
from openexp.backend import configurable
from openexp._canvas.canvas import Canvas
from openexp._coordinates.psycho import Psycho as PsychoCoordinates
from openexp.color import Color
from openexp.canvas_elements import Rect
from psychopy import visual, event, core, logging

# Store the experiment as a singleton, to be used in the _time() function
_experiment = None
# Store the old display gamma value
_old_gamma = None


class Psycho(Canvas, PsychoCoordinates):

    """
    desc:
            This is a canvas backend built on top of PsychoPy (with Pyglet).
            For function specifications and docstrings, see
            `openexp._canvas.canvas`.
    """

    # The settings variable is used by the GUI to provide a list of back-end
    # settings
    settings = {
        u'psychopy_waitblanking': {
            u'name': u'Wait for blanking',
            u'description': u'Block until the display has been shown',
            u'default': u'yes'
        },
        u'psychopy_monitor': {
            u'name': u'Monitor',
            u'description': u'Virtual monitor',
            u'default': u'testMonitor'
        },
        u"psychopy_screen": {
            u"name": u"Screen",
            u"description": u"The physical screen that is used",
            u"default": 0,
        },
        u"psychopy_gamma": {
            u"name": u"Gamma",
            u"description": u"Display gamma value display",
            u"default": u"unchanged",
        },
        u'psychopy_suppress_warnings': {
            u'name': u'Suppress warnings',
            u'description': u'Set PsychoPy logging level to "critical"',
            u'default': u'yes',
        }
    }

    def __init__(self, experiment, auto_prepare=True, **style_args):

        Canvas.__init__(self, experiment, auto_prepare=auto_prepare,
                        **style_args)
        PsychoCoordinates.__init__(self)
        self.clear()

    @configurable
    def clear(self):

        self._elements = OrderedDict()
        self._set_background()

    def set_config(self, **cfg):

        Canvas.set_config(self, **cfg)
        if u'background_color' in cfg and hasattr(self, u'_elements'):
            self._set_background()

    def lower_to_bottom(self, element):

        Canvas.lower_to_bottom(self, element)
        Canvas.lower_to_bottom(self, u'__background__')

    def show(self):

        t0 = self.experiment.clock.time()
        for e in self._elements.values():
            e.show()
        self.experiment.window.flip(clearBuffer=True)
        t1 = self.experiment.clock.time()
        if t1 - t0 > self.MAX_SHOW_DT:
            oslogger.warning('Canvas.show() took {0} ms'.format(t1 - t0))
        return t1

    def _set_background(self):

        if u'__background__' in self:
            del self['__background__']
        self['__background__'] = Rect(
            self.left, self.top, self.width, self.height,
            color=self.background_color.colorspec, fill=True
        )
        Canvas.lower_to_bottom(self, u'__background__')

    def __iter__(self):

        for name, stim in self._elements.items():
            if name == u'__background__':
                continue
            yield name, stim

    def __len__(self):

        return len(self._elements)-1

    @staticmethod
    def init_display(experiment):

        if not py3:
            from json_tricks import utils
            utils.get_arg_names = _get_arg_names

        global _experiment, _old_gamma
        _experiment = experiment
        # Set the PsychoPy monitor, default to testMonitor
        monitor = experiment.var.get(u'psychopy_monitor', u'testMonitor')
        waitblanking = experiment.var.get(u'psychopy_waitblanking', u'yes',
                                          [u'yes', u'no']) == u'yes'
        screen = experiment.var.get(u'psychopy_screen', 0)
        # Print some information to the debug window
        oslogger.info(u'waitblanking = %s' % waitblanking)
        oslogger.info(u'monitor = %s' % monitor)
        oslogger.info(u'screen = %s' % screen)
        # Initialize the PsychoPy window and set various functions
        experiment.window = visual.Window(
            experiment.resolution(),
            screen=screen,
            waitBlanking=waitblanking,
            fullscr=experiment.var.fullscreen == u'yes',
            monitor=monitor,
            units=u'pix',
            color=Color(experiment, experiment.var.background).backend_color,
            winType=u'pyglet',
            allowStencil=True
        )
        event.Mouse(visible=False, win=experiment.window)
        experiment.window.winHandle.set_caption(
            u'OpenSesame (PsychoPy backend)')
        # Set Gamma value if specified
        gamma = experiment.var.get(u'psychopy_gamma', u'unchanged')
        if type(gamma) in (int, float) and gamma > 0:
            _old_gamma = experiment.window.gamma
            experiment.window.setGamma(gamma)
        elif gamma != u'unchanged':
            raise osexception(
                u'Gamma should be a positive numeric value or "unchanged"')
        core.quit = _psychopy_clean_quit
        # Optionally change the logging level to avoid a lot of warnings in the
        # debug window
        if experiment.var.get(u'psychopy_suppress_warnings', u'yes'):
            logging.console.setLevel(logging.CRITICAL)

    @staticmethod
    def close_display(experiment):

        global _old_gamma
        # Restore display gamma if necessary
        if _old_gamma is not None:
            experiment.window.setGamma(_old_gamma)
        # This causes a (harmless) exception in some cases, so we catch it to
        # prevent confusion
        try:
            experiment.window.close()
        except:
            oslogger.error(
                u'An error occurred while closing the PsychoPy window.',
            )


def _get_arg_names(callable):
    """A hack to make json_tricks work on Python 2, after some unknown module
    has injected getfullargspec into inspect.
    """

    from functools import partial
    from logging import warn
    from sys import version_info
    from inspect import getargspec

    if type(callable) == partial and version_info[0] == 2:
        if not hasattr(get_arg_names, '__warned_partial_argspec'):
            get_arg_names.__warned_partial_argspec = True
            warn("'functools.partial' and 'inspect.getargspec' are not compatible in this Python version; "
                 "ignoring the 'partial' wrapper when inspecting arguments of {}, which can lead to problems".format(callable))
        return set(getargspec(callable.func).args)
    argspec = getargspec(callable)
    return set(argspec.args)


def _psychopy_clean_quit():
    """
    desc:
            When PsychoPy encounters an error, it does a sys.exit() which is not
            what we want, because it closes OpenSesame altogether. Instead, we
            nicely inform the user that PsychoPy has signalled an error.
    """

    raise osexception(
        u'PsychoPy encountered an error and aborted the program. See the debug window for PsychoPy error messages.')


# Non PEP-8 alias for backwards compatibility
psycho = Psycho
