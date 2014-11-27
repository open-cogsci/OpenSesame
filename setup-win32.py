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

----

## About

This script will create a binary Windows package of OpenSesame, using py2exe.
If possible, dependencies are simply copied into a subfolder and compiled to
`.pyc` format. If not possible, they are included in the `library.zip` file,
which is the default py2exe way of including dependencies.

## Usage

To compile all source files to `.pyc` (default), call the script as follows:

	python setup-win32.py py2exe

To compile all source files to `.pyo`, call the script as follows:

	python -O setup-win32.py py2exe

or

	python -OO setup-win32.py py2exe

More options can be tweaked by changing the variables below.

## Output

The build will be stored in the `dist` subfolder.

## Python modules

The following Python modules should be installed:

	bidi
		- This is installed as an egg and therefore not packaged properly. For
		  packaging, simply place the `bidi` source folder directly in the
		  Python site-packages.
	cairo
		- Unofficial Windows builds can be downloaded from
		  <http://www.lfd.uci.edu/~gohlke/pythonlibs/#pycairo>
	expyriment
	matplotlib
		Subdependencies:
		- python-dateutil
			- Installed as .egg, so requires manual copying. If it fails to
			  install due to decoding errors, the package can be copied
		  	  manually to site-packages.
		- pytz
			- Installed as .egg, so requires manual copying.
		- six
			- Installed as .egg, so requires manual copying.
	opencv2
		- Download and extract the regular OpenCV2 package
		- Copy cv2.pyd from build/python/2.7 to the Python site-packages
		  folder
	pil
	psychopy
	pyflakes
		- This is installed as an egg and therefore not packaged properly. For
		  packaging, simply place the `pyflakes` source folder directly in the
		  Python site-packages.
	py2exe
	pyaudio
	pygame
	pyglet
		- The installer doesn't work. Need to install from ``.zip`.
	pyopengl
	pyparallel
		- Needs to be installed through the `.zip` package
		- Manually place `simpleio.dll`, which is included with the pyparallel
		  source, in the main Python folder.
	pyparsing
		- Required by matplotlib. The installer doesn't work, so needs to be
		  installed from .zip.
	pyqt4
		- The Python 3 modules will break on compilation, and have to be
		  manually removed/ renamed. These are in `uic/port_v3`.
	pyserial
	numpy
	scipy
	vlc
		- Required only for media_player_vlc
		- Place vlc.py in the media_player_vlc folder. See below for folder
		  structure.
		- Choose the version for VLC 2.0
		- Available from <http://liris.cnrs.fr/advene/download/python-ctypes/>

## Folder structure

If media_player, media_player_vlc, boks, or pygaze are included, they are
assumed to be one folder up. So the folder structure should be as follows:

	/[parent foler]
		/opensesame
		/pygaze
		/boks
		/media_player
		/media_player_vlc
---

"""

from distutils.core import setup
import distutils.sysconfig as sysconfig
import compileall
import py_compile
import glob
import py2exe
import os
import sys
import shutil
import libqtopensesame.qtopensesame
import libopensesame.misc
import psychopy
import urllib
from setup_shared  import included_plugins, included_extensions

# Set this to False to build a 'light' version without the Qt4 gui. This
# options currently breaks opensesamerun as well, so don't set it to False.
include_gui = True

# Miscellaneous settings
include_plugins = True
include_extensions = True
include_media_player = False
include_media_player_vlc = True
include_boks = True
include_pygaze = True
include_examples = True
include_sounds = True
include_faenza = True
include_inpout32 = True
include_simpleio = True
include_pyqt4_plugins = True

python_folder = os.path.dirname(sys.executable)
python_version = "%d.%d" % (sys.version_info[0], sys.version_info[1])

print(u'Python folder: %s' % python_folder)
print(u'Python version: %s' % python_version)

# Determine which files we're going to keep
if '-OO' in sys.argv:
	strip_ext = '.py', '.pyc'
	keep_ext = '.pyo'
	optimize = 2
	print(u'Compiling to .pyo')
elif '-O' in sys.argv:
	strip_ext = '.py', '.pyc'
	keep_ext = '.pyo'
	optimize = 1
	print(u'Compiling to .pyo')
else:
	strip_ext = '.py', '.pyo'
	keep_ext = '.pyc'
	optimize = 0
	print(u'Compiling to .pyc')
print(u'Optimize = %d' % optimize)

# Packages that are too be copied for the site-packages folder, rather than
# included by py2exe in the library .zip file. Copying packages is in general
# preferred, as some packages (e.g. expyriment) do not work well when included
# in the library.zip file that py2exe uses to store packages. Note eggs are not
# copied properly.
copy_packages = [
	'QProgEdit',
	'libopensesame',
	'openexp',
	'expyriment',
	'psychopy',
    'pyflakes',
	'scipy',
	'numpy',
	'serial',
	'parallel',
	'OpenGL',
	'PIL',
	'pygame',
	'pyglet',
	'libqtopensesame',
	'markdown',
	'matplotlib',
	'bidi',
	'yaml',
	'pygaze',
	'pytz',
	'pyparsing',
	'dateutil',
	'six',
	'wx'
	]

# A list of packages that shouldn't be stripped from .py files, because it
# breaks them.
no_strip = [
	'expyriment'
	]

# Packages that are part of the standard Python packages, but should not be
# included
exclude_packages = [
	'idlelib',
	'antigravity', # Kind of funny, importing this opens: http://xkcd.com/353/
	'test', # Avoid automated tests, because they take ages
	]

# Packages that are not part of the standard Python packages (or not detected
# as such), but should nevertheless be included
include_packages = [
	'pyaudio',
	'cairo',
	'Image',
	'cv2',
	'sip',
	'PyQt4.QtCore',
	'PyQt4.QtGui',
	'PyQt4.Qsci',
	'PyQt4.QtWebKit',
	'PyQt4.QtNetwork',
	'PyQt4.uic',
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
os.mkdir(os.path.join("dist", "extensions"))

# Print copy PyQt4 plugins
if include_pyqt4_plugins:
	shutil.copytree('%s\Lib\site-packages\PyQt4\plugins' % python_folder,
		'dist\PyQt4_plugins')

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
		if (ext in strip_ext and os.path.exists(base+keep_ext)) or \
			path[-1] == '~':
			print('stripping %s' % path)
			os.remove(path)

# Copy packages
for pkg in copy_packages:
	print('copying packages %s ... ' % pkg)
	exec('import %s as _pkg' % pkg)
	pkg_folder = os.path.dirname(_pkg.__file__)
	pkg_target = os.path.join("dist", pkg)
	# For modules that are .py files in site-packages
	if pkg_folder.endswith('site-packages'):
		print('\tmodule %s' % _pkg.__file__)
		shutil.copy(os.path.join(pkg_folder, '%s.py' % pkg), 'dist')
		compileall.compile_file(r'dist/%s.py' % pkg)
		os.remove(r'dist/%s.py' % pkg)
	# For packages that are subfolder of site-packages
	else:
		print('\tfrom %s' % pkg_folder)
		shutil.copytree(pkg_folder, pkg_target, symlinks=True, \
			ignore=ignore_package_files)
		compileall.compile_dir(pkg_target, force=True)
		# Expyriment assumes that certain source files are available, see
		# http://code.google.com/p/expyriment/issues/detail?id=16
		if pkg != no_strip:
			strip_py(pkg_target)

# Create a list of standard pakcages that should be included
# http://stackoverflow.com/questions/6463918/how-can-i-get-a-list-of-all-the-python-standard-library-modules
print('detecting standard Python packages and modules ... ')
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
		print(pkg)
		std_pkg.append(pkg)
for pkg in sys.builtin_module_names:
	print(pkg)
	std_pkg.append(pkg)

windows_opensesame = {
		"script" : "opensesame",
		"icon_resources": [(0, os.path.join("resources", "opensesame.ico"))],
		}
windows_opensesamerun = {
		"script" : "opensesamerun",
		"icon_resources": [(0, os.path.join("resources", "opensesamerun.ico"))],
		}
windows = [windows_opensesamerun]
if include_gui:
	windows += [windows_opensesame]

# Setup options
setup(
	# Use 'console' to have the programs run in a terminal and
	# 'windows' to run them normally.
	windows = windows,
	options = {
		"py2exe" : {
		"compressed" : True,
		"optimize": optimize,
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
	print("... %s" % folder)
	for f in files:
		if os.path.splitext(f)[1] in [".csv", ".pyc"] and f not in \
			["icon_map.csv"]:
			l.append(f)
		if 'Faenza' in folder and f == 'scalable':
			l.append(f)
		if f == "Faenza" and (not include_faenza or not include_gui):
			l.append(f)
		if not include_gui and f in ('theme', 'locale', 'templates', 'ts', \
			'ui'):
			l.append(f)
	return l

# Compiling opensesame to opensesame.pyc for the multiprocessing functionality
print("compiling opensesame")
py_compile.compile("opensesame", os.path.join("dist", "opensesame.pyc"))

# Copy resource files
print("copying resources")
shutil.copytree("resources", os.path.join("dist", "resources"), symlinks=True, \
	ignore=ignore_resources)

print("copying README info etc.")
shutil.copyfile("readme.md", os.path.join("dist", "readme.md"))
shutil.copyfile("debian/copyright", os.path.join("dist", "copyright"))
shutil.copyfile("COPYING", os.path.join("dist", "COPYING"))
if include_gui:
	shutil.copytree("help", os.path.join("dist", "help"))

print("copying PyGame/ SDLL dll's")
shutil.copyfile(r"%s\Lib\site-packages\pygame\SDL_ttf.dll" \
	% python_folder, r"dist\SDL_ttf.dll")
shutil.copyfile(r"%s\Lib\site-packages\pygame\libfreetype-6.dll" \
	% python_folder, r"dist\libfreetype-6.dll")
shutil.copyfile(r"%s\Lib\site-packages\pygame\libogg-0.dll" \
	% python_folder, r"dist\libogg-0.dll")

print("copying PIL.pth")
shutil.copyfile(r"%s\Lib\site-packages\PIL.pth" \
	% python_folder, r"dist\PIL.pth")

if include_simpleio:
	print("copying simpleio.dll")
	shutil.copyfile(r"%s\simpleio.dll" \
		% python_folder, r"dist\simpleio.dll")

if include_inpout32:
	print("copying inpout32.dll")
	urllib.urlretrieve ("http://files.cogsci.nl/misc/inpout32.dll", \
		r"dist\inpout32.dll")

# Include plug-ins
if include_plugins:
	print("copying plugins"	)
	for plugin in included_plugins:
		print("copying plugin %s" % plugin)
		shutil.copytree(os.path.join("plugins", plugin), os.path.join("dist", \
			"plugins", plugin))
		for path in os.listdir(os.path.join("plugins", plugin)):
			if path[-1] == "~" or os.path.splitext(path)[1] in [".pyc"]:
				print("removing file %s" % path)
				os.remove(os.path.join("dist", "plugins", plugin, path))

# Include extensions
if include_extensions:
	print("copying extensions"	)
	for extension in included_extensions:
		print("copying extension %s" % extension)
		shutil.copytree(os.path.join("extensions", extension),
			os.path.join("dist", "extensions", extension))
		for path in os.listdir(os.path.join("extensions", extension)):
			if path[-1] == "~" or os.path.splitext(path)[1] in [".pyc"]:
				print("removing file %s" % path)
				os.remove(os.path.join("dist", "extensions", extension, path))

# Include old media_player
if include_media_player:
	print("copying media_player")
	os.mkdir("dist\plugins\media_player")
	shutil.copyfile(r"..\media_player\media_player.py", \
		r"dist\plugins\media_player\media_player.py""")
	shutil.copyfile(r"..\media_player\media_player.html", \
		r"dist\plugins\media_player\media_player.html")
	shutil.copyfile(r"..\media_player\media_player.png", \
		r"dist\plugins\media_player\media_player.png")
	shutil.copyfile(r"..\media_player\media_player_large.png", \
		r"dist\plugins\media_player\media_player_large.png")
	shutil.copyfile(r"..\media_player\info.txt", \
		r"dist\plugins\media_player\info.txt")

# Include new vlc-based media player
if include_media_player_vlc:
	print("copying media_player_vlc")
	os.mkdir("dist\plugins\media_player_vlc")
	shutil.copyfile(r"..\media_player_vlc\vlc.py", \
		r"dist\plugins\media_player_vlc\vlc.py")
	shutil.copyfile( \
		r"..\media_player_vlc\media_player_vlc.py", \
		r"dist\plugins\media_player_vlc\media_player_vlc.py")
	shutil.copyfile( \
		r"..\media_player_vlc\media_player_vlc.md", \
		r"dist\plugins\media_player_vlc\media_player_vlc.md")
	shutil.copyfile( \
		r"..\media_player_vlc\media_player_vlc.png", \
		r"dist\plugins\media_player_vlc\media_player_vlc.png")
	shutil.copyfile( \
		r"..\media_player_vlc\media_player_vlc_large.png", \
		r"dist\plugins\media_player_vlc\media_player_vlc_large.png")
	shutil.copyfile(r"..\media_player_vlc\info.json", \
		r"dist\plugins\media_player_vlc\info.json")

# Include Boks plug-in
if include_boks:
	print("copying boks")
	shutil.copytree(r"..\boks\opensesame\boks",
		r"dist\plugins\boks",
		ignore=shutil.ignore_patterns('*.pyc', '.*', '.pyo'))

# Include PyGaze plug-ins
if include_pygaze:
	print("copying pygaze")
	for plugin in ['init', 'log', 'drift_correct', 'start_recording',
		'stop_recording', 'wait']:
		shutil.copytree(r"..\pygaze\opensesame_plugins\pygaze_%s" % plugin,
			r"dist\plugins\pygaze_%s" % plugin,
			ignore=shutil.ignore_patterns('*.pyc', '.*', '.pyo'))

# Include examples
if include_examples:
	print("copying examples")
	shutil.copytree("examples", os.path.join("dist", "examples"))
	for path in os.listdir(os.path.join("dist", "examples")):
		if path[-1] == "~" or os.path.splitext(path)[1] not in [".opensesame", \
			".gz"]:
			print("removing file %s" % path)
			os.remove(os.path.join("dist", "examples", path))

# Include sounds
if include_sounds:
	print("copying sounds")
	shutil.copytree("sounds", os.path.join("dist", "sounds"))
