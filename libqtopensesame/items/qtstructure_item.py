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


class qtstructure_item(object):

	"""
	desc:
		A base class for items that control the structure of the experiment,
		i.e. those that require rebuilding of the item tree when they are
		changed.
	"""
	
	def __init__(self):
		
		"""
		desc:
			Constructor.
		"""

		self._children = None

	def update(self):

		"""See qtitem."""

		super(qtstructure_item, self).update()
		self.experiment.build_item_tree()

	def apply_script_changes(self):

		"""See qtitem."""

		super(qtstructure_item, self).apply_script_changes()
		self.experiment.build_item_tree()
		
	@staticmethod
	def clears_children_cache(fnc):
		
		"""
		desc:
			A decorator for functions that change the structure of the
			experiment, and thus need a clearing of the children cache.
		"""
		
		def inner(self, *args, **kwargs):
			
			self.experiment.items.clear_cache()
			return fnc(self, *args, **kwargs)
			
		return inner
		
	@staticmethod
	def cached_children(fnc):
		
		"""
		desc:
			A decorator for the children function, which is cached to speed up
			performance.
		"""
		
		def inner(self, *args, **kwargs):
			
			if self._children is not None:
				return self._children
			return fnc(self, *args, **kwargs)
			
		return inner
