#!/usr/bin/env python

from distutils.core import setup
import glob
import os
import os.path
import libopensesame.misc

# Not all plugins are included
included_plugins = ["advanced_delay", "external_script", "fixation_dot", "text_display", "text_input", "notepad"]

def plugins():
	"""
	Create a list of all plugins that need to be included in the release
	"""
	global included_plugins

	l = []
	for plugin in os.listdir("plugins"):

		if plugin in included_plugins:
			l.append( ("/usr/share/opensesame/plugins/%s" % plugin, glob.glob("plugins/%s/*" % plugin)) )

	return l

setup(name="opensesame",

	version = libopensesame.misc.version,
	description = "A graphical experiment builder for the social sciences",
	author = "Sebastiaan Mathot",
	author_email = "s.mathot@cogsci.nl",
	url = "http://www.cogsci.nl",
	scripts = ["opensesame", "opensesamerun"],
	packages = ["openexp", "openexp._canvas", "openexp._keyboard", "openexp._mouse", "openexp._sampler", "openexp._synth", "libopensesame", "libqtopensesame"],
	package_dir = {"openexp" : "openexp", "libopensesame" : "libopensesame", "libqtopensesame" : "libqtopensesame"},
	data_files=[
		("/usr/share/opensesame", ["COPYING"]),
		("/usr/share/applications", ["data/opensesame.desktop"]),
		("/usr/share/opensesame/resources", glob.glob("resources/*.png") + glob.glob("resources/*.opensesame") + glob.glob("resources/*.ttf") + ["resources/tips.txt"]),
		("/usr/share/opensesame/help", glob.glob("help/*.html")),
		("/usr/share/opensesame/sounds", glob.glob("sounds/*")),
		("/usr/share/opensesame/examples", glob.glob("examples/*")),
		] + plugins()
	)


