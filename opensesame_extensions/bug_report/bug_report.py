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
from libqtopensesame.extensions import base_extension
from libqtopensesame.misc.config import cfg
from libopensesame import metadata
from qtpy import QtCore
import sys
import yaml
import os
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'bug_report', category=u'extension')

class capture_stderr(object):

	"""
	desc:
		A file-like object to capture the stderr.
	"""

	def __init__(self, ext):

		"""
		desc:
			Constructor.

		arguments:
			ext:	The bug_report extension.
		"""

		self.ext = ext
		self.clear()
		self.timer = QtCore.QTimer()
		self.timer.setSingleShot(True)
		self.timer.timeout.connect(self.ext.captured_err)

	def clear(self):

		"""
		desc:
			Clear the error buffer.
		"""

		self.buffer = u''

	def write(self, msg):

		"""
		desc:
			Receives a chunk of error message. We use a timer of 1 second to
			report an error if no new error lines come in.

		arguments:
			msg:
				desc:	A chunk of error message.
				type:	str
		"""

		self.buffer += safe_decode(msg, errors=u'ignore')
		self.timer.start(1)
		if sys.__stderr__ is not None:
			sys.__stderr__.write(msg)

	def flush(self):

		"""
		desc:
			Flushes the standard error if available.
		"""

		if sys.__stderr__ is not None:
			sys.__stderr__.flush()

class bug_report(base_extension):

	"""
	desc:
		Captures the stderr and submits bug reports based on it.
	"""

	def event_startup(self):

		"""
		desc:
			Start capturing.
		"""

		self.stderr = capture_stderr(self)
		sys.stderr = self.stderr
		self.traceback = None

	def event_end_experiment(self, ret_val):

		"""
		desc:
			Recapture after the experiment has finished, because the console
			has set the stderr back to the original.
		"""

		sys.stderr = self.stderr

	def indent(self, s):

		"""
		desc:
			Tab-indent a piece of text so that it's code for Markdown.

		arguments:
			s:	The text to indent.

		returns:
			Indented text.
		"""

		return u'\t' + s.replace(u'\n', u'\n\t').replace(os.linesep, u'\n\t')

	def event_bug_report_send(self):

		"""
		desc:
			Sends a bug report for the latest stacktrace. Also closes the
			current tab, which is the report tab, and shows a results tab.
		"""

		self.main_window.tabwidget.close_current()
		if py3:
			from urllib.request import urlopen
			from urllib.parse import urlencode
		else:
			from urllib import urlencode
			from urllib2 import urlopen
		if self.traceback is None:
			return
		q = urlencode({
			u'traceback' : safe_str(self.traceback, errors=u'ignore'),
			u'version' : safe_str(metadata.__version__, errors=u'ignore'),
			u'python_version' : safe_str(metadata.python_version,
				errors=u'ignore'),
			u'platform' : safe_str(metadata.platform, errors=u'ignore'),
			})
		url = cfg.bug_report_url + u'?' + q
		try:
			fd = urlopen(url)
			resp = safe_decode(fd.read(), errors=u'ignore')
			fd.close()
		except:
			self.tabwidget.open_markdown(self.ext_resource(u'failure.md'),
				title=_(u'Bug report not sent'))
			return
		if resp == u'OK':
			self.tabwidget.open_markdown(self.ext_resource(u'success.md'),
				title=_(u'Bug report sent'))
		else:
			self.tabwidget.open_markdown(self.ext_resource(u'failure.md'),
				title=_(u'Bug report not sent'))

	def captured_err(self):

		"""
		desc:
			Shows a report tab when an error message has been captured.
		"""

		with open(self.ext_resource(u'report.md')) as fd:
			md = safe_decode(fd.read())
		self.traceback = self.stderr.buffer
		md = md % {
			u'traceback' : self.indent(self.stderr.buffer),
			u'version' : metadata.__version__,
			u'python_version' : safe_str(metadata.python_version,
				errors=u'ignore'),
			u'platform' : metadata.platform,
			}
		self.tabwidget.open_markdown(md, title=_(u'Oops ...'))
		self.stderr.clear()
