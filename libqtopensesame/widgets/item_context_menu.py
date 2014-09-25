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
from libqtopensesame.misc.config import cfg
from libqtopensesame.misc.base_subcomponent import base_subcomponent

class item_context_menu(base_subcomponent, QtGui.QMenu):

	"""
	desc:
		Provides a basic context menu for an item.
	"""

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
		self.add_action(u"accessories-text-editor", _("Rename"),
			self.treeitem.start_rename, cfg.shortcut_rename)
		self.addSeparator()
		self.add_action(u"edit-copy", _("Copy to clipboard"),
			self.treeitem.copy, cfg.shortcut_copy_clipboard)
		if self.treeitem.clipboard_data() != None:
			self.add_action(u"edit-paste", _("Paste from clipboard"),
				self.treeitem.paste, cfg.shortcut_paste_clipboard)
		if self.treeitem.is_deletable():
			self.addSeparator()
			self.add_action(u"unused", _("Move to unused items"),
				self.treeitem.delete, cfg.shortcut_delete)
			self.add_action(u"list-remove", _("Permanently delete"),
				self.treeitem.permanently_delete,
				cfg.shortcut_permanently_delete)
		if self.treeitem.is_cloneable():
			self.addSeparator()
			self.add_action(u"edit-copy", _("Create linked copy"),
				self.treeitem.create_linked_copy, cfg.shortcut_linked_copy)
			self.add_action(u"edit-copy", _("Create unlinked copy"),
				self.treeitem.create_unlinked_copy, cfg.shortcut_unlinked_copy)
		self.addSeparator()
		self.add_action(u"help",
			_("%s help") % self.item.item_type.capitalize(),
			self.item.open_help_tab)

	def add_action(self, icon, text, func, shortcut=None):

		"""
		desc:
			A convenience function for adding menu actions.

		arguments:
			icon:	An icon name.
			text:	A menu text.
			func:	A function to call when the action is activated.

		keywords:
			shortcut:	A key sequence to activate the action.

		returns:
			type:	QAction
		"""

		action = self.addAction(self.experiment.icon(icon), text, func)
		if shortcut != None:
			action.setShortcut(QtGui.QKeySequence(shortcut))
			action.setShortcutContext(QtCore.Qt.WidgetShortcut)
		return action

	@property
	def item(self):
		return self.treeitem.item
