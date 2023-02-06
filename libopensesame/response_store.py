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


class ResponseInfo:

    r"""A single response."""
    def __init__(self, response_store, response=None, correct=None,
                 response_time=None, item=None, feedback=True):

        self._response_store = response_store

        # Sanity checks
        if not isinstance(response_time, (int, float)) and \
                response_time is not None:
            raise osexception(u'response should be a numeric value or None')
        if response_time is None:
            self.response_time = None
        else:
            self.response_time = float(response_time)
        self.response = response
        self.item = item
        self.feedback = feedback
        if correct not in (0, 1, True, False, None):
            raise osexception(
                u'correct should be 0, 1, True, False, or None')
        if correct is None:
            self.correct = None
        else:
            self.correct = int(correct)

    def match(self, **kwdict):

        for key, val in kwdict.items():
            if getattr(self, key) != val:
                return False
        return True

    def matchnot(self, **kwdict):

        for key, val in kwdict.items():
            if getattr(self, key) == val:
                return False
        return True

    def __str__(self):

        return u'response(response=%s,response_time=%s,correct=%s,item=%s,feedback=%s)' \
            % (self.response, self.response_time, self.correct, self.item,
               self.feedback)


class ResponseStore:

    r"""The `responses` object contains the history of the responses that were
    collected during the experiment.

    A `responses` object is created
    automatically when the experiment starts.

    In addition to the functions
    listed below, the following semantics are
    supported:

    __Example__:

    ~~~
    .python
    # Loop through all responses, where last-given responses come first
    # Each response has correct, response, response_time, item, and feedback
    #
    attributes.
    for response in responses:
            print(response.correct)
    #
    Print the two last-given respones
    print('last_two responses:')
    print(responses[:2])
    ~~~

    [TOC]
    """
    def __init__(self, experiment):
        r"""Constructor.

        Parameters
        ----------
        experiment : experiment.
            The experiment object.
        """
        self._experiment = experiment
        self._responses = []
        self._feedback_from = 0

    @property
    def acc(self):
        r"""The percentage of correct responses for all responses that are
        included in feedback. If there are no responses to give feedback on,
        'undefined' is returned.

        Examples
        --------
        >>> print('The accuracy was %s%%' % responses.acc)
        """
        l = self._select(feedback=True)._selectnot(correct=None).correct
        if not l:
            return u'undefined'
        return 100.*sum(l)/len(l)

    @property
    def avg_rt(self):
        r"""The average response time for all responses that are included in
        feedback. If there are no responses to give feedback on, 'undefined' is
        returned.

        Examples
        --------
        >>> print('The average RT was %s ms' % responses.avg_rt)
        """
        l = self._select(feedback=True)._selectnot(response_time=None) \
                .response_time
        if not l:
            return u'undefined'
        return 1.*sum(l)/len(l)

    @property
    def response(self):
        r"""A list of all response values. (I.e. not response objects, but
        actual response keys, buttons, etc.)

        Examples
        --------
        >>> for response in responses.response:
        >>>         print(response)
        """
        return [r.response for r in self._responses]

    @property
    def correct(self):
        r"""A list of all correct (0, 1, or None) values.

        Examples
        --------
        >>> for correct in responses.correct:
        >>>         print(correct)
        """
        return [r.correct for r in self._responses]

    @property
    def response_time(self):
        r"""A list of all response times (float or None).

        Examples
        --------
        >>> for rt in responses.response_time:
        >>>         print(rt)
        """
        return [r.response_time for r in self._responses]

    @property
    def item(self):
        r"""A list of all item names (str or None) associated with each
        response.

        Examples
        --------
        >>> for item in responses.item:
        >>>         print(item)
        """
        return [r.item for r in self._responses]

    @property
    def feedback(self):
        r"""A list of the feedback status (True or False) associated with each
        response.

        Examples
        --------
        >>> for feedback in responses.feedback:
        >>>         print(feedback)
        """
        return [r.feedback for r in self._responses]

    @property
    def var(self):

        return self._experiment.var

    def add(self, response=None, correct=None, response_time=None, item=None,
            feedback=True):
        r"""Adds a response.

        Parameters
        ----------
        response    The response value, for example, 'space' for the spacebar, 0 for
            joystick button 0, etc.
        correct : bool, int, None, optional
            The correctness of the response.
        response_time : float, int, None, optional
            The response_time.
        item : str, None, optional
            The item that collected the response.
        feedback : bool, optional
            Indicates whether the response should be included in feedback on
            accuracy and average response time.

        Examples
        --------
        >>> responses.add(response_time=500, correct=1, response='left')
        """
        r = ResponseInfo(self, response=response, correct=correct,
                         response_time=response_time, item=item, feedback=feedback)
        if correct is None:
            correct = u'undefined'
        else:
            correct = r.correct
        self._responses.insert(0, r)
        self.var.response = self._experiment.syntax.sanitize(r.response)
        self.var.response_time = r.response_time
        self.var.correct = correct
        if item is not None:
            self.var.set(u'response_%s' % item,
                         self._experiment.syntax.sanitize(r.response))
            self.var.set(u'response_time_%s' % item, r.response_time)
            self.var.set(u'correct_%s' % item, correct)
        self.var.acc = self.var.accuracy = self.acc
        self.var.avg_rt = self.avg_rt
        # Old variables, mostly for backwards compatibility
        rs = self._select(feedback=True)
        self.var.accuracy = self.var.acc
        self.var.average_response_time = self.var.avg_rt
        self.var.total_response_time = sum(
            rs._selectnot(response_time=None).response_time)
        self.var.total_responses = len(rs)
        self.var.total_correct = len(rs._select(correct=1))

    def clear(self):
        r"""Clears all responses.

        Examples
        --------
        >>> responses.clear()
        """
        self._responses = []

    def reset_feedback(self):
        r"""Sets the feedback status of all responses to False, so that only
        new responses will be included in feedback.

        Examples
        --------
        >>> responses.reset_feedback()
        """
        for r in self._responses:
            r.feedback = False

    def _select(self, **kwdict):

        rs = ResponseStore(self._experiment)
        for r in self._responses:
            if r.match(**kwdict):
                rs._responses.append(r)
        return rs

    def _selectnot(self, **kwdict):

        rs = ResponseStore(self._experiment)
        for r in self._responses:
            if r.matchnot(**kwdict):
                rs._responses.append(r)
        return rs

    def __len__(self):

        return len(self._responses)

    def __getitem__(self, key):

        if isinstance(key, slice):
            rs = ResponseStore(self._experiment)
            rs._responses = self._responses[key]
            return rs
        if isinstance(key, int):
            return self._responses[key]
        raise TypeError(u'A key for responses should be either slice or int')

    def __str__(self):

        s = u'%d responses (last response is shown first):\n' % len(self)
        for i, r in enumerate(self):
            s += '%d: %s\n' % (i, r)
        return s

    def __iter__(self):

        for r in self._responses:
            yield r


# Alias for backwards compatibility
response_info = ResponseInfo
response_store = ResponseStore
