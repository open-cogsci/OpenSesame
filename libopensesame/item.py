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
from libopensesame.var_store import var_store
import warnings
from libopensesame.exceptions import osexception
from libopensesame import debug


class item(object):

	"""Abstract class that serves as the basis for all OpenSesame items."""

	encoding = u'utf-8'
	__deepcopy__ = None

	def __init__(self, name, experiment, string=None):

		"""
		Constructor.

		Arguments:
		name 		--	The name of the item.
		experiment 	--	The experiment object.

		Keyword arguments:
		string		--	An definition string. (default=None).
		"""

		try:
			object.__getattr__(self, u'var')
		except:
			self.var = var_store(self, parent=experiment.var)
		self.name = name
		self.experiment = experiment
		self.debug = debug.enabled
		self.count = 0
		self._get_lock = None
		# Deduce item_type from class name
		prefix = self.experiment.item_prefix()
		self.item_type = str(self.__class__.__name__)
		if self.item_type.startswith(prefix):
			self.item_type = self.item_type[len(prefix):]
		if not hasattr(self, u'description'):
			self.var.description = self.default_description
		else:
			self.var.description = self.description
		self.from_string(string)

	@property
	def clock(self):
		return self.experiment._clock

	@property
	def log(self):
		return self.experiment._log

	@property
	def syntax(self):
		return self.experiment._syntax

	@property
	def python_workspace(self):
		return self.experiment._python_workspace

	@property
	def responses(self):
		return self.experiment._responses

	@property
	def default_description(self):
		return u'Default description'

	def reset(self):

		"""
		desc:
			Resets all item variables to their default value.
		"""

		pass

	def prepare(self):

		"""Implements the prepare phase of the item."""

		self.experiment.var.set(u'count_%s' % self.name, self.count)
		self.count += 1

	def run(self):

		"""Implements the run phase of the item."""

		pass

	def parse_variable(self, line):

		"""
		Reads a single variable from a single definition line.

		Arguments:
		line	--	A single definition line.

		Returns:
		True on succes, False on failure.
		"""

		# It is a little ugly to call parse_comment() here, but otherwise
		# all from_string() derivatives need to be modified
		if self.parse_comment(line):
			return True
		l = self.syntax.split(line.strip())
		if len(l) > 0 and l[0] == u'set':
			if len(l) != 3:
				raise osexception( \
					u'Error parsing variable definition: "%s"' % line)
			else:
				self.var.set(l[1], l[2])
				return True
		return False

	def parse_keywords(self, line, from_ascii=False, _eval=False):

		"""
		Parses keywords, e.g. 'my_keyword=my_value'.

		Arguments:
		line		--	A single definition line.

		Keyword arguments:
		from_ascii	--	DEPRECATED KEYWORD.
		_eval		--	Indicates whether the values should be evaluated.
						(default=False)

		Returns:
		A value dictionary with keywords as keys and values as values.
		"""

		# Parse keywords
		l = self.syntax.split(line.strip())
		keywords = {}
		for i in l:
			j = i.find(u'=')
			if j != -1:
				# UGLY HACK: if the string appears to be plain text,
				# rather than a keyword, for example something like
				# 'accuracy = [acc]%', do not parse it as a keyword-
				# value pair. The string needs to occur only once in
				# the full line, both quoted and unquoted.
				q = u'"%s"' % i
				if line.count(q) == 1 and line.count(i) == 1:
					debug.msg( \
						u'"%s" does not appear to be a keyword-value pair in string "%s"' \
						% (i, line))
				else:
					var = str(i[:j])
					val = self.auto_type(i[j+1:])
					if _eval:
						val = self.syntax.eval_text(val)
					keywords[var] = val
		return keywords

	def parse_line(self, line):

		"""
		Allows for arbitrary line parsing, for item-specific requirements.

		Arguments:
		line	--	A single definition line.
		"""

		pass

	def parse_comment(self, line):

		"""
		Parses comments from a single definition line, indicated by # // or '.

		Arguments:
		line	--	A single definition line.

		Returns:
		True on succes, False on failure.
		"""

		line = line.strip()
		if len(line) > 0 and line[0] == u'#':
			self.comments.append(line[1:])
			return True
		elif len(line) > 1 and line[0:2] == u'//':
			self.comments.append(line[2:])
			return True
		return False

	def set_response(self, response=None, response_time=None, correct=None):

		"""
		desc:
			Deprecated by response store.
		"""

		warnings.warn(
			u'set_response() has been deprecated. Use responses object instead.',
			DeprecationWarning)
		self.responses.add(response=response, response_time=response_time,
			correct=correct)

	def __getattr__(self, var):

		if var in self.var.__vars__:
			warnings.warn(u'called %s as item property' % var,
				DeprecationWarning)
			return self.var.get(var)
		if hasattr(self.__class__, var):
			warnings.warn(
				u'called %s as item property and stored as class attribute' \
				% var, DeprecationWarning)
			return getattr(self.__class__, var)
		raise AttributeError(u'%s not found' % var)

	def variable_to_string(self, var):

		"""
		desc:
			Encodes a variable into a definition string.

		arguments:
			var:
				desc:	The name of the variable to encode.
				type:	str

		returns:
			desc:	A definition string.
			type:	str
		"""

		val = safe_decode(self.var.get(var, _eval=False))
		# Multiline variables are stored as a block
		if u'\n' in val or u'"' in val:
			s = u'__%s__\n' % var
			val = val.replace(u'__end__', u'\\__end__')
			for l in val.split(u'\n'):
				s += '\t%s\n' % l
			while s[-1] in (u'\t', u'\n'):
				s = s[:-1]
			s += u'\n\t__end__\n'
			return s
		# Regular variables
		return self.syntax.create_cmd(u'set', arglist=[var, val]) + u'\n'

	def from_string(self, string):

		"""
		desc:
			Parses the item from a definition string.

		arguments:
			string:
				desc:	A definition string, or None to reset the item.
				type:	[str, NoneType]
		"""

		debug.msg()
		textblock_var = None
		self.var.clear()
		self.reset()
		self.comments = []
		if string is None:
			return
		for line in string.split(u'\n'):
			line_stripped = line.strip()
			# The end of a textblock
			if line_stripped == u'__end__':
				if textblock_var is None:
					raise osexception(u'It appears that a textblock has been '
						u'closed without being opened.')
				self.var.set(textblock_var,
					textblock_val.replace(u'\\__end__', u'__end__'))
				textblock_var = None
			# The beginning of a textblock. A new textblock is only started when
			# a textblock is not already ongoing, and only if the textblock
			# start is of the format __VARNAME__
			elif line_stripped[:2] == u'__' and line_stripped[-2:] == u'__' \
				and textblock_var is None:
				textblock_var = line_stripped[2:-2]
				if textblock_var != u'':
					textblock_val = u''
				else:
					textblock_var = None
				# We cannot just strip the multiline code, because that may mess
				# up indentation. So we have to detect if the string is indented
				# based on the opening __varname__ line.
				strip_tab = line[0] == u'\t'
			# Collect the contents of a textblock
			elif textblock_var is not None:
				if strip_tab:
					textblock_val += line[1:] + u'\n'
				else:
					textblock_val += line + u'\n'
			# Parse regular variables
			elif not self.parse_variable(line):
				self.parse_line(line)
		if textblock_var is not None:
			raise osexception(
				u'Missing __end__ block for multiline variable "%s" in item %s' \
				% (textblock_var, self.name))

	def to_string(self, item_type=None):

		"""
		Encodes the item into an OpenSesame definition string.

		Keyword arguments:
		item_type	--	The type of the item or None for autodetect.
						(default=None)

		Returns:
		The unicode definition string
		"""

		if item_type is None:
			item_type = self.item_type
		s = u'define %s %s\n' % (item_type, self.name)
		for comment in self.comments:
			s += u'\t# %s\n' % comment.strip()
		for var in self.var:
			s += u'\t' + self.variable_to_string(var)
		return s

	def resolution(self):

		"""
		desc: |
			Returns the display resolution and checks whether the resolution is
			valid.

			__Important note:__

			The meaning of 'resolution' depends on the back-end. For example,
			the legacy back-end changes the actual resolution of the display,
			whereas the other back-ends do not alter the actual display
			resolution, but create a 'virtual display' with the requested
			resolution that is presented in the center of the display.

		returns:
			desc:	A (width, height) tuple
			type:	tuple
		"""

		w = self.var.get(u'width')
		h = self.var.get(u'height')
		if type(w) != int or type(h) != int:
			raise osexception( \
				u'(%s, %s) is not a valid resolution' % (w, h))
		return w, h

	def set(self, var, val):

		warnings.warn(u'item.set() is deprecated (for var %s)' % var,
			DeprecationWarning)
		setattr(self.var, var, val)

	def unset(self, var):

		warnings.warn(u'item.unset() is deprecated (for var %s)' % var,
			DeprecationWarning)
		self.var.unset(var)

	def get(self, var, _eval=True):

		warnings.warn(u'item.get() is deprecated (for var %s)' % var,
			DeprecationWarning)
		return self.var.get(var, _eval=_eval)

	def get_check(self, var, default=None, valid=None, _eval=True):

		warnings.warn(u'item.var.get() is deprecated (for var %s)' % var,
			DeprecationWarning)
		return self.var.get(var, default=default, _eval=_eval, valid=valid)

	def has(self, var):

		warnings.warn(u'item.has() is deprecated (for var %s)' % var,
			DeprecationWarning)
		return var in self.var

	def get_refs(self, text):

		"""
		desc:
			Returns a list of variables that are referred to by a string of
			text.

		arguments:
			text:
				desc:	A string of text. This can be any type, but will coerced
						to unicode if it is not unicode.

		returns:
			desc:	A list of variable names or an empty list if the string
					contains no references.
			type:	list

		Example: |
			print(self.get_refs('There are [two] [references] here'))
			# Prints ['two', 'references']
		"""

		text = safe_decode(text)

		l = []
		start = -1
		while True:
			# Find the start and end of a variable definition
			start = text.find(u'[', start + 1)
			if start < 0:
				break
			end = text.find(u']', start + 1)
			if end < 0:
				raise osexception( \
					u"Missing closing bracket ']' in string '%s', in item '%s'" \
					% (text, self.name))
			var = text[start+1:end]
			l.append(var)
			var = var[end:]
		return l

	def auto_type(self, val):

		"""
		desc:
			Converts a value into the 'best fitting' or 'simplest' type that is
			compatible with the value.

		arguments:
			val:
				desc:	A value. This can be any type.

		returns:
			desc:	The same value converted to the 'best fitting' type.
			type:	[unicode, int, float]

		Example: |
			print(type(self.auto_type('1'))) # Prints 'int'
			print(type(self.auto_type('1.1'))) # Prints 'float'
			print(type(self.auto_type('some text'))) # Prints 'unicode'
			# Note: Boolean values are converted to 'yes' / 'no' and are
			# therefore also returned as unicode objects.
			print(type(self.auto_type(True))) # Prints 'unicode'
		"""

		# Booleans are converted to True/ False
		if type(val) == bool:
			if val:
				return u'yes'
			else:
				return u'no'
		# Try to convert the value to a numeric type
		try:
			# Check if the value can be converted to an int without loosing
			# precision. If so, convert to int
			if int(float(val)) == float(val):
				return int(float(val))
			# Else convert to float
			else:
				return float(val)
		except:
			# Else, fall back to unicde
			return safe_decode(val)

	def set_item_onset(self, time=None):

		"""
		desc:
			Set a timestamp for the onset time of the item's execution.

		keywords:
			time:	A timestamp or None to use the current time.

		returns:
			desc:	A timestamp.
		"""

		if time is None:
			time = self.time()
		self.experiment.var.set(u'time_%s' % self.name, time)
		return time

	def dummy(self, **args):

		"""
		Dummy function

		Keyword arguments:
		arguments -- accepts all keywords for compatibility
		"""

		pass

	def var_info(self):

		"""
		Give a list of dictionaries with variable descriptions

		Returns:
		A list of (variable, description) tuples
		"""

		return [ (u"time_%s" % self.name, u"[Timestamp of last item call]"), \
			(u"count_%s" % self.name, u"[Number of item calls]") ]

	def sleep(self, ms):

		return self.clock.sleep(ms)

	def time(self):

		return self.clock.time()

	def flush_log(self):

		warnings.warn(u'item.flush_log() has been deprecated',
			DeprecationWarning)

	def split(self, s):

		warnings.warn(
			u'item.split() has been deprecated. Please use syntax.split()',
			DeprecationWarning)
		return self.syntax.split(s)

	def eval_text(self, text, round_float=False, soft_ignore=False,
		quote_str=False):

		warnings.warn(
			u'item.eval_text() has been deprecated. Please use syntax.eval_text()',
			DeprecationWarning)
		return self.syntax.eval_text(text, round_float=round_float)
