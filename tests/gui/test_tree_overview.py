#!/usr/bin/env python
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
import os
import sys
import unittest
from unittest import mock

# These settings must be configured before qtpy imports Qt, and therefore
# cannot be done inside the test methods.
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
os.environ.setdefault('QTWEBENGINE_DISABLE_SANDBOX', '1')
os.environ.setdefault('QTWEBENGINE_CHROMIUM_FLAGS', '--disable-gpu')


class check_tree_overview(unittest.TestCase):
    """Tests the overview tree widget: item selection, renaming through both
    the programmatic and the itemChanged signal paths, fold state, and
    deletion of a child item (which rebuilds the whole tree, the code path
    involved in the #836 crash).
    """

    @classmethod
    def setUpClass(cls):
        import libqtopensesame
        from pathlib import Path
        from libopensesame import misc
        from openexp import resources

        misc.parse_environment_file()
        resources.add_resource_folder(
            Path(libqtopensesame.__file__).parent / 'resources')
        try:
            from qtpy import QtWebEngineWidgets
        except ImportError:
            pass
        from qtpy.QtWidgets import QApplication
        # The code editor's worker pool spawns multiprocessing children,
        # which are not needed by these tests and can keep the test
        # process alive at exit. The pool is disabled.
        try:
            from pyqt_code_editor.worker import manager as worker_manager
            worker_manager.start_worker_pool = lambda: None
        except ImportError:
            pass
        argv = ['opensesame', '--start-clean']
        cls._old_argv = sys.argv[:]
        sys.argv = argv[:]
        cls.app = QApplication.instance() or QApplication(argv)
        from libqtopensesame.misc.config import cfg
        cfg.register('plugin_enabled_analytics', True)
        cfg.plugin_enabled_analytics = False
        from libqtopensesame.qtopensesame import QtOpenSesame
        cls.win = QtOpenSesame(cls.app)
        cls.win.resume_init()
        cls.win.restore_window_state()
        cls.win.show()
        cls.app.processEvents()
        cls.tree = cls.win.ui.itemtree

    @classmethod
    def tearDownClass(cls):
        cls.win.save_state = lambda *args, **kwds: None
        cls.win.save_unsaved_changes = lambda: True
        cls.win.close()
        cls.app.processEvents()
        sys.argv = cls._old_argv

    def _tree_item(self, name):
        """Returns the tree_item_item widget for an experiment item. The
        items() method only returns top-level items and their direct
        children, so the tree is walked recursively."""
        def walk(item):
            if getattr(item, 'name', None) == name:
                return item
            for i in range(item.childCount()):
                found = walk(item.child(i))
                if found is not None:
                    return found
            return None
        for item in self.tree.items():
            found = walk(item)
            if found is not None:
                return found
        return None

    def test_tree_is_populated(self):
        """The default experiment template should populate the tree."""
        self.assertGreater(self.tree.topLevelItemCount(), 0)
        self.assertIsNotNone(self._tree_item('welcome'))
        self.assertIsNotNone(self._tree_item('getting_started'))

    def test_select_item(self):
        """select_item() should select the matching tree item without
        opening an editor tab."""
        self.tree.select_item('welcome', open_tab=False)
        selected = self.tree.selectedItems()
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0].text(0), 'welcome')

    def test_text_edited_rename(self):
        """Editing the item name in the tree (the itemChanged path) should
        rename the item through experiment.items.rename()."""
        tree_item = self._tree_item('welcome')
        self.assertIsNotNone(tree_item)
        tree_item.setText(0, 'welcome_edited')
        self.tree.text_edited(tree_item, 0)
        self.assertIn('welcome_edited', self.win.experiment.items)
        tree_item = self._tree_item('welcome_edited')
        tree_item.setText(0, 'welcome')
        self.tree.text_edited(tree_item, 0)
        self.assertIn('welcome', self.win.experiment.items)

    def test_fold_state(self):
        """The fold state should round-trip without errors."""
        fold_state = self.tree.get_fold_state()
        self.assertIsInstance(fold_state, dict)
        self.assertGreater(len(fold_state), 0)
        self.tree.set_fold_state(fold_state)

    def test_unused_items(self):
        """unused_items() should return a list of item names."""
        unused = self.tree.unused_items()
        self.assertIsInstance(unused, list)

    def test_y_copy_paste_item(self):
        """Copying an item and pasting it onto another tree item should
        create a duplicate through drop_event_item_new(), the same code
        path used by drag-and-drop (including the target-treeitem
        resolution added for #836)."""
        source = self._tree_item('welcome')
        target = self._tree_item('experiment')
        self.assertIsNotNone(source)
        self.assertIsNotNone(target)
        before = set(self.win.experiment.items)
        source.copy_unlinked()
        target.paste()
        self.app.processEvents()
        new_items = set(self.win.experiment.items) - before
        self.assertEqual(len(new_items), 1)
        copy_name = new_items.pop()
        # The copy should be linked into the target sequence.
        self.assertIn('run %s' % copy_name,
                      self.win.experiment.items['experiment'].to_string())
        # Clean up: permanently delete the copy, confirming the dialog.
        from qtpy import QtWidgets
        copy_item = self._tree_item(copy_name)
        with mock.patch.object(QtWidgets.QMessageBox, 'question',
                               return_value=QtWidgets.QMessageBox.Yes):
            copy_item.permanently_delete()
        self.app.processEvents()
        self.assertNotIn(copy_name, self.win.experiment.items)

    def test_z_delete_child_item(self):
        """Deleting a child item removes it from its parent and rebuilds the
        tree; the item itself remains in the item store as an unused item.
        Runs last because it modifies the experiment structure.
        """
        tree_item = self._tree_item('getting_started')
        self.assertIsNotNone(tree_item)
        self.assertTrue(tree_item.is_deletable())
        tree_item.delete()
        self.app.processEvents()
        # The item is no longer part of the experiment sequence.
        self.assertNotIn('run getting_started',
                         self.win.experiment.items['experiment'].to_string())
        # But it still exists as an unused item.
        self.assertIn('getting_started', self.win.experiment.items)
        self.assertIn('getting_started', self.tree.unused_items())


if __name__ == '__main__':
    unittest.main()
