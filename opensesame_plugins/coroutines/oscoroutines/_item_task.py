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
from libopensesame.exceptions import osexception
from oscoroutines._base_task import base_task


class item_task(base_task):

	"""
	desc:
		A task controls the coroutine for one item.
	"""

	def __init__(self, coroutines, _item, start_time, end_time):

		"""
		desc:
			Constructor.

		arguments:
			item:
				desc:	An item object.
				type:	item
		"""

		if not hasattr(_item, u'coroutine'):
			raise osexception(
				u'%s not supported by coroutines' % _item.item_type)
		self._item = _item
		base_task.__init__(self, coroutines, start_time, end_time)
		self.coroutines.event(u'initialize %s' % _item.coroutine)

	def launch(self):

		"""See base_task."""

		self._item.prepare()
		# New-style coroutines take a coroutines keyword, which is used to
		# communicate the coroutines item. Old-style coroutines do not.
		try:
			self.coroutine = self._item.coroutine(coroutines=self.coroutines)
		except TypeError:
			self.coroutine = self._item.coroutine()
		self.coroutines.event('launch %s' % self._item)
		self.coroutine.send(None)
