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
from libopensesame.exceptions import osexception
from libopensesame.oslogging import oslogger
import serial
import os


class libsrbox:

    r"""If you insert the srbox plugin at the start of your experiment, an
    instance of SRBOX automatically becomes part of the experiment
    object and
    can be accessed within an inline_script item as SRBOX.

    __Important note
    1:__

    If you do not specify a device, the plug-in will try to autodetect
    the
    SR Box port. However, on some systems this freezes the experiment, so
    it is better to explicitly specify a device.

    __Important note 2:__

    You
    need to call [srbox.start] to put the SR Box in sending mode,
    before
    calling [srbox.get_button_press] to collect a button press.

    __Example:__
    ~~~ .python
    t0 = clock.time()
    srbox.start()
    button, t1 =
    srbox.get_button_press(allowed_buttons=[1,2],
    require_state_change=True)
    if button == 1:
            response_time = t1 - t0
    print('Button 1 was pressed in %d ms!' % response_time)
    srbox.stop()
    ~~~
    [TOC]
    """
    # The PST sr box only supports five buttons, but some of the VU boxes use
    # higher button numbers
    BUTTON1 = int('11111110', 2)
    BUTTON2 = int('11111101', 2)
    BUTTON3 = int('11111011', 2)
    BUTTON4 = int('11110111', 2)
    BUTTON5 = int('11101111', 2)
    BUTTON6 = int('11011111', 2)
    BUTTON7 = int('10111111', 2)
    BUTTON8 = int('01111111', 2)
    BYTEMASKS = [
        BUTTON1,
        BUTTON2,
        BUTTON3,
        BUTTON4,
        BUTTON5,
        BUTTON6,
        BUTTON7,
        BUTTON8
    ]

    def __init__(self, experiment, dev=None):
        r"""Constructor. An SRBOX object is created automatically by the SRBOX
        plug-in, and you do not generally need to call the constructor
        yourself.

        Parameters
        ----------
        experiment : experiment
            An Opensesame experiment.
        """
        self.experiment = experiment
        self._srbox = None
        self._started = False

        # If a device has been specified, use it
        if dev not in (None, "", "autodetect"):
            try:
                self._srbox = serial.Serial(dev, timeout=0, baudrate=19200)
            except Exception as e:
                raise osexception(
                    "Failed to open device port '%s' in libsrbox: '%s'"
                    % (dev, e)
                )

        else:
            # Else determine the common name of the serial devices on the
            # platform and find the first accessible device. On Windows,
            # devices are labeled COM[X], on Linux there are labeled /dev/tty[X]
            if os.name == "nt":
                for i in range(1, 256):
                    try:
                        dev = "COM%d" % i
                        self._srbox = serial.Serial(
                            dev,
                            timeout=0,
                            baudrate=19200
                        )
                        break
                    except Exception as e:
                        self._srbox = None
                        pass
            elif os.name == "posix":
                for path in os.listdir("/dev"):
                    if path[:3] == "tty":
                        try:
                            dev = "/dev/%s" % path
                            self._srbox = serial.Serial(
                                dev,
                                timeout=0,
                                baudrate=19200
                            )
                            break
                        except Exception as e:
                            self._srbox = None
                            pass
            else:
                raise osexception(
                    u"libsrbox does not know how to auto-detect the SR Box on "
                    u"your platform. Please specify a device."
                )
        if self._srbox is None:
            raise osexception(
                u"libsrbox failed to auto-detect an SR Box. Please specify a "
                u"device."
            )
        oslogger.debug("using device %s" % dev)
        # Turn off all lights
        if self._srbox is not None:
            self._srbox.write(b'\x60')

    def send(self, ch):
        r"""Sends a single character to the SR Box. Send '\x60' to turn off all
        lights, '\x61' for light 1 on, '\x62' for light 2 on,'\x63' for lights
        1 and 2 on etc.

        Parameters
        ----------
        ch : str
            The character to send.
        """
        self._srbox.write(ch)

    def start(self):
        r"""Turns on sending mode, so that the SR Box starts to send output.
        The SR Box must be in sending mode when you call
        [srbox.get_button_press].
        """
        if self._started:
            return
        # Write the start byte
        self._srbox.flushOutput()
        self._srbox.flushInput()
        self._srbox.write(b'\xA0')
        self._started = True

    def stop(self):
        r"""Turns off sending mode, so that the SR Box stops giving output."""
        if not self._started:
            return
        # Write the stop byte and flush the input
        self._srbox.flushOutput()
        self._srbox.flushInput()
        self._srbox.write(b'\x20')
        self._started = False

    def get_button_press(
            self,
            allowed_buttons=None,
            timeout=None,
            require_state_change=False
    ):
        r"""Collects a button press from the SR box.

        Parameters
        ----------
        allowed_buttons : list, NoneType, optional
            A list of buttons that are accepted or `None` to accept all
            buttons. Valid buttons are integers 1 through 8.
        timeout : int, float, NoneType, optional
            A timeout value in milliseconds or `None` for no timeout.
        require_state_change    Indicates whether already pressed button should be accepted
            (False), or whether only a state change from unpressed to pressed
            is accepted (True).

        Returns
        -------
        tuple
            A button_list, timestamp tuple. button_list is None if no button
            was pressed (i.e. a timeout occurred).
        """
        if not self._started:
            raise osexception(
                u'Please call srbox.start() before srbox.get_button_press()')
        t0 = self.experiment.time()
        # Create a list of buttonr, bytemask tuples.
        bytemasks = []
        for buttonnr, bytemask in enumerate(self.BYTEMASKS):
            if allowed_buttons is None or buttonnr + 1 in allowed_buttons:
                bytemasks.append((buttonnr + 1, bytemask))
        inputbyte0 = None
        while True:
            # Get a valid character and convert it to a byte
            inputchar = self._srbox.read(1)
            if inputchar == b'':
                continue
            inputbyte1 = ord(inputchar)
            # Check for a timeout
            t1 = self.experiment.time()
            if timeout is not None and t1 - t0 > timeout:
                break
            # To check for state changes, we need an old and a new state.
            # Therefore, on the first loop we don't do anything.
            if require_state_change and inputbyte0 is None:
                inputbyte0 = inputbyte1
                continue
            # Ignore no responses
            if not inputbyte1:
                inputbyte0 = inputbyte1
                continue
            if require_state_change:
                # If a state change is required, a button should be pressed now
                # but not before. Because there is only one state change at a
                # time, we can return right away.
                for buttonnr, bytemask in bytemasks:
                    if (
                            inputbyte1 | bytemask == 255 and
                            inputbyte0 | bytemask != 255
                    ):
                        return [buttonnr], t1
            else:
                # If no state change is required, only consider the last input
                # and create a list of all buttons that are pressed.
                button_list = []
                for button_nr, bytemask in bytemasks:
                    if inputbyte1 | bytemask == 255:
                        button_list.append(button_nr)
                if button_list:
                    return button_list, t1
            inputbyte0 = inputbyte1
        return None, t1

    def close(self):
        r"""Closes the connection to the srbox. This is done automatically by
        the SRBOX plugin when the experiment finishes.
        """
        self._srbox.close()
        self._started = False
