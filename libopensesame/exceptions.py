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

import traceback

class form_error(Exception):

	"""
	A form_error is thrown when an error occurs in a form or a form widget.
	"""

	def __init__(self, value, full=True):
		super(form_error, self).__init__(value, full)
		if type(value) == str:
			self.value = unicode(value, errors=u'ignore')
		else:
			self.value = value
		self.full = full

	def __str__(self):

		if self.full:
			return u'<b>Error:</b> Form error<br /><b>Description</b>: %s' % \
				self.value
		return self.value

class script_error(Exception):

	"""
	A form_error is thrown when parsing a script using the from_string()
	functions fails.
	"""

	def __init__(self, value, full=True):
		super(script_error, self).__init__(value, full)
		if type(value) == str:
			self.value = unicode(value, errors=u'ignore')
		else:
			self.value = value
		self.full = full

	def __str__(self):

		if self.full:
			return u'<b>Error:</b> Script error<br /><b>Description</b>: %s' % \
				self.value
		return self.value

class runtime_error(Exception):

	"""
	A runtime error is thrown when somethingg oes wrong while running a script,
	which includes the preparation phase.
	"""

	def __init__(self, value, *args):
		super(runtime_error, self).__init__(value, args)
		if type(value) == str:
			self.value = unicode(value, errors=u'ignore')
		else:
			self.value = value

	def __str__(self):

		return u'<b>Error:</b> Runtime error<br /><b>Description</b>: %s' % \
			self.value

class inline_error(runtime_error):

	"""
	An inline error is thrown when something goes wrong in an inline_script
	item. The Python traceback is parsed and returned.
	"""

	def __init__(self, item_name, phase, exception):
		self.name = item_name
		self.phase = phase

		# Split the traceback
		l = traceback.format_exc(exception).split("\n")

		# Print the traceback to the stdout
		for r in l:
			print r

		# We are only interested in the last two lines
		l = l[-3:]

		s = u'<b>Error</b>: Inline script error'
		s += u'<br /><b>In</b>: %s (%s phase)' % (item_name, phase)
		s += u'<br />' + self.parse_line(l[0])
		s += u'<br /><br /><b>Python traceback</b>:'
		for r in l[1:]:
			s += u'<br />%s' % r
		s += u'<br /><i>Full traceback in debug window</i>'
		self.value = s
		super(inline_error, self).__init__(s, item_name, phase, exception)

	def parse_line(self, s):

		s = s.replace(u'File "<string>", line', u'<b>Line:</b>')
		s = s.replace(u', in <module>', u'')
		return s

	def __str__(self):

		return self.value

