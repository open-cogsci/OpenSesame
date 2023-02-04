# -*- coding:utf-8 -*-

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
from libqtopensesame.misc.base_subcomponent import base_subcomponent
from libopensesame import plugins
from qtpy import QtWidgets, QtGui
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'tree_append_menu', category=u'core')


class append_existing_action(base_subcomponent, QtWidgets.QAction):

    """
    desc:
            An action for appending existing items, either as linked or unlinked
            copies.
    """

    def __init__(self, append_menu, menu, item_name):
        """
        desc:
                Constructor.

        arguments:
                append_menu:
                        desc:	The main menu.
                        type:	tree_append_menu
                menu:
                        desc:	The submenu for this action.
                        type:	QMenu
                item_name:
                        desc:	The name of the item to be appended.
                        type:	unicode
        """

        super(append_existing_action, self).__init__(menu)
        self.setup(append_menu)
        self.setText(item_name)
        self.item_name = item_name
        self.setIcon(
            self.theme.qicon(self.experiment.items[item_name].item_icon()))

    def append_item(self, target_item_name):
        """
        desc:
                Performs the append operation.

        arguments:
                target_item_name:
                        desc:	The name of the item (normally a sequence) to which the
                                        append should be applied.
                        type:	unicode
        """

        target_item = self.experiment.items[target_item_name]
        item_name = self.item_name
        target_item.insert_child_item(item_name, len(target_item.items))


class append_new_action(base_subcomponent, QtWidgets.QAction):

    """
    desc:
            An action for appending a new item.
    """

    def __init__(self, append_menu, menu, item_type):
        """
        desc:
                Constructor.

        arguments:
                append_menu:
                        desc:	The main menu.
                        type:	tree_append_menu
                menu:
                        desc:	The submenu for this action.
                        type:	QMenu
                item_type:
                        desc:	The type of item to be created and appended.
                        type:	unicode
        """

        super(append_new_action, self).__init__(menu)
        self.setup(append_menu)
        self.item_type = item_type
        self.setText(item_type)
        if item_type not in self.experiment.core_items:
            icon = self.theme.qicon(plugins.plugin_icon_small(item_type))
        else:
            icon = self.theme.qicon(item_type)
        self.setIcon(icon)

    def append_item(self, target_item_name):
        """
        desc:
                Performs the append operation.

        arguments:
                target_item_name:
                        desc:	The name of the item (normally a sequence) to which the
                                        append should be applied.
                        type:	unicode
        """

        target_item = self.experiment.items[target_item_name]
        item = self.experiment.items.new(
            self.item_type, catch_exceptions=False)
        if item is not None:
            target_item.insert_child_item(item.name, len(target_item.items))


class tree_append_menu(base_subcomponent, QtWidgets.QMenu):

    """
    desc:
            An append item menu.
    """

    def __init__(self, tree_overview, target_treeitem=None):
        """
        desc:
                Constructor.

        arguments:
                tree_overview:
                        desc:	The tree_overview with which this menu is associated.
                        type:	tree_overview

        keywords:
                target_treeitem:
                        desc:	The treewidget item which corresponds to the sequence to
                                        which the append operation should be applied. If `None`,
                                        the top-level item from the tree_overview is used.
                        type:	tree_item_item
        """

        super(tree_append_menu, self).__init__(tree_overview)
        self.setup(tree_overview)
        self.target_treeitem = target_treeitem
        self.tree_overview = tree_overview
        self.action_new_items = QtWidgets.QAction(self.theme.qicon(u'list-add'),
                                                  _(u'Append new item'), self)
        self.addAction(self.action_new_items)
        self.action_linked_copy = QtWidgets.QAction(self.theme.qicon(u'edit-copy'),
                                                    _(u'Append existing item (linked)'), self)
        self.addAction(self.action_linked_copy)
        self.aboutToShow.connect(self.refresh)
        self.triggered.connect(self.append_item)
        self._new_items_menu = None

    def append_item(self, action):
        """
        desc:
                Performs the append action.

        arguments:
                action:
                        desc:	A append_existing_action or append_new_action.
                        type:	QAction
        """

        target_item_name, target_item_ancestry = self.target_treeitem.ancestry()
        action.append_item(target_item_name)
        self.tree_overview.structure_change.emit()
        if self.tree_overview.overview_mode:
            # In overview mode, we need to explicitly update the target item,
            # because this is not linked to the structure_change signal.
            self.experiment.items[target_item_name].update()

    def refresh(self):
        """
        desc:
                Refreshes the menu before it is shown. This is necessary because the
                structure of the experiment may change.
        """

        self._items = None
        if self.target_treeitem is None:
            self.target_treeitem = self.tree_overview.topLevelItem(0)
        self.action_linked_copy.setMenu(self.existing_items_menu())
        self.action_new_items.setMenu(self.new_items_menu())

    def existing_items_menu(self):
        """
        desc:
                Generates a menu with existing items.

        keywords:
                linked:
                        desc:	Indicates whether the actions should result in linked
                                        (True) or unliked (False) copies.
                        type:	bool

        returns:
                type:	QMenu
        """

        self._items = []
        target_item_name = self.target_treeitem.item.name
        for item_name in self.experiment.items:
            if target_item_name in \
                    self.experiment.items[item_name].children() or \
                    item_name == target_item_name:
                continue
            self._items.append(item_name)
        self._items.sort()
        m = QtWidgets.QMenu(self)
        for item_name in self._items:
            m.addAction(append_existing_action(self, m, item_name))
        return m

    def new_items_menu(self):
        """
        desc:
                Generates a menu with new items.

        returns:
                type:	QMenu
        """

        if self._new_items_menu is not None:
            return self._new_items_menu
        self._new_items_menu = QtWidgets.QMenu(self)
        for item_type in self.experiment.core_items + [None] + \
                sorted(plugins.list_plugins()):
            if item_type is None:
                self._new_items_menu.addSeparator()
            else:
                self._new_items_menu.addAction(
                    append_new_action(self, self._new_items_menu, item_type))
        return self._new_items_menu
