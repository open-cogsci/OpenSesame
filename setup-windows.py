#!/usr/bin/env python

from distutils.core import setup
import glob
import pygame
import py2exe
import os
import os.path
import shutil

if not os.path.exists("dist"):
	os.mkdir("dist")
shutil.rmtree("dist")

setup(
	windows = [{
		"script" : "opensesame",
		'icon_resources': [(0, os.path.join("resources", "opensesame.ico"))],
		},{
		"script" : "opensesamerun",
		'icon_resources': [(0, os.path.join("resources", "opensesame.ico"))],
		}],
	options = {
		'py2exe' : {
		'compressed' : True,
		'optimize': 2,
		'bundle_files': 3,
		'includes': 'sip, pygame',
		"dll_excludes" : ["MSVCP90.DLL"]
		}
	},		
)

os.mkdir(os.path.join("dist", "resources"))

# Only copy the relevant resources, to keep the folder clean
for f in os.listdir("resources"):
	if os.path.splitext(f)[1] in [".png", ".ttf", ".opensesame"] or f in ("README", "tips.txt"):
		shutil.copyfile(os.path.join("resources", f), os.path.join("dist", "resources", f))

#shutil.copytree("resources", os.path.join("dist", "resources"))
shutil.copytree("sounds", os.path.join("dist", "sounds"))

os.mkdir(os.path.join("dist", "plugins"))
included_plugins = ["advanced_delay", "external_script", "fixation_dot", "text_display", "text_input", "media_player", "video_player"]
for plugin in included_plugins:
	shutil.copytree(os.path.join("plugins", plugin), os.path.join("dist", "plugins", plugin))

shutil.copyfile("README", os.path.join("dist", "README"))	
shutil.copyfile("COPYING", os.path.join("dist", "COPYING"))
shutil.copytree("examples", os.path.join("dist", "examples"))
shutil.copytree("help", os.path.join("dist", "help"))
shutil.copyfile("""C:\Python26\Lib\site-packages\pygame\SDL_ttf.dll""", """dist\SDL_ttf.dll""")
shutil.copyfile("""C:\Python26\Lib\site-packages\pygame\libfreetype-6.dll""", """dist\libfreetype-6.dll""")
shutil.copyfile("""C:\Python26\Lib\site-packages\pygame\libogg-0.dll""", """dist\libogg-0.dll""")

