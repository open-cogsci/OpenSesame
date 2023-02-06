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


def float_list(l, desc, min_len=None, max_len=None):
    """
    Converts a variable to a list of floats if possible.

    Arguments:
    a		--	The variable to convert.
    desc	--	A description to clarify the osexception.

    Keyword arguments:
    min_len	--	The minimum length of the list. (default=None)
    max_len	--	The maximum length of the list. (default=None)

    Raises:
    A osexception if the variable could not be converted.

    Returns:
    A list of floats.
    """
    try:
        l = list(l)
    except:
        raise osexception(
            u'Expecting a list or compatible type not "%s" for "%s"' % (l,
                                                                        desc))
    if min_len is not None and len(l) < min_len:
        raise osexception(
            u'Expecting a list of at least %d items for "%s"' % (min_len, desc))
    if max_len is not None and len(l) > max_len:
        raise osexception(
            u'Expecting a list of at most %d items for "%s"' % (max_len, desc))
    return l
