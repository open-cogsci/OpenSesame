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

class base_slot(object):

	"""
	desc:
		The base class for all slot objects.
	"""

	def __init__(self, signal, _slot):

		"""
		desc:
			Constructor.

		arguments:
			signal:
				desc:	The signal to which the slot will be connected.
				type:	signal.
			_slot:
				desc:	The name of the slot, such as the name of the Python
						function, or the name of the item.
				type:	[str, unicode, FunctionType]
		"""

		self.signal = signal
		self._slot = _slot

	def __eq__(self, other):

		"""
		desc:
			Implements the == operator.

		arguments:
			other:	An object to test for equality.

		returns:
			desc:	True if self == other, False otherwise.
			type:	bool
		"""

		return unicode(self) == unicode(other)

	def __ne__(self, other):

		"""
		desc:
			Implements the != operator.

		arguments:
			other:	An object to test for inequality.

		returns:
			desc:	True if self != other, False otherwise.
			type:	bool
		"""

		return unicode(self) != unicode(other)

	@property
	def experiment(self):
		return self.signal.experiment

	def prepare(self):

		"""
		desc:
			Prepares the slot. This happens during the prepare phase of items.
		"""

		pass

	def run(self):

		"""
		desc:
			Runs the slot. This happens when a signal is emitted.
		"""

		pass

class item_slot(base_slot):

	"""
	desc:
		A item-style slot.
	"""

	def prepare(self):
		self.experiment.items[self._slot].prepare()

	def run(self, *arglist, **kwdict):
		self.experiment.items[self._slot].run()

	def __unicode__(self):
		return u'item=%s' % self._slot

class direct_function_slot(base_slot):

	"""
	desc:
		A Python-function-style slot for functions that are passed directly.
	"""

	def run(self, *arglist, **kwdict):
		self._slot(*arglist, **kwdict)

	def __unicode__(self):
		return unicode(self._slot)

class inline_function_slot(base_slot):

	"""
	desc:
		A Python-function-style slot for functions defined in an inline script.
	"""

	@property
	def python_workspace(self):
		return self.signal.experiment.python_workspace

	def run(self, *arglist, **kwdict):
		self.python_workspace[self._slot](*arglist, **kwdict)

	def __unicode__(self):
		return u'function=%s' % self._slot

def slot(signal, _slot):

	"""
	desc:
		A factory that creates a derivative of a `base_slot`object based on a
		slot description.
	arguments:
		signal:
			desc:	The signal to which the slot will be connected.
			type:	signal.
		_slot:
			desc:	A slot description or `base_slot` object.
			type:	[base_slot, FuncType, str, unicode]

	returns:
		type:	base_slot
	"""

	if isinstance(_slot, base_slot):
		return _slot
	if inspect.isroutine(_slot):
		return direct_function_slot(signal, _slot)
	if isinstance(_slot, basestring):
		if _slot.startswith(u'item='):
			return item_slot(signal, _slot[5:])
		if _slot.startswith(u'function='):
			return inline_function_slot(signal, _slot[9:])
	raise osexception(u'Invalid slot: %s' % _slot)
