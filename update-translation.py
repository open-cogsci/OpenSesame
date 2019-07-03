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

from libopensesame.py3compat import *
import yaml
import re
import os
import subprocess
import argparse

EXCLUDE_FOLDERS = [u'build', u'dist', 'deb_dist', 'pgs4a-0.9.4']
LUPDATE = u'pylupdate5'
LRELEASE = u'/usr/lib/x86_64-linux-gnu/qt5/bin/lrelease'

pro_tmpl = u'''FORMS = %(ui_list)s
SOURCES = translatables-tmp.py
TRANSLATIONS = %(locales)s
'''

class Translatables(object):

	def __init__(self):

		self._translatables = {}

	def add(self, context, translatable):

		if context not in self._translatables:
			self._translatables[context] = []
		self._translatables[context].append(safe_decode(translatable))

	def to_file(self, path=u'translatables-tmp.py'):

		with open(path, u'w') as fd:
			fd.write(self.__str__())

	def __str__(self):

		l = []
		for context, translatables in self._translatables.items():
			l.append(u'class %s:\n\tdef _():' % context)
			for s in translatables:
				s = s.replace(u"'", u"\\'")
				s = s.replace(u'\n', u'\\n')
				l.append(u'\t\tself.tr(\'%s\')' % s)
		return safe_str(u'\n'.join(l) + u'\n')


def parse_py(path, t):

	print(path)
	re_context = r'_ = translation_context\(u?[\'"](?P<name>\w+)[\'"], category=u?[\'"](?P<category>\w+)[\'"]\)'
	re_translatable = r'\b_\(u?(?P<quote>[\'"])(?P<translatable>.+?)(?P=quote)\)'
	with open(path) as fd:
		src = safe_decode(fd.read())
		if u'\nfrom libqtopensesame.misc import _' in src:
			raise Exception(u'Deprecated translation in %s' % path)
		m = re.search(re_context, src)
		if m is None:
			print(u'\tcontext: None')
			return
		context = u'%s_%s' % (m.group(u'category'), m.group(u'name'))
		print(u'\tcontext: %s' % context)
		m = re.findall(re_translatable, src)
		for quotes, s in m:
			print(u'\ttranslatable: %s' % s)
			t.add(context, s)
		print(u'\t%d translatables' % len(m))


def parse_yaml(path, t, category):

	print(path)
	if category == u'auto':
		folder = os.path.basename(os.path.dirname(os.path.dirname(path)))
		print(folder)
		if folder == u'opensesame_extensions':
			category = u'extension'
		elif folder== u'opensesame_plugins':
			category = u'plugin'
		else:
			raise Exception(u'Unkown category for %s' % path)
	name = os.path.basename(os.path.dirname(path))
	context = u'%s_%s' % (category, name)
	print(u'\tcontext: %s' % context)
	with open(path) as fd:
		s = fd.read().replace('\t', '    ')
		d = yaml.load(s, Loader=yaml.FullLoader)
		for field in [u'label', u'description', u'tooltip']:
			if field not in d:
				continue
			t.add(context, d[field])
			print(u'\ttranslatable: %s' % d[field])
		if 'category' in d:
			t.add(u'core_item_category', d[u'category'])
		if u'controls' in d:
			for _d in d[u'controls']:
				for field in [u'label', u'info', u'prefix', u'suffix']:
					if field not in _d:
						continue
					t.add(context, _d[field])
					print(u'\ttranslatable: %s' % _d[field])


def parse_folder(path, t, ui_list, category):

	for fname in os.listdir(path):
		_fname = os.path.join(path, fname)
		if fname.endswith(u'.py'):
			parse_py(_fname, t)
			continue
		if fname in [u'info.yaml', u'info.json']:
			parse_yaml(_fname, t, category)
			continue
		if fname.endswith(u'.ui'):
			ui_list.append(_fname)
			continue
		if os.path.isdir(_fname) and \
			os.path.basename(_fname) not in EXCLUDE_FOLDERS:
			parse_folder(_fname, t, ui_list, category)


def compile_ts(locales, t, ui_list, fname='translate.pro'):

	t.to_file()
	pro = pro_tmpl % {
		u'ui_list' : u' \\\n\t'.join(ui_list),
		u'locales' : u' \\\n\t'.join(
			[u'opensesame_resources/ts/%s.ts' % locale for locale in locales])
		}
	with open(fname, u'w') as fd:
		fd.write(pro)
	cmd = [LUPDATE, fname]
	subprocess.call(cmd)


def compile_qm(locales):

	for locale in locales:
		cmd = [LRELEASE, u'opensesame_resources/ts/%s.ts' % locale,
			u'-qm', u'opensesame_resources/locale/%s.qm' % locale]
		subprocess.call(cmd)


def check_markdown_translations(dirname, locale):

	for basename in os.listdir(dirname):
		path = os.path.join(dirname, basename)
		if os.path.isdir(path) and basename != u'locale':
			check_markdown_translations(path, locale)
			continue
		if not path.endswith(u'.md'):
			continue
		if os.path.exists(os.path.join(dirname, u'locale', locale, basename)):
			print('+ %s' % path)
		else:
			print('- %s' % path)


def add_message_encoding(locales):

	for locale in locales:
		path = u'opensesame_resources/ts/%s.ts' % locale
		with open(path) as fd:
			content = safe_decode(fd.read())
			if u'<message>' not in content:
				continue
		with open(path, u'w') as fd:
			content = content.replace(
				u'<message>',
				u'<message encoding="UTF-8">'
			)
			fd.write(safe_str(content))
			print('Adding encoding to message tags for %s' % locale)

if __name__ == u'__main__':

	locales = [u'fr_FR', u'de_DE', u'it_IT', u'zh_CN', u'ru_RU', u'es_ES',
		u'ja_JP', u'tr_TR', u'translatables']
	parser = argparse.ArgumentParser(
		description=u'Update ts and qm files for OpenSesame-related projects')
	parser.add_argument('--category', type=str, default=u'auto',
		choices=[u'plugin', u'extension', u'auto'],
		help='Should be "plugin", "extension", or "auto"')
	args = parser.parse_args()
	t = Translatables()
	ui_list = []
	parse_folder(os.path.abspath(u'.'), t, ui_list, category=args.category)
	add_message_encoding(locales)
	compile_ts(locales, t, ui_list)
	compile_qm(locales)
	for locale in locales:
		print('Markdown translations for %s' % locale)
		check_markdown_translations('opensesame_extensions', locale)
		check_markdown_translations('opensesame_plugins', locale)
		check_markdown_translations('opensesame_resources', locale)
		print()
