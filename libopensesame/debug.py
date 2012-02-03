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

def parse_stack(stack):

	"""
	Generate a nice looking stacktrace item

	Returns:
	A string of the stacktrace item
	"""

	return "%s(%d).%s" % (os.path.basename(stack[1]), stack[2], stack[3])

def msg(msg="", reason=None):

	"""
	Print a debugging message. Respects the --debug and --stack parameters.

	Keyword arguments:
	msg -- debug message (default='')
	reason -- a specific reason for the message (default=None)
	"""

	global stack, max_stack
	st = inspect.stack()
	if reason != None:
		print "[%s]" % reason,
	print "%s: %s" % (parse_stack(st[1]), msg)
	st = st[1:]
	if stack:
		i = 1
		while len(st) > 0:
			print " %.3d\t%s\t" % (i, parse_stack(st.pop()))
			i += 1

enabled = "--debug" in sys.argv or "-d" in sys.argv
if enabled:
	import inspect
	stack = "--stack" in sys.argv or "-s" in sys.argv
	if stack:
		msg("debug mode enabled (stacktrace on)")
	else:
		msg("debug mode enabled (stacktrace off)")
else:
	msg = lambda x: None
