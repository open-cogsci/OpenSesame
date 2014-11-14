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

class python_workspace(object):

	"""
	desc:
		Provides a worspace in which Python scripts can be executed. Generally,
		each experiment has one python_workspace object, which is used for all
		inline_script items, and other items that make allow users to execute
		Python code.

		The python_workspace object is dictionary-like, and allows you to get
		and set global variables in a dictionary way, e.g.:

			self.experiment.python_workspace[u'my_var'] = 10
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
		# By setting the __name__ global, the workspace will operate as a
		# module, so that e.g. import statements don't suffer from locality.
		self._globals = {
			u'__name__'		: u'python_workspace',
			u'exp'			: self.experiment,
			}

	def check_syntax(self, script):

		"""
		desc:
			Checks whether a Python script is syntactically correct.

		arguments:
			script:
				desc:	A Python script.
				type:	unicode

		returns:
			desc:	True if the script is correct, False otherwise.
			type:	bool
		"""

		try:
			self._compile(script)
		except:
			return False
		return True

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
