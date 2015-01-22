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
from PyQt4 import QtGui
import sys
from libqtopensesame.misc.base_subcomponent import base_subcomponent
from libopensesame import misc

class base_console(base_subcomponent):

	"""
	desc:
		A base console for debug-window consoles.
	"""

	def clear(self):

		"""
		desc:
			Clears the console.
		"""

		pass

	def capture_stdout(self):

		"""
		desc:
			Starts capturing stdout.
		"""

		sys.stdout = self
		sys.stderr = self

	def default_globals(self):

		"""
		returns:
			desc:	A dict with the default globals for the interpreter.
			type:	dict
		"""

		return {'modules': misc.module_versions}

	def flush(self):

		"""
		desc:
			Must exist to emulate stdout.
		"""

		pass

	def focus(self):

		"""
		desc:
			Steel the keyboard focus.
		"""

		pass

	def release_stdout(self):

		"""
		desc:
			Stops capturing stdout.
		"""

		sys.stdout = sys.__stdout__
		sys.stderr = sys.__stderr__

	def set_workspace_globals(self, _globals={}):

		"""
		desc:
			Updates the IPython globals dict.

		keywords:
			_globals:
				desc:	A new global stack to merge with the old one.
				type:	dict
		"""

		pass

	def setReadOnly(self, state):

		"""
		desc:
			Dummy function, that needs to exist.
		"""

		pass

	def show_prompt(self):

		"""
		desc:
			Shows a new prompt.
		"""

		pass
