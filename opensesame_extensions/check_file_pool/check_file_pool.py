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
from libqtopensesame.extensions import base_extension
from libqtopensesame.dialogs.notification import notification
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'check_file_pool', category=u'extension')


class check_file_pool(base_extension):

	"""
	desc:
		Checks whether the file-pool folder still exists, and if not, offers the
		chance to save the file under a different name.
	"""

	def event_save_experiment(self, path):

		if os.path.exists(self.experiment.pool.folder()):
			return
		notification(self.main_window,
			msg=_(
u'''The file-pool folder has been deleted by the operating system or another
application. If you are running Windows 10, de-activate the option 'Delete
temporary files that my apps aren't using' under 'Storage Sense'. To avoid data
loss, please now save your experiment under a different name.'''),
			title=_(u'File pool missing')
			).exec_()
		os.mkdir(self.experiment.pool.folder())
		self.main_window.save_file_as()
