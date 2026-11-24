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

# These settings must be configured before qtpy imports Qt, and therefore
# cannot be done inside the test methods.
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
os.environ.setdefault('QTWEBENGINE_DISABLE_SANDBOX', '1')
os.environ.setdefault('QTWEBENGINE_CHROMIUM_FLAGS', '--disable-gpu')


class check_item_store(unittest.TestCase):
    """Tests the GUI item store (qtitem_store), which is what the application
    uses for item creation, renaming and deletion, including the interface
    updates (unsaved flag, tree rename, extension events) that the plain
    libopensesame item store does not perform.
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

    @classmethod
    def tearDownClass(cls):
        cls.win.save_state = lambda *args, **kwds: None
        cls.win.save_unsaved_changes = lambda: True
        cls.win.close()
        cls.app.processEvents()
        sys.argv = cls._old_argv

    def test_new_item(self):
        """items.new() should create the item and flag the experiment as
        unsaved."""
        item = self.win.experiment.items.new(
            _type='inline_script', name='store_test_item')
        self.assertIn('store_test_item', self.win.experiment.items)
        self.assertEqual(item.item_type, 'inline_script')
        self.assertTrue(self.win.unsaved_changes)
        del self.win.experiment.items['store_test_item']
        self.app.processEvents()
        self.assertNotIn('store_test_item', self.win.experiment.items)

    def test_new_item_unknown_type(self):
        """items.new() should fall back to a missing_item placeholder when
        the plugin cannot be loaded."""
        item = self.win.experiment.items.new(
            _type='definitely_not_a_plugin', name='store_missing_item')
        self.assertIn('store_missing_item', self.win.experiment.items)
        self.assertEqual(item.item_type, 'missing_item')
        del self.win.experiment.items['store_missing_item']
        self.app.processEvents()

    def test_rename_item(self):
        """items.rename() should rename the item in the store, the tree and
        the experiment, and flag the experiment as unsaved."""
        result = self.win.experiment.items.rename('welcome', 'welcome_renamed')
        self.assertEqual(result, 'welcome_renamed')
        self.assertIn('welcome_renamed', self.win.experiment.items)
        self.assertNotIn('welcome', self.win.experiment.items)
        # The overview tree should have been updated as well.
        from qtpy import QtCore
        self.assertTrue(self.win.ui.itemtree.findItems(
            'welcome_renamed',
            QtCore.Qt.MatchFixedString | QtCore.Qt.MatchRecursive))
        result = self.win.experiment.items.rename(
            'welcome_renamed', 'welcome')
        self.assertEqual(result, 'welcome')
        self.assertIn('welcome', self.win.experiment.items)

    def test_rename_item_failures(self):
        """items.rename() should refuse to rename a nonexistent item or an
        item to its current name, and should auto-generate a unique name
        when the requested name is empty or already taken."""
        self.assertIsNone(
            self.win.experiment.items.rename('no_such_item', 'whatever'))
        self.assertIsNone(
            self.win.experiment.items.rename('welcome', 'welcome'))
        for to_name in ('', 'experiment'):
            result = self.win.experiment.items.rename('welcome', to_name)
            self.assertIsNotNone(result)
            self.assertNotEqual(result, to_name)
            self.win.experiment.items.rename(result, 'welcome')
        self.assertIn('welcome', self.win.experiment.items)


class check_markdown_parser(unittest.TestCase):
    """Tests the Markdown parser used by the embedded browser to render
    help pages (.md files)."""

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
        from libqtopensesame.misc.markdown_parser import MarkdownParser
        cls.parser = MarkdownParser(cls.win)

    @classmethod
    def tearDownClass(cls):
        cls.win.save_state = lambda *args, **kwds: None
        cls.win.save_unsaved_changes = lambda: True
        cls.win.close()
        cls.app.processEvents()
        sys.argv = cls._old_argv

    def test_to_html(self):
        """to_html() should convert Markdown to HTML."""
        html = self.parser.to_html(u'# Title\n\nSome **bold** text.')
        self.assertIn('<h1', html)
        self.assertIn('Title', html)
        self.assertIn('<strong>', html)

    def test_to_html_title(self):
        """A 'title:' line at the start should become an <h1> heading."""
        html = self.parser.to_html(u'title: My Page\n\nBody text.')
        self.assertIn('<h1', html)
        self.assertIn('My Page', html)

    def test_highlight_python(self):
        """~~~python blocks should be syntax-highlighted to HTML."""
        html = self.parser.to_html(
            u'~~~ python\nvar.x = 1\n~~~')
        self.assertIn('var.x', html)
        self.assertNotIn('~~~', html)


if __name__ == '__main__':
    unittest.main()
