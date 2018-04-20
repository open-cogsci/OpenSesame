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


class base_python_workspace(object):

	"""
	desc:
		Provides a basic Python workspace for use in the GUI. This avoids
		unnecessarily importing the entire runtime API.
	"""

	def __init__(self, experiment):

		"""
		desc:
			Constructor.

		arguments:
			experiment:
				desc:	The experiment object.
				type:	experiment
		"""

		self.experiment = experiment
		self._globals = {}

	def check_syntax(self, script):

		"""
		desc:
			Checks whether a Python script is syntactically correct.

		arguments:
			script:
				desc:	A Python script.
				type:	unicode

		returns:
			desc:	0 if script is correct, 1 if there is a syntax warning, and
					2 if there is a syntax error.
			type:	int
		"""

		with warnings.catch_warnings(record=True) as warning_list:
			try:
				self._compile(safe_decode(script))
			except:
				return 2
		if warning_list:
			return 1
		return 0

	def run_file(self, path):

		"""
		desc:
			Reads and executes a files.

		arguments:
			path:
				desc:	The full path to a Python file.
				type:	str
		"""

		with safe_open(path) as fd:
			script = fd.read()
		bytecode = self._compile(script)
		self._exec(bytecode)

	def _compile(self, script):

		"""
		desc:
			Compiles a script into bytecode.

		arguments:
			script:
				desc:	A Python script.
				type:	unicode

		returns:
			desc:	The compiled script.
			type:	code
		"""

		# Prepend source encoding (PEP 0263) and encode scripts. This is
		# necessary, because the exec statement doesn't take kindly to Unicode.
		script = (u'#-*- coding:%s -*-\n' % self.experiment.encoding + script) \
			.encode(self.experiment.encoding)
		return compile(script, u'<string>', u'exec')

	def _exec(self, bytecode):

		"""
		desc:
			Executes bytecode.

		arguments:
			bytecode:
				desc:	A chunk of bytecode.
				type:	code
		"""

		exec(bytecode, self._globals)

	def _eval(self, bytecode):

		"""
		desc:
			Evaluates bytecode.

		arguments:
			bytecode:
				desc:	A chunk of bytecode.
				type:	code

		returns:
			The evaluated value of the bytecode
		"""

		return eval(bytecode, self._globals)

	# The properties below emulate a dict interface.

	@property
	def __setitem__(self):
		return self._globals.__setitem__

	@property
	def __delitem__(self):
		return self._globals.__delitem__

	@property
	def __getitem__(self):
		return self._globals.__getitem__

	@property
	def __len__(self):
		return self._globals.__len__

	@property
	def __iter__(self):
		return self._globals.__iter__

	@property
	def items(self):
		return self._globals.items

	@property
	def keys(self):
		return self._globals.keys

	@property
	def values(self):
		return self._globals.values

	@property
	def copy(self):
		return self._globals.copy
