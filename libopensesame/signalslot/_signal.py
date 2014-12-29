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

import inspect
from libopensesame.exceptions import osexception
from libopensesame.signalslot._slot import slot, base_slot

class signal(object):

	"""
	desc: |
		A signal object.

		%--
		constants:
			slot_desc:
				A `slot` object, or a slot description. To connect an item, use
				a slot description like 'item:[item name]'. To connect a Python
				function, use 'function:[function name]'.
		--%
	"""

	def __init__(self, experiment, args=None, kwargs=None):

		"""
		desc:
			Constructor.

		arguments:
			experiment:
				desc:	The experiment object.
				type:	experiment
		"""

		self.slots = []
		self.args = args
		self.kwargs = kwargs
		self.experiment = experiment

	@property
	def __add__(self):
		return self.connect

	@property
	def __contains__(self):
		return self.is_connected

	@property
	def __sub__(self):
		return self.disconnect

	def connect(self, _slot):

		"""
		desc:
			Connects a slot to the signal.

		arguments:
			slot:
				desc:	"%slot_desc"
				type:	[slot, str, unicode]
		"""

		_slot = slot(self, _slot)
		if _slot not in self:
			self.slots.append(_slot)
		return self

	def disconnect(self, _slot):

		"""
		desc:
			Disconnects a slot from the signal.

		arguments:
			slot:
				desc: 	"%slot_desc"
				type:	[slot, str, unicode]
		"""

		_slot = slot(self, _slot)
		if self.is_connected(_slot):
			self.slots.pop(self.slots.index(_slot))
		return self

	def emit(self, *args, **kwargs):

		"""
		desc:
			Emits the current signal, i.e. calls all connected slots.

		arglist:
			args:
				A list of arguments to be passed to Python-function slots.

		kwdict:
			kwargs:
				A dict with keywords to passed to Python-function slots.
		"""

		for slot in self.slots:
			slot.run(*args, **kwargs)

	def is_connected(self, _slot):

		"""
		desc:
			Checks whether a slot is connected to the signal.

		arguments:
			slot:
				desc: 	"%slot_desc"
				type:	[slot, str, unicode]

		returns:
			desc:	True if the slot is connected, False otherwise.
			type:	bool
		"""

		_slot = slot(self, _slot)
		return _slot in self.slots

	def prepare(self):

		"""
		desc:
			Prepares the signal. This effectively means that the `prepare()`
			function of all connected items is called.
		"""

		for slot in self.slots:
			slot.prepare()
