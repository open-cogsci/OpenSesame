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

	def __init__(self, experiment, device=0, joybuttonlist=None, timeout=None):

		"""<DOC>
		Intializes the joystick object.

		Arguments:
		experiment		--	An instance of libopensesame.experiment.experiment.

		Keyword arguments:
		device			--	The device number of the joystick. (default=0)
		joybuttonlist	--	A list of buttons that are accepted or None to
							accept all buttons. (default=None)
		timeout			--	An integer value specifying a timeout in
							milliseconds or None for no timeout. (default=None)
		</DOC>"""

		raise NotImplementedError()

	def set_joybuttonlist(self, joybuttonlist=None):

		"""<DOC>
		Sets a list of accepted buttons.

		Keyword arguments:
		joybuttonlist	--	A list of button numbers that are accepted or None
							to accept all buttons. (default=None)
		</DOC>"""

		if joybuttonlist == None or joybuttonlist == []:
			self._joybuttonlist = None
		else:
			self._joybuttonlist = []
			for joybutton in joybuttonlist:
				self._joybuttonlist.append(joybutton)

	def set_timeout(self, timeout=None):

		"""<DOC>
		Sets a timeout.

		Keyword arguments:
		timeout		--	An integer value specifying a timeout in milliseconds or
						None for no timeout. (default=None)
		</DOC>"""

		self.timeout = timeout

	def get_joybutton(self, joybuttonlist=None, timeout=None):

		"""<DOC>
		Waits for joystick button input.

		Keyword arguments:
		joybuttonlist	--	A list of button numbers that are accepted or
							None to use the default. This parameter does not
							change the default joybuttonlist. (default = None)
		timeout			--	An integer value specifying a timeout in
							milliseconds or None to use the default. This
							parameter does not change the default timeout.
							(default=None)

		Returns:
		A (joybutton, timestamp) tuple. The joybutton is None if a timeout
		occurs.
		</DOC>"""

		raise NotImplementedError()

	def get_joyaxes(self, timeout=None):

		"""<DOC>
		Waits for joystick axes movement.

		Keyword arguments:
		timeout		--	An integer value specifying a timeout in milliseconds
						or None to use the default. This parameter does not
						change the default timeout. (default=None)

		Returns:
		A (position, timestamp) tuple. The position is None if a timeout occurs.
		</DOC>"""

		raise NotImplementedError()

	def get_joyballs(self, timeout=None):

		"""<DOC>
		Waits for joystick trackball movement.

		Keyword arguments:
		timeout		--	An integer value specifying a timeout in milliseconds
						or None to use the default. This parameter does not
						change the default timeout. (default=None)

		Returns:
		A (position, timestamp) tuple. The position is None if a timeout occurs.
		</DOC>"""

		raise NotImplementedError()

	def get_joyhats(self, timeout=None):

		"""<DOC>
		Waits for joystick hat movement.

		Keyword arguments:
		timeout		--	An integer value specifying a timeout in milliseconds
						or None to use the default. This parameter does not
						change the default timeout. (default=None)

		Returns:
		A (position, timestamp) tuple. The position is None if a timeout occurs.
		</DOC>"""

		raise NotImplementedError()

	def get_joyinput(self, joybuttonlist=None, timeout=None):

		"""<DOC>
		Waits for any joystick input (buttons, axes, hats or balls).

		Keyword arguments:
		joybuttonlist	--	A list of button numbers that are accepted or
							None to use the default. This parameter does not
							change the default joybuttonlist. (default=None)
		timeout			--	An integer value specifying a timeout in
							milliseconds or None to use the default. This
							parameter does not change the default timeout.
							(default=None)

		Returns:
		A (event, value, timestamp) tuple. The value is None if a timeout
		occurs.
		</DOC>"""

		raise NotImplementedError()

	def input_options(self):

		"""<DOC>
		Generates a list with amount of available buttons, axes, balls and hats.

		Returns:
		List with number of inputs as: [buttons, axes, balls, hats]
		</DOC>"""

		raise NotImplementedError()

	def flush(self):

		"""<DOC>
		Clears all pending input, not limited to the joystick.

		Returns:
		True if a joyinput has been made (i.e., if there was something
		to flush) and False otherwise
		</DOC>"""

		raise NotImplementedError()

