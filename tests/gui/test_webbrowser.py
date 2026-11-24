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


class check_webbrowser(unittest.TestCase):
    """Tests the command handling of the embedded browser, in particular the
    `help extension <name>` and `help plugin <name>` commands, which used to
    raise a NameError because the folder variable was never assigned.
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
        # which coverage tools cannot trace and which can keep the test
        # process alive at exit. The widget tests do not use the code
        # editor, so the pool is disabled.
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
        from libqtopensesame.widgets.webbrowser import Webbrowser
        cls.browser = Webbrowser(cls.win)

    @classmethod
    def tearDownClass(cls):
        cls.win.save_state = lambda *args, **kwds: None
        cls.win.close()
        cls.app.processEvents()
        sys.argv = cls._old_argv

    def test_help_plugin(self):
        """`help plugin <name>` should load the plugin's markdown file from
        the plugin folder."""
        plugin_manager = self.win.experiment._plugin_manager
        name = next(iter(plugin_manager._plugins))
        folder = plugin_manager[name].folder
        with mock.patch.object(self.browser, 'load') as load:
            self.browser.command('opensesame://help.plugin.%s' % name)
        load.assert_called_once_with(os.path.join(folder, name + '.md'))

    def test_help_extension(self):
        """`help extension <name>` should load the extension's markdown file
        from the extension folder."""
        extensions = [
            ext for ext in self.win.extension_manager._extensions
            if getattr(ext, 'extension_folder', None)
        ]
        if not extensions:
            self.skipTest('No built extensions available')
        ext = extensions[0]
        name = ext.name()
        with mock.patch.object(self.browser, 'load') as load:
            self.browser.command('opensesame://help.extension.%s' % name)
        load.assert_called_once_with(
            os.path.join(ext.extension_folder, name + '.md'))

    def test_help_topic(self):
        """`help <topic>` should open the corresponding help page through the
        tab widget."""
        with mock.patch.object(
                self.win.ui.tabwidget, 'open_help') as open_help:
            self.browser.command('opensesame://help.getting_started')
        open_help.assert_called_once_with('getting_started')


if __name__ == '__main__':
    unittest.main()
