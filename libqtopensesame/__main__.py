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
import os
import sys
import platform
import multiprocessing
from pathlib import Path

# Platform-specific initialization
if platform.system() == 'Linux':
    # The fork multiprocessing method can be unstable on some Linux systems.
    # Use spawn as the default, but allow customization via environment 
    # variable. See <https://github.com/open-cogsci/OpenSesame/issues/782>
    try:
        multiprocessing.set_start_method(
            os.environ.get('OPENSESAME_MULTIPROCESSING_METHOD', 'spawn'))
    except (RuntimeError, ValueError) as e:
        print(f'Failed to change multiprocessing start method: {e}')
    
    # Solves a library conflict for Linux with Nvidia drivers
    try:
        from OpenGL import GL
    except ImportError:
        pass

elif platform.system() == 'Windows':
    # Attach dummy console when launched with pythonw.exe
    if sys.executable.endswith('pythonw.exe'):
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
        sys.stdin = open(os.devnull)
    os.chdir(os.path.dirname(sys.executable))
    # The Scripts folder is where anaconda puts pip and other important 
    # executables on Windows. This should be in the path.
    scripts_folder = os.path.abspath('Scripts')
    if os.path.isdir(scripts_folder):
        os.environ['PATH'] += f';{scripts_folder}'    

elif platform.system() == 'Darwin':
    # Set SSL certificate locations for macOS app bundles
    try:
        import certifi
        os.environ['SSL_CERT_FILE'] = certifi.where()
        os.environ['SSL_CERT_DIR'] = os.path.dirname(certifi.where())
    except ImportError:
        pass
    
    # Workaround for Qt and macOS compatibility
    os.environ['QT_MAC_WANTS_LAYER'] = '1'
    # Avoid segmentation faults when loading QtWebEngine
    os.environ['QTWEBENGINE_DISABLE_SANDBOX'] = '1'
    os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--disable-gpu'

# Add resources
from openexp import resources
resources.add_resource_folder(Path(__file__).parent / 'resources')


def opensesame():
    """Entry point for the OpenSesame GUI."""    
    # Parse environment file for special paths
    from libopensesame import misc
    misc.parse_environment_file()
    
    # Initialize Qt application
    from qtpy.QtWidgets import QApplication
    from qtpy.QtCore import Qt
    
    # Import QtWebEngine before creating QApplication
    try:
        from qtpy import QtWebEngineWidgets
    except ImportError:
        pass
    
    # Configure high DPI settings for Qt6
    # Note: Qt6 handles high DPI scaling automatically, but we can still
    # set the rounding policy for better appearance
    if hasattr(Qt.HighDpiScaleFactorRoundingPolicy, 'PassThrough'):
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    # Create application
    app = QApplication(sys.argv)
    
    # Initialize OpenSesame
    from libqtopensesame.qtopensesame import QtOpenSesame
    opensesame = QtOpenSesame(app)
    opensesame.__script__ = __file__
    app.processEvents()
    
    # Set up translators for internationalization
    from qtpy.QtCore import QTranslator
    translators = [QTranslator() for _ in range(12)]
    opensesame.set_locale(translators)
    
    # Complete initialization and show window
    opensesame.resume_init()
    opensesame.restore_window_state()
    opensesame.show()
    opensesame.raise_()  # Ensure window appears on macOS
    
    # Run application
    sys.exit(app.exec())