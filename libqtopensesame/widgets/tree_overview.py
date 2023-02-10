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
from qtpy import QtGui, QtCore, QtWidgets
from libqtopensesame.misc.config import cfg
from libqtopensesame.misc import drag_and_drop
from libqtopensesame.misc.shortcut import Shortcut
from libqtopensesame.misc.base_subcomponent import BaseSubcomponent
from libqtopensesame.misc.base_draggable import BaseDraggable
from libqtopensesame.widgets.tree_append_button import TreeAppendButton
from libqtopensesame._input.popup_menu import PopupMenu
from libqtopensesame.items.qtstructure_item import QtStructureItem
from libopensesame.oslogging import oslogger
from libopensesame.exceptions import osexception
from libopensesame.sequence import Sequence
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'tree_overview', category=u'core')


class TreeOverview(BaseSubcomponent, BaseDraggable, QtWidgets.QTreeWidget):

    r"""A tree widget used in sequence items and the overview area."""
    structure_change = QtCore.Signal()
    text_change = QtCore.Signal()

    NAVIGATION_KEYS = [
        QtCore.Qt.Key_Up,
        QtCore.Qt.Key_Down,
        QtCore.Qt.Key_PageUp,
        QtCore.Qt.Key_PageDown,
        QtCore.Qt.Key_Home,
        QtCore.Qt.Key_End,
        QtCore.Qt.Key_Return
    ]

    def __init__(self, main_window, overview_mode=True):
        r"""Constructor.

        Parameters
        ----------
        main_window : qtopensesame
            The main window object.
        overview_mode : int, optional
            Indicates whether the tree should be overview-area style (True) or
            sequence style (False).
        """
        super().__init__(main_window)
        self.locked = False
        self.overview_mode = overview_mode
        self.setAcceptDrops(True)
        if self.overview_mode:
            self.setHeaderHidden(True)
        else:
            self.setHeaderHidden(False)
            self.setHeaderLabels([_(u'Item name'), _(u'Run if')])
        self.setAlternatingRowColors(True)
        self.itemChanged.connect(self.text_edited)
        self.pending_drag_data = None
        self.drag_timer = None
        self.inhibit_drag = False
        if not self.overview_mode:
            Shortcut(self, cfg.shortcut_edit_runif, self.start_edit_runif)
            self.append_button = TreeAppendButton(self)
        else:
            self.append_button = None
        Shortcut(self, cfg.shortcut_context_menu, self.show_context_menu)
        Shortcut(self, cfg.shortcut_rename, self.start_rename)
        Shortcut(self, cfg.shortcut_copy_clipboard_unlinked,
                 self.copy_item_unlinked)
        Shortcut(self, cfg.shortcut_copy_clipboard_linked,
                 self.copy_item_linked)
        Shortcut(self, cfg.shortcut_paste_clipboard, self.paste_item)
        Shortcut(self, cfg.shortcut_delete, self.delete_item)
        Shortcut(self, cfg.shortcut_permanently_delete,
                 self.permanently_delete_item)
        self.drop_indicator = None
        self.drop_indicator_pen = QtGui.QPen(QtGui.QBrush(
            QtGui.QColor(u'#73d216')), 2, QtCore.Qt.SolidLine)
        self.set_supported_drop_types([u'item-snippet', u'item-existing',
                                       u'url-local'])

    def items(self):

        l = []
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            l += [item] + item.children()
        return l

    def default_fold_state(self):

        self.topLevelItem(0).expand()
        if self.topLevelItemCount() > 0:
            self.topLevelItem(1).collapse()

    def get_fold_state(self):

        fold_state = {}
        for item in self.items():
            fold_state[item.path()] = item.isExpanded()
        return fold_state

    def set_fold_state(self, fold_state):

        for item in self.items():
            a = item.path()
            if a in fold_state:
                item.setExpanded(fold_state[a])
            else:
                item.expand()

    def show_context_menu(self):

        item = self.currentItem()
        if item is None:
            return
        index = self.indexFromItem(item)
        rect = self.visualRect(index)
        item.show_context_menu(self.mapToGlobal(rect.topLeft()))

    def copy_item_unlinked(self):
        r"""Copies the currently selected treeitem to the clipboard (if
        supported by the treeitem) as an unlinked copy.
        """
        target_treeitem = self.currentItem()
        if target_treeitem is not None:
            target_treeitem.copy_unlinked()

    def copy_item_linked(self):
        r"""Copies the currently selected treeitem to the clipboard (if
        supported by the treeitem) as a linked copy.
        """
        target_treeitem = self.currentItem()
        if target_treeitem is not None:
            target_treeitem.copy_linked()

    def paste_item(self):
        r"""Pastes the clipboard onto the currently selected treeitem (if
        supported by the treeitem).
        """
        target_treeitem = self.currentItem()
        if target_treeitem is not None:
            target_treeitem.paste()

    def delete_item(self):
        r"""Deletes the currently selected treeitem (if supported by the
        treeitem).
        """
        target_treeitem = self.currentItem()
        if target_treeitem is not None:
            target_treeitem.delete()

    def permanently_delete_item(self):
        r"""Permanently deletes the currently selected treeitem (if supported
        by the treeitem).
        """
        target_treeitem = self.currentItem()
        if target_treeitem is not None:
            target_treeitem.permanently_delete()

    def create_linked_copy(self):
        r"""Creates a linked copy of the currently selected item (if supported
        by the treeitem).
        """
        target_treeitem = self.currentItem()
        if target_treeitem is not None:
            target_treeitem.create_linked_copy()

    def create_unlinked_copy(self):
        r"""Creates an unlinked copy of the currently selected item (if
        supported by the treeitem).
        """
        target_treeitem = self.currentItem()
        if target_treeitem is not None:
            target_treeitem.create_unlinked_copy()

    def select_item(self, name, open_tab=True):
        r"""Selects all items that match the specified name.

        Parameters
        ----------
        name
            The name to select.
        """
        self.clearSelection()
        l = self.findItems(name,
                           QtCore.Qt.MatchFixedString | QtCore.Qt.MatchRecursive, 0)
        if len(l) == 0:
            return
        for _l in l:
            _l.setSelected(True)
        if open_tab:
            self.experiment.items[name].open_tab(select_in_tree=False)

    def text_edited(self, treeitem, col):
        r"""Processes edits to the item names and run-if statements.

        Parameters
        ----------
        treeitem : QTreeWidgetItem
            A tree item
        col : int
            The column that was edited.
        """
        if col == 0:
            if hasattr(treeitem, u'name'):
                from_name = treeitem.name
                to_name = self.experiment.items.rename(
                    from_name, treeitem.text(0))
                if to_name is None:
                    self.itemChanged.disconnect()
                    treeitem.setText(0, from_name)
                    self.itemChanged.connect(self.text_edited)
                    to_name = from_name
                if from_name != to_name:
                    self.itemChanged.disconnect()
                    treeitem.setText(0, to_name)
                    self.itemChanged.connect(self.text_edited)
                treeitem.name = to_name
                self.text_change.emit()
        elif col == 1:
            # Don't allow editing the run-if statement of the top-level sequence
            # if we are in non-overview mode.
            if treeitem.parent() is None:
                self.itemChanged.disconnect()
                treeitem.setText(1, u'')
                self.itemChanged.connect(self.text_edited)
                return
            if hasattr(treeitem, u'ancestry'):
                parent_item_name, ancestry = treeitem.ancestry()
                parent_item_name, index = self.parent_from_ancestry(ancestry)
                parent_item = self.experiment.items[parent_item_name]
                if parent_item.item_type == u'sequence':
                    cond = str(treeitem.text(1))
                    if cond.strip() == u'':
                        cond = u'always'
                    parent_item.set_run_if(index, cond)
                    self.itemChanged.disconnect()
                    treeitem.setText(1, cond)
                    self.itemChanged.connect(self.text_edited)
                self.text_change.emit()

    def mousePressEvent(self, e):
        r"""Initiates a drag event after a mouse press, these are used to
        implement item moving, shallow copying, and deep copying.

        Parameters
        ----------
        e : QMouseEvent
            A mouse event.
        """
        super().mousePressEvent(e)
        if e.buttons() != QtCore.Qt.LeftButton:
            return
        # Get item and open tab.
        target_treeitem = self.itemAt(e.pos())
        if target_treeitem is None:
            return
        # When opening a tab takes a while, a drag may be inadvertently
        # started. For that reason, items can set the inhibit_drag flag to
        # True so that a drag is inhibited, but only once.
        self.inhibit_drag = False
        if self.overview_mode:
            target_treeitem.open_tab()
        # Only start drags for draggable tree items.
        if self.inhibit_drag or not self.draggable(target_treeitem):
            e.ignore()
            return
        # Get the target item
        target_item_name, target_item_ancestry = target_treeitem.ancestry()
        # Automated bug reports suggest that target_item_name can sometimes be
        # an empty string. How this is possible is unclear, but this should
        # avoid these mysterious crashes.
        if not target_item_name:
            e.ignore()
            return
        target_item = self.experiment.items[target_item_name]
        data = {
            u'type': u'item-existing',
            u'move': True,
            u'item-name': target_item.name,
            u'item-type': target_item.item_type,
            u'structure-item': isinstance(target_item, QtStructureItem),
            u'ancestry': target_item_ancestry,
            u'script': target_item.to_string(),
            u'application-id': self.main_window._id(),
            u'QTreeWidgetItem': str(target_treeitem),
        }
        # Drags are not started right away, but only after the mouse has been
        # pressed for a minimum interval. To accomplish this, we set a timer,
        # and cancel the timer when the mouse cursor is released.
        if self.drag_timer is not None:
            self.drag_timer.stop()
        self.pending_drag_data = data
        self.drag_timer = QtCore.QTimer()
        self.drag_timer.setSingleShot(True)
        self.drag_timer.setInterval(cfg.start_drag_delay)
        self.drag_timer.timeout.connect(self.start_drag)
        self.drag_timer.start()

    def start_drag(self):
        r"""Starts a pending drag operation (if any)."""
        if self.pending_drag_data is None:
            return
        drag_and_drop.send(self, self.pending_drag_data)
        self.end_drag()
        self.pending_drag_data = None

    def end_drag(self):
        r"""Ends a drag operation."""
        self.drop_indicator = None
        self.viewport().update()

    def mouseReleaseEvent(self, e):
        r"""Cancels pending drag operations when the mouse is released to
        quickly. This avoids accidental dragging.

        Parameters
        ----------
        e : QMouseEvent
            A mouse event.
        """
        super().mouseReleaseEvent(e)
        self.pending_drag_data = None

    def parent_from_ancestry(self, ancestry):
        r"""Gets the parent item, and the index of the item in the parent,
        based on an item's ancestry, as returned by ancestry_from_treeitem.

        Parameters
        ----------
        ancestry : unicode
            An ancestry string.

        Returns
        -------
        tuple
            A (parent item name, index) tuple.
        """
        l = ancestry.split(u'.')
        if len(l) == 1:
            return None, None
        parent_item_name = l[1].split(u':')[0]
        index = int(l[0].split(u':')[1])
        return parent_item_name, index

    def droppable(self, treeitem, data):
        r"""Determines if a tree item is able to accept drops.

        Parameters
        ----------
        treeitem : QTreeWidgetItem
            A tree item.
        data : dict
            Drag-and-drop data.

        Returns
        -------
        bool
            A bool indicating if the tree item is droppable.
        """
        return treeitem is not None and treeitem.droppable(data)

    def draggable(self, treeitem):
        r"""Determines if a tree item can be dragged.

        Parameters
        ----------
        treeitem : QTreeWidgetItem
            A tree item.

        Returns
        -------
        bool
            A bool indicating if the tree item is draggable.
        """
        return treeitem is not None and treeitem.draggable()

    def drop_event_item_existing(self, data, e=None, target_treeitem=None):
        """
        desc:
                Handles drop events for item moves.

        arguments:
                data:
                        desc:	A drop-data dictionary.
                        type:	dict:
                e:
                        desc:	A drop event.
                        type:	QDropEvent
        """
        if not drag_and_drop.matches(data, [u'item-existing']):
            if e is not None:
                e.ignore()
            return
        # Only accept existing-item drops from this application
        if data[u'application-id'] != self.main_window._id():
            oslogger.debug(u'Drop ignored: from different instance')
            if e is not None:
                e.ignore()
            return
        if target_treeitem is None:
            target_treeitem = self.itemAt(e.pos())
        if not self.droppable(target_treeitem, data):
            oslogger.debug(u'Drop ignored: target not droppable')
            if e is not None:
                e.ignore()
            return
        # Don't drop on the same item that was the source (if any)
        if u'QTreeWidgetItem' in data and \
                data[u'QTreeWidgetItem'] == str(target_treeitem):
            oslogger.debug(u'Drop ignored: dropping on self')
            if e is not None:
                e.ignore()
            return
        item_name = data[u'item-name']
        # Check for recursion when dropping sequences and loops. The target item
        # may not have the dropped item in its ancestry. However, the target
        # item may occur multiple times in the experiment, so we need to check
        # that this constraint holds for all linked copies of the target item.
        if data.get(u'structure-item', False):
            for linked_target_treeitem in self.findItems(
                    target_treeitem.name,
                    QtCore.Qt.MatchFixedString | QtCore.Qt.MatchRecursive
            ):
                target_item_name, target_item_ancestry = (
                    linked_target_treeitem.ancestry()
                )
                if (
                        target_item_ancestry.startswith(u'%s:' % item_name)
                        or u'.%s:' % item_name in target_item_ancestry
                ):
                    oslogger.debug(u'Drop ignored: recursion prevented')
                    if e is not None:
                        e.ignore()
                    return
            # If the dropped item is in the unused items bin, then we need to
            # check whether the target item is a child.
            if item_name in self.unused_items():
                if (
                        target_treeitem.name
                        in self.experiment.items[item_name].children()
                ):
                    if e is not None:
                        e.ignore()
                    return
        # Don't drop on undroppable parents
        parent_item_name, index = self.parent_from_ancestry(data[u'ancestry'])
        if parent_item_name is None:
            oslogger.debug(u'Drop ignored: no parent')
            if e is not None:
                e.ignore()
            return
        # The logic below is a bit complicated, but works as follows:
        # - If we're in a move action, remove the dragged item from its parent,
        #   and set need_restore so that we know this happened.
        # - Try to drop the dragged item onto the target item
        # - If the drop action was unsuccesful, and if need_restore is set,
        #   re-add the dragged item to its former parent.
        need_restore = False
        if data[u'move']:
            if parent_item_name not in self.experiment.items:
                oslogger.debug(
                    u'Don\'t know how to remove item from %s'
                    % parent_item_name
                )
            else:
                self.locked = True
                need_restore = True
                self.experiment.items[parent_item_name].remove_child_item(
                    item_name,
                    index
                )
                self.locked = False
        if self.drop_event_item_new(data, e, target_treeitem=target_treeitem):
            if not data['move']:
                self.extension_manager.fire('new_linked_copy', name=item_name)
            return
        if need_restore:
            self.experiment.items[parent_item_name].insert_child_item(
                item_name,
                index
            )
            self.experiment.build_item_tree()

    def drop_get_item_snippet(self, data):
        r"""Gets the item and list of newly created items for item-snippet
        drops.

        Parameters
        ----------
        data : dict
            The drop data.

        Returns
        -------
        tuple
            An (name, new_items) tuple.
        """
        for item_dict in data[u'items']:
            if not self.experiment.items.valid_type(item_dict[u'item-type']):
                raise osexception(
                    _(u'Unknown item type: %s') % item_dict[u'item-type'])
        rename = []
        new_items = []
        main_item = None
        for item_dict in data[u'items']:
            item = self.experiment.items.new(item_dict[u'item-type'],
                                             item_dict[u'item-name'], item_dict[u'script'],
                                             catch_exceptions=False)
            if item_dict[u'item-name'] == data[u'main-item-name']:
                main_item = item
            # If the item didn't get the suggested name
            if item.name != item_dict[u'item-name']:
                rename.append((item_dict[u'item-name'], item.name))
            new_items.append(item)
            self.extension_manager.fire(u'new_item', name=item.name,
                                        _type=item.item_type)
        # Inform all newly created items of any renames that occurred
        for old_name, new_name in rename:
            for item in new_items:
                item.rename(old_name, new_name)
        return main_item, [item.name for item in new_items]

    def drop_get_item_existing(self, data):
        r"""Gets the item and list of newly created items for existing-item
        drops.

        Parameters
        ----------
        data : dict
            The drop data.

        Returns
        -------
        tuple
            An (name, new_items) tuple, where new_items is always empty for
            existing-item drops.
        """
        if data[u'item-name'] not in self.experiment.items:
            raise osexception(u'Unknown item: %s' % data[u'item-name'])
        return self.experiment.items[data[u'item-name']], []

    def drop_event_item_new(self, data, e=None, target_treeitem=None):
        """
        desc:
                Handles drop events for item creation.

        arguments:
                data:
                        desc:	A drop-data dictionary.
                        type:	dict:

        keywords:
                e:
                        desc:	A drop event or None if a target treeitem is provided.
                        type:	[QDropEvent, NoneType]
                target_treeitem:
                        desc:	A target tree item or None in a drop event is specified.
                        type:	[tree_base_item, NoneType]

        returns:
                desc:	True if the drop was successful, False otherwise.
                type:	bool
        """
        self.main_window.set_busy(True)
        if not drag_and_drop.matches(data, [u'item-snippet', u'item-existing']):
            if e is not None:
                e.ignore()
            self.main_window.set_busy(False)
            return False
        if (
                data[u'type'] == u'item-existing'
                and data[u'item-name'] not in self.experiment.items
        ):
            self.notify(_(u'Cannot create linked copy of "%s". Has '
                          u'the item been permanently deleted?') % data[u'item-name'])
            if e is not None:
                e.ignore()
            self.main_window.set_busy(False)
            return False
        # Ignore drops on non-droppable tree items.
        if target_treeitem is None:
            target_treeitem = self.itemAt(e.pos())
        if not self.droppable(target_treeitem, data):
            if e is not None:
                e.ignore()
            self.main_window.set_busy(False)
            return False
        # Accept drops on the unused items bin and unused items (i.e. items
        # in the bin)
        if target_treeitem.name == u'__unused__' or \
                (target_treeitem.parent() is not None and
                 target_treeitem.parent().name == u'__unused__'):
            e.accept()
            self.structure_change.emit()
            self.main_window.set_busy(False)
            return True
        # Get the target item, check if it exists, and, if so, drop the source
        # item on it.
        target_item_name = target_treeitem.text(0)
        if target_item_name not in self.experiment.items:
            oslogger.debug(u'Don\'t know how to drop on %s' % target_item_name)
            if e is not None:
                e.ignore()
            self.structure_change.emit()
            self.main_window.set_busy(False)
            return False
        target_item = self.experiment.items[target_item_name]
        if data[u'type'] == u'item-existing':
            item, new_items = self.drop_get_item_existing(data)
        else:
            # Creating an item may fail, and we therefore need to clean up when
            # this happens. But we don't catch the Exception itself, because it
            # will be handled with higher up, for example by the bug_report
            # extension.
            try:
                item = None
                item, new_items = self.drop_get_item_snippet(data)
            finally:
                if item is None:
                    if e is not None:
                        e.ignore()
                    self.structure_change.emit()
                    self.main_window.set_busy(False)
                    self.end_drag()
        inserted = False
        # If the item has no parent or if it is the experiment starting point,
        # we insert into it directly.
        if target_treeitem.parent() is None or \
                target_item.name == self.experiment.var.start:
            target_item.insert_child_item(item.name)
            inserted = True
        else:
            if isinstance(target_item, QtStructureItem):
                self.main_window.set_busy(False)
                resp = PopupMenu(self, [
                    (0, _('Insert into %s') % target_item.name, u'go-next'),
                    (1, _('Insert after %s') %
                     target_item.name, u'go-down')
                ]).show()
                # If the popup was cancelled
                if resp is None:
                    if e is not None:
                        e.accept()
                    self.main_window.set_busy(False)
                    for item in new_items:
                        del self.experiment.items[item]
                    return False
                # If the user chose to insert into the target item
                if resp == 0:
                    target_item.insert_child_item(item.name)
                    inserted = True
        # Otherwise, we find the parent of the target item, and insert the
        # new item at the correct position.
        if not inserted:
            while True:
                try:
                    parent_treeitem = target_treeitem.parent()
                except:
                    # A race condition can occur in which the tree_overview has
                    # been rebuild, thus destroying target_treeitem. If this
                    # happens, we re-take target_treeitem based on the mouse
                    # coordinates.
                    target_treeitem = self.itemAt(e.pos())
                    parent_treeitem = target_treeitem.parent()
                if parent_treeitem is None:
                    e.accept()
                    del self.experiment.items[item.name]
                    self.main_window.set_busy(False)
                    return False
                parent_item_name = str(parent_treeitem.text(0))
                parent_item = self.experiment.items[parent_item_name]
                if isinstance(parent_item, Sequence):
                    break
                target_treeitem = parent_treeitem
            index = parent_treeitem.indexOfChild(target_treeitem) + 1
            # Below we correct the index when an item is moved down in the same
            # sequence. In this case, the item is first removed from the
            # sequence (in drop_event_item_existing) and because the treewidget
            # is not refreshed, the index as returned by the parent_treeitem
            # is one too high. (This is clearly a hack, but it seems to work.)
            children = parent_item.direct_children()
            if len(children) > 1:
                try:
                    if (
                            children[index - 1] != target_item.name and
                            children[index - 2] == target_item.name
                    ):
                        index -= 1
                except IndexError:
                    pass
            parent_item.insert_child_item(item.name, index=index)
        if e is not None:
            e.accept()
        self.structure_change.emit()
        if self.overview_mode:
            item.open_tab()
        self.main_window.set_busy(False)
        return True

    def dropEvent(self, e):
        r"""Accept drops.

        Parameters
        ----------
        e : QDragLeaveEvent
            A drop event.
        """
        # The focusOutEvent arrives too late, so here we explictly give the
        # currently opened item the opportunity to get ready
        item_name = self.tabwidget.current_item()
        if item_name is not None:
            self.item_store[item_name].get_ready()
        data = drag_and_drop.receive(e)
        if data[u'type'] == u'item-snippet':
            self.drop_event_item_new(data, e)
        elif data[u'type'] == u'item-existing':
            self.drop_event_item_existing(data, e)
        elif data[u'type'] == u'url-local':
            self.main_window.open_file(path=data[u'url'])
            e.accept()
        else:
            e.ignore()
        self.end_drag()

    def dragLeaveEvent(self, e):
        r"""Cancels the drop indicator when a drag leaves.

        Parameters
        ----------
        e : QDragLeaveEvent
            A drag-move event.
        """
        self.end_drag()

    def dragMoveEvent(self, e):
        r"""Handles drag-move events to see if the item tree can handle
        incoming drops.

        Parameters
        ----------
        e : QDragMoveEvent
            A drag-move event.
        """
        data = drag_and_drop.receive(e)
        self.drop_indicator = None
        if drag_and_drop.matches(data, [u'url-local']):
            e.accept()
            self.end_drag()
            return
        if not drag_and_drop.matches(data, [u'item-snippet', u'item-existing']):
            e.accept()
            self.end_drag()
            return
        target = self.itemAt(e.pos())
        if not self.droppable(target, data):
            self.end_drag()
            e.ignore()
            return
        e.accept()
        # Update the drop indicator
        index = self.indexFromItem(target)
        rect = self.visualRect(index)
        if target.name == u'__unused__' or (
                target.item.name in self.experiment.items.used() and
                isinstance(target.item, QtStructureItem) and
                target.item.name != self.experiment.var.start and
                target.parent() is not None):
            self.drop_indicator = rect
        else:
            self.drop_indicator = QtCore.QRect(rect.left(), rect.bottom(),
                                               rect.width(), 0)
        self.viewport().update()

    def paintEvent(self, e):
        r"""A custom pain event for the drop_indicator.

        Parameters
        ----------
        e : QPaintEvent
        """
        painter = QtGui.QPainter(self.viewport())
        self.drawTree(painter, e.region())
        if self.drop_indicator is not None:
            painter.setPen(self.drop_indicator_pen)
            if self.drop_indicator.height() == 0:
                painter.drawLine(self.drop_indicator.topLeft(),
                                 self.drop_indicator.topRight())
            else:
                painter.drawRect(self.drop_indicator)

    def contextMenuEvent(self, e):
        r"""Asks a tree item to show a context menu.

        Parameters
        ----------
        e : QContextMenuEvent
        """
        item = self.itemAt(e.pos())
        if item is not None:
            item.show_context_menu(e.globalPos())

    def keyPressEvent(self, e):
        """
        Capture key presses to auto-activate selected items

        Arguments:
        e -- a QKeyEvent
        """
        super().keyPressEvent(e)
        current_item = self.currentItem()
        if current_item is None:
            return
        # In overview mode, navigating through the items causes tabs to be
        # opened
        if self.overview_mode:
            if e.key() in self.NAVIGATION_KEYS:
                current_item.open_tab()
            return
        # In sequence view, the run-if statements can be changed using
        # Control+Plus (always) and Control+Minus (never)
        if QtCore.Qt.ControlModifier & e.modifiers():
            if e.key() == QtCore.Qt.Key_Minus:
                current_item.setText(1, u'never')
            elif e.key() in [QtCore.Qt.Key_Plus, QtCore.Qt.Key_Equal]:
                current_item.setText(1, u'always')

    def recursive_children(self, item):
        """
        Get a list of unused items from the itemtree

        Returns:
        A list of items (strings) that are children of the parent item
        """
        children = []
        for i in range(item.childCount()):
            child = item.child(i)
            children.append(str(child.text(0)))
            children += self.recursive_children(child)
        return children

    def unused_items(self):
        """
        Get a list of unused items

        Returns:
        A list of unused items (names as strings)
        """
        return self.main_window.ui.itemtree.recursive_children(
            self.main_window.ui.itemtree.topLevelItem(
                self.main_window.ui.itemtree.topLevelItemCount()-1))

    def rename(self, from_name, to_name):
        r"""Renames an item.

        Parameters
        ----------
        from_name : unicode
            The old name.
        to_name : unicode
            The new name.
        """
        self.itemChanged.disconnect()
        for i in range(self.topLevelItemCount()):
            self.topLevelItem(i).rename(from_name, to_name)
        self.itemChanged.connect(self.text_edited)

    def set_icon(self, name, icon):
        r"""Changes an item's icon.

        Parameters
        ----------
        name : unicode
            The item name.
        icon : unicode
            The icon name.
        """
        self.itemChanged.disconnect()
        for i in range(self.topLevelItemCount()):
            self.topLevelItem(i).set_icon(name, icon)
        self.itemChanged.connect(self.text_edited)

    def start_edit_runif(self):
        r"""Edits the run-if statement. This is not applicable in overview
        mode.
        """
        if self.overview_mode:
            return
        target_treeitem = self.currentItem()
        if target_treeitem is None:
            return
        if target_treeitem.parent() is None:
            # The top-level item is the sequence itself, which doesn't have a
            # run-if statement.
            return
        self.editItem(target_treeitem, 1)

    def start_rename(self):
        r"""Edits the item name."""
        target_treeitem = self.currentItem()
        if target_treeitem is not None \
                and target_treeitem.flags() & QtCore.Qt.ItemIsEditable:
            self.editItem(target_treeitem, 0)

    def setup(self, main_window):
        r"""This function needs to be overridden so that the append button is
        also set up.
        """
        super().setup(main_window)
        if self.append_button is not None:
            self.append_button.setup(main_window)

    def clear(self):
        r"""If the tree is cleared, we need to unset the target tree item in
        the append menu (if any).
        """
        super().clear()
        if self.append_button is None:
            return
        self.append_button.append_menu.target_treeitem = None

    def focusInEvent(self, e):
        r"""Select the general tab if no item is currently selected."""
        super().focusInEvent(e)
        if len(self.selectedItems()) == 0:
            self.setCurrentItem(self.topLevelItem(0))


# Alias for backwards compatibility
tree_overview = TreeOverview
