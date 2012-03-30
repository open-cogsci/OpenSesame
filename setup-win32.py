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
import py2exe
import os
import os.path
import shutil
import libqtopensesame.qtopensesame
import libopensesame.misc
import psychopy
import urllib

# Some settings
include_plugins = True
include_media_player = True
include_media_player_vlc = False
include_examples = True
include_sounds = True
include_faenza = True
include_inpout32 = True
include_simpleio = False
python_folder = "C:\\Python26"
python_version = "2.6"

# Create empty destination folders
if os.path.exists("dist"):
	shutil.rmtree("dist")
os.mkdir("dist")
os.mkdir(os.path.join("dist", "plugins"))

# Setup options
setup(

	# Use 'console' to have the programs run in a terminal and
	# 'windows' to run them normally.
	windows = [{
		"script" : "opensesame",
		"icon_resources": [(0, os.path.join("resources", "opensesame.ico"))],
		},{
		"script" : "opensesamerun",
		"icon_resources": [(0, os.path.join("resources", "opensesame.ico"))],
		}],
	options = {
		"py2exe" : {
		"compressed" : True,
		"optimize": 2,
		"bundle_files": 3,
		"includes": "libqtopensesame.*, " + \
			"libqtopensesame.items.*, " + \
			"libqtopensesame.widgets.*, " + \
			"libqtopensesame.actions.*, " + \
			"libqtopensesame.ui.*, " + \
			"libqtopensesame.dialogs.*, " + \
			"libqtopensesame.misc.*, " + \
			"sip, pygame, ctypes, weakref, logging, " + \
			"OpenGL.platform.win32, OpenGL.arrays.ctypesarrays, " + \
			"OpenGL.arrays.numpymodule, OpenGL.arrays.lists, " + \
			"OpenGL.arrays.numbers, OpenGL.arrays.strings, OpenGL.GL, " + \
			"OpenGL.GLU",
		"dll_excludes" : ["MSVCP90.DLL", "libzmq.dll"]
		}
	},
)

def ignore_resources(folder, files):
	l = []
	print "... %s" % folder
	for f in files:
		if os.path.splitext(f)[1] in [".csv", ".pyc"] and f not in \
			["icon_map.csv"]:
			l.append(f)
		if f == "Faenza" and not include_faenza:
			l.append(f)
	return l

print "copying resources"
shutil.copytree("resources", os.path.join("dist", "resources"), symlinks=True, \
	ignore=ignore_resources)

print "copying README info etc."
shutil.copyfile("README", os.path.join("dist", "README"))
shutil.copyfile("LICENSE-BIN", os.path.join("dist", "LICENSE"))
shutil.copyfile("COPYING", os.path.join("dist", "COPYING"))
shutil.copytree("help", os.path.join("dist", "help"))

print "copying PyGame/ SDLL dll's"
shutil.copyfile("""%s\Lib\site-packages\pygame\SDL_ttf.dll""" \
	% python_folder, """dist\SDL_ttf.dll""")
shutil.copyfile("""%s\Lib\site-packages\pygame\libfreetype-6.dll""" \
	% python_folder, """dist\libfreetype-6.dll""")
shutil.copyfile("""%s\Lib\site-packages\pygame\libogg-0.dll""" \
	% python_folder, """dist\libogg-0.dll""")

if include_simpleio:
	print "copying simpleio.dll"
	shutil.copyfile("""%s\Lib\site-packages\parallel\simpleio.dll""" \
		% python_folder, """dist\simpleio.dll""")

# Required by psychopy
print "copying PsychoPy Windows.spec"
shutil.copyfile( \
	"""%s\Lib\site-packages\PsychoPy-%s-py%s.egg\psychopy\preferences\Windows.spec""" \
	% (python_folder, psychopy.__version__, python_version), \
	"""dist\\resources\Windows.spec""")

if include_inpout32:
	print "copying inpout32.dll"
	urllib.urlretrieve ("http://files.cogsci.nl/misc/inpout32.dll", \
		"dist\\inpout32.dll")

if include_plugins:
	print "copying plugins"
	included_plugins = [ \
		"advanced_delay", \
		"external_script", \
		"fixation_dot",
		"text_display", \
		"text_input", \
		"notepad", \
		"srbox", \
		"port_reader", \
		"reset_feedback", \
		]

	for plugin in included_plugins:
		print "copying plugin", plugin
		shutil.copytree(os.path.join("plugins", plugin), os.path.join("dist", \
			"plugins", plugin))
		for path in os.listdir(os.path.join("plugins", plugin)):
			if path[-1] == "~" or os.path.splitext(path)[1] in [".pyc"]:
				print "removing file", path
				os.remove(os.path.join("dist", "plugins", plugin, path))

if include_media_player:
	print "copying media_player"
	os.mkdir("dist\plugins\media_player")
	shutil.copyfile("""..\media_player\media_player.py""", \
		"""dist\plugins\media_player\media_player.py""")
	shutil.copyfile("""..\media_player\media_player.html""", \
		"""dist\plugins\media_player\media_player.html""")
	shutil.copyfile("""..\media_player\media_player.png""", \
		"""dist\plugins\media_player\media_player.png""")
	shutil.copyfile("""..\media_player\media_player_large.png""", \
		"""dist\plugins\media_player\media_player_large.png""")
	shutil.copyfile("""..\media_player\info.txt""", \
		"""dist\plugins\media_player\info.txt""")

if include_media_player_vlc:
	print "copying media_player_vlc"
	os.mkdir("dist\plugins\media_player_vlc")
	shutil.copyfile("""..\media_player_vlc\\vlc.py""", \
		"""dist\plugins\media_player_vlc\\vlc.py""")	
	shutil.copyfile("""..\media_player_vlc\media_player_vlc.py""", \
		"""dist\plugins\media_player_vlc\media_player_vlc.py""")
	shutil.copyfile("""..\media_player_vlc\media_player_vlc.html""", \
		"""dist\plugins\media_player_vlc\media_player_vlc.html""")
	shutil.copyfile("""..\media_player_vlc\media_player_vlc.png""", \
		"""dist\plugins\media_player_vlc\media_player_vlc.png""")
	shutil.copyfile("""..\media_player_vlc\media_player_vlc_large.png""", \
		"""dist\plugins\media_player_vlc\media_player_vlc_large.png""")
	shutil.copyfile("""..\media_player_vlc\info.txt""", \
		"""dist\plugins\media_player_vlc\info.txt""")		

if include_examples:
	print "copying examples"
	shutil.copytree("examples", os.path.join("dist", "examples"))
	for path in os.listdir(os.path.join("dist", "examples")):
		if path[-1] == "~" or os.path.splitext(path)[1] not in [".opensesame", \
			".gz"]:
			print "removing file", path
			os.remove(os.path.join("dist", "examples", path))

if include_sounds:
	print "copying sounds"
	shutil.copytree("sounds", os.path.join("dist", "sounds"))
