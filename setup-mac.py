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
    python setup-mac.py py2app
"""

from setuptools import setup
import os
import shutil

from setup_shared  import included_plugins, included_extensions

from libopensesame.metadata import __version__ as version, codename

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
shutil.copytree("/Users/daniel/anaconda/python.app/Contents/Resources/qt_menu.nib", "qt_menu.nib")

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
		{
			'argv_emulation': True, 
			'includes' : [
				'PyQt4.QtNetwork', 'serial', 'opensesamerun', 'skimage', 'sip', \
				'billiard',
			],
			'excludes': [
				'Finder','idlelib', 'gtk', 'matplotlib', 'pandas', 'PyQt4.QtDesigner',\
			 	'PyQt4.QtOpenGL', 'PyQt4.QtScript', 'PyQt4.QtSql', 'PyQt4.QtTest', \
			 	'PyQt4.QtXml', 'PyQt4.phonon', 'rpy2', 'wx', 'pycurl','mkl','dynd','bokeh',
			],
			'resources' : ['qt_menu.nib', 'resources', 'sounds', 'help', 'data'],
			'packages' : [
				'openexp','expyriment','psychopy','QProgEdit','libqtopensesame','libopensesame',\
				'IPython','ipykernel','jupyter_client','qtconsole','pygments','OpenGL_accelerate',
			],
			'iconfile' : 'resources/opensesame.icns',
			'plist': {
				'CFBundleName': 'OpenSesame',
				'CFBundleShortVersionString': version,
				'CFBundleVersion': ' '.join([version, codename]),
				'CFBundleIdentifier':'nl.cogsci.osdoc',
				'NSHumanReadableCopyright': 'Sebastiaan Mathot (2010-2016)',
				'CFBundleDevelopmentRegion': 'English', 	
				'CFBundleDocumentTypes': [ 
					{
                    	'CFBundleTypeExtensions' : ['osexp'],
                    	'CFBundleTypeIconFile' : 'resources/opensesame.icns',
                    	'CFBundleTypeRole' : 'Editor',
                    	'CFBundleTypeName' : 'OpenSesame File',
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
	del included_extensions[included_extensions.index('psychopy_monitor_center')]

# Copy extensions into app
for extension in included_extensions:
	shutil.copytree(os.path.join("extensions",extension), os.path.join("dist/opensesame.app/Contents/Resources/extensions/",extension))

# Copy plugins into app
for plugin in included_plugins:
	shutil.copytree(os.path.join("plugins",plugin), os.path.join("dist/opensesame.app/Contents/Resources/plugins/",plugin))

# Anaconda libpng version is too old for pygame (min required version is 36). Copy homebrew version instead
# try:
# 	shutil.copy('/usr/local/opt/libpng/lib/libpng16.16.dylib','dist/OpenSesame.app/Contents/Frameworks/libpng16.16.dylib')
# except:
# 	print("Could not copy newer libpng16.16.dylib")

# Remove opensesame.py
try:
	os.remove("opensesame.py")
	os.remove("opensesamerun.py")
except:
	pass
