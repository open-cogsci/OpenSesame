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

from distutils.core import setup
import glob
import os
import os.path
import fnmatch
import libqtopensesame.qtopensesame
import libopensesame.misc

# List of included plug-ins
included_plugins = [
	'advanced_delay',
	'external_script',
	'fixation_dot',
	'form_base',
	'form_text_input',
	'form_consent',
	'form_text_display',
	'form_multiple_choice',
	'joystick',
	'notepad',
	'parallel',
	'port_reader',
	'repeat_cycle',
	'reset_feedback',
	'srbox',
	'text_display',
	'text_input',
	'touch_response',
	]

share_folder = "/usr/share/opensesame"

exclude_resources = [
	'.hidden',
	'eco_alt_template.opensesame.tar.gz'
	]

def resources():

	"""
	Create a list of all resource files that need to be included

	Returns:
	A list of resource files
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

def plugins():

	"""
	Create a list of all plugins that need to be included in the release

	Returns:
	A list of plugins
	"""

	global included_plugins
	l = []
	for plugin in os.listdir("plugins"):
		if plugin in included_plugins:
			# Copy all files in the plug-in folder, but not any subdirectories,
			# because those will trigger an error
			target_folder = os.path.join(share_folder, "plugins", plugin)
			src_folder = "plugins/%s" % plugin
			file_list = []
			for fname in os.listdir(src_folder):
				path = os.path.join(src_folder, fname)
				if not os.path.isdir(path):
					file_list.append(path)
			l.append( (target_folder, file_list) )
	# Copy plug-in subfolders where necessary. These are manual hacks to deal
	# with plug-ins that have subdirectories.
	l.append( (os.path.join(share_folder, 'plugins/joystick/_libjoystick'), \
		glob.glob('plugins/joystick/_libjoystick/*')) )
	return l

setup(name="opensesame",
	version = libopensesame.misc.version,
	description = "A graphical experiment builder for the social sciences",
	author = "Sebastiaan Mathot",
	author_email = "s.mathot@cogsci.nl",
	url = "http://osdoc.cogsci.nl/",
	scripts = ["opensesame", "opensesamerun"],
	packages = ["openexp",
		"openexp._canvas",
		"openexp._keyboard",
		"openexp._mouse",
		"openexp._sampler",
		"openexp._synth",
		"libopensesame",
		"libopensesame.widgets",
		"libopensesame.widgets.themes",
		"libqtopensesame",
		"libqtopensesame.actions",
		"libqtopensesame.dialogs",
		"libqtopensesame.items",
		"libqtopensesame.misc",
		"libqtopensesame.runners",
		"libqtopensesame.ui",
		"libqtopensesame.widgets",
		],
	package_dir = {
		"openexp" : "openexp",
		"libopensesame" : "libopensesame",
		"libqtopensesame" : "libqtopensesame"
		},
	data_files=[
		("/usr/share/opensesame", ["COPYING"]),
		("/usr/share/mime/packages", ["data/x-opensesame-experiment.xml"]),
		("/usr/share/applications", ["data/opensesame.desktop"]),
		("/usr/share/opensesame/help", glob.glob("help/*.md")),
		("/usr/share/opensesame/sounds", glob.glob("sounds/*")),
		("/usr/share/opensesame/examples", \
			glob.glob("examples/*.opensesame") + \
			glob.glob("examples/*.opensesame.tar.gz")),
		] + plugins() + resources()
	)
