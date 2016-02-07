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
from translatables import Translatables
import yaml
import re
import os


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


def parse_yaml(path, t):

	print(path)
	if path.startswith(u'./extension'):
		category = u'extension'
	else:
		category = u'plugin'
	name = os.path.basename(os.path.dirname(path))
	context = u'%s_%s' % (category, name)
	print(u'\tcontext: %s' % context)
	with open(path) as fd:
		d = yaml.load(safe_decode(fd.read().replace(u'\t', u'    ')))
		for field in [u'label', u'description', u'tooltip', u'category']:
			if field not in d:
				continue
			t.add(context, d[field])
			print(u'\ttranslatable: %s' % d[field])
		if u'controls' in d:
			for _d in d[u'controls']:
				for field in [u'label', u'tooltip', u'prefix', u'suffix']:
					if field not in _d:
						continue
					t.add(context, _d[field])
					print(u'\ttranslatable: %s' % _d[field])


def parse_folder(path, t):

	for fname in os.listdir(path):
		fname = os.path.join(path, fname)
		if fname.endswith(u'.py'):
			parse_py(fname, t)
			continue
		if fname.endswith(u'.yaml') or fname.endswith(u'.json'):
			parse_yaml(fname, t)
			continue
		if os.path.isdir(fname):
			parse_folder(fname, t)


if __name__ == u'__main__':
	t = Translatables()
	parse_folder(u'.', t)
	with open(u'translatables-tmp.py', u'w') as fd:
		fd.write(safe_str(t))
