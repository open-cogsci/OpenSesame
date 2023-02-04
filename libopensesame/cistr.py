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
import operator


class CIStr(str):

    """
    desc:
        A class for case-insensitive string comparisons. This is used to speed
        up the item store, which gets a lot of look ups for item names. This is
        not a full emulation of the str protocol, only those parts that are used
        by the item store.
    """

    def __init__(self, s):

        if py3:
            str.__init__(s)
        else:
            str.__init__(self, s)
        self._lower = s.lower()
        self._hash = hash(self._lower)

    def __eq__(self, other):

        try:
            return other._hash == self._hash
        except AttributeError:
            if hasattr(other, u'lower'):
                return other.lower() == self._lower
        return other == self._lower

    def __ne__(self, other):

        try:
            return other._hash != self._hash
        except AttributeError:
            if hasattr(other, u'lower'):
                return other.lower() != self._lower
        return other != self._lower

    def __hash__(self):

        return self._hash


# Alias for backwards compatibility
cistr = CIStr
