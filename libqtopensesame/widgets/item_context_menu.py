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
from qtpy import QtCore, QtGui, QtWidgets
from libqtopensesame.misc.config import cfg
from libqtopensesame.misc.base_subcomponent import base_subcomponent
from libqtopensesame.widgets.tree_append_menu import tree_append_menu
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'item_context_menu', category=u'core')


class item_context_menu(base_subcomponent, QtWidgets.QMenu):

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
		self.addAction(self.theme.qicon(self.item.item_icon()), _('Open'),
			self.item.open_tab)
		self.addSeparator()
		self.add_action(u"accessories-text-editor", _("Rename"),
			self.treeitem.start_rename, cfg.shortcut_rename)
		if not self.treewidget.overview_mode and self.treeitem.parent() is not None:
			self.add_action(u"accessories-text-editor",
				_("Edit run-if statement"),
				self.treeitem.start_edit_runif, cfg.shortcut_edit_runif)
		self.addSeparator()
		self.add_action(u"edit-copy", _("Copy (unlinked)"),
			self.treeitem.copy_unlinked, cfg.shortcut_copy_clipboard_unlinked)
		self.add_action(u"edit-copy", _("Copy (linked)"),
			self.treeitem.copy_linked, cfg.shortcut_copy_clipboard_linked)
		if self.treeitem.clipboard_data() is not None:
			self.add_action(u"edit-paste", _("Paste"),
				self.treeitem.paste, cfg.shortcut_paste_clipboard)
		if self.treeitem.is_deletable():
			self.addSeparator()
			self.add_action(u"list-remove", _("Delete"),
				self.treeitem.delete, cfg.shortcut_delete)
			self.add_action(u"list-remove",
				_("Permanently delete all linked copies"),
				self.treeitem.permanently_delete,
				cfg.shortcut_permanently_delete)
		elif self.treeitem.is_unused():
			self.addSeparator()
			self.add_action(u"list-remove", _("Permanently delete"),
				self.treeitem.permanently_delete,
				cfg.shortcut_permanently_delete)
		if self.treeitem.has_append_menu():
			# An append menu for sequence items
			menu = tree_append_menu(self.treeitem.treeWidget(), self.treeitem)
			action = QtWidgets.QAction(self.theme.qicon(u'list-add'),
				u'Append item', self)
			action.setMenu(menu)
			self.addSeparator()
			self.addAction(action)
		self.addSeparator()
		self.add_action(u"help", _("Help"), self.item.open_help_tab)

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

		action = self.addAction(self.theme.qicon(icon), text, func)
		if shortcut is not None:
			action.setShortcut(QtGui.QKeySequence(shortcut))
			action.setShortcutContext(QtCore.Qt.WidgetShortcut)
		return action

	@property
	def item(self):
		return self.treeitem.item

	@property
	def treewidget(self):
		return self.treeitem.treeWidget()
