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

# A regular expression that (purportedly) detects all Python strings in the code
# From:
# http://code.activestate.com/recipes/475109-regular-expression-for-python-string-literals/
regex_str = (r"""
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
regex_trans = re.compile(r'_\(%s\)' % regex_str, re.VERBOSE)

translatables = []
n_files = 0

def detect_translatables(path):

	"""
	Scans a Python script for translatables and adds these to the list of
	translatables
	
	Arguments:
	path -- the path to Python script	
	"""

	global translatables
	s = open(path).read()	
	for i in regex_trans.findall(s):
		translatables.append(i[2:-1])	
		
def encode_translatables(path='dev-scripts/translatables.py'):

	"""
	Writes all translatables to a Python script, which can be interpreted by
	pylupdate4
	
	Arguments:
	path -- the path to the Python script that is generated	
	"""

	global translatables		
	f = open(path, 'w')
	f.write('class script:\n\tdef _():\n')
	for t in translatables:
		f.write('\t\tself.tr(%s)\n' % t)
	f.close()
	print '%d translatables written to %s' % (len(translatables), path)
	
def validate(path):

	"""
	Checks whether a Python script is valid, i.e. starts with a proper Encoding
	message etc.
	
	Arguments:
	path -- the path to Python script	
	"""
	s = open(path).readline().strip()
	if s not in ('#-*- coding:utf-8 -*-', '# -*- coding: utf-8 -*-'):
		print 'no-utf8: %s' % path
	
def parse_file(path, translate=True):

	"""
	Processes a single file
		
	Arguments:
	path -- the path to Python script	
	
	Keyword arguments:
	translate -- indicates whether the script should be checked for
				 translatables (default=True)
	"""	

	global n_files
	n_files += 1
	validate(path)
	if translate:
		detect_translatables(path)
	
def parse_folder(path, translate=True):

	"""
	Processes a single folder
		
	Arguments:
	path -- the path to the folder
	
	Keyword arguments:
	translate -- indicates whether the folder should be checked for
				 translatables (default=True)
	"""	

	for f in os.listdir(path):
		_path = os.path.join(path, f)
		if os.path.isdir(_path):
			parse_folder(_path, translate)
		elif f in ['qtopensesame'] or os.path.splitext(_path)[1] == '.py':
			parse_file(_path, translate)
	
parse_folder('libqtopensesame')
parse_folder('libopensesame', translate=False)
parse_folder('openexp', translate=False)
encode_translatables()
print 'Parsed %d files' % n_files
