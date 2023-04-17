#!/usr/bin/env python
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
import yaml
import re
import os
import sys
import subprocess
import argparse
from pathlib import Path
from translation_utils import *

EXCLUDE_FOLDERS = ['build', 'dist', 'deb_dist', 'pgs4a-0.9.4', 'doc']
LUPDATE = ['pylupdate5']
TRANSLATABLES_PY = Path('translatables.py')
TRANSLATE_PRO = Path('translate.pro')
pro_tmpl = '''FORMS = {ui_list}
SOURCES = {sources}
TRANSLATIONS = {translatables}
CODECFORTR = UTF-8
CODECFORSRC = UTF-8
'''


class Translatables(object):

    def __init__(self):

        self._translatables = {}

    def add(self, context, translatable):

        if context not in self._translatables:
            self._translatables[context] = set()
        self._translatables[context].add(safe_decode(translatable))

    def to_file(self, path=TRANSLATABLES_PY):

        with open(path, 'w') as fd:
            fd.write(str(self))

    def __str__(self):

        ls = []
        for context, translatables in self._translatables.items():
            ls.append('class %s:\n\tdef _():' % context)
            for s in translatables:
                # Escape all unescapted single quotes
                s = re.sub(r"(?<!\\)'", "\\'", s)
                s = s.replace('\n', '\\n')
                ls.append('\t\tself.tr(\'%s\')' % s)
        return safe_str('\n'.join(ls) + '\n')


def parse_py(path, t):

    print(path)
    re_context = r'_ = translation_context\(u?[\'"](?P<name>\w+)[\'"], category=u?[\'"](?P<category>\w+)[\'"]\)'
    re_translatable = r'\b_\(u?(?P<quote>[\'"])(?P<translatable>.+?)(?P=quote)\)'
    with open(path) as fd:
        src = safe_decode(fd.read())
        m = re.search(re_context, src)
        if m is None:
            print('\tcontext: None')
            return
        context = '%s_%s' % (m.group('category'), m.group('name'))
        print('\tcontext: %s' % context)
        m = re.findall(re_translatable, src)
        for quotes, s in m:
            print('\ttranslatable: %s' % s)
            t.add(context, s)
        print('\t%d translatables' % len(m))
        

def parse_init(path, t):
    print(f'parsing init file {path}')
    category = path.parts[-4].split('_')[1]
    context = f'{category[:-1]}_{path.parts[-2]}'
    d = {}
    exec(path.read_text(), d)
    for field in ['label', 'description', 'tooltip', '__doc__']:
        if field in d:
            t.add(context, d[field])
    t.add(context, d['__doc__'])
    if 'category' in d:
        t.add(context, d['category'])
    if 'controls' in d:
        for control in d['controls']:
            for field in ['label', 'info', 'tooltip', 'prefix', 'suffix']:
                if field in control:
                    t.add(context, control[field])


def parse_folder(path, t, ui_list):

    for fpath in path.iterdir():
        if fpath.suffix == '.py':
            if (fpath.name == '__init__.py'
                    and len(fpath.parts) >= 4
                    and fpath.parts[-4] in ('opensesame_plugins',
                                            'opensesame_extensions')):
                parse_init(fpath, t)
            else:
                parse_py(fpath, t)
            continue
        if fpath.suffix == '.ui':
            ui_list.append(fpath)
            continue
        if (fpath.is_dir() and fpath.name not in EXCLUDE_FOLDERS):
            parse_folder(fpath, t, ui_list)


def compile_ts(t, ui_list, ts_folder, fname=TRANSLATE_PRO):

    t.to_file()
    if not os.path.exists(ts_folder):
        print('No ts files found')
        return
    pro = pro_tmpl.format(
        ui_list=' \\\n\t'.join([str(p) for p in ui_list]),
        sources=TRANSLATABLES_PY,
        translatables=TRANSLATABLES)
    with open(fname, 'w') as fd:
        fd.write(pro)
    cmd = LUPDATE + [fname]
    subprocess.call(cmd)


translatables = Translatables()
ui_list = []
print('Parsing folders …')
parse_folder(Path(args.src_folder), translatables, ui_list)
print('Compiling ts …')
compile_ts(translatables, ui_list, Path(args.ts_folder))
