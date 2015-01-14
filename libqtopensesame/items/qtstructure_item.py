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

	def update(self):

		"""See qtitem."""

		super(qtstructure_item, self).update()
		self.experiment.build_item_tree()

	def apply_script_changes(self):

		"""See qtitem."""

		super(qtstructure_item, self).apply_script_changes()
		self.experiment.build_item_tree()
