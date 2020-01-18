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

from libopensesame.py3compat import *
import os
import sys
import platform

# On Linux this appears to be buggy
if platform.system() != 'Linux':
	os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
# Attach a dummy console when launched with pythonw.exe. This is necessary for
# some libraries.
if sys.executable.endswith('pythonw.exe'):
	sys.stdout = open(os.devnull, 'w')
	sys.stderr = open(os.devnull, 'w')
	sys.stdin = open(os.devnull)


def patch_pyqt():

	"""This patches PyQt such that properties are removed from objects before
	connectSlotsByName() tries to inspect the object. This is necessary because
	in some versions, the introspection crashes when properties cannot be
	accessed, for example because the object to be initialized first.
	"""

	def _(fnc):

		def make_object_safe(obj, cls):

			tmp = {}
			for name, value in list(cls.__dict__.items()):
				try:
					getattr(obj, name)
				except AttributeError:
					tmp[name] = value
					delattr(cls, name)
			return tmp

		def restore_object(cls, tmp):

			for name, value in tmp.items():
				setattr(cls, name, value)

		def inner(obj):

			tmp = {}
			for cls in obj.__class__.mro():
				tmp[cls] = make_object_safe(obj, cls)
			fnc(obj)
			for cls in tmp:
				restore_object(cls, tmp[cls])

		return inner

	from qtpy import QtCore
	QtCore.QMetaObject.connectSlotsByName = \
		_(QtCore.QMetaObject.connectSlotsByName)


def set_paths():

	from libopensesame import misc
	import sys
	import platform
	# On Windows, the working directory should be the folder with the Python
	# interpreter. If not, Qt will have difficulty finding the correct paths.
	if platform.system() == 'Windows':
		os.chdir(os.path.dirname(sys.executable))
	# Update the system path so that Qt can find itself
	path = os.path.join(os.getcwd(), 'Library', 'bin')
	if os.path.exists(path):
		os.environ['PATH'] += ';' + path
	# Add the Scripts subfolder, which is where Anaconda scripts are located
	path = os.path.join(os.getcwd(), 'Scripts')
	if os.path.exists(path):
		os.environ['PATH'] += ';' + path
	from qtpy import QtCore
	# Add the folder that contains the OpenSesame modules to the path. This is
	# generally only necessary if OpenSesame is directly run from source,
	# instead from an installation.
	if os.path.exists(os.path.join(os.getcwd(), 'libopensesame')):
		sys.path.insert(0, os.getcwd())
	# Add the Qt plugin folders to the library path, if they exists. Where
	# these folders are depends on the version of Qt4, but these are two
	# possible locations.
	qt_plugin_path = os.path.join(
		os.path.dirname(sys.executable), 'Library', 'plugins')
	if os.path.isdir(qt_plugin_path):
		QtCore.QCoreApplication.addLibraryPath(
			safe_decode(qt_plugin_path, enc=misc.filesystem_encoding())
		)
	qt_plugin_path = os.path.join(
		os.path.dirname(sys.executable), 'Library', 'lib', 'qt4', 'plugins')
	if os.path.isdir(qt_plugin_path):
		QtCore.QCoreApplication.addLibraryPath(
			safe_decode(qt_plugin_path, enc=misc.filesystem_encoding())
		)


def opensesame():

	set_paths()
	if py3:
		patch_pyqt()
	# Support for multiprocessing when packaged
	# In OS X the multiprocessing module is horribly broken, but a fixed
	# version has been released as the 'billiard' module
	if platform.system() == 'Darwin':
		# Use normal multiprocessing module from python 3.4 and on
		if sys.version_info >= (3, 4):
			from multiprocessing import freeze_support, set_start_method
			freeze_support()
			set_start_method('spawn')
		else:
			from billiard import freeze_support, forking_enable
			freeze_support()
			forking_enable(0)
	else:
		from multiprocessing import freeze_support
		freeze_support()
	# Parse the (optional) environment file that contains special paths, etc.
	from libopensesame.misc import parse_environment_file
	parse_environment_file()
	# Force the new-style Qt API
	import sip
	import qtpy
	sip.setapi('QString', 2)
	sip.setapi('QVariant', 2)
	# Do the basic window initialization
	from qtpy.QtWidgets import QApplication
	# From Qt 5.6 on, QtWebEngine is the default way to render web pages
	# QtWebEngineWidgets must be imported before a QCoreApplication instance is
	# created.
	try:
		from qtpy import QtWebEngineWidgets
	except ImportError:
		pass
	if platform.system() != 'Linux':
		# Enable High DPI pixmaps with PyQt5
		if hasattr(qtpy.QtCore.Qt, 'AA_UseHighDpiPixmaps'):
			QApplication.setAttribute(qtpy.QtCore.Qt.AA_UseHighDpiPixmaps)
		# Enable scaling for High DPI displays with PyQt5
		if hasattr(qtpy.QtCore.Qt, 'AA_EnableHighDpiScaling'):
			QApplication.setAttribute(qtpy.QtCore.Qt.AA_EnableHighDpiScaling)
	from libqtopensesame.qtopensesame import qtopensesame
	app = QApplication(sys.argv)
	opensesame = qtopensesame(app)
	opensesame.__script__ = __file__
	app.processEvents()
	# Install the translator. For some reason, the translator needs to be
	# instantiated here and not in the set_locale() function, otherwise the
	# locale is ignored.
	from qtpy.QtCore import QTranslator
	translator = QTranslator()
	opensesame.set_locale(translator)
	# Now that the window is shown, load the remaining modules and resume the
	# GUI initialization.
	opensesame.resume_init()
	opensesame.restore_window_state()
	opensesame.show()
	# Added for OS X, otherwise Window will not appear
	opensesame.raise_()
	# Exit using the application exit status
	sys.exit(app.exec_())


def opensesamerun():

	set_paths()
	from libopensesame.oslogging import oslogger
	oslogger.start(u'gui')
	import libopensesame.misc
	libopensesame.misc.parse_environment_file()
	import libopensesame.experiment
	# Parse the command line options
	options = libopensesame.misc.opensesamerun_options()
	app = None
	# If the command line options haven't provided sufficient information to
	# run right away, present a GUI
	while not libopensesame.misc.opensesamerun_ready(options):
		# If PyQt4 is not available (e.g., this might be the case on Mac OS)
		# give an error instead of showing a GUI. This makes sure that even
		# without PyQt4, people can still run experiments.
		try:
			# Change Qt API
			import sip
			sip.setapi('QString', 2)
			sip.setapi('QVariant', 2)
			from qtpy import QtGui, QtCore, QtWidgets
		except:
			libopensesame.misc.messagebox(u"OpenSesame Run", u"Incorrect or "
				u"missing options.\n\nRun 'opensesame --help' from a terminal "
				u"(or command prompt) to see a list of available options, or "
				u"install Python Qt4 to enable the graphical user interface.")
			sys.exit()
		# Create the GUI and show it
		import libqtopensesame.qtopensesamerun
		if app is None:
			app = QtWidgets.QApplication(sys.argv)
			myapp = libqtopensesame.qtopensesamerun.qtopensesamerun(options)
		myapp.show()
		app.exec_()
		# Update the options from the GUI
		options = myapp.options
		# Exit if the GUI was canceled
		if not myapp.run:
			sys.exit()
	# Decode the experiment path and logfile
	experiment = os.path.abspath(options.experiment)
	if isinstance(experiment, bytes):
		experiment = safe_decode(
			experiment,
			enc=libopensesame.misc.filesystem_encoding(),
			errors=u'ignore'
		)
	# experiment_path = os.path.dirname(experiment)
	logfile = options.logfile
	if isinstance(logfile, bytes):
		logfile = safe_decode(
			logfile,
			enc=libopensesame.misc.filesystem_encoding(),
			errors=u'ignore'
		)
	experiment_path = safe_decode(
		os.path.abspath(options.experiment),
		enc=libopensesame.misc.filesystem_encoding()
	)
	if options.debug:
		# In debug mode, don't try to catch any exceptions
		exp = libopensesame.experiment.experiment(
			u"Experiment",
			experiment,
			experiment_path=experiment_path
		)
		exp.set_subject(options.subject)
		exp.var.fullscreen = options.fullscreen
		exp.logfile = logfile
		exp.run()
		exp.end()
	else:
		# Try to parse the experiment from a file
		try:
			exp = libopensesame.experiment.experiment(
				u"Experiment",
				experiment,
				experiment_path=experiment_path
			)
		except Exception as e:
			libopensesame.misc.messagebox(
				u"OpenSesame Run",
				libopensesame.misc.strip_tags(e)
			)
			sys.exit()
		# Set some options
		exp.set_subject(options.subject)
		exp.var.fullscreen = options.fullscreen
		exp.logfile = logfile
		# Initialize random number generator
		import random
		random.seed()
		# Try to run the experiment
		try:
			exp.run()
		except Exception as e:
			# Try to nicely end the experiment, even though an exception
			# occurred.
			try:
				exp.end()
			except Exception as f:
				libopensesame.misc.messagebox(
					u"OpenSesame Run",
					libopensesame.misc.strip_tags(f)
				)
			libopensesame.misc.messagebox(
				u"OpenSesame Run",
				libopensesame.misc.strip_tags(e)
			)
	libopensesame.experiment.clean_up(exp.debug)
