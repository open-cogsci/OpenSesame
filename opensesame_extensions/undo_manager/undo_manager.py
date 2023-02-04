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
from libqtopensesame.extensions import base_extension, suspend_events
from libqtopensesame.items.qtstructure_item import qtstructure_item
from qtpy.QtWidgets import QMenu, QToolBar
from undo_stack import undo_stack
import difflib
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'undo_manager', category=u'extension')


class undo_manager(base_extension):

    """
    desc:
            An extension that implements undo/ redo.
    """

    def event_startup(self):
        """
        desc:
                Initializes the extension on startup.
        """

        self.undo_action = self.qaction(u'edit-undo', _(u'Undo'), self.undo,
                                        tooltip=_(u'Undo most recent action'),
                                        shortcut=u'Alt+Ctrl+Z')
        for w in self.action.associatedWidgets():
            if not isinstance(w, QMenu) and not isinstance(w, QToolBar):
                continue
            w.insertAction(self.action, self.undo_action)
        self.initialize()

    def event_open_experiment(self, path):
        """
        desc:
                Re-initializes when a new experiment is opened.
        """

        self.initialize()

    def event_change_item(self, name):
        """
        desc:
                Remember an items state when it has changed.
        """

        self.remember_item_state(name)

    def event_new_item(self, name, _type):
        """
        desc:
                Remember addition of a new item.
        """

        self.remember_new_item(name)

    def activate(self):
        """
        desc:
                Activated the redo action (undo is added as custom action in
                event_startup).
        """

        self.redo()

    def initialize(self):
        """
        desc:
                Initializes an empty undo stack.
        """

        self.stack = undo_stack()
        for item in self.experiment.items:
            self.remember_item_state(item)
        self.undo_action.setEnabled(self.stack.can_undo())

    def remember_experiment_state_before(self):
        """
        desc:
                Remember the entire experiment state before it has changed.
        """

        self.remember_experiment_state()

    def remember_experiment_state_after(self):
        """
        desc:
                Remember the entire experiment state after it has changed, and
                update the current-item status. If no change has actually occurred
                the last two experiments are discarded.
        """

        self.remember_experiment_state()
        if self.prune_unchanged_experiment():
            return
        for item in self.experiment.items:
            self.make_current(item)

    def make_current(self, item):
        """
        desc:
                Update the current-item status for one item.

        arguments:
                item:	The item name.
        """

        script = self.experiment.items[item].cached_script
        self.stack.set_current(item, script)

    def remember_item_state(self, item):
        """
        desc:
                Push the state of an item to the undo stack.

        arguments:
                item:	The item name.
        """

        script = self.experiment.items[item].cached_script
        self.stack.add(item, script)
        self.set_enabled(self.stack.can_redo())
        self.undo_action.setEnabled(self.stack.can_undo())

    def remember_experiment_state(self):
        """
        desc:
                Push the state of the entire experiment to the undo stack.
        """

        script = self.experiment.to_string()
        self.stack.add(u'__experiment__', script)
        self.set_enabled(self.stack.can_redo())
        self.undo_action.setEnabled(self.stack.can_undo())

    def remember_new_item(self, name):

        self.stack.add(u'__newitem__', name)
        self.set_enabled(self.stack.can_redo())
        self.undo_action.setEnabled(self.stack.can_undo())

    def prune_unchanged_experiment(self):
        """
        desc:
                If the last two items on the undo stack are full experiments, and
                there is no change between them, discard them.
        """

        if len(self.stack) < 2:
            return False
        key1, state1 = self.stack.peek(-1)
        key2, state2 = self.stack.peek(-2)
        if key1 == key2 == u'__experiment__' and state1 == state2:
            self.stack.history = self.stack.history[:-2]
            return True
        return False

    @suspend_events
    def undo(self, dummy=False):
        """
        desc:
                Perform an undo action.
        """

        if not self.stack:
            return
        item, script = self.stack.undo()
        if item == u'__experiment__':
            self.main_window.regenerate(script)
        elif item == u'__newitem__':
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
        """
        desc:
                Perform a redo action.
        """

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
        """
        desc:
                Print a summary of undo actions to the debug window.
        """

        item, old_script = self.stack.peek()
        if item is None:
            print(u'\nThe undo stack is empty')
            return
        self.console.write(u'\nMost recent: %s\n\n' % item)
        if item == u'__experiment__':
            old_script = self.stack.peek(-2)[1]
            new_script = self.stack.peek(-1)[1]
        elif item == u'__newitem__':
            new_script = old_script
        else:
            new_script = self.stack.current[item][0]
        for line in difflib.ndiff(old_script.splitlines(),
                                  new_script.splitlines()):
            if line.startswith(u'+'):
                self.console.write(u'\x1b[32;1m')
            elif line.startswith(u'-'):
                self.console.write(u'\x1b[31;1m')
            else:
                continue
            self.console.write(line + u'\n')
        self.console.write(u'\x1b[0m')
        self.console.write(u'\nFull stack:\n\n')
        for i, (item, script) in enumerate(self.stack.history[::-1]):
            self.console.write(u'%d - %s\n' % (i, item))

    # All these events simply undo by restoring the complete experiment state.
    # This is crude, but works for now.

    def event_prepare_regenerate(self):
        self.extension_manager.suspend_until(u'regenerate')
        self.remember_experiment_state_before()

    def event_regenerate(self):
        self.remember_experiment_state_after()

    def event_prepare_delete_item(self, name):
        self.extension_manager.suspend_until(u'delete_item')
        self.remember_experiment_state_before()

    def event_delete_item(self, name):
        self.remember_experiment_state_after()

    def event_prepare_rename_item(self, from_name, to_name):
        self.extension_manager.suspend_until(u'rename_item')
        self.remember_experiment_state_before()

    def event_rename_item(self, from_name, to_name):
        self.remember_experiment_state_after()

    def event_prepare_purge_unused_items(self):
        self.extension_manager.suspend_until(u'purge_unused_items')
        self.remember_experiment_state_before()

    def event_purge_unused_items(self):
        self.remember_experiment_state_after()

    def event_prepare_change_experiment(self):
        self.extension_manager.suspend_until(u'change_experiment')
        self.remember_experiment_state_before()

    def event_change_experiment(self):
        self.remember_experiment_state_after()
