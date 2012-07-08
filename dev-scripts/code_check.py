#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import os

# From
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

regex_trans = re.compile(r'_\(%s\)' % regex_str, re.VERBOSE)

translatables = []
n_files = 0

def detect_translatables(path):

	global translatables
	s = open(path).read()	
	for i in regex_trans.findall(s):
		translatables.append(i[2:-1])	
		
def encode_translatables(path='dev-scripts/translatables.py'):

	global translatables
		
	f = open(path, 'w')
	f.write('class script:\n\tdef _():\n')
	for t in translatables:
		f.write('\t\tself.tr(%s)\n' % t)
	f.close()

	print '%d translatables written to %s' % (len(translatables), path)
	
def validate(path):

	s = open(path).readline().strip()
	if s not in ('#-*- coding:utf-8 -*-', '# -*- coding: utf-8 -*-'):
		print 'no-utf8: %s' % path
	
def parse_file(path, translate=True):

	global n_files
	n_files += 1

	validate(path)
	if translate:
		detect_translatables(path)
	
def parse_folder(path, translate=True):

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
