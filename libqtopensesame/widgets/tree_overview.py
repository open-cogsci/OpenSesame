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
from libqtopensesame.misc.run_if_delegate import RunIfDelegate
from libqtopensesame.misc.item_name_delegate import ItemNameDelegate
from libqtopensesame.widgets.tree_append_button import TreeAppendButton
from libqtopensesame._input.popup_menu import PopupMenu
from libqtopensesame.items.qtstructure_item import QtStructureItem
from libopensesame.oslogging import oslogger
from libopensesame.sequence import Sequence
from libqtopensesame.misc.translate import translation_context
_ = translation_context('tree_overview', category='core')


class TreeOverview(BaseSubcomponent, BaseDraggable, QtWidgets.QTreeWidget):

    """A tree widget used in sequence items and the overview area."""
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

    def __init__(self, parent, overview_mode=True):
        """Constructor.

        Parameters
        ----------
        parent : qtopensesame
            The main window object.
        overview_mode : int, optional
            Indicates whether the tree should be overview-area style (True) or
            sequence style (False).
        """
        super().__init__(parent)
        self.locked = False
        self.overview_mode = overview_mode
        self.setAcceptDrops(True)
        self.setItemDelegateForColumn(0, ItemNameDelegate(self))
        if self.overview_mode:
            self.setHeaderHidden(True)
        else:
            self.setItemDelegateForColumn(1, RunIfDelegate(self))
            self.setHeaderHidden(False)
            self.setHeaderLabels([_('Item name'), _('Run if')])
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
            QtGui.QColor('#73d216')), 2, QtCore.Qt.SolidLine)
        self.set_supported_drop_types(['item-snippet', 'item-existing',
                                       'url-local'])

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
        """Copies the currently selected treeitem to the clipboard (if
        supported by the treeitem) as an unlinked copy.
        """
        target_treeitem = self.currentItem()
        if target_treeitem is not None:
            target_treeitem.copy_unlinked()

    def copy_item_linked(self):
        """Copies the currently selected treeitem to the clipboard (if
        supported by the treeitem) as a linked copy.
        """
        target_treeitem = self.currentItem()
        if target_treeitem is not None:
            target_treeitem.copy_linked()

    def paste_item(self):
        """Pastes the clipboard onto the currently selected treeitem (if
        supported by the treeitem).
        """
        target_treeitem = self.currentItem()
        if target_treeitem is not None:
            target_treeitem.paste()

    def delete_item(self):
        """Deletes the currently selected treeitem (if supported by the
        treeitem).
        """
        target_treeitem = self.currentItem()
        if target_treeitem is not None:
            target_treeitem.delete()

    def permanently_delete_item(self):
        """Permanently deletes the currently selected treeitem (if supported
        by the treeitem).
        """
        target_treeitem = self.currentItem()
        if target_treeitem is not None:
            target_treeitem.permanently_delete()

    def create_linked_copy(self):
        """Creates a linked copy of the currently selected item (if supported
        by the treeitem).
        """
        target_treeitem = self.currentItem()
        if target_treeitem is not None:
            target_treeitem.create_linked_copy()

    def create_unlinked_copy(self):
        """Creates an unlinked copy of the currently selected item (if
        supported by the treeitem).
        """
        target_treeitem = self.currentItem()
        if target_treeitem is not None:
            target_treeitem.create_unlinked_copy()

    def select_item(self, name, open_tab=True):
        """Selects all items that match the specified name.

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
        """Processes edits to the item names and run-if statements.

        Parameters
        ----------
        treeitem : QTreeWidgetItem
            A tree item
        col : int
            The column that was edited.
        """
        if col == 0:
            if hasattr(treeitem, 'name'):
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
            # Don't allow editing the run-if statement of the top-level
            # sequence if we are in non-overview mode.
            if treeitem.parent() is None:
                self.itemChanged.disconnect()
                treeitem.setText(1, '')
                self.itemChanged.connect(self.text_edited)
                return
            if hasattr(treeitem, 'ancestry'):
                parent_item_name, ancestry = treeitem.ancestry()
                parent_item_name, index = self.parent_from_ancestry(ancestry)
                parent_item = self.experiment.items[parent_item_name]
                if parent_item.item_type == 'sequence':
                    self.itemChanged.disconnect()
                    cond = treeitem.set_extra_info(treeitem.text(1).strip())
                    parent_item.set_run_if(index, cond)
                    self.itemChanged.connect(self.text_edited)
                self.text_change.emit()

    def mousePressEvent(self, e):
        """Initiates a drag event after a mouse press, these are used to
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
            'type': 'item-existing',
            'move': True,
            'item-name': target_item.name,
            'item-type': target_item.item_type,
            'structure-item': isinstance(target_item, QtStructureItem),
            'ancestry': target_item_ancestry,
            'script': target_item.to_string(),
            'application-id': self.main_window._id(),
            'QTreeWidgetItem': str(target_treeitem),
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
        """Starts a pending drag operation (if any)."""
        if self.pending_drag_data is None:
            return
        drag_and_drop.send(self, self.pending_drag_data)
        self.end_drag()
        self.pending_drag_data = None

    def end_drag(self):
        """Ends a drag operation."""
        self.drop_indicator = None
        self.viewport().update()

    def mouseReleaseEvent(self, e):
        """Cancels pending drag operations when the mouse is released to
        quickly. This avoids accidental dragging.

        Parameters
        ----------
        e : QMouseEvent
            A mouse event.
        """
        super().mouseReleaseEvent(e)
        self.pending_drag_data = None

    def parent_from_ancestry(self, ancestry):
        """Gets the parent item, and the index of the item in the parent,
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
        l = ancestry.split('.')
        if len(l) == 1:
            return None, None
        parent_item_name = l[1].split(':')[0]
        index = int(l[0].split(':')[1])
        return parent_item_name, index

    def droppable(self, treeitem, data):
        """Determines if a tree item is able to accept drops.

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
        """Determines if a tree item can be dragged.

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
        """Handles drop events for item moves.

        Parameters
        ----------
        data: dict
            A drop-data dictionary
        e: QDropEvent, optional
        target_tree_item: TreeItemItem, optional
        """
        if not drag_and_drop.matches(data, ['item-existing']):
            if e is not None:
                e.ignore()
            return
        # Only accept existing-item drops from this application
        if data['application-id'] != self.main_window._id():
            oslogger.debug('Drop ignored: from different instance')
            if e is not None:
                e.ignore()
            return
        if target_treeitem is None:
            try:
                pos = e.pos()
            except AttributeError:
                # This seems to be a backwards-incompatibility bug in PyQt6,
                # which has not implemented the pos() function
                pos = e.position().toPoint()
            target_treeitem = self.itemAt(pos)
        if not self.droppable(target_treeitem, data):
            oslogger.debug('Drop ignored: target not droppable')
            if e is not None:
                e.ignore()
            return
        # Don't drop on the same item that was the source (if any)
        if 'QTreeWidgetItem' in data and \
                data['QTreeWidgetItem'] == str(target_treeitem):
            oslogger.debug('Drop ignored: dropping on self')
            if e is not None:
                e.ignore()
            return
        item_name = data['item-name']
        # Check for recursion when dropping sequences and loops. The target item
        # may not have the dropped item in its ancestry. However, the target
        # item may occur multiple times in the experiment, so we need to check
        # that this constraint holds for all linked copies of the target item.
        if data.get('structure-item', False):
            for linked_target_treeitem in self.findItems(
                    target_treeitem.name,
                    QtCore.Qt.MatchFixedString | QtCore.Qt.MatchRecursive
            ):
                target_item_name, target_item_ancestry = (
                    linked_target_treeitem.ancestry()
                )
                if (
                        target_item_ancestry.startswith('%s:' % item_name)
                        or '.%s:' % item_name in target_item_ancestry
                ):
                    oslogger.debug('Drop ignored: recursion prevented')
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
        parent_item_name, index = self.parent_from_ancestry(data['ancestry'])
        if parent_item_name is None:
            oslogger.debug('Drop ignored: no parent')
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
        if data['move']:
            if parent_item_name not in self.experiment.items:
                oslogger.debug(
                    'Don\'t know how to remove item from %s'
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
        """Gets the item and list of newly created items for item-snippet
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
        for item_dict in data['items']:
            if not self.experiment.items.valid_type(item_dict['item-type']):
                raise TypeError(
                    _('Unknown item type: %s') % item_dict['item-type'])
        rename = []
        new_items = []
        main_item = None
        # Loop through all to-be-created items and instantiate them based on
        # the type, name, and script. The script is empty for newly created
        # items, but not for unlinked copies. The name functions as a
        # suggestion, which will be ignored if the suggested name is already
        # taken. In that case, we remember all the renamings and inform all
        # newly created items of this at the very end.
        for item_dict in data['items']:
            item = self.experiment.items.new(item_dict['item-type'],
                                             item_dict['item-name'],
                                             item_dict['script'],
                                             catch_exceptions=False)
            if item_dict['item-name'] == data['main-item-name']:
                main_item = item
            # If the item didn't get the suggested name
            if item.name != item_dict['item-name']:
                rename.append((item_dict['item-name'], item.name))
            new_items.append(item)
            self.extension_manager.fire('new_item', name=item.name,
                                        _type=item.item_type)
        # Inform all newly created items of any renames that occurred
        for old_name, new_name in rename:
            for item in new_items:
                item.rename(old_name, new_name)
        return main_item, [item.name for item in new_items]

    def drop_get_item_existing(self, data):
        """Gets the item and list of newly created items for existing-item
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
        if data['item-name'] not in self.experiment.items:
            raise NameError('Unknown item: %s' % data['item-name'])
        return self.experiment.items[data['item-name']], []

    def drop_event_item_new(self, data, e=None, target_treeitem=None):
        """Handles drop events for item creation.

        Parameters
        ----------
        data : dict
            A drop-data dictionary.
        e : QDropEvent or None, optional
            A drop event or None if a target treeitem is provided.
        target_treeite : TreeBaseItem or None, optional
            A target tree item or None in a drop event is specified.

        Returns
        -------
        bool
            True if the drop was successful, False otherwise.
        """
        self.main_window.set_busy(True)
        if not drag_and_drop.matches(data,
                                     ['item-snippet', 'item-existing']):
            if e is not None:
                e.ignore()
            self.main_window.set_busy(False)
            return False
        # Check that we're not trying to make a linked copy of a non-existent
        # item. This could happen if the user first performs a linked-copy
        # action, then deletes the copied item, and finally tries to paste the
        # linked copy.
        if data['type'] == 'item-existing' and \
                data['item-name'] not in self.experiment.items:
            self.notify(
                _('Cannot create linked copy of "%s". Has '
                  'the item been permanently deleted?') % data['item-name'])
            if e is not None:
                e.ignore()
            self.main_window.set_busy(False)
            return False
        # Determine the tree item on which the drop is performed. While doing
        # so we take into account what seems to be a backwards-incompatibility
        # bug in PyQt6, which has not implemented the pos() function
        if target_treeitem is None:
            try:
                pos = e.pos()
            except AttributeError:
                pos = e.position().toPoint()
            target_treeitem = self.itemAt(pos)
        # Ignore drops on non-droppable tree items.
        if not self.droppable(target_treeitem, data):
            if e is not None:
                e.ignore()
            self.main_window.set_busy(False)
            return False
        # Accept drops on the unused items bin and unused items (i.e. items
        # in the bin)
        if target_treeitem.name == '__unused__' or \
                (target_treeitem.parent() is not None and
                 target_treeitem.parent().name == '__unused__'):
            e.accept()
            self.structure_change.emit()
            self.main_window.set_busy(False)
            return True
        # Get the target item, and ignore the drop action if the target item
        # doesn't exist. (Note that the target item refers to an Item object
        # whereas the target treeitem refers to a TreeItemItem object that
        # represents an Item object in the overview area.)
        target_item_name = target_treeitem.text(0)
        if target_item_name not in self.experiment.items:
            oslogger.debug('Don\'t know how to drop on %s' % target_item_name)
            if e is not None:
                e.ignore()
            self.structure_change.emit()
            self.main_window.set_busy(False)
            return False
        target_item = self.experiment.items[target_item_name]
        # Perform the drop action, which results in an (item name, new_items)
        # tuple, where the item name is the item to be insert into the target
        # item, and the new_items is a list of newly created Items objects,
        # which may be empty (in the case of linked copies)
        if data['type'] == 'item-existing':
            # Perform a linked copy.
            item, new_items = self.drop_get_item_existing(data)
        else:
            # Perform an unlinked copy.
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
                    (0, _('Insert into %s') % target_item.name, 'go-next'),
                    (1, _('Insert after %s') %
                     target_item.name, 'go-down')
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
        """Accept drops.

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
        if data['type'] == 'item-snippet':
            self.drop_event_item_new(data, e)
        elif data['type'] == 'item-existing':
            self.drop_event_item_existing(data, e)
        elif data['type'] == 'url-local':
            self.main_window.open_file(path=data['url'])
            e.accept()
        else:
            e.ignore()
        self.end_drag()

    def dragLeaveEvent(self, e):
        """Cancels the drop indicator when a drag leaves.

        Parameters
        ----------
        e : QDragLeaveEvent
            A drag-move event.
        """
        self.end_drag()

    def dragMoveEvent(self, e):
        """Handles drag-move events to see if the item tree can handle
        incoming drops.

        Parameters
        ----------
        e : QDragMoveEvent
            A drag-move event.
        """
        data = drag_and_drop.receive(e)
        self.drop_indicator = None
        if drag_and_drop.matches(data, ['url-local']):
            e.accept()
            self.end_drag()
            return
        if not drag_and_drop.matches(data, ['item-snippet', 'item-existing']):
            e.accept()
            self.end_drag()
            return
        try:
            pos = e.pos()
        except AttributeError:
            # This seems to be a backwards-incompatibility bug in PyQt6,
            # which has not implemented the pos() function
            pos = e.position().toPoint()
        target = self.itemAt(pos)
        if not self.droppable(target, data):
            self.end_drag()
            e.ignore()
            return
        e.accept()
        # Update the drop indicator
        index = self.indexFromItem(target)
        rect = self.visualRect(index)
        if target.name == '__unused__' or (
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
        """A custom pain event for the drop_indicator.

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
        """Asks a tree item to show a context menu.

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
                current_item.setText(1, 'never')
            elif e.key() in [QtCore.Qt.Key_Plus, QtCore.Qt.Key_Equal]:
                current_item.setText(1, 'always')

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
        """Renames an item.

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
        """Changes an item's icon.

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
        """Edits the run-if statement. This is not applicable in overview
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
        """Edits the item name."""
        target_treeitem = self.currentItem()
        if target_treeitem is not None \
                and target_treeitem.flags() & QtCore.Qt.ItemIsEditable:
            self.editItem(target_treeitem, 0)

    def setup(self, main_window):
        """This function needs to be overridden so that the append button is
        also set up.
        """
        super().setup(main_window)
        if self.append_button is not None:
            self.append_button.setup(main_window)

    def clear(self):
        """If the tree is cleared, we need to unset the target tree item in
        the append menu (if any).
        """
        super().clear()
        if self.append_button is None:
            return
        self.append_button.append_menu.target_treeitem = None

    def focusInEvent(self, e):
        """Select the general tab if no item is currently selected."""
        super().focusInEvent(e)
        if len(self.selectedItems()) == 0:
            self.setCurrentItem(self.topLevelItem(0))


# Alias for backwards compatibility
tree_overview = TreeOverview
