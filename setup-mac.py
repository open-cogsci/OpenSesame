#!/usr/bin/env python
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

This scripts builds OpenSesame as a standalone application for Mac OS.

Usage:
    python setup-mac.py py2app
"""

import macholib
from setuptools import setup
import os
import sys
import shutil

from setup_shared import included_plugins, included_extensions
from libopensesame.metadata import __version__ as version, codename

"""
Monkey-patch macholib to fix "dyld_find() got an unexpected keyword argument 'loader'".
"""
#print("~"*60 + "macholib verion: "+macholib.__version__)
if macholib.__version__ <= "1.7":
    print("Applying macholib patch...")
    import macholib.dyld
    import macholib.MachOGraph
    dyld_find_1_7 = macholib.dyld.dyld_find

    def dyld_find(name, loader=None, **kwargs):
        #print("~"*60 + "calling alternate dyld_find")
        if loader is not None:
            kwargs['loader_path'] = loader
        return dyld_find_1_7(name, **kwargs)
    macholib.MachOGraph.dyld_find = dyld_find
"""
END Monkey-patch macholib"
"""

# Get the root folder of anaconda
anaconda_path = os.path.dirname(os.path.dirname(sys.executable))

# Clean up previous builds
try:
    shutil.rmtree("dist")
except:
    pass
try:
    shutil.rmtree("build")
except:
    pass

# Copy qt_menu.nib folder
try:
    shutil.rmtree("qt_menu.nib")
except:
    pass
shutil.copytree(os.path.join(anaconda_path,
                             "python.app/Contents/Resources/qt_menu.nib"), "qt_menu.nib")

# Py2app doesn't like extensionless Python scripts
try:
    os.remove("opensesame.py")
    os.remove("opensesamerun.py")
except:
    pass
shutil.copyfile("opensesame", "opensesame.py")
shutil.copyfile("opensesamerun", "opensesamerun.py")

# Build!
setup(
    app=['opensesame.py'],
    data_files=['opensesame.py'],
    options={'py2app':
             {
                 'argv_emulation': True,
                 'includes': [
                     'PyQt4.QtNetwork', 'serial', 'opensesamerun', 'sip',
                     'billiard', 'QNotifications', 'arrow', 'humanize',
                     'requests_oauthlib', 'pyaudio', 'imageio', 'sounddevice',
                 ],
                 'excludes': [
                     'Finder', 'idlelib', 'gtk', 'matplotlib', 'pandas', 'PyQt4.QtDesigner',
                     'PyQt4.QtOpenGL', 'PyQt4.QtScript', 'PyQt4.QtSql', 'PyQt4.QtTest',
                     'PyQt4.QtXml', 'PyQt4.phonon', 'rpy2', 'wx', 'pycurl', 'dynd', 'bokeh',
                 ],
                 'resources': ['qt_menu.nib', 'opensesame_resources'],
                 'packages': [
                     'openexp', 'expyriment', 'psychopy', 'libqtopensesame',
                     'libopensesame', 'IPython', 'ipykernel', 'jupyter_client',
                     'qtconsole', 'pygments', 'OpenGL_accelerate', 'markdown',
                     'QOpenScienceFramework', 'moviepy', 'qtawesome', 'pyqcode.core',
                                'pyqode.python'
                 ],
                 'iconfile': 'opensesame_resources/opensesame.icns',
                 'plist': {
                     'CFBundleName': 'OpenSesame',
                     'CFBundleShortVersionString': version,
                     'CFBundleVersion': ' '.join([version, codename]),
                     'CFBundleIdentifier': 'nl.cogsci.osdoc',
                     'NSHumanReadableCopyright': 'Sebastiaan Mathot (2010-2016)',
                     'CFBundleDevelopmentRegion': 'English',
                     'CFBundleDocumentTypes': [
                         {
                                        'CFBundleTypeExtensions': ['osexp'],
                                        'CFBundleTypeIconFile': 'opensesame_resources/opensesame.icns',
                                        'CFBundleTypeRole': 'Editor',
                                        'CFBundleTypeName': 'OpenSesame File',
                         },
                     ]
                 }
             }
             },
    setup_requires=['py2app'],
)

# Clean up qt_menu.nib
shutil.rmtree("qt_menu.nib")

# Psychopy monitor center does not play nicely together with the OpenSesame GUI
if 'psychopy_monitor_center' in included_extensions:
    del included_extensions[included_extensions.index(
        'psychopy_monitor_center')]

# Copy extensions into app
for extension in included_extensions:
    shutil.copytree(os.path.join("opensesame_extensions", extension),
                    os.path.join("dist/OpenSesame.app/Contents/Resources/opensesame_extensions/", extension))

# Open Science Framework extension
try:
    osf_path = os.path.abspath(os.path.join(anaconda_path,
                                            'share/opensesame_extensions/OpenScienceFramework'))
    shutil.copytree(osf_path,
                    "dist/opensesame.app/Contents/Resources/opensesame_extensions/OpenScienceFramework")
except Exception as e:
    print("Could not copy OSF extension: {}".format(e))

# Copy plugins into app
for plugin in included_plugins:
    shutil.copytree(os.path.join("opensesame_plugins", plugin),
                    os.path.join("dist/OpenSesame.app/Contents/Resources/opensesame_plugins/", plugin))

# Copy media_player_mpy plugin
try:
    mp_path = os.path.abspath(os.path.join(anaconda_path,
                                           'share/opensesame_plugins/media_player_mpy'))
    shutil.copytree(mp_path,
                    "dist/opensesame.app/Contents/Resources/opensesame_plugins/media_player_mpy")
except Exception as e:
    print("Could not copy media_player_mpy plugin: {}".format(e))

# Copy ffmpeg (required by media_player_mpy)
try:
    import imageio
    appdata_dir = imageio.core.appdata_dir('imageio')
    ffmpeg_path = os.path.abspath(os.path.join(appdata_dir,
                                               'ffmpeg/ffmpeg.osx'))
    shutil.copy(ffmpeg_path,
                "dist/opensesame.app/Contents/Resources/ffmpeg.osx")
except Exception as e:
    print("Could not copy media_player_mpy plugin: {}".format(e))

# Anaconda libpng version is too old for pygame (min required version is 36).
# Copy homebrew version instead
try:
    shutil.copy('/usr/local/opt/libpng/lib/libpng16.16.dylib',
                'dist/OpenSesame.app/Contents/Frameworks/libpng16.16.dylib')
except Exception as e:
    print("Could not copy newer libpng16.16.dylib: {}".format(e))

# Remove opensesame.py
try:
    os.remove("opensesame.py")
    os.remove("opensesamerun.py")
except:
    pass
