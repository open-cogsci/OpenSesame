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
import warnings

class log(object):

	"""
	desc: |
		The `log` provides data logging.

		__Example__:

		~~~ .python
		# Write one line of text
		log.write(u'My custom log message')
		# Write all variables
		log.write_vars()
		~~~

		[TOC]
	"""

	def __init__(self, experiment, path):

		"""
		desc:
			Constructor to create a new `log` object. You do not generally
			call this constructor directly, because a `log` object is created
			automatically when the experiment is launched.

		arguments:
			experiment:
				desc:	The experiment object.
				type:	experiment
		"""

		self.experiment = experiment
		self.experiment.var.logfile = path
		self._all_vars = None
		self.open(path)

	def __call__(self, msg):

		warnings.warn(u'item.flog() has been deprecated. '
			u'Use experiment.log.write() instead.', DeprecationWarning)
		self.write(msg)

	def close(self):

		"""
		desc:
			Closes the current log.

		example: |
			log.close()
		"""

		pass

	def all_vars(self):

		"""
		visible: False

		returns:
			A list of all variables that exist in the experiment.
		"""

		if self._all_vars is None:
			self._all_vars = list(self.experiment.var.inspect().keys())
		return self._all_vars

	def open(self, path):

		"""
		desc:
			Opens the current log. If a log was already open, it is closed
			automatically.

		arguments:
			path:
				desc:	The path to the current logfile. In most cases (unless)
						a custom log back-end is used, this will be a filename.
				type:	[str, unicode]

		example: |
			# Open a new log
			log.open(u'/path/to/new/logfile.csv')
		"""

		pass

	def write(self, msg, newline=True):

		"""
		desc:
			Write one message to the log.

		arguments:
			msg:
				desc:	A text message. When using Python 2, this should be
						either `unicode` or a utf-8-encoded `str`. When using
						Python 3, this should be either `str` or a utf-8-encoded
						`bytes`.
				type:	[str, unicode]

		keywords:
			newline:
				desc:	Indicates whether a newline should be written after the
						message.
				type:	bool

		example: |
			# Write a single string of text
			log.write(u'time = %s' % clock.time())
		"""

		pass

	def write_vars(self, var_list=None):

		"""
		desc:
			Writes variables to the log.

		keywords:
			var_list:
				desc:	A list of variable names to write, or None to write all
						variables that exist in the experiment.
				type:	[list, NoneType]

		example: |
			# Write all variables to the logfile
			log.write_vars()
		"""

		pass
