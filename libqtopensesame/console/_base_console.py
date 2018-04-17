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
import sys
from libqtopensesame.misc.base_subcomponent import base_subcomponent
from libqtopensesame.misc.config import cfg
from libopensesame import misc
from libopensesame import metadata
if py3:
	from io import StringIO
else:
	from StringIO import StringIO


class base_console(base_subcomponent):

	"""
	desc:
		A base console for debug-window consoles.
	"""

	def __init__(self, main_window):

		super(base_console, self).__init__(main_window)
		self.vault = StringIO()
		self.orig_stdout = sys.stdout
		self.orig_stderr = sys.stderr

	def isatty(self):

		"""
		desc:
			Indicates that the output is not attached to a terminal.
		"""

		return False

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

	def _modules(self):

		self.extension_manager[u'system_information'].activate()
		print(u'Activated system_information extension')

	def default_globals(self):

		"""
		returns:
			desc:	A dict with the default globals for the interpreter.
			type:	dict
		"""

		return {
			'console' : self,
			'opensesame' : self.main_window,
			'cfg' : cfg,
			'modules' : self._modules,
			'__spec__' : None, # Required by multiprocessing
			}

	def start(self):

		"""
		desc:
			Can implement a deferred start.
		"""

		pass

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

	def focusInEvent(self, e):

		"""
		desc:
			Processes focus-in events to set the style of the debug window.

		arguments:
			e:
				type:	QFocusEvent
		"""

		self.setTheme()
		super(base_console, self).focusInEvent(e)

	def release_stdout(self):

		"""
		desc:
			Stops capturing stdout.
		"""

		sys.stdout = self.orig_stdout
		sys.stderr = self.orig_stderr

	def reset(self):

		"""
		desc:
			Resets the console, which clears the window and resets the
			workspace.
		"""

		self.main_window.set_run_status(u'inactive')
		self.main_window.extension_manager.fire(u'reset_console')

	def get_workspace_globals(self):

		"""
		returns:
			desc:	The console's globals dict.
			type:	dict

		"""

		return {}

	def execute(self, s):

		"""
		desc:
			Executes a code snippet.

		arguments:
			s:
				desc:	A code snippet.
				type:	str
		"""

		pass

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

	def setup(self, main_window):

		"""See base_subcomponent."""

		super(base_console, self).setup(main_window)
		self.setTheme()

	def suppress_stdout(self):

		"""
		desc:
			Suppresses stdout.
		"""

		sys.stdout = self.vault
		sys.stderr = self.vault

	def banner(self):

		"""
		returns:
			A banner shown when initializing the debug window.
		"""

		s = u'''Python %s

* Type "help()", "copyright()", "credits()" or "license()" for more information.
* Use the "print([msg])" function in inline_script items to print to this debug window.
* Inspect inline_script variables when an experiment is finished.
''' % metadata.python_version
		return s
