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

from libopensesame.item_store import item_store
from libqtopensesame.misc import _
from libqtopensesame.misc.base_subcomponent import base_subcomponent

class qtitem_store(item_store):

	"""
	desc:
		The GUI counterpart of the item store, which also distributes item
		changes etc.
	"""

	def __init__(self, experiment):

		"""
		desc:
			Constructor.

		arguments:
			main_window:
				desc:	The main window object.
				type:	qtopensesame
		"""

		super(qtitem_store, self).__init__(experiment)

	@property
	def main_window(self):
		return self.experiment.main_window

	@property
	def itemtree(self):
		return self.experiment.main_window.itemtree

	@property
	def extension_manager(self):
		return self.main_window.extension_manager

	def __delitem__(self, name):

		"""
		desc:
			Deletes an item, and notifies other items of the deletion.

		arguments:
			name:
				desc:	The name of the item to be deleted.
				type:	[str, unicode]
		"""

		del self.__items__[name]
		for _name in self:
			self[_name].remove_child_item(name, index=-1)

	def new(self, _type, name=None, script=None):

		"""See item_store."""

		item = super(qtitem_store, self).new(_type, name=name, script=script)
		self.main_window.set_unsaved(True)
		return item

	def unlinked_copy(self, item):

		"""
		desc:
			Creates an unlinked (deep) copy of an item.

		arguments:
			item:	The item to copy.

		returns:
			The new item.
		"""

		return self.new(item.item_type, item.name, item.to_string())

	def rename(self, from_name, to_name):

		"""
		desc:
			Renames an item and updates the interface. This function may show
			a notification dialog.

		arguments:
			from_name:
				desc:	The old item name.
				type:	unicode
			to_name:
				desc:	The desired new item name.
				type:	unicode

		returns:
			desc:	The new name of the item, if renaming was successful, None
					otherwise.
			type:	[NoneType, unicode]
		"""

		if from_name not in self:
			self.experiment.notify(_(u'Item "%s" doesn\'t exist' % from_name))
			return None
		if from_name == to_name:
			return None
		to_name = self.valid_name(self[from_name].item_type, suggestion=to_name)
		if to_name in self:
			self.experiment.notify(_(u'An item with that name already exists.'))
			return None
		if to_name == u'':
			self.experiment.notify(_(u'An item name cannot be empty.'))
			return None
		# Copy the item in the __items__dictionary
		self.__items__[to_name] = self.__items__[from_name]
		del self.__items__[from_name]
		# Give all items a chance to update
		for item in self.values():
			item.rename(from_name, to_name)
		self.experiment.rename(from_name, to_name)
		self.itemtree.rename(from_name, to_name)
		self.main_window.set_unsaved(True)
		self.extension_manager.fire(u'rename_item', from_name=from_name,
			to_name=to_name)
		return to_name

	def set_icon(self, name, icon):

		"""
		desc:
			Changes an item's icon.

		arguments:
			name:
				desc:	The item name.
				type:	unicode
			icon:
				desc:	The icon name.
				type:	unicode
		"""

		self.itemtree.set_icon(name, icon)

	def used(self):

		"""
		returns:
			desc:	A list of used item names.
			type:	list
		"""

		if self.experiment.var.start not in self:
			return []
		return [self.experiment.var.start] \
			+ self[self.experiment.var.start].children()

	def unused(self):

		"""
		returns:
			desc:	A list of unused item names.
			type:	list
		"""

		_used = self.used()
		return filter(lambda item: item not in _used, self.__items__.keys())
