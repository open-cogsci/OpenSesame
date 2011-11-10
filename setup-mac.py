#!/usr/bin/env python

"""
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
shutil.copytree("/opt/local/lib/Resources/qt_menu.nib", "qt_menu.nib")

# Py2app doesn't like extensionless Python scripts
try:
	os.remove("opensesame.py")
except:
	pass
shutil.copyfile("opensesame", "opensesame.py")

# Build!
setup(
    app = ['opensesame.py'],
    data_files = ['opensesame.py'],
    options = {'py2app' : {'argv_emulation': False, 
		'includes' : ['sip', 'PyQt4.QtGui', 'PyQt4.QtCore', 'pygame', 'numpy', \
			'serial', 'openexp', 'libqtopensesame', 'libopensesame' \
			],
		'resources' : ['qt_menu.nib', 'resources', 'examples', 'sounds', \
			'plugins', 'help', 'data'
			]
		}},
    setup_requires=['py2app'],
)

# Clean up qt_menu.nib
shutil.rmtree("qt_menu.nib")

# Remove opensesame.py
try:
	os.remove("opensesame.py")
except:
	pass
