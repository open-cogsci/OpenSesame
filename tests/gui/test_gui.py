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

# The tests in this group run the graphical user interface on a virtual
# (offscreen) display, so that no real X server or Wayland session is
# required. These settings must be configured before qtpy imports Qt, and
# therefore cannot be done inside runTest().
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
os.environ.setdefault('QTWEBENGINE_DISABLE_SANDBOX', '1')
os.environ.setdefault('QTWEBENGINE_CHROMIUM_FLAGS', '--disable-gpu')


class check_gui(unittest.TestCase):

    """Runs the OpenSesame graphical user interface offscreen (i.e. on a virtual
    display) to see whether the application can be started.
    """
    def runTest(self):
        
        from pathlib import Path
        from libopensesame import misc
        from openexp import resources

        print('Starting the graphical user interface offscreen ...')
        # The application folder needs to be registered so that user
        # interface files, themes, and templates can be found.
        import libqtopensesame
        misc.parse_environment_file()
        resources.add_resource_folder(
            Path(libqtopensesame.__file__).parent / 'resources')
        # Import QtWebEngine before creating the QApplication, just like the
        # regular entry point does, and create the application. An existing
        # instance is reused, because Qt doesn't allow more than one
        # QApplication per process.
        try:
            from qtpy import QtWebEngineWidgets
        except ImportError:
            pass
        from qtpy.QtWidgets import QApplication
        # The main window parses the command line during construction, so we
        # present it with the same arguments as the regular entry point. Qt
        # also requires a non-empty argument list, or QtWebEngine subprocesses
        # will abort.
        argv = ['opensesame', '--start-clean']
        old_argv = sys.argv[:]
        sys.argv = argv[:]
        app = QApplication.instance() or QApplication(argv)
        try:
            from libqtopensesame.misc.config import cfg
            # The analytics extension pings a server through a hidden web view
            # when the application starts up, which is not appropriate during
            # a unit test, so the extension is disabled. The corresponding
            # configuration key needs to be registered first, because it's the
            # extension itself that normally registers this key, whereas the
            # extension manager checks it to decide whether the extension
            # should be built at all.
            cfg.register('plugin_enabled_analytics', True)
            cfg.plugin_enabled_analytics = False
            from libqtopensesame.qtopensesame import QtOpenSesame
            win = None
            try:
                win = QtOpenSesame(app)
                win.resume_init()
                # The analytics extension should not have been built.
                self.assertFalse('Analytics' in [
                    ext.name() for ext in win.extension_manager._extensions
                ])
                win.restore_window_state()
                win.show()
                app.processEvents()
                self.assertTrue(win.isVisible())
                self.assertIn('OpenSesame', win.windowTitle())
                # The default experiment template should have been loaded,
                # just like during a regular startup.
                self.assertGreater(len(win.experiment.items), 0)
                print('Main window created with %d items'
                    % len(win.experiment.items))
            finally:
                if win is not None:
                    # Close the window through its regular close event, but
                    # don't save the configuration, so that running the test
                    # doesn't modify the settings of the user who runs it.
                    win.save_state = lambda *args, **kwds: None
                    win.close()
        finally:
            sys.argv = old_argv


if __name__ == '__main__':
    unittest.main()
