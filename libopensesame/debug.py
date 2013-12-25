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

import sys
import os.path

def parse_stack(st):

	"""
	Generates a nice looking stacktrace for a single item.

	Returns:
	A string of the stacktrace item
	"""

	return u'%s(%d).%s' % (os.path.basename(st[1]), st[2], st[3])

def format_stack(st, skip=0):
	
	"""
	Generates a nice looking full stracktrace.
	
	Returns:
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

def msg(msg=u'', reason=None):

	"""
	Prints a debugging message. Respects the --debug and --stack parameters.

	Keyword arguments:
	msg 	--	A debug message. (default=u'')
	reason	--	A specific reason for the message. (default=None)
	"""

	global stack, max_stack
	st = inspect.stack()
	if reason != None:
		print u'[%s]' % reason,
	# The terminal may not like anythin but plain ASCII
	if isinstance(msg, str):
		msg = msg.decode(u'utf-8', u'ignore')
	try:
		print u'%s: %s' % (parse_stack(st[1]), msg)
	except:
		# This should not happen!
		print u'%s: Failed to print message to debug window' % \
			parse_stack(st[1])
	if stack:
		print format_stack(st, skip=2)
			
enabled = '--debug' in sys.argv or '-d' in sys.argv
if enabled:
	import inspect
	stack = '--stack' in sys.argv or '-s' in sys.argv
	if stack:
		msg(u'debug mode enabled (stacktrace on)')
	else:
		msg(u'debug mode enabled (stacktrace off)')
else:
	# Replace the message function with a dummy function to turn off debugging
	# output
	stack = False
	msg = lambda msg=None, reason=None: None
