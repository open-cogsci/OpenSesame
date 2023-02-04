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
import warnings


class Keyboard(Backend):

    """
    desc: |
            The `Keyboard` class is used to collect keyboard responses. You
            generally create a `Keyboard` object with the `Keyboard()` factory
            function, as described in the section
            [Creating a Keyboard](#creating-a-keyboard).

            __Example:__

            ~~~ .python
            # Wait for a 'z' or 'x' key with a timeout of 3000 ms
            my_keyboard = Keyboard(keylist=['z', 'x'], timeout=3000)
            start_time = clock.time()
            key, end_time = my_keyboard.get_key()
            var.response = key
            var.response_time = end_time - start_time
            ~~~

            [TOC]

            ## Things to know

            ### Creating a Keyboard

            You generally create a `Keyboard` with the `Keyboard()` factory function:

            ~~~ .python
            my_keyboard = Keyboard()
            ~~~

            Optionally, you can pass [Response keywords](#response-keywords) to
            `Keyboard()` to set the default behavior:

            ~~~ .python
            my_keyboard = Keyboard(timeout=2000)
            ~~~

            ### Key names

            - Key names may differ between backends.
            - Keys can be identified either by character or name, and are
              case-insentive. For example:
              - The key 'a' is represented by 'a' and 'A'
              - The up arrow is represented by 'up' and 'UP'
              - The '/' key is represented by '/', 'slash', and 'SLASH'
              - The spacebar is represented by 'space' and 'SPACE'
            - To find out the name of key, you can:
              - Click on the 'list available keys' button of the
                KEYBOARD_RESPONSE item.
              - Collect a key press with a KEYBOARD_RESPONSE item, and display
                the key name through a FEEDBACK item with the text 'You
                pressed [response]' in it.

            ### Response keywords

            Functions that accept `**resp_args` take the following keyword
            arguments:

            - `timeout` specifies a timeout value in milliseconds, or is set to
              `None` to disable the timeout.
            - `keylist` specifies a list of keys that are accepted, or is set to
              `None` accept all keys.

            ~~~ .python
            # Get a left or right arrow press with a timeout of 3000 ms
            my_keyboard = Keyboard()
            key, time = my_keyboard.get_key(keylist=[u'left', u'right'],
                    timeout=3000)
            ~~~

            Response keywords only affect the current operation (except when passed
            to [keyboard.\_\_init\_\_][__init__]). To change the behavior for all
            subsequent operations, set the response properties directly:

            ~~~ .python
            # Get two key A or B presses with a 5000 ms timeout
            my_keyboard = Keyboard()
            my_keyboard.keylist = [u'a', u'b']
            my_keyboard.timeout = 5000
            key1, time1 = my_keyboard.get_key()
            key2, time2 = my_keyboard.get_key()
            ~~~

            Or pass the response options to [keyboard.\_\_init\_\_][__init__]:

            ~~~ .python
            # Get two key A or B presses with a 5000 ms timeout
            my_keyboard = Keyboard(keylist=[u'a', u'b'], timeout=5000)
            key1, time1 = my_keyboard.get_key()
            key2, time2 = my_keyboard.get_key()
            ~~~
    """

    def __init__(self, experiment, **resp_args):
        """
        visible: False

        desc: |
                Constructor to create a new `Keyboard` object. You do not generally
                call this constructor directly, but use the `Keyboard()` function,
                which is described here: [/python/common/]().

        arguments:
                experiment:
                        desc:		The experiment object.
                        type:		experiment

        keyword-dict:
                resp_args:
                        Optional [response keywords](#response-keywords) (`timeout`
                        and `keylist`) that will be used as the default for this
                        `Keyboard` object.

        example: |
                my_keyboard = Keyboard(keylist=['z', 'm'], timeout=2000)
        """

        self.experiment = experiment
        Backend.__init__(self, configurables={
            u'timeout': self.assert_numeric_or_None,
            u'keylist': self.assert_list_or_None,
        }, **resp_args)

    def set_config(self, **cfg):

        # Create a new keylist that also contains synonyms
        if u'keylist' in cfg and isinstance(cfg[u'keylist'], list):
            keylist = list(cfg[u'keylist'])
            for key in keylist:
                keylist += [key for key in self.synonyms(key)
                            if key not in keylist]
            cfg[u'keylist'] = keylist
        Backend.set_config(self, **cfg)

    def default_config(self):

        return {
            u'timeout': None,
            u'keylist': None,
        }

    @configurable
    def get_key(self, **resp_args):
        """
        desc:
                Collects a single key press.

        keyword-dict:
                resp_args:
                        Optional [response keywords](#response-keywords) (`timeout
                        and `keylist`) that will be used for this call to
                        `Keyboard.get_key()`. This does not affect subsequent
                        operations.

        returns:
                desc:		A `(key, timestamp)` tuple. `key` is None if a timeout
                                        occurs.
                type:		tuple

        example: |
                my_keyboard = Keyboard()
                response, timestamp = my_keyboard.get_key(timeout=5000)
                if response is None:
                        print(u'A timeout occurred!')
        """

        raise NotImplementedError()

    @configurable
    def get_key_release(self, **resp_args):
        """
        desc: |
                *New in v3.2.0*

                Collects a single key release.

                *Important:* This function currently assumes a QWERTY keyboard
                layout (unlike `Keyboard.get_key()`). This means that the returned
                `key` may be incorrect on non-QWERTY keyboard layouts. In addition,
                this function is not implemented for the *psycho* backend.

        keyword-dict:
                resp_args:
                        Optional [response keywords](#response-keywords) (`timeout`
                        and `keylist`) that will be used for this call to 
                        `Keyboard.get_key_release()`. This does not affect subsequent
                        operations.

        returns:
                desc:		A `(key, timestamp)` tuple. `key` is None if a timeout
                                        occurs.
                type:		tuple

        example: |
                my_keyboard = Keyboard()
                response, timestamp = my_keyboard.get_key_release(timeout=5000)
                if response is None:
                        print(u'A timeout occurred!')
        """

        raise NotImplementedError()

    def get_mods(self):
        """
        desc:
                Returns a list of keyboard moderators (e.g., shift, alt, etc.) that
                are currently pressed.

        returns:
                desc:	A list of keyboard moderators. An empty list is returned if
                                no moderators are pressed.
                type:	list

        example: |
                my_keyboard = Keyboard()
                moderators = my_keyboard.get_mods()
                if u'shift' in moderators:
                        print(u'The shift-key is down!')
        """

        raise NotImplementedError()

    def valid_keys(self):
        """
        desc:
                Tries to guess which key names are accepted by the back-end. For
                internal use.

        visible:
                False

        returns:
                desc:	A list of valid key names.
                type:	list
        """

        raise NotImplementedError()

    def synonyms(self, key):
        """
        desc:
                Gives a list of synonyms for a key, either codes or names. Synonyms
                include all variables as types and as Unicode strings
                (if applicable).

        visible:
                False

        returns:
                desc:	A list of synonyms
                type:	list
        """

        raise NotImplementedError()

    def flush(self):
        """
        desc:
                Clears all pending keyboard input, not limited to the keyboard.

        returns:
                desc:	True if a key had been pressed (i.e., if there was something
                                to flush) and False otherwise.
                type:	bool

        Example: |
                my_keyboard = Keyboard()
                my_keyboard.flush()
                response, timestamp = my_keyboard.get_key()
        """

        raise NotImplementedError()

    def show_virtual_keyboard(self, visible=True):
        """
        desc: |
                Shows or hides a virtual keyboard if this is supported by the
                back-end. This function is only necessary if you want the virtual
                keyboard to remain visible while collecting multicharacter
                responses. Otherwise, `Keyboard.get_key()` will implicitly show and
                hide the keyboard for a single-character response.

                This function does nothing for back-ends that do not support virtual
                keyboards.

        keywords:
                visible:
                        desc:	True if the keyboard should be shown, False otherwise.
                        type:	bool

        example: |
                my_keyboard = Keyboard()
                my_keyboard.show_virtual_keyboard(True)
                response1, timestamp2 = my_keyboard.get_key()
                response2, timestamp2 = my_keyboard.get_key()
                my_keyboard.show_virtual_keyboard(False)
        """

        pass

    def _keycode_to_str(self, keycode):
        """visible:	False"""

        raise NotImplementedError()

    # Deprecated functions

    def to_chr(self, key):
        """
        visible:	False
        desc:		deprecated
        """

        warnings.warn(u'keyboard.to_chr() has been deprecated.',
                      DeprecationWarning)
        return key

    def set_keylist(self, keylist=None):
        """
        visible:	False
        desc:		deprecated
        """

        warnings.warn(u'keyboard.set_keylist() has been deprecated. '
                      'Use keyboard.keylist instead.', DeprecationWarning)
        self.keylist = keylist

    def set_timeout(self, timeout=None):
        """
        visible:	False
        desc:		deprecated
        """

        warnings.warn(u'keyboard.set_timeout() has been deprecated. '
                      'Use keyboard.timeout instead.', DeprecationWarning)
        self.timeout = timeout


# Non PEP-8 alias for backwards compatibility
keyboard = Keyboard
