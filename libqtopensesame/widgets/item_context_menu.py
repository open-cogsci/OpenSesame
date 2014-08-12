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

from PyQt4 import QtCore, QtGui
from libqtopensesame.misc import _
from libqtopensesame.misc.base_subcomponent import base_subcomponent

class item_context_menu(base_subcomponent, QtGui.QMenu):

	"""Provides a basic context menu for an item"""

	def __init__(self, main_window, treeitem):

		"""
		desc:
			Constructor.

		arguments:
			main_window:
				desc:	The main-window object.
				type:	qtopensesame
			treeitem:
				desc:	The tree item.
				type:	tree_item_item
		"""

		super(item_context_menu, self).__init__(main_window)
		self.setup(main_window)
		self.treeitem = treeitem
		self.addAction(self.experiment.icon(self.item.item_type),
			_("Open %s") % self.item.name, self.item.open_tab)
		self.addSeparator()
		self.addAction(self.experiment.icon(u"edit-copy"), _("Copy"),
			self.treeitem.copy)
		if self.treeitem.clipboard_data() != None:
			self.addAction(self.experiment.icon(u"edit-paste"), _("Paste"),
				self.treeitem.paste)
		self.addAction(self.experiment.icon(u"accessories-text-editor"), _("Rename"),
			self.treeitem.rename)
		if self.treeitem.is_deletable():
			self.addAction(self.experiment.icon(u"list-remove"), _("Delete"),
				self.treeitem.delete)
		self.addSeparator()
		self.addAction(self.experiment.icon(u"help"),
			_("%s help") % self.item.item_type.capitalize(),
			self.item.open_help_tab)

	@property
	def item(self):
		return self.treeitem.item
