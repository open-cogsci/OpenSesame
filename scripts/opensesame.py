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

if __name__ == u'__main__':
	import os, sys, platform
	# Add the folder that contains the OpenSesame modules to the path. This is
	# generally only necessary if OpenSesame is directly run from source,
	# instead from an installation.
	if os.path.exists(os.path.join(os.getcwd(), 'libopensesame')):
		sys.path.insert(0, os.getcwd())
	# Support for multiprocessing when packaged
	# In OS X the multiprocessing module is horribly broken, but a fixed
	# version has been released as the 'billiard' module
	if platform.system() == 'Darwin':
		# Use normal multirpocessing module from python 3.4 and on
		if sys.version_info >= (3,4):
			from multiprocessing import freeze_support, set_start_method
			freeze_support()
			set_start_method('forkserver')
		else:
			from billiard import freeze_support, forking_enable
			freeze_support()
			forking_enable(0)
	else:
		from multiprocessing import freeze_support
		freeze_support()
	# Parse the (optional) environment file that contains special paths, etc.
	from libopensesame.misc import resource, filesystem_encoding, \
		parse_environment_file
	parse_environment_file()
	# Force the new-style Qt API
	import sip
	sip.setapi('QString', 2)
	sip.setapi('QVariant', 2)
	# Load debug package (this must be after the working directory change)
	from libopensesame import debug
	# Do the basic window initialization
	from qtpy.QtWidgets import QApplication
	app = QApplication(sys.argv)
	from libqtopensesame.qtopensesame import qtopensesame
	opensesame = qtopensesame(app)
	opensesame.__script__ = __file__
	app.processEvents()
	# Import the remaining modules
	from qtpy.QtCore import QObject, QLocale, QTranslator
	from libopensesame.py3compat import *
	import os.path
	# Load the locale for UI translation. The locale can be specified on the
	# command line using the --locale parameter
	locale = str(QLocale().system().name())
	for i in range(len(sys.argv)-1):
		if sys.argv[i] == '--locale':
			locale = sys.argv[i+1]
	opensesame._locale = locale
	qm = resource(os.path.join(u'locale', locale) + u'.qm')
	if qm is not None:
		debug.msg(u'installing %s translator' % qm)
		translator = QTranslator()
		translator.load(qm)
		app.installTranslator(translator)
	else:
		debug.msg(u'no translator found for %s' % locale)
	# Now that the window is shown, load the remaining modules and resume the
	# GUI initialization.
	opensesame.resume_init()
	opensesame.restore_window_state()
	opensesame.refresh()
	opensesame.show()
	# Added for OS X, otherwise Window will not appear
	opensesame.raise_()
	# Exit using the application exit status
	sys.exit(app.exec_())
