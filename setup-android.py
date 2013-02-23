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

import shutil
import os
import subprocess

pgs4a_folder = 'pgs4a-0.9.4'
build_cmd = './android.py build opensesame release install'
module_folder = '/usr/lib/python2.7'

# A list of OpenSesame folders that need to be included
folder_list = [
	'libopensesame',
	'libqtopensesame',
	'openexp',
	]
	
# A list of pure Python modules that are not included by default but are 
# required for OpenSesame
module_list = [
	'HTMLParser.py',
	'markupbase.py',
	]
	
# A list of files/folders in the resources folder that should be copied
resources_whitelist = [
	'widgets',
	'gray',
	'android',
	'menu.opensesame.tar.gz',
	'box-checked.png',
	'box-unchecked.png',
	'mono.ttf',
	'sans.ttf',
	'serif.ttf',
	'android-splash.jpg'	
	]
	
# Not all plugins are included
included_plugins = [
	"advanced_delay",
	"external_script",
	"fixation_dot",
	"form_base",
	"form_consent",
	"form_text_display",
	"form_text_input",
	"form_multiple_choice",
	"joystick",
	"notepad",
	"parallel",
	"repeat_cycle",
	"reset_feedback",
	"srbox",
	"text_display",
	"text_input",
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

target = os.path.join(pgs4a_folder, 'opensesame')

if os.path.exists(target):
	print 'Removing %s' % target
	shutil.rmtree(target)
print 'Creating %s' % target
os.mkdir(target)
	
for folder in folder_list:
	print 'Copying %s' % folder
	shutil.copytree(folder, os.path.join(target, folder), \
		ignore=ignore_bytecode)
print 'Copying resources'
shutil.copytree('resources', os.path.join(target, 'resources'), \
	ignore=ignore_resources)
print 'Copying examples'
shutil.copytree('examples', os.path.join(target, 'examples'))

print 'Copying plugins'
os.mkdir(os.path.join(target, 'plugins'))
for plugin in included_plugins:
	print 'Copying plugin %s' % plugin
	shutil.copytree(os.path.join('plugins', plugin), os.path.join(target, \
		'plugins', plugin))

print 'Copying modules'
for module in module_list:
	print 'Copying %s' % module
	shutil.copyfile(os.path.join(module_folder, module), \
		os.path.join(target, module))
	
print 'Copying dummy PyQt4'
shutil.copytree('PyQt4.dummy', os.path.join(target, 'PyQt4'))
print 'Copying main.py'
shutil.copyfile('android-main.py', os.path.join(target, 'main.py'))
print 'Copying .android.json'
shutil.copyfile('resources/android/android.json', os.path.join(target, '.android.json'))
print 'Copying android-icon.png'
shutil.copyfile('resources/android/android-icon.png', \
	os.path.join(target, 'android-icon.png'))
print 'Copying android-splash.png'
shutil.copyfile('resources/android/android-splash.jpg', \
	os.path.join(target, 'android-splash.jpg'))
print 'Building'
os.chdir(pgs4a_folder)
subprocess.call(build_cmd.split())