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
from libopensesame.oslogging import oslogger
from libopensesame.item_stack import item_stack_singleton
from libopensesame.py3compat import *
import traceback
import time


class AbortCoroutines(Exception):

	"""
	desc:
		A messaging Exception to indicate that coroutines should be aborted.
		That is, if a task raises an AbortCoroutines, then the currently running
		coroutines should abort.
	"""

	pass


class osexception(Exception):

	"""
	desc:
		A general Exception class for exceptions that occur within OpenSesame.
		Ideally, only `osexception`s should occur, all other exceptions indicate
		a (usually harmless) bug somewhere.
	"""

	def __init__(self, msg, exception=None, **info):

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

		keyword-dict:
			info:		Optional additional info for the exception.
		"""

		super(osexception, self).__init__(msg)
		# Create both HTML and plain text representations of the Exception.
		self.enc = u'utf-8'
		self.user_triggered = info.get(u'user_triggered', False)
		self.exception = exception
		info = self._exception_info(msg, info)
		self._md, self._plaintext = self._exception_details(msg, info)
		if self.exception is None:
			return
		tb_md, tb_plaintext = self._parse_traceback(info)
		self._md += tb_md
		self._plaintext += tb_plaintext

	def _traceback(self):

		"""
		desc:
			Returns the traceback as a formatted string.
		"""

		if py3:
			return traceback.format_exc()
		return safe_decode( traceback.format_exc(self.exception), enc=self.enc,
			errors=u'ignore')

	def _parse_traceback(self, info):

		"""
		desc:
			Processes the traceback by replacing generic <string> references to
			Inline script, and by correct the line offset to compensate for the
			added utf-8 encoding header, which increments the line number by
			one.
		"""

		tb = self._traceback()
		md = u'## Traceback (also in debug window)\n\n'
		plaintext = u'\nTraceback:\n'
		_tb = u''
		for l in tb.split(u'\n')[1:]:
			if u'line_offset' in info:
				for g in re.finditer(
					u'File "<string>", line (?P<linenr>\d+)', l):
					try:
						l = l.replace(g.group(), u'%s, line %d' % \
								(info.get(u'item_type', u'Inline script'),
								int(g.group(u'linenr')) + info[u'line_offset'])
							)
					except:
						oslogger.error(
							u'failed to correct inline_script exception'
						)
			_tb += l + u'\n'
		plaintext += _tb
		md += u'~~~ .traceback\n%s\n~~~\n' % _tb
		return md, plaintext

	def _exception_details(self, msg, info):

		"""
		desc:
			Provides a markdown and plaintext overview of relevant information.
		"""

		md = u'%s\n\n## Details\n\n' % msg
		plaintext = u'\n%s\n\n' % msg
		for key, val in info.items():
			if key == u'line_offset': # For internal use only
				continue
			md += u'- %s: `%s`\n' % (key, val)
			plaintext += u'%s: %s\n' % (key, val)
		md += u'\n'
		return md, plaintext

	def _exception_info(self, msg, info):

		"""
		desc:
			Updates the info dict based on the type of Exception and the
			exception message.
		"""

		if isinstance(self.exception, SyntaxError):
			return self._syntaxerror_info(msg, info)
		return self._defaultexception_info(msg, info)

	def _syntaxerror_info(self, msg, info):

		"""
		desc:
			Updates the info dict specifically for SyntaxErrors
		"""

		info = self._defaultexception_info(msg, info)
		# Syntax errors are dealt with specially, because they provide
		# introspective information.
		for g in re.finditer(u'<string>, line (?P<linenr>\d+)', msg):
			msg = msg.replace(g.group(), u'%s, line %d' % (
					info.get(u'item_type', u'Inline script'),
					int(g.group(u'linenr')) \
						+ info.get(u'line_offset', -1))
				)
		info[u'exception message'] = msg
		info[u'line'] = self.exception.lineno + info.get(u'line_offset', -1)
		if self.exception.text is not None:
			info[u'code'] = safe_decode(self.exception.text, enc=self.enc,
				errors=u'ignore')
		return info

	def _defaultexception_info(self, msg, info):

		"""
		desc:
			Updates the info dict for all Exceptions.
		"""

		info[u'item-stack'] = str(item_stack_singleton)
		info[u'time'] = time.ctime()
		if self.exception is None:
			return info
		info[u'exception type'] = safe_decode(
			self.exception.__class__.__name__, enc=self.enc,
			errors=u'ignore')
		try:
			info[u'exception message'] = safe_decode(self.exception, errors=u'ignore')
		except:
			info[u'exception message'] = u'Description unavailable'
		return info

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
