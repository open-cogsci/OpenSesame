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

## WinPython-based process

The easiest way to create a package is to start from a WinPython distribution,
which already comes with many of the dependencie. From there, only a few
remaining dependencies need to be installed.

### Notes

pyqt4 is installed, but contains mixed bindings for py2 and py3. These have to
be manually removed. These are in `uic/port_v[3|2]`.

### All Python versions

The following packages are the same for Python 2 and 3:

- QProgEdit (>= 3.0.0)
- markdown
- bidi
- webcolors

### Python 2.7

The following packages have specific python 2 installers, or are only available
for Python 2:

- pygame 1.9.1
- cv2
	- Download and extract the regular OpenCV2 package
	- Copy cv2.pyd from build/python/2.7 to the Python site-packages
	  folder
- psychopy 1.82.02
- expyriment 0.8.0
	- Installer is currently broken, and needs to be manually hacked.
- pyglet
- wx
- parallel
	- Manually place `simpleio.dll`, which is included with the pyparallel
	  source, in the main Python folder.
- vlc
	- Required only for media_player_vlc
	- Place vlc.py in the media_player_vlc folder. See below for folder
	  structure.
	- Choose the version for VLC 2.0
	- Available from <http://liris.cnrs.fr/advene/download/python-ctypes/>

### Python 3.4 and 3.5

- pygame (1.9.2)
	- Available from: <http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame>
- pyaudio
	- Available from: <http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio>

## Usage

First, a list of all importable modules from the Python standar library must be
created. This requires Python `stdlib-list`, which is available from:

- <https://github.com/jackmaney/python-stdlib-list>

The list can be built by runnning:

	python setup-pkg-list.py

Next, compile all source files to `.pyc` (default) as follows:

	python setup-win32.py py2exe

More options can be tweaked by changing the variables below.

## Output

The build will be stored in the `dist` subfolder. In addition, a `zip` is build
if release_zip is set to True.

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

from libopensesame.py3compat import *
if not py3:
	import sip
	sip.setapi(u'QString', 2)
	sip.setapi(u'QVariant', 2)

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
if py3:
	from urllib.request import urlretrieve
else:
	from urllib import urlretrieve
from setup_shared  import included_plugins, included_extensions

# Set this to False to build a 'light' version without the Qt4 gui. This
# options currently breaks opensesamerun as well, so don't set it to False.
include_gui = True

# Miscellaneous settings
include_plugins = True
include_extensions = True
include_media_player = False
include_media_player_vlc = not py3
include_boks = not py3
include_pygaze = not py3
include_sounds = True
include_faenza = True
include_inpout32 = not py3
include_simpleio = not py3
include_pyqt4_plugins = True
jupyter = py3
release_zip = True
release_build = 1
channel = u'win32'

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
	'decorator',
	'libopensesame',
	'openexp',
    'pyflakes',
	'scipy',
	'numpy',
	'serial',
	'IPython',
	'pygments',
	'PyQt4',
	'OpenGL',
	'PIL',
	'pygame',
	'libqtopensesame',
	'markdown',
	'matplotlib',
	'bidi',
	'yaml',
	'pytz',
	'pyparsing',
	'dateutil',
	'six',
	'wx',
	'webcolors',
	'zmq'
	]

if jupyter:
	copy_packages += [
		'jupyter_client',
		'jupyter_console',
		'jupyter_core',
		'qtconsole',
		'ipython_genutils',
		'traitlets',
		'ipykernel',
		'ipyparallel',
		'ipywidgets',
		'jupyter',
		'pickleshare',
		'path',
		'simplegeneric',
	]

if not py3:
	copy_packages += [
		'parallel',
		'expyriment',
		'psychopy',
		'pyglet',
		'pygaze',
		]

# A list of packages that shouldn't be stripped from .py files, because it
# breaks them.
no_strip = [
	'expyriment'
	]

# Packages that are part of the standard Python packages, but should not be
# included, because they cause trouble
exclude_packages = ['os.path']
if py3:
	exclude_packages += [
	'__main__',
	'site',
	'xml.parsers.expat.errors',
	'xml.parsers.expat.model',
	'xml.parsers.expat'
	]

# Packages that are not part of the standard Python packages (or not detected
# as such), but should nevertheless be included. These are different from the
# copy_packages in that they are not copied, but included through the standard
# py2exe way of including it in `library.zip`.
include_packages = [
	'pyaudio',
	'sip',
	]

if not py3:
	include_packages += [
		'cv2'
		]

exclude_dll = [
	"MSVCP90.DLL",
	"libzmq.dll",
	]

# Create empty destination folders. For some reason, rmtree and mkdir usually
# fail, so we keep trying until it works.
while os.path.exists("dist"):
	try:
		shutil.rmtree("dist")
	except:
		print(u'Trying to delete dist ...')
while not os.path.exists("dist"):
	try:
		os.mkdir("dist")
	except:
		print(u'Trying to recreate dist ...')
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
failed_packages = []
for pkg in copy_packages:
	print('copying packages %s ... ' % pkg)
	try:
		exec('import %s as _pkg' % pkg)
	except ImportError:
		failed_packages.append(pkg)
		continue
	pkg_folder = os.path.dirname(_pkg.__file__)
	pkg_target = os.path.join("dist", pkg)
	# For modules that are .py files in site-packages
	if pkg_folder.endswith('site-packages'):
		print('\tmodule %s' % _pkg.__file__)
		shutil.copy(os.path.join(pkg_folder, '%s.py' % pkg), 'dist')
		# In Python 3, the legacy parameter indicates that the byte-compiled
		# file should be placed alongside the source file.
		if py3:
			compileall.compile_file(r'dist/%s.py' % pkg, legacy=True)
		else:
			compileall.compile_file(r'dist/%s.py' % pkg)
		os.remove(r'dist/%s.py' % pkg)
	# For packages that are subfolder of site-packages
	else:
		print('\tfrom %s' % pkg_folder)
		shutil.copytree(pkg_folder, pkg_target, symlinks=True,
			ignore=ignore_package_files)
		# Set the correct metadata channel
		if pkg == 'libopensesame' and channel is not None:
			with open(u'dist/libopensesame/metadata.py') as fd:
				s = fd.read()
			s = s.replace(u"channel = u'dev'", u"channel = u'%s'" % channel)
			with open(u'dist/libopensesame/metadata.py', u'w') as fd:
				fd.write(s)
		if py3:
			compileall.compile_dir(pkg_target, force=True, legacy=True)
		else:
			compileall.compile_dir(pkg_target, force=True)
		# Expyriment assumes that certain source files are available, see
		# http://code.google.com/p/expyriment/issues/detail?id=16
		if pkg != no_strip:
			strip_py(pkg_target)

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

# Read the previously generated packages list, and exclude the explicitly
# excluded packages
with open('pkg-list-py%s.txt' % python_version) as fd:
	for pkg in fd:
		pkg = pkg.strip()
		if pkg not in exclude_packages:
			include_packages.append(pkg)

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
		"includes" : include_packages,
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

print(u'copying PyGame/ SDLL dll\'s')
folder = u'%s/Lib/site-packages/pygame' % python_folder
for fname in os.listdir(folder):
	if not fname.endswith('.dll'):
		continue
	path = os.path.join(folder, fname)
	print('Copying %s' % path)
	shutil.copyfile(path, os.path.join(u'dist', fname))

if include_simpleio:
	print("copying simpleio.dll")
	shutil.copyfile(r"%s\simpleio.dll" \
		% python_folder, r"dist\simpleio.dll")

if include_inpout32:
	print("copying inpout32.dll")
	urlretrieve("http://files.cogsci.nl/misc/inpout32.dll", \
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
	for fname in [u'vlc.py', u'media_player_vlc.py', u'media_player_vlc.md',
		u'media_player_vlc.png', u'media_player_vlc_large.png', u'info.yaml']:
		shutil.copyfile(r"..\media_player_vlc\media_player_vlc\%s" % fname,
			r"dist\plugins\media_player_vlc\%s" % fname)

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

# Include sounds
if include_sounds:
	print("copying sounds")
	shutil.copytree("sounds", os.path.join("dist", "sounds"))

# Create a zip release of the folder
if release_zip:
	import zipfile
	target_folder = u'opensesame_%s-py%s-win32-%s' \
		% (libopensesame.__version__, python_version, release_build)
	target_zip = target_folder + u'.zip'
	print('zipping to %s' % target_zip)
	shutil.move(u'dist', target_folder)
	zipf = zipfile.ZipFile(target_zip, 'w', zipfile.ZIP_DEFLATED)
	for root, dirs, files in os.walk(target_folder):
		for file in files:
			path = os.path.join(root, file)
			print('Adding %s' % path)
			zipf.write(path)
	zipf.close()
	shutil.move(target_folder, 'dist')
	print('zipfile: %s' % target_zip)

if len(failed_packages) > 0:
	print('The following packages were not copied: %s' % failed_packages)
