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

import re
import os
import yaml

# A regular expression that (purportedly) detects all Python strings in the code
# From:
# http://code.activestate.com/recipes/475109-regular-expression-for-python-string-literals/
regex_str = (ur"""
[uU]?[rR]?
  (?:              # Single-quote (') strings
  '''(?:                 # Tripple-quoted can contain...
      [^']               | # a non-quote
      \\'                | # a backslashed quote
      '{1,2}(?!')          # one or two quotes
    )*''' |
  '(?:                   # Non-tripple quoted can contain...
     [^']                | # a non-quote
     \\'                   # a backslashded quote
   )*'(?!') | """+
r'''               # Double-quote (") strings
  """(?:                 # Tripple-quoted can contain...
      [^"]               | # a non-quote
      \\"                | # a backslashed single
      "{1,2}(?!")          # one or two quotes
    )*""" |
  "(?:                   # Non-tripple quoted can contain...
     [^"]                | # a non-quote
     \\"                   # a backslashded quote
   )*"(?!")
)''')

# A regular expression that detects all translatables in the code
regex_trans = re.compile(ur'_\(%s\)' % regex_str, re.VERBOSE)

translatables = {}
n_files = 0

def detect_translatables_py(path, context):

	"""
	desc:
		Scans a Python script for translatables and adds these to the list of
		translatables.

	arguments:
		path:
			desc:	The path to the file.
			type:	unicode
		context:
			desc:	A translation context.
			type:	unicode
	"""

	global translatables
	s = open(path).read().decode(u'utf-8')
	for i in regex_trans.findall(s):
		if context not in translatables:
			translatables[context] = []
		translatables[context].append(i[2:-1])

def detect_translatables_yaml(path, context):

	"""
	desc:
		Scans a YAML extension script for translatables and adds these to the
		list of translatables.

	arguments:
		path:
			desc:	The path to the file.
			type:	unicode
		context:
			desc:	A translation context.
			type:	unicode
	"""

	global translatables
	s = open(path).read().replace('\t', '    ').decode('utf-8')
	d = yaml.load(s, Loader=yaml.FullLoader)
	for field in [u'label', u'description', u'tooltip', u'category']:
		if field in d:
			if context not in translatables:
				translatables[context] = []
			translatables[context].append('u"%s"' \
				% (d[field].replace(u'"', u'\\"')))
	if u'controls' in d:
		for _d in d[u'controls']:
			for field in [u'label', u'tooltip', u'prefix', u'suffix']:
				if field in _d:
					if context not in translatables:
						translatables[context] = []
					translatables[context].append('u"%s"' \
						% (_d[field].replace(u'"', u'\\"')))

def encode_translatables(path=u'dev-scripts/translatables.py'):

	"""
	desc:
		Writes all translatables to a Python script, which can be interpreted by
		pylupdate4.

	arguments:
		path:
			desc:	The path to the Python script that is generated.
			type:	[str, unicode]
	"""

	global translatables
	f = open(path, u'w')
	for context, _translatables in translatables.items():
		f.write('class %s:\n\tdef _():\n' % context)
		for t in _translatables:
			f.write((u'\t\tself.tr(%s)\n' % t).encode(u'utf-8'))
	f.close()
	print(u'%d translatables written to %s' % (len(translatables), path))

def validate_py(path):

	"""
	desc:
		Checks whether a Python script is valid, i.e. starts with a proper
		Encoding message etc.

	arguments:
		path:
			desc:	The path to the file.
			type:	[str, unicode]
	"""

	s = open(path).readline().strip()
	if s not in (u'#-*- coding:utf-8 -*-', '# -*- coding: utf-8 -*-'):
		print(u'no-utf8: %s' % path)

def parse_py(path, context, translate=True):

	"""
	desc:
		Processes a single Python file.

	arguments:
		path:
			desc:	The path to the file.
			type:	unicode
		context:
			desc:	A translation context.
			type:	unicode

	keywords:
		translate:
			desc:	Indicates whether the folder should be checked for
					translatables.
			type:	bool
	"""

	global n_files
	n_files += 1
	validate_py(path)
	if translate:
		detect_translatables_py(path, context)

def parse_folder(path, context=None, translate=True, py=True, yaml=True):

	"""
	desc:
		Processes a single folder.

	arguments:
		path:
			desc:	The path to the folder.
			type:	unicode

	keywords:
		context:
			desc:	A translation context.
			type:	unicode
		translate:
			desc:	Indicates whether the folder should be checked for
					translatables.
			type:	bool
		py:
			desc:	Indicates whether .py files should be processed.
			type:	bool
		yaml:
			desc:	Indicates whether .yaml / .json  files should be processed.
			type:	bool
	"""

	for f in os.listdir(path):
		if context is not None:
			_context = context
		elif path in [u'extensions', u'plugins']:
			_context = f
		else:
			_context = u'script'
		_path = os.path.join(path, f)
		ext = os.path.splitext(_path)[1]
		if os.path.isdir(_path):
			parse_folder(_path, _context, translate)
		elif py and (f in [u'qtopensesame'] or ext == u'.py'):
			parse_py(_path, _context, translate)
		elif yaml and ext in [u'.yaml', u'.json']:
			detect_translatables_yaml(_path, _context)

if __name__ == u'__main__':

	parse_folder('extensions')
	parse_folder('plugins', py=False)
	parse_folder('libqtopensesame')
	parse_folder('libopensesame', translate=False)
	parse_folder('openexp', translate=False)
	encode_translatables()
	print('Parsed %d files' % n_files)
