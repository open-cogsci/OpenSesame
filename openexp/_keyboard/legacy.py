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
import platform
import pygame
from pygame.locals import *
from string import whitespace
from libopensesame.exceptions import osexception
from openexp._keyboard.keyboard import Keyboard
from openexp.backend import configurable

# Whitespace, backspace, and empty strings are not acceptable names for keys.
# These should be converted to descriptions, e.g. '\t' to 'tab'
invalid_unicode = [u'', u'\x08', u'\x7f'] + list(whitespace)
# On mac arrow keys are not accepted as valid input either. Add them to this list
if platform.system() == "Darwin":
    invalid_unicode += [
        u'\uf702',  # left
        u'\uf703',  # right
        u'\uf700',  # up
        u'\uf701',  # down
        u'\uf729',  # home
        u'\uf72b',  # end
        u'\uf72c',  # page up
        u'\uf72d',  # page down
        u'\uf728',  # delete
        u'\uf739',  # numlock
    ]


class Legacy(Keyboard):

    """
    desc:
            This is a keyboard backend built on top of PyGame.
            For function specifications and docstrings, see
            `openexp._keyboard.keyboard`.
    """

    def __init__(self, experiment, **resp_args):

        pygame.init()
        self.key_code_to_name = {}
        self.key_name_to_code = {}
        for i in dir(pygame):
            if i[:2] == u"K_":
                code = getattr(pygame, i)
                name1 = self.key_name(code).lower()
                name2 = name1.upper()
                name3 = i[2:].lower()
                name4 = name3.upper()
                self.key_code_to_name[code] = [name1, name2, name3, name4]
                try:
                    i = int(name5)
                    self.key_code_to_name[code].append(name5)
                except:
                    pass
                self.key_name_to_code[name1] = code
                self.key_name_to_code[name2] = code
                self.key_name_to_code[name3] = code
                self.key_name_to_code[name4] = code
        self.persistent_virtual_keyboard = False
        Keyboard.__init__(self, experiment, **resp_args)

    @configurable
    def get_key(self):

        return self._get_key_event(pygame.KEYDOWN)

    @configurable
    def get_key_release(self):

        return self._get_key_event(pygame.KEYUP)

    def _get_key_event(self, event_type):

        start_time = pygame.time.get_ticks()
        time = start_time
        keylist = self.keylist
        timeout = self.timeout
        while True:
            time = pygame.time.get_ticks()
            # Some input methods send multiple key events at the same time,
            # for example when composing a multicharacter Chinese or Japanese
            # string. That's why we process up all events, rather than
            # assuming that there's only a single relevant event in the queue.
            key = u''
            for event in pygame.event.get(event_type):
                if event.key == pygame.K_ESCAPE:
                    self.experiment.pause()
                # KEYUP events don't have a unicode property, so in that case
                # we fall back to converting the key code straight to an ASCII
                # value. This is not great, because it assumes a QWERTY
                # keyboard layout.
                if hasattr(event, u'unicode'):
                    ucode = event.unicode
                elif event.key < 128:
                    ucode = chr(event.key)
                else:
                    ucode = u''
                if ucode in invalid_unicode:
                    key += self.key_name(event.key)
                else:
                    key += ucode
            if key and (keylist is None or key in keylist):
                return key, time
            if timeout is not None and time - start_time >= timeout:
                break
        return None, time

    def get_mods(self):

        l = []
        mods = pygame.key.get_mods()
        if mods & KMOD_LSHIFT or mods & KMOD_RSHIFT or mods & KMOD_SHIFT:
            l.append(u"shift")
        if mods & KMOD_LCTRL or mods & KMOD_RCTRL or mods & KMOD_CTRL:
            l.append(u"ctrl")
        if mods & KMOD_LALT or mods & KMOD_RALT or mods & KMOD_ALT:
            l.append(u"alt")
        if mods & KMOD_LMETA or mods & KMOD_RMETA or mods & KMOD_META:
            l.append(u"meta")
        return l

    def valid_keys(self):

        return sorted(self.key_name_to_code.keys())

    def synonyms(self, key):

        # If the key is not familiar, simply return it plus its string
        # representation.
        if key not in self.key_name_to_code:
            return [key, safe_decode(key)]
        return self.key_code_to_name[self.key_name_to_code[key]]

    def flush(self):

        keypressed = False
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                keypressed = True
                if event.key == pygame.K_ESCAPE:
                    self.experiment.pause()
        pygame.event.pump()
        return keypressed

    def key_name(self, key):

        return str(pygame.key.name(key)).replace(u'[', u'').replace(u']',
                                                                    u'')

    def _keycode_to_str(self, keycode):

        return safedecode(pygame.key.name(keycode)) \
            .replace(u'[', u'').replace(u']', u'').lower()


# Non PEP-8 alias for backwards compatibility
legacy = Legacy
