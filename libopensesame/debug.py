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

import sys
import os.path
import inspect

def parse_stack(st):

	"""
	desc:
		Generates a nice looking stacktrace for a single item.
		
	arguments:
		st:		A stacktrace item.

	returns:
		A string for the stacktrace item.
	"""

	return u'%s(%d).%s' % (os.path.basename(st[1]), st[2], st[3])

def format_stack(st, skip=0):

	"""
	desc:
		Generates a nice looking full stracktrace.
		
	arguments:
		st:		A stacktrace object.
		
	keywords:
		skip:	Indicates whether any initial stacktrace items should be
				skipped.

	returns:
		A string corresponding to the stacktrace.
	"""

	st = st[skip:]
	st.reverse()
	i = 1
	s = u''
	while len(st) > 0:
		s += u' %.3d\t%s\n' % (i, parse_stack(st.pop()))
		i += 1
	return s

def _msg(msg=u'', reason=None):

	"""
	desc:
		Prints a debugging message. Respects the --debug and --stack parameters.

	keywords:
		msg:	A debug message.
		reason:	A reason for the message.
	"""

	global stack, max_stack
	st = inspect.stack()
	if reason != None:
		print(u'[%s]' % reason)
	# The terminal may not like anythin but plain ASCII
	if isinstance(msg, str):
		msg = msg.decode(u'utf-8', u'ignore')
	try:
		print(u'%s: %s' % (parse_stack(st[1]), msg))
	except:
		# This should not happen!
		print(u'%s: Failed to print message to debug window' % \
			parse_stack(st[1]))
	if stack:
		print(format_stack(st, skip=2))
		
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
		if isinstance(msg, str):
			print(msg.decode(u'ascii', u'ignore'))
		elif isinstance(msg, unicode):
			print(msg.encode(u'ascii', u'ignore'))

enabled = '--debug' in sys.argv or '-d' in sys.argv
if enabled:
	msg = _msg
else:
	# Replace the message function with a dummy function to turn off debugging
	# output
	stack = False
	msg = lambda msg=None, reason=None: None
stack = '--stack' in sys.argv or '-s' in sys.argv
if enabled:
	if stack:
		_msg(u'debug mode enabled (stacktrace on)')
	else:
		_msg(u'debug mode enabled (stacktrace off)')
