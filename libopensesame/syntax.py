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

import shlex
import re
import codecs
import os
from libopensesame.exceptions import osexception
from libopensesame.py3compat import *

class syntax(object):

	"""
	desc:
		The `syntax` class implement text operations, including those that are
		necessary for interpreting OpenSesame script.
	"""

	def __init__(self, experiment):

		"""
		desc:
			Constructor.

		arguments:
			experiment:	The experiment object.
		"""

		self.experiment = experiment
		# A regular expression to match keywords, which are characterized by:
		# - Start with a letter or underscore
		# - Consists only of letters, numbers, or underscores, except for
		# - The last character, which is an equals sign
		self.re_cmd = re.compile(r'\A[_a-zA-Z]+[_a-zA-Z0-9]*=')
		# A regular expression to match [variables] in text
		self.re_txt = re.compile(r'(?<!\\)(\[[_a-zA-Z]+[_a-zA-Z0-9]*\])')
		# A regular expression to match inline Python statements, like so:
		# [=10*10]
		# [\[test\]]
		self.re_txt_py = re.compile(r'(?<!\\)(\[=.*?[^\\]\])')
		# Catch single equals signs
		self.re_single_eq = re.compile(r'(?<!=)(=)(?!=)')
		# Catch 'never' and 'always'
		self.re_never = re.compile(r'\bnever\b', re.I)
		self.re_always = re.compile(r'\balways\b', re.I)
		# Strict no-variables is used to remove all characters except
		# alphanumeric ones
		self.re_sanitize_strict_novars = re.compile(r'[^\w]')
		# Strict with variables is used to remove all characters except
		# alphanumeric ones and [] signs that indicate variables
		self.re_sanitize_strict_vars = re.compile(r'[^\w\[\]]')
		# Loose is used to remove double-quotes, slashes, and newlines
		self.re_sanitize_loose = re.compile(r'[\n\"\\]')
		# Unsanitization is used to replace U+XXXX unicode notation
		self.re_from_ascii = re.compile(r'U\+([A-F0-9]{4})')

	def split(self, s):

		"""
		desc:
			A unicode-safe bash-style split function. This is a wrapper around
			shlex.split() which is not unicode-safe on Python 2.

		arguments:
			s:
				desc:	The string to split.
				type:	[str, unicode]

		returns:
			desc:	The string split into a list.
			type:	list
		"""

		try:
			if py3:
				return shlex.split(s)
			# In Python 2, shlex is not unicode safe, so we need to do some manual
			# encoding and decoding
			return [safe_decode(_s) for _s in shlex.split(safe_encode(s))]
		except Exception as e:
			raise osexception(
				u'Failed to parse line "%s". Is there a closing quotation missing?' \
				% s, exception=e)

	def parse_cmd(self, cmd):

		"""
		desc:
			Parses OpenSesame command strings, which consist of a command,
			optionally followed by arguments, optionally followed by keywords.

			For example:

				widget 0 0 1 1 label text="Demo text"

			Here, `widget` is the command, `0` through `label` are arguments,
			and `text` is a keyword.

		arguments:
			cmd:
				desc:	The command string to parse.
				type:	[str, unicode]

		returns:
			desc:	A (command, arglist, kwdict) tuple.
			type:	tuple
		"""

		l = self.split(cmd)
		if len(l) == 0:
			return None, [], {}
		cmd = l[0]
		arglist = []
		kwdict = {}
		for s in l[1:]:
			m = self.re_cmd.match(s)
			if m is not None:
				arg = s[:m.end()-1]
				val = s[m.end():]
				kwdict[arg] = val
			else:
				arglist.append(s)
		return cmd, arglist, kwdict

	def eval_text(self, txt, round_float=False):

		"""
		desc:
			Evaluates variables and inline Python in a text string.

			Examples:

				The resolution is [width] by [height] pixels
				This evaluates to 100: [=10x10]

		arguments:
			txt:	The string to evaluate. If the input is not a string, then
					the value will be returned unmodified.

		keywords:
			round_float:
				desc:	Indicates whether floating point values should be
						rounded or not.
				type:	bool

		returns:
			The evaluated string, or the input value for non-string input.
		"""

		if not isinstance(txt, basestring):
			return txt
		if round_float:
 			float_template = u'%%.%sf' % self.experiment.var.round_decimals
		while True:
			m = self.re_txt.search(txt)
			if m is None:
				break
			val = self.experiment.var.get(m.group()[1:-1])
			if round_float and isinstance(val, float):
				val = float_template % val
			else:
				val = safe_decode(val)
			txt = txt[:m.start(0)] + val + txt[m.end(0):]
		# Detect Python inlines [=10*10]
		while True:
			m = self.re_txt_py.search(txt)
			if m is None:
				break
			py = self.unescape(m.group()[2:-1])
			val = self.experiment.python_workspace._eval(py)
			txt = txt[:m.start(0)] + safe_decode(val) + txt[m.end(0):]
		return self.unescape(txt)

	def compile_cond(self, cnd, bytecode=True):

		"""
		desc:
			Compiles OpenSesame conditional statements.

			Examples:
				[width] > 100
				=var.width > 100

		arguments:
			cnd:
				desc:	The conditional statement to compile.
				type:	[str, unicode]

		keywords:
			bytecode:
				desc:	Indicates whether the conditional statement should be
						returned as bytecode (True) or a Python string (False).
				type:	bool

		returns:
			desc:	The conditional statement as a Python string or bytecode.
			type:	[str, bytecode]
		"""

		# Python conditions `=True` don't have to be evaluated
		if cnd.startswith(u'='):
			cnd = cnd[1:]
		else:
			# Replace [variables] by var.variables
			while True:
				m = self.re_txt.search(cnd)
				if m is None:
					break
				cnd = cnd[:m.start()] + u'var.%s' % m.group()[1:-1] \
					+ cnd[m.end():]
			# Replace single equals signs (=) by doubles (==)
			cnd = self.re_single_eq.sub(u'==', cnd)
			# Replace always and never words by True or False
			cnd = self.re_never.sub(u'False', cnd)
			cnd = self.re_always.sub(u'True', cnd)
		if bytecode:
			try:
				return compile(cnd, u"<conditional statement>", u"eval")
			except:
				raise osexception(
					u"'%s' is not a valid conditional statement" % cnd)
		return self.unescape(cnd)

	def unescape(self, s):

		return s.replace(u'\[', u'[').replace(u'\]', u']')

	def sanitize(self, s, strict=False, allow_vars=True):

		"""
		desc:
			Removes invalid characters (notably quotes) from the string.

		arguments:
			s:
				desc:	The string to be sanitized. This can be any type, but
						if it is not unicode, it will be coerced to unicode.

		keywords:
			strict:
				desc:	If True, all except underscores and alphanumeric
						characters are stripped.
				type:	bool
			allow_vars:
				desc:	If True, square brackets are not sanitized, so you can
						use variables.
				type:	bool

		returns:
			desc:	A sanitized string.
			type:	unicode

		example: |
			# Prints 'Universit Aix-Marseille'
			print(self.sanitize('\"Université Aix-Marseille\"'))
			# Prints 'UniversitAixMarseille'
			print(self.sanitize('\"Université Aix-Marseille\""', strict=True))
		"""

		s = safe_decode(s)
		if strict:
			if allow_vars:
				return self.re_sanitize_strict_vars.sub(u'', s)
			return self.re_sanitize_strict_novars.sub(u'', s)
		return self.re_sanitize_loose.sub(u'', s)

	def to_ascii(self, s, strict=False):

		"""
		desc:
			Converts all non-ASCII characters to U+XXXX notation, so that the
			resulting string can be treated as plain ASCII text.

		arguments:
			s:
				desc:	A unicode string to be santized
				type:	unicode

		keywords:
			strict:
				desc:	If True, special characters are ignored rather than
						recoded.
				type:	bool

		returns:
			desc:	A regular Python string with all special characters replaced
					by U+XXXX notation or ignored (if strict).
			type:	str
		"""

		if strict:
			_s = safe_encode(s, enc=u'ascii', errors=u'ignore')
		else:
			_s = codecs.encode(s, u'ascii', u'osreplace')
		_s = safe_decode(_s)
		return _s.replace(os.linesep, u'\n')

	def from_ascii(self, s):

		"""
		desc:
			Converts an ascii str with U+XXXX notation to actual Unicode.

		arguments:
			s:
			 	desc:	A plain-ascii string.
				type:	str

		returns:
			desc:	A string with all U+XXXX characters converted to the corresponding
					unicode characters.
			type:	unicode
		"""

		if not isinstance(s, basestring):
			raise osexception(
				u'from_ascii() expects first argument to be unicode or str, not "%s"' \
				% type(s))
		s = safe_decode(s)
		while True:
			m = self.re_from_ascii.search(s)
			if m is None:
				break
			if py3:
				_unichr = chr
			else:
				_unichr = unichr
			s = s.replace(m.group(0), _unichr(int(m.group(1), 16)), 1)
		return s

def osreplace(exc):

	"""
	desc:
		A replacement function to allow opensame-style replacement of unicode
		characters.

	arguments:
		exc:
			type:	UnicodeEncodeError

	returns:
		desc:	A (replacement, end) tuple.
		type:	tuple
	"""

	_s = u''
	for ch in exc.object[exc.start:exc.end]:
		_s += u'U+%.4X' % ord(ch)
	return _s, exc.end

codecs.register_error(u'osreplace', osreplace)
