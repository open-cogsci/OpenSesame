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

__author__ = "Sebastiaan Mathot"
__license__ = "GPLv3"

from distutils.core import setup
import glob
import os
import os.path
import fnmatch
import libqtopensesame.qtopensesame
import libopensesame.misc

share_folder = "/usr/share/opensesame"

# Not all plugins are included
included_plugins = [ \
	"advanced_delay", \
	"external_script", \
	"fixation_dot", \
	"notepad", \
	"reset_feedback", \
	"srbox", \
	"text_display", \
	"text_input", \
	]
	
def resources():

	"""
	Create a list of all resource files that need to be included
	
	Returns:
	A list of resource files
	"""
	
	l = []
	for root, dirnames, filenames in os.walk("resources"):
		print root
		if root in ["resources/bak", "resources/ui"]:
			continue
		for f in filenames:			
			if os.path.splitext(f)[1] not in [".csv"] or f  in ["icon_map.csv"]:
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
			l.append( (os.path.join(share_folder, "plugins", plugin), \
				glob.glob("plugins/%s/*" % plugin)) )
	return l

setup(name="opensesame",

	version = libopensesame.misc.version,
	description = "A graphical experiment builder for the social sciences",
	author = "Sebastiaan Mathot",
	author_email = "s.mathot@cogsci.nl",
	url = "http://www.cogsci.nl/",
	scripts = ["opensesame", "opensesamerun"],
	packages = ["openexp", \
		"openexp._canvas", \
		"openexp._keyboard", \
		"openexp._mouse", \
		"openexp._sampler", \
		"openexp._synth", \
		"libopensesame", \
		"libqtopensesame", \
		"libqtopensesame.actions", \
		"libqtopensesame.dialogs", \
		"libqtopensesame.items", \
		"libqtopensesame.misc", \
		"libqtopensesame.ui", \
		"libqtopensesame.widgets", \
		],
	package_dir = {"openexp" : "openexp", "libopensesame" : "libopensesame", \
		"libqtopensesame" : "libqtopensesame"},
	data_files=[
		("/usr/share/opensesame", ["COPYING"]),
		("/usr/share/applications", ["data/opensesame.desktop"]),
		("/usr/share/opensesame/help", glob.glob("help/*.html")),
		("/usr/share/opensesame/sounds", glob.glob("sounds/*")),
		("/usr/share/opensesame/examples", \
			glob.glob("examples/*.opensesame") + \
			glob.glob("examples/*.opensesame.tar.gz")),
		] + plugins() + resources()
	)


