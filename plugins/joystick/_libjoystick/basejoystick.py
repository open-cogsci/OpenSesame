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

class basejoystick(object):

	"""
	desc: |
		If you insert the `joystick` plugin at the start of your experiment, a
		`joystick` object automatically becomes part of the experiment object
		and can be accessed from within an inline_script item as `exp.joystick`.

		__Function list:__

		%--
		toc:
			mindepth: 2
			maxdepth: 2
		--%

		%--
		constant:
			arg_joybuttonlist: |
				A list of buttons that are accepted or `None` to accept all
				buttons.
			arg_timeout: |
				An timeout value in milliseconds or `None` for no timeout.
		--%
	"""


	def __init__(self, experiment, device=0, joybuttonlist=None, timeout=None):

		"""
		desc:
			Intializes the joystick object.

		arguments:
			experiment:
				desc:	An Opensesame experiment.
				type:	experiment

		keywords:
			device:
				desc:	The joystick device number.
				type:	int
			joybuttonlist:
				desc:	"%arg_joybuttonlist"
				type:	[list, NoneType]
			timeout:
				desc:	"%arg_timeout"
				type:	[int, float, NoneType]
		"""

		raise NotImplementedError()

	def set_joybuttonlist(self, joybuttonlist=None):

		"""
		desc:
			Sets a list of accepted buttons.

		keywords:
			joybuttonlist:
				desc:	"%arg_joybuttonlist"
				type:	[list, NoneType]
		"""

		if joybuttonlist == None or joybuttonlist == []:
			self._joybuttonlist = None
		else:
			self._joybuttonlist = []
			for joybutton in joybuttonlist:
				self._joybuttonlist.append(joybutton)

	def set_timeout(self, timeout=None):

		"""
		desc:
			Sets a timeout.

		keywords:
			timeout:
				desc:	"%arg_timeout"
				type:	[int, float, NoneType]
		"""

		self.timeout = timeout

	def get_joybutton(self, joybuttonlist=None, timeout=None):

		"""
		desc:
			Collects joystick button input.

		keywords:
			joybuttonlist:
				desc:	A list of buttons that are accepted or `None` to
						default joybuttonlist.
				type:	[list, NoneType]
			timeout:
				desc:	A timeout value in milliseconds or `None` to use default
						timeout.
				type:	[int, float, NoneType]

		returns:
			desc: 	A (joybutton, timestamp) tuple. The joybutton is `None` if a
					timeout occurs.
			type:	tuple
		"""

		raise NotImplementedError()

	def get_joyaxes(self, timeout=None):

		"""
		desc:
			Waits for joystick axes movement.

		keywords:
			timeout:
				desc:	A timeout value in milliseconds or `None` to use default
						timeout.
				type:	[int, float, NoneType]

		returns:
			desc:	A (position, timestamp) tuple. The position is None if a
					timeout occurs.
			type:	tuple
		"""

		raise NotImplementedError()

	def get_joyballs(self, timeout=None):

		"""
		desc:
			Waits for joystick trackball movement.

		keywords:
			timeout:
				desc:	A timeout value in milliseconds or `None` to use default
						timeout.
				type:	[int, float, NoneType]

		returns:
			desc:	A (position, timestamp) tuple. The position is `None` if a
					timeout occurs.
			type:	tuple
		"""

		raise NotImplementedError()

	def get_joyhats(self, timeout=None):

		"""
		desc:
			Waits for joystick hat movement.

		keywords:
			timeout:
				desc:	A timeout value in milliseconds or `None` to use default
						timeout.
				type:	[int, float, NoneType]

		returns:
			desc:	A (position, timestamp) tuple. The position is `None` if a
					timeout occurs.
			type:	tuple
		"""

		raise NotImplementedError()

	def get_joyinput(self, joybuttonlist=None, timeout=None):

		"""
		desc:
			Waits for any joystick input (buttons, axes, hats or balls).

		keywords:
			joybuttonlist:
				desc:	A list of buttons that are accepted or `None` to
						default joybuttonlist.
				type:	[list, NoneType]
			timeout:
				desc:	A timeout value in milliseconds or `None` to use default
						timeout.
				type:	[int, float, NoneType]

		returns:
			desc:	A (event, value, timestamp) tuple. The value is `None` if a
					timeout occurs.
			type:	tuple
		"""

		raise NotImplementedError()

	def input_options(self):

		"""
		desc:
			Generates a list with the number of available buttons, axes, balls
			and hats.

		returns:
			desc:	|
					A list with number of inputs as: [buttons, axes, balls,
					hats].
			type:	list
		"""

		raise NotImplementedError()

	def flush(self):

		"""
		desc:
			Clears all pending input, not limited to the joystick.

		returns:
			desc:	True if joyinput was pending (i.e., if there was something
					to flush) and False otherwise.
			type:	bool
		"""

		raise NotImplementedError()
