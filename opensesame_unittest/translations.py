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


NO_PUNCTUATION_CHECK = [
	u'zh_CN',
	u'ja_JP'
	]


class check_translations(unittest.TestCase):

	def check_punctuation(self, path):

		for locale in NO_PUNCTUATION_CHECK:
			if path.endswith(locale + u'.ts'):
				return False
		return True

	def extractWildcards(self, s):

		return re.findall('(?<!%)%(\(\w+\)){0,1}([dfs]){1}', s)

	def validateTranslation(self, original, translation, punctuation=True):

		print(u'"%s" -> "%s"' % (safe_decode(original), safe_decode(translation)))
		self.assertEqual(
			self.extractWildcards(original), self.extractWildcards(translation))
		self.assertEqual(original[-1] == u' ', translation[-1] == u' ')
		self.assertEqual(original[-1] == u'\n', translation[-1] == u'\n')
		self.assertEqual(original[:1] == u' ', translation[:1] == u' ')
		if not punctuation:
			return
		if not original.endswith(u'nr.'):
			self.assertEqual(original[-1] == u'.', translation[-1] == u'.')
		self.assertEqual(original[-1] == u'?', translation[-1] == u'?')
		self.assertEqual(original[-1] == u'…', translation[-1] == u'…')
		self.assertEqual(original[-1] == u':', translation[-1] == u':')

	def checkMarkdown(self, dirname):

		for basename in os.listdir(dirname):
			if basename == u'locale':
				continue
			path = os.path.join(dirname, basename)
			if os.path.isdir(path):
				self.checkMarkdown(path)
				continue
			if not path.endswith(u'.md'):
				continue
			print(path)
			localedirname = os.path.join(dirname, u'locale')
			if not os.path.exists(localedirname):
				print(u'-> no translations')
				continue
			for locale in os.listdir(localedirname):
				localepath = os.path.join(localedirname, locale, basename)
				if not os.path.exists(localepath):
					continue
				print(u'-> '+localepath)
				with open(path) as fd:
					original = safe_decode(fd.read())
				with open(localepath) as fd:
					translation = safe_decode(fd.read())
				self.validateTranslation(original, translation,
					self.check_punctuation(localepath))

	def checkXML(self, path):

		print(path)
		import xml.etree.ElementTree as ET
		tree = ET.parse(path)
		root = tree.getroot()
		for context in root:
			for message in context:
				if message.tag != u'message':
					continue
				_translation = message.find(u'translation')
				if _translation.attrib.get(u'type', u'?') == u'obsolete':
					continue
				original = message.find(u'source').text
				translation = _translation.text
				if translation is None:
					continue
				self.validateTranslation(original, translation,
					self.check_punctuation(path))

	def checkTs(self, dirname):

		for basename in os.listdir(dirname):
			if not basename.endswith(u'.ts'):
				continue
			path = os.path.join(dirname, basename)
			print(path)
			self.checkXML(path)

	def runTest(self):

		self.checkMarkdown(u'opensesame_resources')
		self.checkMarkdown(u'opensesame_plugins')
		self.checkMarkdown(u'opensesame_extensions')
		self.checkTs(u'opensesame_resources/ts')


if __name__ == '__main__':
	unittest.main()
