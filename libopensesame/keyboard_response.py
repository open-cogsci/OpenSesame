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
from libopensesame.base_response_item import BaseResponseItem
from openexp.keyboard import Keyboard


class KeyboardResponseMixin(object):

    """
    desc:
            A mixin class that should be inherited along with base_response_item
            by all classes that want to collect keyboard responses.
    """

    def prepare_response_func(self):
        """See base_response_item."""

        self._keyboard = Keyboard(self.experiment, timeout=self._timeout,
                                  keylist=self._allowed_responses)
        if self.var.get(u'event_type', default=u'keypress') == u'keypress':
            return self._keyboard.get_key
        if self.var.event_type == u'keyrelease':
            return self._keyboard.get_key_release
        raise osexception(u'event_type should be "keypress" or "keyrelease"')


class KeyboardResponse(KeyboardResponseMixin, BaseResponseItem):

    """
    desc:
            An item for collecting keyboard responses.
    """

    description = u'Collects keyboard responses'
    process_feedback = True

    def reset(self):
        """See item."""

        self.var.flush = u'yes'
        self.var.timeout = u'infinite'
        self.var.duration = u'keypress'
        self.var.event_type = u'keypress'
        self.var.unset(u'allowed_responses')
        self.var.unset(u'correct_response')

    def prepare(self):
        """See item."""

        super().prepare()
        self._flush = self.var.flush == u'yes'

    def response_matches(self, test, ref):
        """See base_response_item."""

        return any(safe_decode(r) in self._keyboard.synonyms(test) for r in ref)

    def run(self):
        """See item."""

        if self._flush:
            self._keyboard.flush()
        super().run()

    def coroutine(self):
        """See coroutines plug-in."""

        self._keyboard.timeout = 0
        alive = True
        yield
        self._t0 = self.set_item_onset()
        if self._flush:
            self._keyboard.flush()
        while alive:
            key, time = self._keyboard.get_key()
            if key is not None:
                break
            alive = yield
        self.process_response((key, time))


# Alias for backwards compatibility
keyboard_response = KeyboardResponse
keyboard_response_mixin = KeyboardResponseMixin
