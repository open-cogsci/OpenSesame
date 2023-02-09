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
from libopensesame.oslogging import oslogger
from libopensesame.base_response_item import BaseResponseItem
from openexp.keyboard import Keyboard
from .libsrbox import LibSrbox


class Srbox(BaseResponseItem):

    process_feedback = True

    def reset(self):
        self.var.timeout = u'infinite'
        self.var.lights = u''
        self.var.dev = u'autodetect'
        self.var._dummy = u'no'
        self.var.require_state_change = u'no'

    def validate_response(self, response):
        try:
            response = int(response)
        except (ValueError, TypeError):
            return False
        return 0 <= response <= 255

    def process_response(self, response_args):
        response, t1 = response_args
        if isinstance(response, list):
            response = response[0]
        super().process_response((safe_decode(response), t1))

    def _get_button_press(self):
        r"""Calls srbox.get_button_press() with the correct arguments."""
        return self.experiment.srbox.get_button_press(
            allowed_buttons=self._allowed_responses,
            timeout=self._timeout,
            require_state_change=self._require_state_change
        )

    def prepare_response_func(self):
        self._keyboard = Keyboard(self.experiment,
                                  keylist=self._allowed_responses,
                                  timeout=self._timeout)
        if self.var._dummy == u'yes':
            return self._keyboard.get_key
        # Prepare the device string
        dev = self.var.dev
        if dev == u"autodetect":
            dev = None
        # Dynamically create an srbox instance
        if not hasattr(self.experiment, "srbox"):
            self.experiment.srbox = LibSrbox(self.experiment, dev)
            self.experiment.cleanup_functions.append(self.close)
            self.python_workspace[u'srbox'] = self.experiment.srbox
        # Prepare the light byte
        s = "010"  # Control string
        for i in range(5):
            if str(5 - i) in str(self.var.lights):
                s += "1"
            else:
                s += "0"
        self._lights = chr(int(s, 2))
        oslogger.debug(u"lights string set to %s (%s)" % (s, self.var.lights))
        if self._allowed_responses is not None:
            self._allowed_responses = [int(r) for r in self._allowed_responses]
        self._require_state_change = self.var.require_state_change == u'yes'
        return self._get_button_press

    def run(self):
        """See item."""
        self._keyboard.flush()
        if self.var._dummy != u'yes':
            self.experiment.srbox.start()
        super().run()
        if self.var._dummy != u'yes':
            self.experiment.srbox.stop()

    def close(self):
        r"""Neatly close the connection to the srbox."""
        if (
                not hasattr(self.experiment, "srbox") or
                self.experiment.srbox is None
        ):
            oslogger.debug("no active srbox")
            return
        try:
            self.experiment.srbox.close()
            self.experiment.srbox = None
            oslogger.debug("srbox closed")
        except Exception as e:
            oslogger.error("failed to close srbox")
