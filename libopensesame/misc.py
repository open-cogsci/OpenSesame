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

import os
import os.path
import sys

version = u'0.27.2 for Mac'
codename = u'Frisky Freud'

use_global_resources = '--no-global-resources' not in sys.argv
from libopensesame import debug

def change_working_dir():

	"""A horrifyingly ugly hack to change the working directory under Windows"""

	import libqtopensesame.qtopensesame

	if os.name == "nt":
		try:
			# Extract the part of the description containing the path
			s = unicode(libqtopensesame.qtopensesame)
			i = s.find(u'from \'') + 6
			j = s.find(u'\'>\'') - 1
			s = s[i:j]
			# Go up the tree until the path of the current script
			while not os.path.exists(os.path.join(s, u'opensesame')) and \
				not os.path.exists(os.path.join(s, u'opensesame.exe'))and \
				not os.path.exists(os.path.join(s, u'opensesamerun')) and \
				not os.path.exists(os.path.join(s, u'opensesamerun.exe')):
				s = os.path.dirname(s)
			os.chdir(s)
			if s not in sys.path:
				sys.path.append(s)
			debug.msg(s)
		except Exception as e:
			debug.msg(u'failed to change working directory: %s' % e)

def opensesamerun_options():

	"""Parse the command line options for opensesamerun"""

	import optparse
	global version, codename

	parser = optparse.OptionParser( \
		u'usage: opensesamerun [experiment] [options]', version=u'%s \'%s\'' % \
		(version, codename))

	parser.set_defaults(subject=0)
	parser.set_defaults(logfile=None)
	parser.set_defaults(debug=False)
	parser.set_defaults(fullscreen=False)
	parser.set_defaults(pylink=False)
	parser.set_defaults(width=1024)
	parser.set_defaults(height=768)
	parser.set_defaults(custom_resolution=False)
	group = optparse.OptionGroup(parser, u'Subject and log file options')
	group.add_option(u"-s", u"--subject", action=u"store", dest=u"subject", \
		help=u"Subject number")
	group.add_option(u"-l", u"--logfile", action=u"store", dest=u"logfile", \
		help=u"Logfile")
	parser.add_option_group(group)
	group = optparse.OptionGroup(parser, u"Display options")
	group.add_option(u"-f", u"--fullscreen", action=u"store_true", dest= \
		"fullscreen", help=u"Run fullscreen")
	group.add_option(u"-c", u"--custom_resolution", action=u"store_true", \
		dest=u"custom_resolution", help= \
		u"Do not use the display resolution specified in the experiment file")
	group.add_option(u"-w", u"--width", action=u"store", dest=u"width", help= \
		u"Display width")
	group.add_option(u"-e", u"--height", action=u"store", dest=u"height", \
		help=u"Display height")
	parser.add_option_group(group)
	group = optparse.OptionGroup(parser, u"Miscellaneous options")
	group.add_option(u"-d", u"--debug", action=u"store_true", dest=u"debug", \
		help=u"Print lots of debugging messages to the standard output")
	group.add_option(u"--stack", action=u"store_true", dest=u"stack", help= \
		u"Print stack information")
	parser.add_option_group(group)
	group = optparse.OptionGroup(parser, u"Miscellaneous options")
	group.add_option(u"--pylink", action=u"store_true", dest=u"pylink", help= \
		u"Load PyLink before PyGame (necessary for using the Eyelink plug-ins in non-dummy mode)")
	parser.add_option_group(group)
	options, args = parser.parse_args(sys.argv)

	# Set the default logfile based on the subject nr
	if options.logfile == None:
		options.logfile = u"subject%s.csv" % options.subject

	if len(sys.argv) > 1 and os.path.exists:
		options.experiment = sys.argv[1]
	else:
		options.experiment = u""

	try:
		options.subject = int(options.subject)
	except:
		parser.error(u"Subject (-s / --subject) should be numeric")

	try:
		options.width = int(options.width)
	except:
		parser.error(u"Width (-w / --width) should be numeric")

	try:
		options.height = int(options.height)
	except:
		parser.error(u"Height (-e / --height) should be numeric")

	return options

def opensesamerun_ready(options):

	"""
	Check if the opensesamerun options are sufficiently complete to run the
	experiment

	Arguments:
	options -- a dictionary containing the options

	Returns:
	True or False, depending on whether the options are sufficient
	"""

	# Check if the experiment exists
	if not os.path.exists(options.experiment):
		return False

	# Check if the logfile is writable
	try:
		open(options.logfile, u"w")
	except:
		return False

	# Ready to run!
	return True

def messagebox(title, msg):

	"""
	Presents a simple tk messagebox

	Arguments:
	title -- the title of the messagebox
	msg -- the message
	"""

	import Tkinter
	root = Tkinter.Tk()
	root.title(title)
	l = Tkinter.Label(root, text=msg, justify=Tkinter.LEFT, padx=8, pady=8, \
		wraplength=300)
	l.pack()
	b = Tkinter.Button(root, text=u"Ok", command=root.quit)
	b.pack(side=Tkinter.RIGHT)
	root.mainloop()

def strip_tags(s):

	"""
	Strip html tags from a string and convert breaks to newlines.

	Arguments:
	s -- the string to be stripped

	Returns:
	The stripped string
	"""

	import re
	return re.compile(r'<.*?>').sub('', unicode(s).replace("<br />", \
		"\n").replace("<br>", "\n"))

def resource(name):

	"""
	A hacky way to get a resource using the functionality from openexp

	Arguments:
	name -- the name of the requested resource

	Returns:
	The full path to the resource
	"""

	global use_global_resources
	path = os.path.join(u"resources", name)
	if os.path.exists(path):
		return os.path.join(u"resources", name)
	if os.name == u"posix" and use_global_resources:
		path = u"/usr/share/opensesame/resources/%s" % name
		if os.path.exists(path):
			return path
	return None

def home_folder():

	"""
	Determines the home folder

	Returns:
	A path to the home folder
	"""

	import platform

	# Determine the home folder
	if platform.system() == u"Windows":
		return os.environ[u"APPDATA"]
	if platform.system() == u"Darwin":
		return os.environ[u"HOME"]
	if platform.system() == u"Linux":
		return os.environ[u"HOME"]
	home_folder = os.environ[u"HOME"]
	print u"qtopensesame.__init__(): unknown platform '%s', using '%s' as home folder" \
		% (platform.system(), home_folder)
	return home_folder

def module_versions():

	"""
	Get version info

	Returns:
	A string with version numbers
	"""

	from PyQt4 import QtCore

	s = u"OpenSesame %s" % version
	s += u"\nPython %d.%d.%d" % (sys.version_info[0], sys.version_info[1], \
		sys.version_info[2])

	# OpenCV
	try:
		import cv
		s += u'\nOpenCV is available (version is unknown)'
	except:
		s += u'\nOpenCV is not available'

	# OpenCV 2
	try:
		import cv2
		s += u'\nOpenCV 2 is available (version is unknown)'
	except:
		s += u'\nOpenCV 2 is not available'

	# Expyriment
	try:
		_out = sys.stdout
		sys.stdout = open(os.devnull, 'w')
		import expyriment
		sys.stdout = _out
		s += u'\nExpyriment %s' % expyriment.get_version()
	except:
		s += u'\nExpyriment is not available (or version is unknown)'

	# NumPy
	try:
		import numpy
		s += u'\nNumPy %s' % numpy.version.version
	except:
		s += u'\nNumPy is not available (or version is unknown)'

	# PyAudio
	try:
		import pyaudio
		s += u"\nPyAudio %s" % pyaudio.__version__
	except:
		s += u"\nPyAudio not available (or version is unknown)"

	# PyGame
	try:
		import pygame
		s += u"\nPyGame %s" % pygame.ver
	except:
		s += u"\nPyGame not available (or version is unknown)"

	# PyOpenGL
	try:
		import OpenGL
		s += u"\nPyOpenGL %s" % OpenGL.__version__
	except:
		s += u"\nPyOpenGL not available (or version is unknown)"

	# PyQt
	s += u"\nPyQt %s" % QtCore.PYQT_VERSION_STR

	# PySerial
	try:
		import serial
		s += u'\nPySerial %s' % serial.VERSION
	except:
		s += u'\nPySerial not available (or version is unknown)'

	# PsychoPy
	try:
		import psychopy
		s += u"\nPsychoPy %s" % psychopy.__version__
	except:
		s += "\nPsychoPy not available (or version is unknown)"

	# Pyglet
	try:
		import pyglet
		s += u"\nPyglet %s" % pyglet.version
	except:
		s += u"\nPyglet not available (or version is unknown)"

	# SciPy
	try:
		import scipy
		s += u'\nSciPy %s' % scipy.version.version
	except:
		s += u'\nScipy is not available (or version is unknown)'

	return s

def open_url(url):

	"""
	Open a URL in an OS specific way. The URL can be a file, website, etc.

	Arguments:
	url -- a url
	"""

	debug.msg(url)
	import platform
	import subprocess
	if platform.system() == u"Linux":
		pid = subprocess.Popen([u"xdg-open", url]).pid
	elif platform.system() == u"Darwin":
		pid = subprocess.Popen(["open", url]).pid
	elif platform.system() == u"Windows":
		try:
			os.startfile(url)
		except:
			debug.msg(u"Failed to open '%s'" % url, reason=u"warning")
	else:
		debug.msg(u"Failed to open '%s'" % url, reason=u"warning")

def filesystem_encoding():

	"""
	Gets the current file system encoding. This wrapper is necessary, because
	sys.getfilesystemencoding() returns None on Android.

	Returns:
	A string with the file system encoding, such as 'utf-8' or 'mdcs'
	"""

	enc = sys.getfilesystemencoding()
	if enc == None:
		enc = u'utf-8'
	return enc