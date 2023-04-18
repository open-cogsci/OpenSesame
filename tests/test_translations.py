#!/usr/bin/env python
#-*- coding:utf-8 -*-

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
import os
import re
import unittest
from libopensesame.py3compat import *


PUNCTUATION_CHECK = ['nl', 'de', 'fr', 'es', 'it', 'pt', 'ru', 'tr']


class check_translations(unittest.TestCase):

    def check_punctuation(self, path):

        for locale in PUNCTUATION_CHECK:
            if path.endswith(locale + '.ts'):
                return True
        return False

    def extractWildcards(self, s):

        return re.findall('(?<!%)%(\(\w+\)){0,1}([dfs]){1}', s)

    def validateTranslation(self, original, translation, punctuation=True,
                            whitespace=True):

        print('"%s" -> "%s"' % (safe_decode(original), safe_decode(translation)))
        self.assertEqual(
            self.extractWildcards(original), self.extractWildcards(translation))
        if whitespace:
            self.assertEqual(original[-1] == ' ', translation[-1] == ' ')
            self.assertEqual(original[-1] == '\n', translation[-1] == '\n')
            self.assertEqual(original[:1] == ' ', translation[:1] == ' ')
        if not punctuation:
            return
        if not original.endswith('nr.'):
            self.assertEqual(original[-1] == '.', translation[-1] == '.')
        self.assertEqual(original[-1] == '?', translation[-1] == '?')
        self.assertEqual(original[-1] == '…', translation[-1] == '…')
        self.assertEqual(original[-1] == ':', translation[-1] == ':')

    def checkMarkdown(self, dirname):

        for basename in os.listdir(dirname):
            if basename == 'locale':
                continue
            path = os.path.join(dirname, basename)
            if os.path.isdir(path):
                self.checkMarkdown(path)
                continue
            if not path.endswith('.md'):
                continue
            print(path)
            localedirname = os.path.join(dirname, 'locale')
            if not os.path.exists(localedirname):
                print('-> no translations')
                continue
            for locale in os.listdir(localedirname):
                localepath = os.path.join(localedirname, locale, basename)
                if not os.path.exists(localepath):
                    continue
                print('-> '+localepath)
                with open(path) as fd:
                    original = safe_decode(fd.read())
                with open(localepath) as fd:
                    translation = safe_decode(fd.read())
                self.validateTranslation(original, translation,
                    self.check_punctuation(localepath), whitespace=False)

    def checkXML(self, path):

        print(path)
        import xml.etree.ElementTree as ET
        tree = ET.parse(path)
        root = tree.getroot()
        for context in root:
            for message in context:
                if message.tag != 'message':
                    continue
                _translation = message.find('translation')
                if _translation.attrib.get('type', '?') == 'obsolete':
                    continue
                original = message.find('source').text
                translation = _translation.text
                if translation is None:
                    continue
                self.validateTranslation(original, translation,
                    self.check_punctuation(path))

    def checkTs(self, dirname):

        for basename in os.listdir(dirname):
            if not basename.endswith('.ts'):
                continue
            path = os.path.join(dirname, basename)
            print(path)
            self.checkXML(path)

    def runTest(self):

        self.checkMarkdown('libqtopensesame/resources')
        self.checkMarkdown('opensesame_plugins')
        self.checkMarkdown('opensesame_extensions')
        self.checkTs('libqtopensesame/resources/ts')


if __name__ == '__main__':
    unittest.main()
