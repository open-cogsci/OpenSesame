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

***

This file includes all kinds of things so that py2exe incorporates
them into the distribution. This is necessary, because items are
loaded at runtime, and therefore escape the detection of py2exe.
"""

import sys
from libopensesame import debug
from libopensesame.py3compat import *

# Below is a quick hack to deal with pylinks quirky behavior.
# Pylink needs to be imported prior to pygame, otherwise it
# gives a DLL not found error. However, if we use a regular
# import statement, py2exe will include pylink with OpenSesame
# which is not allowed. This hack loads pylink if available,
# prior to pygame, without giving an error if pylink is not
# installed.

if "--pylink" in sys.argv:
	try:
		exec("import pylink") # This makes sure that py2exe doesn't try to include pylink
	except Exception as e:
		debug.msg( \
			"failed to import pylink module. You will not be able to use eyelink connectivity")

# Explicitly importing these modules ensures that Py2exe will
# bundle them. This is therefore only required for Windows.

if "--preload" in sys.argv:

	import warnings

	debug.msg("preloading modules ...")
	debug.msg("preloading 'legacy' back-end")
	try:
		import openexp,\
			openexp._canvas.legacy,\
			openexp._keyboard.legacy,\
			openexp._mouse.legacy,\
			openexp._sampler.legacy,\
			openexp._synth.legacy
	except Exception as e:
		debug.msg("failed to import 'legacy' back-end. Error: %s" % e)

	debug.msg("preloading 'opengl' back-end")
	try:
		import openexp,\
			openexp._canvas.xpyriment,\
			openexp._mouse.xpyriment
	except Exception as e:
		debug.msg("failed to import 'xpyriment' back-end. Error: %s" % e)

	debug.msg("preloading 'opengl' back-end")
	try:
		import openexp,\
			openexp._canvas.opengl
	except Exception as e:
		debug.msg("failed to import 'opengl' back-end. Error: %s" % e)

	debug.msg("preloading 'psycho' back-end")
	try:
		with warnings.catch_warnings():
			warnings.simplefilter("ignore")
			import openexp,\
				openexp._canvas.psycho,\
				openexp._keyboard.psycho,\
				openexp._mouse.psycho
	except Exception as e:
		debug.msg("failed to import 'psycho' back-end. Error: %s" % e)

	debug.msg("preloading 'psychopy'")
	try:
		with warnings.catch_warnings():
			warnings.simplefilter("ignore")
			from psychopy import core, visual, data, event, filters, gui, hardware, log, misc, monitors, sound, platform_specific # info, serial and parallel produce errors
	except Exception as e:
		debug.msg("failed to import 'psychopy' <http://www.psychopy.org/>. You will not be able to use PsychoPy or the psycho back-end. Error: %s" % e)

	debug.msg("preloading 'pyffmpeg'")
	try:
		import pyffmpeg
		import pyffmpeg_numpybindings
		from audioqueue import AudioQueue, Queue_Empty, Queue_Full
	except Exception as e:
		debug.msg("failed to import 'pyffmpeg' <http://code.google.com/p/pyffmpeg/>. You will not be able to use the media_player plug-in. Error: %s" % e)

	debug.msg("preloading 'PIL'")
	try:
		# The correct way to import PIL appears to depend on the version. So
		# try both methods.
		try:
			import PIL
			import PIL.Image
		except:
			import Image
	except Exception as e:
		debug.msg("failed to import 'PIL' <http://www.pythonware.com/products/pil/>. You will not be able the Python Imaging library. Error: %s" % e)

	debug.msg("preloading 'pyaudio'")
	try:
		import pyaudio
	except Exception as e:
		debug.msg("failed to import 'pyaudio' <http://people.csail.mit.edu/hubert/pyaudio/>. You will not be able to use portaudio and the media_player plug-in. Error: %s" % e)

	debug.msg("preloading 'wave'")
	try:
		import wave
	except Exception as e:
		debug.msg("failed to import 'wave'. Error: %s" % e)

	# OpenGL requires hacks to work with Py2Exe. The approach here is based on
	# information from <http://www.py2exe.org/index.cgi/PyOpenGL>
	debug.msg("preloading 'OpenGL'")
	try:
		from OpenGL.GL import *
		from OpenGL.platform import win32
	except AttributeError:
		pass
	try:
		from ctypes import util
		import OpenGL
	except Exception as e:
		debug.msg("failed to import 'OpenGL' <http://pyopengl.sourceforge.net/>. You will not be able to use OpenGL. Error: %s" % e)

	debug.msg("preloading 'cv'")
	try:
		import cv
	except Exception as e:
		debug.msg("failed to import 'cv' <http://opencv.willowgarage.com/wiki/>. You will not be able to use the Open Computer Vision libraries. Error: %s" % e)

	debug.msg("preloading 'serial'")
	try:
		import serial
	except Exception as e:
		debug.msg("failed to import 'serial' module <http://pyserial.sourceforge.net/>. You will not be able to use serial port connectivity. Error: %s" % e)

	debug.msg("preloading 'parallel'")
	try:
		import parallel
		import parallel.parallelutil
	except Exception as e:
		debug.msg("failed to import 'parallel' module <http://pyserial.sourceforge.net/pyparallel.html>. You will not be able to use parallel port connectivity. Error: %s" % e)

	debug.msg("preloading 'pyglet'")
	try:
		import pyglet
	except Exception as e:
		debug.msg("failed to import 'pyglet' module <http://www.pyglet.org/>. You will not be able to use PsychoPy. Error: %s" % e)

	debug.msg("preloading modules required by questionnaire plug-ins")
	try:
		import htmllib
		import htmlentitydefs
		import HTMLParser
		import sgmllib
		import markupbase
	except Exception as e:
		debug.msg("failed to import modules required by questionnaire plug-ins")

	debug.msg("preloading IPython")
	try:
		from IPython.frontend.qt.console.ipython_widget import IPythonWidget
		from IPython.frontend.qt.kernelmanager import QtKernelManager
		from IPython.utils.localinterfaces import LOCALHOST
	except Exception as e:
		debug.msg("failed to import IPython <http://www.ipython.org/>. You will not be able to use the IPython console. Error: %s" % e)

	debug.msg("preloading OSX dependencies")
	try:
		from libqtopensesame.widgets import pool_widget, statusbar, tree_overview, toolbar_items, variable_inspector
		from libqtopensesame.items import exceptions, experiment, feedback, inline_script, item, keyboard_response, logger, loop, misc, mouse_response, plugins, sampler, sequence, sketchpad, synth
	except Exception as e:
		debug.msg('Failed to load libqtopensesame.items modules')
	try:
		import pygame._view
	except Exception as e:
		debug.msg('Failed to load pygame._view')
