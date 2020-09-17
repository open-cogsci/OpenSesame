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

from libopensesame.py3compat import *
import os
import sys
import shutil
from setuptools import setup
from libopensesame import metadata
from setup_shared import included_plugins, included_extensions
import fnmatch

# Fix a bug in the packaging of stdeb
try:
	from stdeb3 import util
except ImportError:
	pass
else:
	if not hasattr(util, 'RULES_BINARY_ALL_TARGET'):
		util.RULES_BINARY_ALL_TARGET = '\nbinary: binary-indep\n'

# For debian packaging, we use a slightly different version-number scheme, which
# is triggered by setting the USEDEBVERSION environment variable.
if 'USEDEBVERSION' in os.environ and os.environ['USEDEBVERSION'] == '1':
	version = metadata.deb_version
else:
	version = metadata.__version__

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
	for root, dirnames, filenames in os.walk(u'opensesame_resources'):
		for f in filenames:
			path = os.path.join(root, f)
			if not is_excluded(path):
				l.append((os.path.join(u'share', root), [path]))
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
	l.append( (os.path.join(u'share', target_folder), path_list) )
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
	for plugin in os.listdir(u'opensesame_%s' % _type):
		if plugin in included:
			folder = os.path.join(u'opensesame_%s' % _type, plugin)
			l += recursive_glob(folder, folder)
	return l


def data_files():

	return (
		[
			(u"share/icons/hicolor/scalable/apps", [u"mime/opensesame.svg"]),
			(u"share/applications", [u"mime/opensesame.desktop"]),
		] +
		plugins(included=included_plugins, _type=u'plugins') +
		plugins(included=included_extensions, _type=u'extensions') +
		resources()
	)


# Temporarily create README.txt
shutil.copy(u'readme.md', u'README.txt')
setup(
	# The PyPi name is python-opensesame
	name=u'opensesame' if u'bdist_deb' in sys.argv else u'python-opensesame',
	version=version,
	description=u"A graphical experiment builder for the social sciences",
	author=u"Sebastiaan Mathot",
	author_email=u"s.mathot@cogsci.nl",
	url=u"http://osdoc.cogsci.nl/",
	entry_points={
		'gui_scripts': [
			'opensesame = libqtopensesame.__main__:opensesame',
			'opensesamerun = libqtopensesame.__main__:opensesamerun',
		]
	},
	# scripts=['opensesame', 'opensesamerun'],
	include_package_data=False,
	packages=[
		"openexp",
		"openexp._canvas",
		"openexp._canvas._arrow",
		"openexp._canvas._circle",
		"openexp._canvas._element",
		"openexp._canvas._ellipse",
		"openexp._canvas._fixdot",
		"openexp._canvas._gabor",
		"openexp._canvas._image",
		"openexp._canvas._line",
		"openexp._canvas._noise_patch",
		"openexp._canvas._polygon",
		"openexp._canvas._rect",
		"openexp._canvas._richtext",
		"openexp._keyboard",
		"openexp._mouse",
		"openexp._sampler",
		"openexp._coordinates",
		"openexp._clock",
		"openexp._log",
		"openexp._color",
		"libopensesame",
		"libopensesame.osexpfile",
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
		],
	data_files=data_files(),
	install_requires=[
		'pyqode3.python',
		'python-qdatamatrix',
		'python-pseudorandom',
		'python-qnotifications',
		'python-fileinspector',
		'PyYAML',
		'webcolors',
		],
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
