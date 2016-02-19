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

class items_adapter(object):

	"""
	desc:
		Gives an editable view on (item_name, start_time, end_time, cond) tuple
		(schedule) used by coroutines that funtions like an (item_name, cond)
		tuple as used by sequences.
	"""

	def __init__(self, schedule):

		self.schedule = schedule

	def __delitem__(self, index):

		del self.schedule[index]

	def __getitem__(self, index):

		return self.schedule[index][0], self.schedule[index][3]

	def __setitem__(self, index, val):

		self.schedule[index] = (val[0],) + self.schedule[index][1:3] + (val[1],)

	def __iter__(self):

		for item_name, start_time, end_time, cond in self.schedule:
			yield item_name, cond

	def __len__(self):

		return len(self.schedule)

	def insert(self, index, item):

		self.schedule.insert(index, ( (item[0],) + (0, 0) + (item[1],) ) )

	def append(self, item):

		self.schedule.append( ( (item[0],) + (0, 0) + (item[1],) ) )
