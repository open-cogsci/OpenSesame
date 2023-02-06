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


class basejoystick:

    r"""If you insert the JOYSTICK plugin at the start of your experiment, a
    JOYSTICK object automatically becomes part of the experiment object
    and can
    be used within an inline_script item as JOYSTICK.

    %--
    constant:
    arg_joybuttonlist: |
                    A list of buttons that are accepted or
    `None` to accept all
                    buttons.
            arg_timeout: |
    A timeout value in milliseconds or `None` for no timeout.
    --%

    [TOC]
    """
    def __init__(self, experiment, device=0, joybuttonlist=None, timeout=None):
        r"""Intializes the joystick object.

        Parameters
        ----------
        experiment : experiment
            An Opensesame experiment.
        device : int, optional
            The joystick device number.
        joybuttonlist : list, NoneType, optional
            %arg_joybuttonlist
        timeout : int, float, NoneType, optional
            %arg_timeout
        """
        raise NotImplementedError()

    def set_joybuttonlist(self, joybuttonlist=None):
        r"""Sets a list of accepted buttons.

        Parameters
        ----------
        joybuttonlist : list, NoneType, optional
            %arg_joybuttonlist
        """
        if joybuttonlist is None or joybuttonlist == []:
            self._joybuttonlist = None
        else:
            self._joybuttonlist = []
            for joybutton in joybuttonlist:
                self._joybuttonlist.append(joybutton)

    def set_timeout(self, timeout=None):
        r"""Sets a timeout.

        Parameters
        ----------
        timeout : int, float, NoneType, optional
            %arg_timeout
        """
        self.timeout = timeout

    def get_joybutton(self, joybuttonlist=None, timeout=None):
        r"""Collects joystick button input.

        Parameters
        ----------
        joybuttonlist : list, NoneType, optional
            A list of buttons that are accepted or `None` to default
            joybuttonlist.
        timeout : int, float, NoneType, optional
            A timeout value in milliseconds or `None` to use default timeout.

        Returns
        -------
        tuple
            A (joybutton, timestamp) tuple. The joybutton is `None` if a
            timeout occurs.
        """
        raise NotImplementedError()

    def get_joyaxes(self, timeout=None):
        r"""Waits for joystick axes movement.

        Parameters
        ----------
        timeout : int, float, NoneType, optional
            A timeout value in milliseconds or `None` to use default timeout.

        Returns
        -------
        tuple
            A `(position, timestamp)` tuple. `position` is `None` if a timeout
            occurs. Otherwise, `position` is an `(x, y, z)` tuple.
        """
        raise NotImplementedError()

    def get_joyballs(self, timeout=None):
        r"""Waits for joystick trackball movement.

        Parameters
        ----------
        timeout : int, float, NoneType, optional
            A timeout value in milliseconds or `None` to use default timeout.

        Returns
        -------
        tuple
            A `(position, timestamp)` tuple. The position is `None` if a
            timeout occurs.
        """
        raise NotImplementedError()

    def get_joyhats(self, timeout=None):
        r"""Waits for joystick hat movement.

        Parameters
        ----------
        timeout : int, float, NoneType, optional
            A timeout value in milliseconds or `None` to use default timeout.

        Returns
        -------
        tuple
            A `(position, timestamp)` tuple. `position` is `None` if a timeout
            occurs. Otherwise, `position` is an `(x, y)` tuple.
        """
        raise NotImplementedError()

    def get_joyinput(self, joybuttonlist=None, timeout=None):
        r"""Waits for any joystick input (buttons, axes, hats or balls).

        Parameters
        ----------
        joybuttonlist : list, NoneType, optional
            A list of buttons that are accepted or `None` to default
            joybuttonlist.
        timeout : int, float, NoneType, optional
            A timeout value in milliseconds or `None` to use default timeout.

        Returns
        -------
        tuple
            A (event, value, timestamp) tuple. The value is `None` if a timeout
            occurs. `event` is one of `None`, 'joybuttonpress',
            'joyballmotion', 'joyaxismotion', or 'joyhatmotion'
        """
        raise NotImplementedError()

    def input_options(self):
        r"""Generates a list with the number of available buttons, axes, balls
        and hats.

        Returns
        -------
        list
            A list with number of inputs as: [buttons, axes, balls,
            hats].
        """
        raise NotImplementedError()

    def flush(self):
        r"""Clears all pending input, not limited to the joystick.

        Returns
        -------
        bool
            True if joyinput was pending (i.e., if there was something to
            flush) and False otherwise.
        """
        raise NotImplementedError()
