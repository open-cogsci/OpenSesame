# coding=utf-8

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


CHAR_TO_NAME = {
    u'`': u'grave',
    u'~': u'asciitilde',
    u'^': u'asciicircum',
    u'%': u'percent',
    u'!': u'exclamation',
    u'"': u'doublequote',
    u'#': u'hash',
    u'$': u'dollar',
    u'&': u'ampersand',
    u'\'': u'apostrophe',
    u'*': u'asterisk',
    u'+': u'plus',
    u',': u'comma',
    u'-': u'minus',
    u'.': u'period',
    u'/': u'slash',
    u':': u'colon',
    u';': u'semicolon',
    u'=': u'equal',
    u'?': u'question',
    u'@': u'at',
    u'\\': u'backslash',
    u'|': u'bar',
    u'<': u'less',
    u'>': u'greater',
    u'[': u'bracketleft',
    u']': u'bracketright',
    u'(': u'parenleft',
    u')': u'parenright',
    u'{': u'braceleft',
    u'}': u'braceright',
    u'_': u'underscore'
}
NAME_TO_CHAR = {name: char for char, name in CHAR_TO_NAME.items()}


class KeyBabel(object):

    """
    desc:
            Converts between different ways to represent keys through numeric
            values (keycodes), different names (strings), and None (for timeout).
    """

    def __init__(self, keyboard):
        """
        desc:
                Constructor.

        arguments:
                keybaord:	A Keyboard object
        """

        self._keyboard = keyboard

    def standard_name(self, key, shift=False):
        """
        desc:
                Gives the standard name for a key. This is the shortest name, so
                it corresponds to a character if a character is available.

        arguments:
                key:	The key to standardize.

        keywords:
                shift:	Indicates whether the name should be cast to uppercase
                                (True) or lowercase (False)

        returns:
                The standard name for the key.
        """

        short_name = (
            key
            if isinstance(key, basestring) and len(key) == 1
            else sorted(self.synonyms(key), key=len)[0]
        )
        return short_name.upper() if shift else short_name.lower()

    def synonyms(self, key):
        """
        desc:
                Gives a set of synonyms for a key.

        arguments:
                key:	The key to find synonyms for.

        returns:
                A set of synonyms.
        """

        if key is None:
            return self._none_synonyms()
        if isinstance(key, int):
            return self._keycode_synonyms(key)
        if isinstance(key, basestring):
            return self._str_synonyms(key)
        raise osexception(
            u'Key names should be string, numeric, or None, not %s'
            % type(key)
        )

    def _none_synonyms(self):

        return {None, 'None', 'none', 'NONE'}

    def _keycode_synonyms(self, key):

        keyname = self._keyboard._keycode_to_str(key)
        return {key, keyname.upper(), keyname.lower()}

    def _str_synonyms(self, key):

        key_lower = key.lower()
        synonyms = {key, key.upper(), key_lower}
        if key_lower in CHAR_TO_NAME:
            # Add 'exclamation' for '!'
            synonyms.add(CHAR_TO_NAME[key_lower])
        elif key_lower in NAME_TO_CHAR:
            # Add '!' for 'exclamation'
            synonyms.add(NAME_TO_CHAR[key_lower])
        # Add timeout as NoneType
        if key_lower == u'none':
            synonyms.add(None)
        return synonyms
