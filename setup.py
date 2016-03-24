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

import glob
import os
import shutil
from setuptools import setup
from libopensesame import metadata
from setup_shared  import included_plugins, included_extensions

if os.name == 'nt':
	share_folder = ''
else:
	share_folder = "/usr/share/opensesame"
exclude_resources = [
	'.hidden',
	'eco_alt_template.opensesame.tar.gz'
	]

def resources():

	"""
	desc:
		Create a list of all resource files that need to be included

	returns:
		A list of (target folder, filenames) tuples.
	"""

	l = []
	for root, dirnames, filenames in os.walk("resources"):
		print(root)
		if root in ["resources/bak", "resources/ui"]:
			continue
		for f in filenames:
			if f not in exclude_resources and (os.path.splitext(f)[1] not in \
				[".csv"] or f in ["icon_map.csv"]):
				l.append( (os.path.join(share_folder, root), [os.path.join( \
					root, f)] ) )
	return l

def recursive_glob(src_folder, target_folder):

	"""
	desc:
		Recursively gets all files that are in src folder.

	arguments:
		src_folder:		The source folder.
		target_folder:	The target folder.

	returns:
		A list of (target folder, filenames) tuples.
	"""

	l = []
	print(src_folder)
	path_list = []
	for path in os.listdir(src_folder):
		full_path = os.path.join(src_folder, path)
		if os.path.isdir(full_path):
			l += recursive_glob(full_path, os.path.join(target_folder, path))
			continue
		if path.startswith('.'):
			continue
		if path.endswith('.pyc'):
			continue
		if path.endswith('.pyo'):
			continue
		if path.endswith('~'):
			continue
		print('\t%s' % full_path)
		path_list.append(full_path)
	l.append( (target_folder, path_list) )
	return l

def plugins(included, _type='plugins'):

	"""
	desc:
		Create a list of all plugin files that need to be included.

	arguments:
		included:	A list of included plugin names.
		_type:		The plugin type, i.e. 'plugins' or 'extensions'.

	returns:
		A list of (target folder, filenames) tuples.
	"""

	l = []
	for plugin in os.listdir(_type):
		if plugin in included:
			target_folder = os.path.join(share_folder, _type, plugin)
			src_folder = os.path.join(_type, plugin)
			l += recursive_glob(src_folder, target_folder)
	return l

def data_files_linux():

	return [
		("/usr/share/icons/hicolor/scalable/apps", ["data/opensesame.svg"]),
		("/usr/share/opensesame", ["COPYING"]),
		("/usr/share/mime/packages", ["data/x-opensesame-experiment.xml"]),
		("/usr/share/applications", ["data/opensesame.desktop"]),
		("/usr/share/opensesame/help", glob.glob("help/*.md")),
		("/usr/share/opensesame/sounds", glob.glob("sounds/*"))
		] + \
		plugins(included=included_plugins, _type='plugins') + \
		plugins(included=included_extensions, _type='extensions') + \
		resources()

def data_files_windows():

	return [
		("help", glob.glob("help/*.md")),
		("sounds", glob.glob("sounds/*"))
		] + \
		plugins(included=included_plugins, _type='plugins') + \
		plugins(included=included_extensions, _type='extensions') + \
		resources()


def data_files():

	if os.name == 'nt':
		return data_files_windows()
	return data_files_linux()

# Temporarily create README.txt
shutil.copy('readme.md', 'README.txt')

setup(name="opensesame",
	version = metadata.deb_version,
	description = "A graphical experiment builder for the social sciences",
	author = "Sebastiaan Mathot",
	author_email = "s.mathot@cogsci.nl",
	url = "http://osdoc.cogsci.nl/",
	scripts = ["opensesame", "opensesamerun"],
	packages = [
		"openexp",
		"openexp._canvas",
		"openexp._keyboard",
		"openexp._mouse",
		"openexp._sampler",
		"openexp._coordinates",
		"openexp._clock",
		"openexp._log",
		"openexp._color",
		"libopensesame",
		"libopensesame.widgets",
		"libopensesame.widgets.themes",
		"libopensesame.sketchpad_elements",
		"libqtopensesame",
		"libqtopensesame.extensions",
		"libqtopensesame.actions",
		"libqtopensesame.dialogs",
		"libqtopensesame.items",
		"libqtopensesame.misc",
		"libqtopensesame.runners",
		"libqtopensesame.widgets",
		"libqtopensesame.validators",
		"libqtopensesame.sketchpad_elements",
		"libqtopensesame._input",
		"libqtopensesame.console",
		],
	package_dir = {
		"openexp" : "openexp",
		"libopensesame" : "libopensesame",
		"libqtopensesame" : "libqtopensesame"
		},
	data_files=data_files()
	)

# Clean up temporary readme
os.remove('README.txt')
