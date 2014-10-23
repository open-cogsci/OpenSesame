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

---

# Usage

## Assumptions

- The PyGame subset for Android is installed in the folder indicated under
`pgs4a_folder`.
- The Python modules are installed in the folder indicated under
`module_folder`

## Build environment

Currently, most development is done on Kubuntu 14.04. Most of the dependencies
for pgs4a are described on their homepage, but in addition you need to install
the Oracle Java JDK (v8 currently used). This is available from
`ppa:webupd8team/java`. Instructions taken from:

- <http://www.mameau.com/pygame-subset-for-android-pgs4a-on-ubuntu-precise-12-04/>

## Building

Build the `.apk` with the following command:

	python setup-android.py [install]

The `install` parameter is optional, and indicates that the `.apk` should be
installed on an attached Android device or emulator. The resulting `.apk` can
be found in the `bin` subfolder of the PyGame subset for Android folder.
---
"""

import shutil
import sys
import os
import subprocess
import importlib
from setup_shared import *

pgs4a_folder = 'pgs4a-0.9.4'
module_folder = '/usr/lib/python2.7'
clear_cmd = \
	'./android-sdk/platform-tools/adb shell pm clear nl.cogsci.opensesame'
build_cmd = './android.py build opensesame release'
if 'install' in sys.argv:
	build_cmd += ' install'

# A list of pure Python modules that are not included by default but are
# required for OpenSesame
module_list = [
	'HTMLParser',
	'markupbase',
	]

# A list of pure Python packages that are not included by default but are
# required for OpenSesame
package_list = [
	'yaml',
	'libopensesame',
	'libqtopensesame',
	'openexp'
	]

# A list of files/folders in the resources folder that should be copied
resources_whitelist = [
	'widgets',
	'gray',
	'android',
	'menu.opensesame',
	'box-checked.png',
	'box-unchecked.png',
	'mono.ttf',
	'sans.ttf',
	'serif.ttf',
	'android-splash.jpg'
	]

# A filter to ignore non-relevant package files
def ignore_bytecode(folder, files):
	l = []
	for f in files:
		if os.path.splitext(f)[1] in [".pyo", ".pyc"]:
			l.append(f)
	return l

# A filter to strip non-relevant resources
def ignore_resources(folder, files):
	l = []
	for f in files:
		if f not in resources_whitelist:
			l.append(f)
	return l

# A filter to strip non-relevant examples
def ignore_examples(folder, files):
	l = []
	for f in files:
		if '_android' not in f:
			l.append(f)
	return l

target = os.path.join(pgs4a_folder, 'opensesame')

if os.path.exists(target):
	print('Removing %s' % target)
	shutil.rmtree(target)
print('Creating %s' % target)
os.mkdir(target)

print('Copying resources')
shutil.copytree('resources', os.path.join(target, 'resources'), \
	ignore=ignore_resources)
print('Copying examples')
shutil.copytree('examples', os.path.join(target, 'examples'), \
	ignore=ignore_examples)

print('Copying plugins')
os.mkdir(os.path.join(target, 'plugins'))
for plugin in included_plugins:
	print('Copying plugin %s' % plugin)
	shutil.copytree(os.path.join('plugins', plugin), os.path.join(target, \
		'plugins', plugin))

print('Copying modules')
for module in module_list:
	mod = importlib.import_module(module)
	fname = mod.__file__
	if fname.endswith('.pyc'):
		fname = fname[:-1]
	print('\t%s (%s)' % (module, fname))
	shutil.copyfile(fname, os.path.join(target, module+'.py'))

print('Copying packages')
for package in package_list:
	pkg = importlib.import_module(package)
	folder = os.path.dirname(pkg.__file__)
	print('\t%s (%s)' % (package, folder))
	shutil.copytree(folder, os.path.join(target, package))

print('Copying dummy PyQt4')
shutil.copytree('resources/android/PyQt4', os.path.join(target, 'PyQt4'))
print('Copying main.py')
shutil.copyfile('opensesameandroid.py', os.path.join(target, 'main.py'))
print('Copying .android.json')
shutil.copyfile('resources/android/android.json', os.path.join(target,
	'.android.json'))
print('Copying android-icon.png')
shutil.copyfile('resources/android/android-icon.png',
	os.path.join(target, 'android-icon.png'))
print('Copying android-presplash.png')
shutil.copyfile('resources/android/android-presplash.jpg',
	os.path.join(target, 'android-presplash.jpg'))
print('Building')
os.chdir(pgs4a_folder)
print('Clearing application data')
subprocess.call(clear_cmd.split())
print('Building')
subprocess.call(build_cmd.split())
