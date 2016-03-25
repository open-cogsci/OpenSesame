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
import fnmatch

if os.name == u'nt':
	SHARE_FOLDER = u''
else:
	SHARE_FOLDER = u'/usr/share/opensesame'

EXCLUDE = [
	u'[\\/].*',
	u'*eco_alt_template.osexp',
	u'*~',
	u'*.pyc',
	u'*.pyo',
	u'*__pycache__*'
	]


def is_excluded(path):

	for m in EXCLUDE:
		if fnmatch.fnmatch(path, m):
			return True
	return False


def resources():

	"""
	desc:
		Create a list of all resource files that need to be included

	returns:
		A list of (target folder, filenames) tuples.
	"""

	l = []
	for root, dirnames, filenames in os.walk(u'resources'):
		for f in filenames:
			path = os.path.join(root, f)
			if not is_excluded(path):
				l.append((os.path.join(SHARE_FOLDER, root), [path]))
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
		if is_excluded(full_path):
			continue
		print(u'\t%s' % full_path)
		path_list.append(full_path)
	l.append( (target_folder, path_list) )
	return l


def plugins(included, _type=u'plugins'):

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
			target_folder = os.path.join(SHARE_FOLDER, _type, plugin)
			src_folder = os.path.join(_type, plugin)
			l += recursive_glob(src_folder, target_folder)
	return l


def data_files_linux():

	return [
		(u"/usr/share/icons/hicolor/scalable/apps", [u"data/opensesame.svg"]),
		(u"/usr/share/opensesame", [u"COPYING"]),
		(u"/usr/share/mime/packages", [u"data/x-opensesame-experiment.xml"]),
		(u"/usr/share/applications", [u"data/opensesame.desktop"]),
		(u"/usr/share/opensesame/help", glob.glob(u"help/*.md")),
		(u"/usr/share/opensesame/sounds", glob.glob(u"sounds/*"))
		] + \
		plugins(included=included_plugins, _type=u'plugins') + \
		plugins(included=included_extensions, _type=u'extensions') + \
		resources()


def data_files_windows():

	return [
		(u"help", glob.glob(u"help/*.md")),
		(u"sounds", glob.glob(u"sounds/*"))
		] + \
		plugins(included=included_plugins, _type=u'plugins') + \
		plugins(included=included_extensions, _type=u'extensions') + \
		resources()


def data_files():

	if os.name == u'nt':
		return data_files_windows()
	return data_files_linux()


# Temporarily create README.txt
shutil.copy(u'readme.md', u'README.txt')

setup(name=u"python-opensesame",
	version=metadata.__version__,
	description=u"A graphical experiment builder for the social sciences",
	author=u"Sebastiaan Mathot",
	author_email=u"s.mathot@cogsci.nl",
	url=u"http://osdoc.cogsci.nl/",
	scripts=[u"scripts/opensesame.py", u"scripts/opensesamerun.py"],
	include_package_data=False,
	packages=[
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
	data_files=data_files(),
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
		],
	)

# Clean up temporary readme
os.remove(u'README.txt')
