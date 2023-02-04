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
from qtpy import QtCore, QtWidgets
from libqtopensesame.widgets.tree_base_item import tree_base_item
from libqtopensesame.items.qtstructure_item import qtstructure_item
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'tree_item_item', category=u'core')


class tree_item_item(tree_base_item):

    """
    desc:
            Corresponds to an item widget in the overview area.
    """

    def __init__(self, item, extra_info=None, parent_item=None, index=None):
        """
        desc:
                Constructor.

        arguments:
                item:
                        desc:	An item.
                        type:	qtitem

        keywords:
                extra_info:
                        desc:	Extra info that is shown in the second column. Not shown
                                        in overview mode.
                        type:	[NoneType, unicode]
        """

        super(tree_item_item, self).__init__()
        self.setup(item.main_window)
        self.item = item
        tooltip = _(u"Type: %s\nDescription: %s") % (item.item_type,
                                                     item.var.description)
        self.setText(0, item.name)
        if extra_info is not None:
            self.setText(1, safe_decode(extra_info))
        self.setFlags(QtCore.Qt.ItemIsEditable | self.flags())
        self.setIcon(0, self.theme.qicon(item.item_icon()))
        self.name = item.name
        # Only allow drops on used items
        self._droppable = self.item.name in self.item.experiment.items.used()
        self._draggable = True
        self._lock = False
        self.setToolTip(0, tooltip)

    @property
    def open_tab(self):
        return self.item.open_tab

    @property
    def close_tab(self):
        return self.item.close_tab

    def has_append_menu(self):

        return self.item.item_type == u'sequence'

    def ancestry(self):
        """
        desc:
                Gets the full ancestry of a tree item, i.e. a sequence of items that
                are above the item in the hierarchy. The index of the item in the
                parent is indicated by a ':'. The index is 0 in the case of most
                items, but is mostly necessary for indicating the position in
                sequence items.

                For example:

                        fixdot:2.trial_sequence:0.block_loop:0.experiment:0

        arguments:
                treeitem:
                        desc:	The tree item that contains the item.
                        type:	QTreeWidgetItem

        returns:
                desc:	A (item name, ancestry) tuple. For example:

                                        (u'trial_sequence',
                                        u'trial_sequence:0.block_loop:0.experiment:0')

                type:	tuple
        """

        treeitem = self
        item_name = str(treeitem.text(0))
        l = []
        while True:
            if treeitem.parent() is not None:
                index = treeitem.parent().indexOfChild(treeitem)
            else:
                index = 0
            l.append(str(treeitem.text(0))+u':'+str(index))
            treeitem = treeitem.parent()
            if treeitem is None or not treeitem.droppable:
                break
        return item_name, u'.'.join(l)

    def show_context_menu(self, pos):
        """
        desc:
                Pops up the item context menu.

        arguments:
                pos:
                        desc:	The cursor position.
                        type:	QPoint
        """

        from libqtopensesame.widgets.item_context_menu import item_context_menu
        menu = item_context_menu(self.main_window, self)
        menu.popup(pos)

    def rename(self, from_name, to_name):
        """
        desc:
                Renames an item.

        arguments:
                from_name:
                        desc:	The old item name.
                        type:	unicode
                to_name:
                        desc:	The new item name.
                        type:	unicode
        """

        super(tree_item_item, self).rename(from_name, to_name)
        if str(self.text(0)) == from_name:
            self.setText(0, to_name)
            self.name = to_name

    def start_rename(self):
        """
        desc:
                Goes into edit mode for the item's name.
        """

        self.treeWidget().editItem(self, 0)

    def start_edit_runif(self):
        """
        desc:
                Goes into edit mode for the item's run-if statement. This is only
                applicable to sequences, i.e. not if the treewidget is in overview
                mode.
        """

        if not self.treeWidget().overview_mode:
            self.treeWidget().editItem(self, 1)

    def set_icon(self, name, icon):
        """See tree_base_item."""

        super(tree_item_item, self).set_icon(name, icon)
        if str(self.text(0)) == name:
            self.setIcon(0, self.theme.qicon(icon))

    def drop_hint(self):

        if self.treeWidget().overview_mode or self.parent() is None:
            if self.item.item_type == u'loop':
                return _(u'Set as item to run for %s') % self.name
            if self.item.item_type == u'sequence':
                return _(u'Insert into %s') % self.name
        return _(u'Drop below %s') % self.name

    def is_deletable(self):
        """
        returns:
                desc:	True if the item for this treeitem can be deleted, False
                                otherwise.
                type:	bool
        """

        return hasattr(self.parent(), u'item')

    def is_unused(self):
        """
        returns:
                desc:	True if the item is unused, False otherwise.
                type:	bool
        """

        return self.parent() is not None and self.parent().name == u'__unused__'

    def is_cloneable(self):
        """
        returns:
                desc:	True if the item for this treeitem can be cloned, False
                                otherwise. An item can be cloned if it is in a sequence.
                type:	bool
        """

        if not hasattr(self.parent(), u'item'):
            return False
        if not getattr(self.parent(), u'item').item_type == u'sequence':
            return False
        return True

    def delete(self):
        """
        desc:
                Deletes the item, if possible.
        """

        if not self.is_deletable():
            return
        index = self.parent().indexOfChild(self)
        parent_item = self.parent().item
        parent_item.remove_child_item(self.item.name, index)
        parent_item.update()
        self.experiment.build_item_tree()

    def permanently_delete(self):
        """
        desc:
                Permanently deletes the item, if possible.
        """

        if not self.is_deletable() and not self.is_unused():
            return
        if QtWidgets.QMessageBox.question(self.treeWidget(),
                                          _(u'Permanently delete item'),
                                          _(u'Are you sure you want to permanently delete <b>%s</b>? All linked copies of <b>%s</b> will be deleted. You will not be able to undo this.')
                                          % (self.name, self.name),
                                          buttons=(
                                              QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No),
                                          defaultButton=QtWidgets.QMessageBox.No) \
                != QtWidgets.QMessageBox.Yes:
            return
        del self.item_store[self.name]
        self.close_tab()
        try:
            # Sometimes the treeWidget has already been deleted, in which case
            # this gives an Exception. But it when it hasn't been deleted, a
            # structure_change has to be emitted, otherwise the GUI doesn't
            # update properly.
            self.treeWidget().structure_change.emit()
        except:
            pass

    def copy_unlinked(self):
        """
        desc:
                Copies a snippet of the current item plus children to the keyboard.
        """

        import json

        data = {
            u'type': u'item-snippet',
            u'main-item-name': self.item.name,
            u'items': [],
        }

        for item_name in [self.item.name] \
                + self.experiment.items[self.item.name].children():
            item = self.experiment.items[item_name]
            data[u'items'].append({
                u'item-name': item_name,
                u'item-type': item.item_type,
                u'script': item.to_string()
            })

        text = safe_decode(json.dumps(data))
        QtWidgets.QApplication.clipboard().setText(text)

    def copy_linked(self):
        """
        desc:
                Copies a linked copy to the keyboard
        """

        import json

        data = {
            u'type': u'item-existing',
            u'item-name': self.item.name,
            u'item-type': self.item.item_type,
            u'move': False,
            u'application-id': self.main_window._id(),
            u'ancestry': self.ancestry()[1],
            u'structure-item': isinstance(self.item, qtstructure_item),
        }
        text = safe_decode(json.dumps(data))
        QtWidgets.QApplication.clipboard().setText(text)

    def paste(self):
        """
        desc:
                Pastes clipboard data onto the current item, if possible.
        """

        data = self.clipboard_data()
        if data is None:
            return
        if data[u'type'] == u'item-existing':
            self.treeWidget().drop_event_item_existing(data,
                                                       target_treeitem=self)
        else:
            self.treeWidget().drop_event_item_new(data, target_treeitem=self)

    def clipboard_data(self):
        """
        desc:
                Gets an item data dictionary from the clipboard.

        returns:
                desc:	A data dictionary or None if no valid data was found.
                type:	[dict, NoneType]
        """

        import json
        from libqtopensesame.misc import drag_and_drop

        text = QtWidgets.QApplication.clipboard().text()
        try:
            data = json.loads(text)
        except:
            return None
        if drag_and_drop.matches(data, [u'item-snippet', u'item-existing']):
            return data
        return None
