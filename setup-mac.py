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

This scripts builds OpenSesame as a standalone application for Mac OS.

Usage:
    python setup.py py2app
"""

from setuptools import setup
import os
import shutil

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
shutil.copytree("/Library/Frameworks/QtGui.framework/Resources/qt_menu.nib", "qt_menu.nib")

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
    app = ['opensesame.py'],
    data_files = ['opensesame.py'],
    options = {'py2app' : 
			{'argv_emulation': False, 
			 'includes' : ['sip', 'PyQt4.QtNetwork', 'pygame', 'numpy', 'serial', 'openexp', 'libqtopensesame','libopensesame','libopensesame.widgets', 'libqtopensesame.widgets', 'opensesamerun','cv','cv2'],
			 'resources' : ['qt_menu.nib', 'qt.conf', 'resources', 'sounds', 'plugins', 'help', 'data'],
			 'packages' : ['expyriment'],
			 'iconfile' : 'resources/opensesame.icns',			
			}
		   },
    setup_requires=['py2app'],
)

# Clean up qt_menu.nib
shutil.rmtree("qt_menu.nib")

# Remove unwanted plugins from build
shutil.rmtree("dist/opensesame.app/Contents/Resources/plugins/pp_io")
shutil.rmtree("dist/opensesame.app/Contents/Resources/plugins/port_reader")

# Remove opensesame.py
try:
	os.remove("opensesame.py")
	os.remove("opensesamerun.py")
except:
	pass
