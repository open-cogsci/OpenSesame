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
import random
import openexp.keyboard
import openexp.mouse
from libopensesame.oslogging import oslogger
from libopensesame.exceptions import osexception


class generic_response:

    """
    Deals with overlapping functionality for items that are able to process a
    reponse.
    """

    auto_response = u"a"
    process_feedback = False

    def prepare_timeout(self):
        """Prepare the response timeout"""

        # Set the timeout
        if self.var.get(u'timeout', default=u'infinite') == u'infinite':
            self._timeout = None
        else:
            try:
                self._timeout = int(self.var.timeout)
                assert(self._timeout >= 0)
            except:
                raise osexception(
                    u"'%s' is not a valid timeout in item '%s'. Expecting a positive integer or 'infinite'."
                    % (self.var.timeout, self.name))

    def auto_responder(self, dev=u'keyboard'):
        """
        Mimicks participant responses.

        Keyword arguments:
        dev		--	The device that should be simulated. (default=u'keyboard')

        Returns:
        A simulated (response_time, response) tuple
        """

        if self._timeout is None:
            self.sleep(random.randint(200, 1000))
        else:
            self.sleep(random.randint(min(self._timeout, 200), self._timeout))

        if self._allowed_responses is None:
            resp = self.auto_response
        else:
            resp = random.choice(self._allowed_responses)

        oslogger.debug(
            u"generic_response.auto_responder(): responding '%s'" % resp)
        if dev == u'mouse':
            pos = random.randint(0, self.var.width), random.randint(0,
                                                                    self.var.height)
            return resp, pos, self.time()
        return resp, self.time()

    def auto_responder_mouse(self):
        """An ugly hack to make auto-response work for mouse_response items."""

        return self.auto_responder(dev=u'mouse')

    def process_response_keypress(self, retval):
        """Process a keypress response"""

        self.experiment._start_response_interval = self.sri
        key, self.experiment.end_response_interval = retval
        self.experiment.var.response = self.syntax.sanitize(key)
        self.synonyms = self._keyboard.synonyms(self.experiment.var.response)

    def process_response_mouseclick(self, retval):
        """Process a mouseclick response"""

        self.experiment._start_response_interval = self.sri
        self.experiment.var.response, pos, self.experiment.end_response_interval = \
            retval
        self.synonyms = self._mouse.synonyms(self.experiment.var.response)
        if pos is not None:
            self.experiment.var.cursor_x = pos[0]
            self.experiment.var.cursor_y = pos[1]
        else:
            self.experiment.var.cursor_x = u'NA'
            self.experiment.var.cursor_y = u'NA'

    def process_response(self):
        """A generic method for handling response collection"""

        # Wait for a fixed duration
        retval = self._duration_func()
        self.synonyms = None

        # If the duration function did not give any kind of return value
        # there is no response to process
        if retval is None:
            return

        process_func = u"process_response_%s" % self.var.duration
        if hasattr(self, process_func):
            getattr(self, process_func)(retval)
        else:
            raise osexception(
                u"Don't know how to process responses for duration '%s' in item '%s'"
                % (self.var.duration, self.name))

        self.response_bookkeeping()

    def response_bookkeeping(self):
        """Do some bookkeeping for the response"""

        # The respone and response_time variables are always set, for every
        # response item
        self.experiment.var.set(u"response_time",
                                self.experiment.end_response_interval -
                                self.experiment._start_response_interval)
        self.experiment.var.set(u"response_%s" % self.name,
                                self.var.get(u"response"))
        self.experiment.var.set(u"response_time_%s" % self.name,
                                self.var.get(u"response_time"))
        self.experiment._start_response_interval = None

        # But correctness information is only set for dedicated response items,
        # such as keyboard_response items, because otherwise we might confound
        # the feedback
        if self.process_feedback:
            oslogger.debug(u"processing feedback for '%s'" % self.name)
            if u"correct_response" in self.var:
                # If a correct_response has been defined, we use it to determine
                # accuracy etc.
                correct_response = self.var.correct_response
                if hasattr(self, u"synonyms") and self.synonyms is not None:
                    if correct_response in self.synonyms or \
                            safe_decode(correct_response) in self.synonyms:
                        self.experiment.var.correct = 1
                        self.experiment.var.total_correct += 1
                    else:
                        self.experiment.var.correct = 0
                else:
                    if self.experiment.response in (correct_response,
                                                    safe_decode(correct_response)):
                        self.experiment.var.correct = 1
                        self.experiment.var.total_correct += 1
                    else:
                        self.experiment.var.correct = 0
            else:
                # If a correct_response hasn't been defined, we simply set
                # correct to undefined
                self.experiment.var.correct = u"undefined"
            # Do some response bookkeeping
            self.experiment.var.total_response_time += \
                self.experiment.var.response_time
            self.experiment.var.total_responses += 1
            self.experiment.var.accuracy = self.experiment.var.acc = \
                100.0 * self.experiment.var.total_correct / \
                self.experiment.var.total_responses
            self.experiment.var.average_response_time = \
                self.experiment.var.avg_rt = \
                self.experiment.var.total_response_time / \
                self.experiment.var.total_responses
            self.experiment.var.set(u"correct_%s" % self.name,
                                    self.var.correct)

    def set_sri(self, reset=False):
        """
        Sets the start of the response interval

        Keyword arguments:
        reset -- determines whether the start of the response interval should
                         be reset to the start of the current item (default=False)
        """

        if reset:
            self.sri = self.var.get(u"time_%s" % self.name)
            self.experiment._start_response_interval = self.var.get("time_%s" %
                                                                    self.name)

        if self.experiment._start_response_interval is None:
            self.sri = self.var.get(u"time_%s" % self.name)
        else:
            self.sri = self.experiment._start_response_interval

    def prepare_allowed_responses(self):
        """Prepare the allowed responses"""

        if self.var.get(u'allowed_responses', default=u'') == u'':
            self._allowed_responses = None
            return

        # Create a list of allowed responses that are separated by semicolons.
        # Also trim any whitespace.
        allowed_responses = [allowed_response.strip() for allowed_response in
                             safe_decode(self.var.allowed_responses).split(u";")]

        if self.var.duration == u"keypress":
            # For keypress responses, we don't check if the allowed responses
            # make sense.
            self._allowed_responses = allowed_responses

        elif self.var.duration == u"mouseclick":
            # For mouse clicks, we check whether allowed responses make sense
            self._allowed_responses = []
            for r in allowed_responses:
                if r in self.resp_codes.values():
                    for code, resp in self.resp_codes.items():
                        if resp == r:
                            self._allowed_responses.append(code)
                else:
                    try:
                        r = int(r)
                        if r in self.resp_codes:
                            self._allowed_responses.append(r)
                        else:
                            raise osexception(
                                u"Unknown allowed_response '%s' in mouse_response item '%s'"
                                % (r, self.name))
                    except Exception as e:
                        raise osexception(
                            u"Unknown allowed_response '%s' in mouse_response item '%s'"
                            % (r, self.name), exception=e)

        # If allowed responses are provided, the list should not be empty
        if len(self._allowed_responses) == 0:
            raise osexception(
                u"'%s' are not valid allowed responses in keyboard_response '%s'"
                % (self.var.get(u"allowed_responses"), self.name))

    def prepare_duration(self):
        """Prepare the duration"""

        if type(self.var.duration) == int:

            # Prepare a duration in milliseconds
            self._duration = int(self.var.duration)
            if self._duration == 0:
                self._duration_func = self.dummy
            else:
                self._duration_func = self.sleep_for_duration

        else:

            # Prepare a special duration, such as 'keypress', which are
            # handles by special functions
            prepare_func = u"prepare_duration_%s" % self.var.duration
            if hasattr(self, prepare_func):
                getattr(self, prepare_func)()
            else:
                raise osexception(
                    u"'%s' is not a valid duration in item '%s'" %
                    (self.var.duration, self.name))

    def prepare_duration_keypress(self):
        """Prepare a keypress duration"""

        self._keyboard = openexp.keyboard.keyboard(self.experiment)
        if self.experiment.auto_response:
            self._duration_func = self.auto_responder
        else:
            self._keyboard.set_config(timeout=self._timeout,
                                      keylist=self._allowed_responses)
            self._duration_func = self._keyboard.get_key

    def prepare_duration_mouseclick(self):
        """Prepare a mouseclick duration"""

        self._mouse = openexp.mouse.mouse(self.experiment)
        if self.experiment.auto_response:
            self._duration_func = self.auto_responder_mouse
        else:
            # Prepare mouseclick
            self._mouse.set_config(timeout=self._timeout,
                                   buttonlist=self._allowed_responses)
            self._duration_func = self._mouse.get_click

    def prepare(self):
        """A generic method for preparing a response item"""

        self.prepare_timeout()
        self.prepare_allowed_responses()
        self.prepare_duration()

    def sleep_for_duration(self):
        """Sleep for a specified time"""

        self.sleep(self._duration)

    def var_info(self):
        """
        Return a list of dictionaries with variable descriptions

        Returns:
        A list of (name, description) tuples
        """

        l = []
        l.append((u"response", u"[Depends on response]"))
        l.append((u"response_time", u"[Depends on response]"))
        l.append((u"response_%s" % self.name, u"[Depends on response]"))
        l.append(("response_time_%s" % self.name, u"[Depends on response]"))
        if self.process_feedback:
            l.append((u"correct", u"[Depends on response]"))
            l.append((u"correct_%s" % self.name, u"[Depends on response]"))
            l.append((u"average_response_time", u"[Depends on response]"))
            l.append((u"avg_rt", u"[Depends on response]"))
            l.append((u"accuracy", u"[Depends on response]"))
            l.append((u"acc", u"[Depends on response]"))
        return l
