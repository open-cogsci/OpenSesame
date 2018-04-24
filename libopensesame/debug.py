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

# About

Provides printing of debug output, which is only shown when OpenSesame is
started in debug mode by passing the `--debug` command-line argument, optionally
with a full stacktrace if the `--stack` argument is passed as well. To print
debug output, simply use the following structure:

	from libopensesame import debug
	debug.print(u'This is a debug message')
"""

from libopensesame.py3compat import *
import sys

stack_lvl = 0
msg_nr = 0

def indent(d=1):

	global stack_lvl
	stack_lvl += d

def _msg(msg=u'', reason=None):

	"""
	desc:
		Prints a debugging message. Respects the --debug and --stack parameters.

	keywords:
		msg:	A debug message.
		reason:	A reason for the message.
	"""

	global stack, max_stack, msg_nr
	if reason is not None:
		msg = u'[%s] %s' % (reason, msg)
	# The terminal may not like anything but plain ASCII
	if not isinstance(msg, basestring):
		msg = str(msg)
	msg = safe_encode(msg, enc=u'ascii', errors=u'ignore')
	try:
		print(u'%.6d %s%s' % (msg_nr, u'| '*stack_lvl, msg))
	except:
		# This should not happen!
		print(u'%.6d %sFailed to print message' % (msg_nr, u'| '*stack_lvl))
	msg_nr += 1

def _print(msg):

	"""
	desc:
		Prints a message to the standard output, just like the normal `print`
		statement/ function. This is necessary to capture encoding errors while
		printing.

	arguments:
		msg:
			desc:	A message to print.
			type:	[unicode, str]
	"""

	try:
		print(msg)
	except:
		if isinstance(msg, bytes):
			print(safe_decode(msg, enc=u'ascii', errors=u'ignore'))
		elif isinstance(msg, str):
			print(safe_encode(msg, enc=u'ascii', errors=u'ignore'))

enabled = '--debug' in sys.argv or '-d' in sys.argv
if enabled:
	msg = _msg
else:
	# Replace the message function with a dummy function to turn off debugging
	# output
	msg = lambda msg=None, reason=None: None
