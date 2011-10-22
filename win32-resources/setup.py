#!/usr/bin/env python

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

# Create empty destination folders
if os.path.exists("dist"):
	shutil.rmtree("dist")
os.mkdir("dist")
os.mkdir(os.path.join("dist", "resources"))
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
		"includes": "sip, pygame, ctypes, weakref, logging, " + \
			"OpenGL.platform.win32, OpenGL.arrays.ctypesarrays, " + \
			"OpenGL.arrays.numpymodule, OpenGL.arrays.lists, " + \
			"OpenGL.arrays.numbers, OpenGL.arrays.strings, OpenGL.GL, OpenGL.GLU",
		"dll_excludes" : ["MSVCP90.DLL"]
		}
	},
)

# Only copy the relevant resources, to keep the folder clean
for f in os.listdir("resources"):
	if os.path.splitext(f)[1] in [".png", ".ttf", ".opensesame", ".qss"] or f in ("README", "tips.txt"):
		shutil.copyfile(os.path.join("resources", f), os.path.join("dist", "resources", f))

# Copy the plug-ins
included_plugins = ["advanced_delay", "external_script", "fixation_dot",
	"text_display", "text_input", "notepad", "srbox", "port_reader",
	"reset_feedback"]

for plugin in included_plugins:
	print "copying plugin", plugin
	shutil.copytree(os.path.join("plugins", plugin), os.path.join("dist", "plugins", plugin))
	for path in os.listdir(os.path.join("plugins", plugin)):
		if path[-1] == "~" or os.path.splitext(path)[1] in [".pyc"]:
			print "removing file", path
			os.remove(os.path.join("dist", "plugins", plugin, path))

# Copy the media_player separately
os.mkdir("dist\plugins\media_player")
shutil.copyfile("""..\media_player\media_player.py""", """dist\plugins\media_player\media_player.py""")
shutil.copyfile("""..\media_player\media_player.html""", """dist\plugins\media_player\media_player.html""")
shutil.copyfile("""..\media_player\media_player.png""", """dist\plugins\media_player\media_player.png""")
shutil.copyfile("""..\media_player\media_player_large.png""", """dist\plugins\media_player\media_player_large.png""")
shutil.copyfile("""..\media_player\info.txt""", """dist\plugins\media_player\info.txt""")

# Copy Remaining resources and dll that have been missed by Py2exe
shutil.copyfile("README", os.path.join("dist", "README"))
shutil.copyfile("COPYING", os.path.join("dist", "COPYING"))
shutil.copytree("sounds", os.path.join("dist", "sounds"))
shutil.copytree("help", os.path.join("dist", "help"))

# Copy the examples
shutil.copytree("examples", os.path.join("dist", "examples"))
for path in os.listdir(os.path.join("dist", "examples")):
		if path[-1] == "~" or os.path.splitext(path)[1] not in [".opensesame", ".gz"]:
			print "removing file", path
			os.remove(os.path.join("dist", "examples", path))

shutil.copyfile("""C:\Python26\Lib\site-packages\pygame\SDL_ttf.dll""", """dist\SDL_ttf.dll""")
shutil.copyfile("""C:\Python26\Lib\site-packages\pygame\libfreetype-6.dll""", """dist\libfreetype-6.dll""")
shutil.copyfile("""C:\Python26\Lib\site-packages\pygame\libogg-0.dll""", """dist\libogg-0.dll""")

# Required by pyparallel
shutil.copyfile("""C:\Python26\Lib\site-packages\parallel\simpleio.dll""", """dist\simpleio.dll""")

# Required by psychopy
shutil.copyfile("""C:\Python26\Lib\site-packages\PsychoPy-%s-py2.6.egg\psychopy\preferences\Windows.spec""" % psychopy.__version__, """dist\\resources\Windows.spec""")

# Provides easy access to the parallel port
shutil.copyfile("win32-resources\inpout32.dll", "dist\inpout32.dll")
