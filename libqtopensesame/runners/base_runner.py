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
from PyQt4 import QtGui
from libqtopensesame.misc import config, _
from libopensesame import debug
from libopensesame.exceptions import osexception
from libopensesame.experiment import experiment
from libopensesame.py3compat import *

class base_runner(object):

	"""
	A runner implements a specific way to execute an OpenSesame experiment from
	within the GUI. The base_runner is an abstract runner that is inherited by
	actual runners.
	"""

	valid_logfile_extensions = u'.csv', u'.txt', u'.dat', u'.log'
	default_logfile_extension = u'.csv'

	def __init__(self, main_window):

		"""
		Constructor.

		Arguments:
		main_window		--	An QtGui.QMainWindow object. Typically this will be
							the qtopensesame object.
		"""

		self.main_window = main_window

	@property
	def console(self):
		return self.main_window.ui.console

	def execute(self):

		"""
		Executes the experiments. This function should be transparent and leave
		no mess to clean up for the GUI.

		Returns:
		None if the experiment finished cleanly, or an Exception (any kind) if
		an exception occurred.
		"""

		pass

	def get_logfile(self, quick=False, subject_nr=0):

		"""
		Gets the logfile for the current session, either by falling back to a
		default value ('quickrun.csv') or through a pop-up dialogue.

		Keyword arguments:
		quick		--	Indicates whether we are quickrunning the experiment.
						(default=False)
		subject_nr	--	Indicates the subject number, which is used to
						suggest a logfile. (default=0)

		Returns:
		A pathname for the logfile or None if no logfile was chosen (i.e. the
		dialogue was cancelled).
		"""

		remember_logfile = True
		if quick:
			logfile = os.path.join(config.get_config( \
				u'default_logfile_folder'), config.get_config( \
				u'quick_run_logfile'))
			try:
				open(logfile, u'w').close()
			except:
				import tempfile
				from libopensesame import misc
				debug.msg(u'Failed to open %s' % logfile)
				logfile = os.path.join(safe_decode(tempfile.gettempdir(),
					enc=misc.filesystem_encoding()), safe_decode(
					tempfile.gettempprefix(),
					enc=misc.filesystem_encoding())+u'quickrun.csv')
				debug.msg(u'Using temporary file %s' % logfile)
				remember_logfile = False
		else:
			# Suggested filename
			suggested_path = os.path.join(config.get_config( \
				u'default_logfile_folder'), u'subject-%d.csv' % subject_nr)
			# Get the data file
			csv_filter = u'Comma-separated values (*.csv)'
			logfile = str(QtGui.QFileDialog.getSaveFileName( \
				self.main_window.ui.centralwidget, \
				_(u"Choose location for logfile (press 'escape' for default location)"), \
				suggested_path, filter=csv_filter))
			# An empty string indicates that the dialogue was cancelled, in
			# which case we fall back to a default location.
			if logfile == u'':
				logfile = os.path.join(config.get_config( \
						'default_logfile_folder'), u'defaultlog.csv')
			# If a logfile was provided, but it did not have a proper extension,
			# we add a `.csv` extension.
			else:
				if os.path.splitext(logfile)[1].lower() not in \
					self.valid_logfile_extensions:
					logfile += self.default_logfile_extension
		# If the logfile is not writable, inform the user and cancel.
		try:
			open(logfile, u'w').close()
		except:
			self.main_window.experiment.notify( \
				_(u"The logfile '%s' is not writable. Please choose another location for the logfile.") \
				% logfile)
			return None
		if remember_logfile:
			# Remember the logfile folder for the next run
			config.set_config('default_logfile_folder', os.path.dirname(logfile))
		return logfile

	def get_subject_nr(self, quick=False):

		"""
		Gets the subject number for the current session, either by falling back
		to a default value of 999 (in quickmode) or through a pop-up dialogue.

		Keyword arguments:
		quick	--	Indicates whether we are quickrunning the experiment.
					(default=False)

		Returns:
		A subject number or None if no subject number was chosen (i.e. the
		dialogue was cancelled).
		"""

		if quick:
			return 999
		subject_nr, ok = QtGui.QInputDialog.getInt( \
			self.main_window.ui.centralwidget, _(u'Subject number'), \
			_(u'Please enter the subject number'), min=0)
		if not ok:
			return None
		return subject_nr

	def init_experiment(self, quick=False, fullscreen=False, auto_response= \
		False):

		"""
		Initializes a new experiment, which is a newly generated instance of the
		experiment currently active in the user interface.

		Keyword arguments:
		quick		--	Indicates whether we are quickrunning the experiment.
						(default=False)

		Returns:
		True if the experiment was successfully initiated, False it was not.
		"""

		# First tell the experiment to get ready, to apply any pending changes,
		# and then initialize the script. This can trigger errors.
		try:
			self.main_window.get_ready()
			script = self.main_window.experiment.to_string()
		except Exception as e:
			if not isinstance(e, osexception):
				e = osexception(u'Unexpected error', exception=e)
			self.console.write(e)
			self.main_window.experiment.notify(e.html())
			return False
		# Get and set the subject number
		subject_nr = self.get_subject_nr(quick=quick)
		if subject_nr is None:
			return False
		# Get and set the logfile
		logfile = self.get_logfile(quick=quick, subject_nr=subject_nr)
		if logfile is None:
			return False
		# Build a new experiment. This can trigger a script error.
		try:
			self.experiment = experiment(string=script, pool_folder= \
				self.main_window.experiment.pool_folder, experiment_path= \
				self.main_window.experiment.experiment_path, fullscreen= \
				fullscreen, auto_response=auto_response, subject_nr= \
				subject_nr, logfile=logfile)
		except Exception as e:
			if not isinstance(e, osexception):
				e = osexception(u'Unexpected error', exception=e)
			self.console.write(e)
			self.main_window.experiment.notify(e.html())
		return True

	def on_exception(self, e):

		"""
		Is called when an exception has occurred during the experiment.

		Arguments:
		e		--	An exception, or an (exception, traceback) tuple.
		"""

		if not isinstance(e, osexception):
			e = osexception(msg=u'Unexpected error', exception=e)
		self.console.write(e)
		self.main_window.experiment.notify(e.html(), title=u'Exception')

	def on_success(self, quick=False):

		"""
		Is called when an experiment has successfully ended, and gives the user
		the opportunity to copy the logfile to the file pool.

		Keyword arguments:
		quick		--	Indicates whether we are quickrunning the experiment.
						(default=False)
		"""

		if quick:
			return
		resp = QtGui.QMessageBox.question(self.main_window.ui.centralwidget, \
			_(u"Finished!"), \
			_(u"The experiment is finished and data has been logged to '%s'. Do you want to copy the logfile to the file pool?") \
			% self.experiment.logfile, QtGui.QMessageBox.Yes, \
			QtGui.QMessageBox.No)
		if resp == QtGui.QMessageBox.Yes:
			self.main_window.copy_to_pool(self.experiment.logfile)

	def run(self, quick=False, fullscreen=False, auto_response=False):

		"""
		Runs the experiment.

		Keyword arguments:
		quick			--	Indicates whether we are quickrunning the
							experiment. (default=False)
		fullscreen		--	Indicates whether the experiment should be run in
							fullscreen. (default=False)
		auto_response	--	Indicates whether auto-response mode should be
							enabled. (default=False)
		"""

		self.console.capture_stdout()
		print(u'\n')
		if not self.init_experiment(quick=quick, fullscreen=fullscreen,
			auto_response=auto_response):
			return
		ret_val = self.execute()
		if ret_val is not None:
			self.on_exception(ret_val)
		elif not quick:
			self.on_success(quick=quick)
		self.console.set_workspace_globals(self.workspace_globals())
		self.console.release_stdout()
		self.console.show_prompt()

	def workspace_globals(self):

		"""
		desc:
			Returns the experiment's globals dictionary as it was when the
			experiment finished.

		returns:
			desc:	A globals dictionary.
			type:	dict
		"""

		return {}
