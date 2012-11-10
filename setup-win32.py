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

ABOUT
=====
This script will create a binary Windows package of OpenSesame, using py2exe.
If possible, dependencies are simply copied into a subfolder and compiled to
.pyo format. If not possible, they are included in the library.zip file, which
is the default py2exe way of including dependencies.

USAGE
=====
Don't forget to invoke Python with the -O argument. Otherwise, the dependencies
will be compiled to .pyc, instead of .pyo, and the .py source files will not be
pruned. And that doesn't look very professional (although it does work).

$ ./python -O setup-win32.py py2exe

"""

from distutils.core import setup
import distutils.sysconfig as sysconfig
import compileall
import glob
import py2exe
import os
import sys
import shutil
import libqtopensesame.qtopensesame
import libopensesame.misc
import psychopy
import urllib

# Some settings
include_plugins = True
include_media_player = False
include_media_player_vlc = False
include_examples = True
include_sounds = True
include_faenza = True
include_inpout32 = True
include_simpleio = True
python_folder = "C:\\Python_2.7.3-32"
python_version = "2.7"

# Packages that are too be copied for the site-packages folder, rather than
# included by py2exe in the library .zip file
copy_packages = [
	'libopensesame',
	'libqtopensesame',
	'openexp',
	'expyriment',
	'psychopy',
	'scipy',
	'numpy',
	'serial',
	'parallel',
	'OpenGL',
	'PIL',
	'pygame',
	'pyglet',
	]

# Packages that are part of the standard Python packages, but should not be
# included
exclude_packages = [
	'idlelib',
	'antigravity', # Kind of funny, importing this opens: http://xkcd.com/353/
	'test', # Avoid automated tests, because they take ages
	]

# Packages that are not part of the standard Python packages (or not detected
# as such), but should nevertheless be includes
include_packages = [
	'sip',
	'pyaudio',
	'Image',
	'PyQt4.QtCore',
	'PyQt4.QtGui',
	'PyQt4.Qsci',
	'PyQt4.QtWebKit',
	'PyQt4.QtNetwork',
	'cv2',
	]

exclude_dll = [
	"MSVCP90.DLL",
	"libzmq.dll",
	]
	
# Create empty destination folders
if os.path.exists("dist"):
	shutil.rmtree("dist")
os.mkdir("dist")
os.mkdir(os.path.join("dist", "plugins"))

# A filter to ignore non-relevant package files
def ignore_package_files(folder, files):
	l = []
	for f in files:
		if os.path.splitext(f)[1] in [".pyo", ".pyc"]:
			l.append(f)
	return l

# A function to strip non-compiled scripts and backup files
def strip_py(folder):
	for path in os.listdir(folder):
		path = os.path.join(folder, path)
		if os.path.isdir(path):
			strip_py(path)
			continue
		base, ext = os.path.splitext(path)
		if (ext in ('.py', '.pyc') and os.path.exists(base+'.pyo')) or \
			path[-1] == '~':
			print 'stripping %s' % path
			os.remove(path)

# Copy packages	
for pkg in copy_packages:
	print 'copying packages %s ... ' % pkg
	exec('import %s as _pkg' % pkg)
	pkg_folder = os.path.dirname(_pkg.__file__)
	pkg_target = os.path.join("dist", pkg)
	shutil.copytree(pkg_folder, pkg_target, symlinks=True, \
		ignore=ignore_package_files)
	compileall.compile_dir(pkg_target, force=True)
	strip_py(pkg_target)

# Create a list of standard pakcages that should be included
# http://stackoverflow.com/questions/6463918/how-can-i-get-a-list-of-all-the-python-standard-library-modules
print 'detecting standard Python packages and modules ... '
std_pkg = []
std_lib = sysconfig.get_python_lib(standard_lib=True)
for top, dirs, files in os.walk(std_lib):
	for nm in files:
		prefix = top[len(std_lib)+1:]
		if prefix[:13] == 'site-packages':
			continue
		if nm == '__init__.py':
			pkg = top[len(std_lib)+1:].replace(os.path.sep,'.')
		elif nm[-3:] == '.py':
			pkg =  os.path.join(prefix, nm)[:-3].replace(os.path.sep,'.')
		elif nm[-3:] == '.so' and top[-11:] == 'lib-dynload':
			pkg = nm[0:-3]
		if pkg[0] == '_':
			continue
		exclude = False
		for _pkg in exclude_packages:
			if pkg.find(_pkg) == 0:
				exclude = True
				break
		if exclude:
			continue
		try:
			exec('import %s' % pkg)
		except:
			continue
		print pkg			
		std_pkg.append(pkg)
for pkg in sys.builtin_module_names:
	print pkg			
	std_pkg.append(pkg)

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
		"excludes": copy_packages,
		"includes" : std_pkg + include_packages,
		"dll_excludes" : exclude_dll,
		}
	}
)

# A filter to ignore non-relevant resource files
def ignore_resources(folder, files):
	l = []
	print "... %s" % folder
	for f in files:
		if os.path.splitext(f)[1] in [".csv", ".pyc"] and f not in \
			["icon_map.csv"]:
			l.append(f)
		if 'Faenza' in folder and f == 'scalable':
			l.append(f)
		if f == "Faenza" and not include_faenza:
			l.append(f)
	return l

# Copy resource files
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
	
print "copying PIL.pth"
shutil.copyfile("""%s\Lib\site-packages\PIL.pth""" \
	% python_folder, """dist\PIL.pth""")

if include_simpleio:
	print "copying simpleio.dll"
	shutil.copyfile("""%s\Lib\site-packages\parallel\simpleio.dll""" \
		% python_folder, """dist\simpleio.dll""")

if include_inpout32:
	print "copying inpout32.dll"
	urllib.urlretrieve ("http://files.cogsci.nl/misc/inpout32.dll", \
		"dist\\inpout32.dll")

# Include plug-ins
if include_plugins:
	print "copying plugins"
	included_plugins = [
		"advanced_delay",
		"external_script",
		"fixation_dot",
		"text_display",
		"text_input",
		"notepad",
		"srbox",
		"port_reader",
		"reset_feedback",
		"repeat_cycle",
		"parallel",
		"form_base",
		"form_text_input",
		"form_consent",
		"form_text_display",
		"form_multiple_choice",
		]

	for plugin in included_plugins:
		print "copying plugin", plugin
		shutil.copytree(os.path.join("plugins", plugin), os.path.join("dist", \
			"plugins", plugin))
		for path in os.listdir(os.path.join("plugins", plugin)):
			if path[-1] == "~" or os.path.splitext(path)[1] in [".pyc"]:
				print "removing file", path
				os.remove(os.path.join("dist", "plugins", plugin, path))

# Include old media_player
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

# Include new vlc-based media player
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

# Include examples
if include_examples:
	print "copying examples"
	shutil.copytree("examples", os.path.join("dist", "examples"))
	for path in os.listdir(os.path.join("dist", "examples")):
		if path[-1] == "~" or os.path.splitext(path)[1] not in [".opensesame", \
			".gz"]:
			print "removing file", path
			os.remove(os.path.join("dist", "examples", path))

# Include sounds
if include_sounds:
	print "copying sounds"
	shutil.copytree("sounds", os.path.join("dist", "sounds"))
