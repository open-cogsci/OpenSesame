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
from libopensesame.exceptions import InvalidValue


def float_list(l, desc, min_len=None, max_len=None):
    """Converts a variable to a list of floats if possible.

    Parameters
    ----------
    l
        The variable to convert.
    desc
        A description to clarify the osexception.
    min_len, optional
        The minimum length of the list.
    max_len, optional
        The maximum length of the list.

    Raises
    ------
    InvalidValue
        If the variable could not be converted.

    Returns
    -------
    list of float
    """
    try:
        l = list(l)
    except:
        raise InvalidValue(
            f'Expecting a list or similar type not {l} for {desc}')
    if min_len is not None and len(l) < min_len:
        raise InvalidValue(
            f'Expecting a list of at least {min_len} items for {desc}')
    if max_len is not None and len(l) > max_len:
        raise InvalidValue(
            f'Expecting a list of at most {max_len} items for {desc}')
    return l
