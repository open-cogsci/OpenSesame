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
from openexp._keyboard.keyboard import Keyboard
from openexp.backend import configurable

# Whitespace, backspace, and empty strings are not acceptable names for keys.
# These should be converted to descriptions, e.g. '\t' to 'tab'
invalid_unicode = ['', '\x08', '\x7f'] + list(whitespace)
# On mac arrow keys are not accepted as valid input either. Add them to this list
if platform.system() == "Darwin":
    invalid_unicode += [
        '\uf702',  # left
        '\uf703',  # right
        '\uf700',  # up
        '\uf701',  # down
        '\uf729',  # home
        '\uf72b',  # end
        '\uf72c',  # page up
        '\uf72d',  # page down
        '\uf728',  # delete
        '\uf739',  # numlock
    ]


class Legacy(Keyboard):

    """This is a keyboard backend built on top of PyGame. For function
    specifications and docstrings, see `openexp._keyboard.keyboard`.
    """

    # Class-level cache for key mappings (populated once on first init)
    _key_code_to_name = None
    _key_name_to_code = None

    @classmethod
    def _init_key_cache(cls):
        """Populate the class-level key mapping caches (idempotent)."""
        if cls._key_code_to_name is not None:
            return
        cls._key_code_to_name = {}
        cls._key_name_to_code = {}
        for i in dir(pygame):
            if i[:2] == "K_":
                code = getattr(pygame, i)
                name1 = cls.key_name(code).lower()
                name2 = name1.upper()
                name3 = i[2:].lower()
                name4 = name3.upper()
                cls._key_code_to_name[code] = [name1, name2, name3, name4]
                cls._key_name_to_code[name1] = code
                cls._key_name_to_code[name2] = code
                cls._key_name_to_code[name3] = code
                cls._key_name_to_code[name4] = code

    def __init__(self, experiment, **resp_args):

        self._init_key_cache()
        # Instance-level references to the class-level caches (for backward
        # compatibility with any code that accesses these as instance attrs)
        self.key_code_to_name = self._key_code_to_name
        self.key_name_to_code = self._key_name_to_code
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
            key = ''
            for event in pygame.event.get(event_type):
                if event.key == pygame.K_ESCAPE:
                    self.experiment.pause()
                # KEYUP events don't have a unicode property, so in that case
                # we fall back to converting the key code straight to an ASCII
                # value. This is not great, because it assumes a QWERTY
                # keyboard layout.
                if hasattr(event, 'unicode'):
                    ucode = event.unicode
                elif event.key < 128:
                    ucode = chr(event.key)
                else:
                    ucode = ''
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
            l.append("shift")
        if mods & KMOD_LCTRL or mods & KMOD_RCTRL or mods & KMOD_CTRL:
            l.append("ctrl")
        if mods & KMOD_LALT or mods & KMOD_RALT or mods & KMOD_ALT:
            l.append("alt")
        if mods & KMOD_LMETA or mods & KMOD_RMETA or mods & KMOD_META:
            l.append("meta")
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

    @classmethod
    def key_name(cls, key):

        return str(pygame.key.name(key)).replace('[', '').replace(']', '')

    def _keycode_to_str(self, keycode):

        return (safedecode(pygame.key.name(keycode))
                .replace('[', '').replace(']', '').lower())


# Non PEP-8 alias for backwards compatibility
legacy = Legacy
