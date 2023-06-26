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
from libqtopensesame.extensions import BaseExtension, suspend_events
from libqtopensesame.items.qtstructure_item import qtstructure_item
from qtpy.QtWidgets import QMenu, QToolBar
from .undo_stack import UndoStack
import difflib
from libqtopensesame.misc.translate import translation_context
_ = translation_context('undo_manager', category='extension')


class UndoManager(BaseExtension):
    """An extension that implements undo/ redo."""
    
    def event_startup(self):
        """Initializes the extension on startup."""
        self.undo_action = self.qaction('edit-undo', _('Undo'), self.undo,
                                        tooltip=_('Undo most recent action'),
                                        shortcut='Alt+Ctrl+Z')
        # fThis extension has two actions instead of one. This is a hacky
        # solution to insert the second action after the first one in both
        # the toolbar and menu.
        menu_pos = self.menu_pos()
        if menu_pos is not None:
            submenu_text, index, separator_before, separator_after = menu_pos
            submenu = self.get_submenu(submenu_text)
            submenu.insertAction(self.action, self.undo_action)
        if self.toolbar_pos() is not None:
            self.toolbar.insertAction(self.action, self.undo_action)
        self.initialize()

    def event_open_experiment(self, path):
        """Re-initializes when a new experiment is opened."""
        self.initialize()

    def event_change_item(self, name):
        """Remember an items state when it has changed."""
        self.remember_item_state(name)

    def event_new_item(self, name, _type):
        """Remember addition of a new item."""
        self.remember_new_item(name)

    def activate(self):
        """Activated the redo action (undo is added as custom action in
        event_startup).
        """
        self.redo()

    def initialize(self):
        """Initializes an empty undo stack."""
        self.stack = UndoStack()
        for item in self.experiment.items:
            self.remember_item_state(item)
        self.undo_action.setEnabled(self.stack.can_undo())

    def remember_experiment_state_before(self):
        """Remember the entire experiment state before it has changed."""
        self.remember_experiment_state()

    def remember_experiment_state_after(self):
        """Remember the entire experiment state after it has changed, and
        update the current-item status. If no change has actually occurred the
        last two experiments are discarded.
        """
        self.remember_experiment_state()
        if self.prune_unchanged_experiment():
            return
        for item in self.experiment.items:
            self.make_current(item)

    def make_current(self, item):
        """Update the current-item status for one item.

        Parameters
        ----------
        item
            The item name.
        """
        script = self.experiment.items[item].cached_script
        self.stack.set_current(item, script)

    def remember_item_state(self, item):
        """Push the state of an item to the undo stack.

        Parameters
        ----------
        item
            The item name.
        """
        script = self.experiment.items[item].cached_script
        self.stack.add(item, script)
        self.set_enabled(self.stack.can_redo())
        self.undo_action.setEnabled(self.stack.can_undo())

    def remember_experiment_state(self):
        """Push the state of the entire experiment to the undo stack."""
        script = self.experiment.to_string()
        self.stack.add('__experiment__', script)
        self.set_enabled(self.stack.can_redo())
        self.undo_action.setEnabled(self.stack.can_undo())

    def remember_new_item(self, name):

        self.stack.add('__newitem__', name)
        self.make_current(name)
        self.set_enabled(self.stack.can_redo())
        self.undo_action.setEnabled(self.stack.can_undo())

    def prune_unchanged_experiment(self):
        """If the last two items on the undo stack are full experiments, and
        there is no change between them, discard them.
        """
        if len(self.stack) < 2:
            return False
        key1, state1 = self.stack.peek(-1)
        key2, state2 = self.stack.peek(-2)
        if key1 == key2 == '__experiment__' and state1 == state2:
            self.stack.history = self.stack.history[:-2]
            return True
        return False

    @suspend_events
    def undo(self, dummy=False):
        """Perform an undo action."""
        if not self.stack:
            return
        item, script = self.stack.undo()
        if item == '__experiment__':
            self.main_window.regenerate(script)
        elif item == '__newitem__':
            del self.experiment.items[script]
            self.tabwidget.close_all()
        else:
            if item not in self.experiment.items:
                return
            self.experiment.items[item].from_string(script)
            self.experiment.items[item].update()
            self.experiment.items[item].open_tab()
            if isinstance(self.experiment.items[item], qtstructure_item):
                self.experiment.items.clear_cache()
                self.experiment.build_item_tree()
        self.set_enabled(self.stack.can_redo())
        self.undo_action.setEnabled(self.stack.can_undo())

    @suspend_events
    def redo(self):
        """Perform a redo action."""
        item, script = self.stack.redo()
        if item not in self.experiment.items:
            return
        self.experiment.items[item].from_string(script)
        self.experiment.items[item].update()
        self.experiment.items[item].open_tab()
        if isinstance(self.experiment.items[item], qtstructure_item):
            self.experiment.items.clear_cache()
            self.experiment.build_item_tree()
        self.set_enabled(self.stack.can_redo())
        self.undo_action.setEnabled(self.stack.can_undo())

    def show(self):
        """Print a summary of undo actions to the debug window."""
        item, old_script = self.stack.peek()
        if item is None:
            print('\nThe undo stack is empty')
            return
        self.console.write('\nMost recent: %s\n\n' % item)
        if item == '__experiment__':
            old_script = self.stack.peek(-2)[1]
            new_script = self.stack.peek(-1)[1]
        elif item == '__newitem__':
            new_script = old_script
        else:
            new_script = self.stack.current[item][0]
        for line in difflib.ndiff(old_script.splitlines(),
                                  new_script.splitlines()):
            if line.startswith('+'):
                self.console.write('\x1b[32;1m')
            elif line.startswith('-'):
                self.console.write('\x1b[31;1m')
            else:
                continue
            self.console.write(line + '\n')
        self.console.write('\x1b[0m')
        self.console.write('\nFull stack:\n\n')
        for i, (item, script) in enumerate(self.stack.history[::-1]):
            self.console.write('%d - %s\n' % (i, item))

    # All these events simply undo by restoring the complete experiment state.
    # This is crude, but works for now.

    def event_prepare_regenerate(self):
        self.extension_manager.suspend_until('regenerate')
        self.remember_experiment_state_before()

    def event_regenerate(self):
        self.remember_experiment_state_after()

    def event_prepare_delete_item(self, name):
        self.extension_manager.suspend_until('delete_item')
        self.remember_experiment_state_before()

    def event_delete_item(self, name):
        self.remember_experiment_state_after()
        
    def event_prepare_move_item(self, name):
        self.extension_manager.suspend_until('move_item')
        self.remember_experiment_state_before()

    def event_move_item(self, name):
        self.remember_experiment_state_after()
        
    def event_prepare_linked_copy(self, name):
        self.extension_manager.suspend_until('linked_copy')
        self.remember_experiment_state_before()

    def event_linked_copy(self, name):
        self.remember_experiment_state_after()

    def event_prepare_rename_item(self, from_name, to_name):
        self.extension_manager.suspend_until('rename_item')
        self.remember_experiment_state_before()

    def event_rename_item(self, from_name, to_name):
        self.remember_experiment_state_after()

    def event_prepare_purge_unused_items(self):
        self.extension_manager.suspend_until('purge_unused_items')
        self.remember_experiment_state_before()

    def event_purge_unused_items(self):
        self.remember_experiment_state_after()

    def event_prepare_change_experiment(self):
        self.extension_manager.suspend_until('change_experiment')
        self.remember_experiment_state_before()

    def event_change_experiment(self):
        self.remember_experiment_state_after()
