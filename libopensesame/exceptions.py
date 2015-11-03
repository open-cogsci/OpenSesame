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

---
desc: |
	Provides the `osexception` class for throwing OpenSesame-specific
	exceptions.

example: |
	from libopensesame.exceptions import osexception
	raise osexception(u'This is a custom exception!')
---
"""

import re
from libopensesame.misc import escape_html
from libopensesame import debug
from libopensesame.item_stack import item_stack_singleton
from libopensesame.py3compat import *
import traceback
import time
import sys

class osexception(Exception):

	"""
	desc:
		A general Exception class for exceptions that occur within OpenSesame.
		Ideally, only `osexception`s should occur, all other exceptions indicate
		a (usually harmless) bug somewhere.
	"""

	def __init__(self, msg, exception=None, line_offset=0, **info):

		"""
		desc:
			Constructor.

		arguments:
			msg:
				desc:	An Exception message.
				type:	[str, unicode]

		keywords:
			exception:
				desc:	An exception that was intercepted or None for
						self-generated exceptions.
				type:	[Exception, NoneType]
			line_offset:
				desc:	A value to decrease/ increase line numbers. The primary
						goal for this keyword is to re-align line numbers that
						arise in inline_scripts, which need to be compensated
						for the source encoding line that is added to the
						source.
				type:	int

		keyword-dict:
			info:		Optional additional info for the exception.
		"""

		super(osexception, self).__init__(msg)
		# Create both HTML and plain text representations of the Exception.
		self._md = u'%s\n\n' % msg
		self._plaintext = u'\n%s\n\n' % msg
		self.enc = u'utf-8'
		self.user_triggered = u'user_triggered' in info \
			and info[u'user_triggered']
		# If an Exception is passed, i.e. if we are catching an Exception,
		# summarize this exception here.
		self.exception = exception
		if self.exception is not None:
			info[u'exception type'] = safe_decode(
				self.exception.__class__.__name__, enc=self.enc,
				errors=u'ignore')
			try:
				msg = safe_decode(self.exception, errors=u'ignore')
			except:
				msg = u'Description unavailable'
			info[u'exception message'] = msg
			if isinstance(self.exception, SyntaxError):
				# Syntax errors are dealt with specially, because they provide
				# introspective information.
				info[u'line'] = self.exception.lineno + line_offset
				if self.exception.text is not None:
					info[u'code'] = safe_decode(self.exception.text,
						enc=self.enc, errors=u'ignore')
		info[u'item-stack'] = str(item_stack_singleton)
		info[u'time'] = time.ctime()
		# List any additional information that was passed
		self._md += u'## Details\n\n'
		for key, val in info.items():
			self._md += u'- %s: `%s`\n' % (key, val)
			self._plaintext += u'%s: %s\n' % (key, val)
		self._md += u'\n'
		# If an Exception is passed, we should include a traceback.
		if self.exception is None:
			return
		if py3:
			tb = traceback.format_exc()
		else:
			tb = safe_decode(traceback.format_exc(self.exception), enc=self.enc,
				errors=u'ignore')
		self._md += u'## Traceback (also in debug window)\n\n'
		self._plaintext += u'\nTraceback:\n'
		_tb = u''
		for l in tb.split(u'\n')[1:]:
			# It is confusing that the contents of the inline script are
			# described as <string>, so replace that. In addition, we need to
			# decrease the line numer by 1, to compensate for the extra (hidden)
			# source-encoding line that the inline script has.
			if u'item' in info and info[u'item'] == u'inline_script':
				for g in re.finditer(
					u'File "<string>", line (?P<linenr>\d+),', l):
					try:
						l = l.replace(g.group(), u'Inline_script, line %d,' % \
							(int(g.group(u'linenr')) + line_offset))
					except:
						debug.msg(u'Failed to correct inline_script exception')
			_tb += l + u'\n'
		self._plaintext += _tb
		self._md += u'~~~ .traceback\n%s\n~~~\n' % _tb

	def __unicode__(self):

		"""
		returns:
			desc:	A representation of the exception in plaintext.
			type:	unicode
		"""

		return self._plaintext

	def __str__(self):

		"""
		returns:
			desc:	A representation of the exception in plaintext.
			type:	str
		"""

		if py3:
			return self._plaintext
		return safe_encode(self._plaintext)

	def plaintext(self):

		"""
		returns:
			desc:	A string representation of the exception in plaintext.
			type:	unicode
		"""

		return str(self)

	def markdown(self):

		"""
		returns:
			desc:	A representation of the exception in Markdown format.
			type:	unicode
		"""

		return self._md

# For backwards compatibility, we should also define the old Exception classes
runtime_error = osexception
script_error = osexception
form_error = osexception
