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
from libqtopensesame.extensions import base_extension
from libqtopensesame.misc.config import cfg
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'opensesame_3_notifications', category=u'extension')

class opensesame_3_notifications(base_extension):

	"""
	desc:
		Provides tips for new users of OpenSesame 3.
	"""

	def event_os3n_dismiss_startup(self):

		"""
		desc:
			Permanently disables the startup tab.
		"""

		cfg.os3n_new_user_notification = False
		self.main_window.tabwidget.close_current()

	def event_os3n_dismiss_old_experiment(self):

		"""
		desc:
			Permanently disables the old-experiment tab.
		"""

		cfg.os3n_old_experiment_notification = False
		self.main_window.tabwidget.close_current()

	def event_startup(self):

		"""
		desc:
			Called at the end of the OpenSesame startup process.
		"""

		if cfg.os3n_new_user_notification:
			self.tabwidget.open_markdown(self.ext_resource(u'new-user.md'),
				title=u'Welcome!')

	def event_open_experiment(self, path):

		"""
		desc:
			Opens a notification tab when opening an experiment that was created
			with an older version of OpenSesame.

		arguments:
			path:
				desc:	The full path of the experiment file.
				type:	unicode
		"""

		if self.experiment.front_matter[u'API'] >= 2:
			return
		self.main_window.current_path = None
		self.main_window.window_message(u'New experiment')
		self.main_window.set_unsaved(True)
		if not cfg.os3n_old_experiment_notification:
			return
		self.tabwidget.open_markdown(self.ext_resource(u'old-experiment.md'))
