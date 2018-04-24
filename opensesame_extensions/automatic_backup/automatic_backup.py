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
import time
from qtpy import QtCore
from libopensesame import misc
from libopensesame.oslogging import oslogger
from libqtopensesame.extensions import base_extension
from libqtopensesame.misc.config import cfg
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'automatic_backup', category=u'extension')


class automatic_backup(base_extension):

	"""
	desc:
		An extension that periodically saves the experiment.
	"""

	def activate(self):

		"""
		desc:
			Opens the autosave folder.
		"""

		if os.name == u"nt":
			os.startfile(self.autosave_folder)
		elif os.name == u"posix":
			misc.open_url(self.autosave_folder)

	def event_startup(self):

		"""
		desc:
			Initializes the extension on OpenSesame startup.
		"""

		# Create the autosave folder if it doesn't exist yet
		if not os.path.exists(os.path.join(self.main_window.home_folder,
			u".opensesame", u"backup")):
			os.mkdir(os.path.join(self.main_window.home_folder, u".opensesame",
				u"backup"))
		self.autosave_folder = os.path.join(self.main_window.home_folder,
			u".opensesame", u"backup")

		# Remove expired backups
		for path in os.listdir(self.autosave_folder):
			_path = os.path.join(self.autosave_folder, path)
			t = os.path.getctime(_path)
			age = (time.time() - t)/(60*60*24)
			if age > cfg.autosave_max_age:
				oslogger.debug(u"removing '%s'" % path)
				try:
					os.remove(_path)
				except:
					oslogger.error(u"failed to remove '%s'" % path)

		self.start_autosave_timer()

	def event_run_experiment(self, fullscreen):

		"""
		desc:
			Suspend autosave timer when the experiment starts.
		"""

		if self.autosave_timer is not None:
			oslogger.debug(u"stopping autosave timer")
			self.autosave_timer.stop()

	def event_end_experiment(self, ret_val):

		"""
		desc:
			Resume autosave timer when the experiment ends.
		"""

		if self.autosave_timer is not None:
			oslogger.debug(u"resuming autosave timer")
			self.autosave_timer.start()

	def start_autosave_timer(self):

		"""
		desc:
			Starts the autosave timer.
		"""

		if cfg.autosave_interval > 0:
			oslogger.debug(u"autosave interval = %d ms" % cfg.autosave_interval)
			self.autosave_timer = QtCore.QTimer()
			self.autosave_timer.setInterval(cfg.autosave_interval)
			self.autosave_timer.setSingleShot(True)
			self.autosave_timer.timeout.connect(self.autosave)
			self.autosave_timer.start()
		else:
			oslogger.debug(u"autosave disabled")
			self.autosave_timer = None

	def autosave(self):

		"""
		desc:
			Autosave the experiment if there are unsaved changes.
		"""

		if self.main_window.unsaved_changes:
			path = os.path.join(self.autosave_folder,
				u'%s.osexp' % str(time.ctime()).replace(u':',
				u'_'))
			try:
				self.main_window.get_ready()
				self.experiment.save(path, overwrite=True, update_path=False)
				oslogger.debug(u"saving backup as %s" % path)
			except:
				pass
		self.start_autosave_timer()
