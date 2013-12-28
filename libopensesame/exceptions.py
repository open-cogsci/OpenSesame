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

<DOC>
Provides the `osexception` class for throwing OpenSesame-specific exceptions.

	from libopensesame.exceptions import osexception
	raise osexception(u'This is a custom exception!')
</DOC>
"""

from libopensesame.misc import escape_html
from libopensesame import debug
import traceback
import inspect
import sys

class osexception(Exception):
	
	"""
	A general Exception class for exceptions that occur within OpenSesame.
	Ideally, only `osexception`s should occur, all other exceptions indicate
	a (usually harmless) bug somewhere.
	"""

	def __init__(self, msg, exception=None, **info):
		
		"""
		Constructor.
		
		Arguments:
		msg		--	An Exception message.
		
		Keyword arguments:
		exception	--	An exception that was intercepted or None for
						self-generated exceptions. (default=None)
		**info		--	A dictionary with optional additional info for the
						exception.
		"""
		
		super(osexception, self).__init__(msg)
		# Create both HTML and plain text representations of the Exception.
		self._html = u'<b>%s</b><br />\n' % msg
		self._plaintext = u'\n%s\n\n' % msg
		self.enc = u'utf-8'
		# If an Exception is passed, i.e. if we are catching an Exception,
		# summarize this exception here.
		self.exception = exception
		if self.exception != None:
			info[u'exception type'] = self.exception.__class__.__name__ \
				.decode(self.enc, u'ignore')
			info[u'exception message'] = self.exception.message.decode( \
				self.enc, u'ignore')
			try:
				# This is a hacky way to extract the line number from the
				# stacktrace. Since it's not clear whether this is fullproof,
				# we try-except it for now.
				info[u'line'] = traceback.extract_tb(sys.exc_info()[2])[-1][1]
			except:
				pass
		# List any additional information that was passed
		for key, val in info.items():
			self._html += u'<i>%s</i>: %s<br />\n' % (key, val)
			self._plaintext += u'%s: %s\n' % (key, val)
		# If an Exception is passed, we should include a traceback.
		if self.exception == None:
			return
		tb = traceback.format_exc(self.exception).decode(self.enc, u'ignore')
		self._html += u'<br /><b>Traceback (also in debug window)</b>:<br />\n'
		self._plaintext += u'\nTraceback:\n'
		for l in tb.split(u'\n')[1:]:
			# It is confusing that the contents of the inline script are
			# described as <string>, so replace that.
			l = l.replace(u'File "<string>"', u'Inline_script')
			self._html += escape_html(l) + u'<br />\n'
			self._plaintext += l + u'\n'
			
	def __unicode__(self):
		
		"""
		Returns:
		A unicode representation of the exception in plaintext.
		"""
		
		return self._plaintext

	def __str__(self):
		
		"""
		Returns:
		A string representation of the exception in plaintext.
		"""

		return self._plaintext.encode(u'utf-8')
	
	def plaintext(self):
		
		"""
		Returns:
		A string representation of the exception in plaintext.
		"""
		
		return unicode(self)
	
	def html(self):
		
		"""
		Returns:
		A unicode representation of the exception in HTML format.
		"""
		
		return self._html

# For backwards compatibility, we should also define the old Exception classes
runtime_error = osexception
script_error = osexception
form_error = osexception
