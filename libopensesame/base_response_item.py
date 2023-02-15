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
from libopensesame.item import Item
from libopensesame.exceptions import InvalidValue


class BaseResponseItem(Item):
    r"""The base class for items that collect responses, such as
    keyboard_response, mouse_response, joystick, etc.
    """
    
    # Override as True for objects that should be included in feedback
    process_feedback = False

    def prepare_response_func(self):
        r"""Should return a function that, when called, returns a (response,
        timestamp) tuple. This function needs to be implemented in every
        response item.

        Returns
        -------
        FunctionType
        """
        raise NotImplementedError()

    def validate_response(self, response):
        r"""Optionally checks whether a response is valid for this item. This
        can be used to check whether the list of allowed responses is valid.

        Parameters
        ----------
        response
            The response to check.

        Returns
        -------
        bool
            True if response is valid, False otherwise.
        """
        return True

    def response_matches(self, test, ref):
        r"""Checks whether two responses are the same. This can be re-
        implemented to take synonyms into account.

        Parameters
        ----------
        test
            The first response.
        ref
            The second response.

        Returns
        -------
        bool
            True if the responses match, False otherwise.
        """
        return test in ref

    def process_response(self, response_args):
        r"""Processes a collected responses, so that it is added to the
        response_store, etc.

        Parameters
        ----------
        response_args : tuple
            The return value of the function created by
            prepare_response_func().
        """
        response, t1 = response_args
        if self._correct_responses is not None:
            correct = self.response_matches(response, self._correct_responses)
        else:
            correct = None
        self.responses.add(
            response=response, response_time=t1-self._t0, correct=correct,
            item=self.name, feedback=self.process_feedback
        )

    def prepare(self):
        """See item."""
        super().prepare()
        self._timeout = self._prepare_timeout()
        self._allowed_responses = self._prepare_responses(u'allowed_responses')
        self._correct_responses = self._prepare_responses(u'correct_response')
        self._collect_response = self.prepare_response_func()
        self._t0 = None

    def run(self):
        """See item."""
        super().run()
        if self._t0 is None:
            self._t0 = self.set_item_onset()
        retval = self._collect_response()
        if retval is None:
            return
        self.process_response(retval)

    def var_info(self):
        """See item."""
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
        return super().var_info() + l

    # Private functions

    def _prepare_timeout(self):
        r"""Processes the timeout variable, and checks whether it is valid.

        Returns
        -------
        float
            A timeout value.
        """
        timeout = self.var.get(u'timeout', default=u'infinite')
        if timeout == u'infinite':
            return
        try:
            timeout = int(timeout)
            assert(timeout >= 0)
        except Exception:
            raise InvalidValue(f'"{timeout}" is not a valid timeout. '
                               f'Expecting a positive integer or "infinite".')
        return timeout

    def _prepare_responses(self, var):
        r"""Parses a semicolon-separated list of responses into a list of
        responses or None if no responses are provided.

        Parameters
        ----------
        var : str
            The name of the variable that contains the responses.

        Returns
        -------
        NoneType, list
        """
        responses = safe_decode(self.var.get(var, default=u''))
        if responses == u'':
            return
        responses = [r.strip() for r in responses.split(';')]
        for r in responses:
            if not self.validate_response(r):
                raise InvalidValue(f'Invalid value in {var}: {r}')
        # If allowed responses are provided, the list should not be empty
        if not responses:
            raise InvalidValue(f'{var} should not be an empty list')
        return responses

    def _prepare_sleep_func(self, duration):
        r"""Creates a function that sleeps for a specific duration.

        Parameters
        ----------
        duration : int, float
            The duration to sleep for.

        Returns
        -------
        FunctionType
            A sleep function with a fixed duration.
        """
        if duration == 0:
            return lambda: None
        if self.var.duration > 0:
            return lambda: self.clock.sleep(self.var.duration)
        raise InvalidValue('Duration should not be negative')


# Alias for backwards compatibility
base_response_item = BaseResponseItem
