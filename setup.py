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
import libqtopensesame.qtopensesame
import libopensesame.misc

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
			l.append( ("/usr/share/opensesame/plugins/%s" % plugin, \
				glob.glob("plugins/%s/*" % plugin)) )
	return l

setup(name="opensesame",

	version = libopensesame.misc.version,
	description = "A graphical experiment builder for the social sciences",
	author = "Sebastiaan Mathot",
	author_email = "s.mathot@cogsci.nl",
	url = "http://www.cogsci.nl/",
	scripts = ["opensesame", "opensesamerun"],
	packages = ["openexp", "openexp._canvas", "openexp._keyboard", \
		"openexp._mouse", "openexp._sampler", "openexp._synth", "libopensesame", \
		"libqtopensesame"],
	package_dir = {"openexp" : "openexp", "libopensesame" : "libopensesame", \
		"libqtopensesame" : "libqtopensesame"},
	data_files=[
		("/usr/share/opensesame", ["COPYING"]),
		("/usr/share/applications", ["data/opensesame.desktop"]),
		("/usr/share/opensesame/resources", glob.glob("resources/*.png")
			+ glob.glob("resources/*.opensesame")
			+ glob.glob("resources/*.ttf")
			+ glob.glob("resources/*.qss")
			+ ["resources/tips.txt"]),
		("/usr/share/opensesame/help", glob.glob("help/*.html")),
		("/usr/share/opensesame/sounds", glob.glob("sounds/*")),
		("/usr/share/opensesame/examples", \
			glob.glob("examples/*.opensesame") + \
			glob.glob("examples/*.opensesame.tar.gz")),
		] + plugins()
	)


