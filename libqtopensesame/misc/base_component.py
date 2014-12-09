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
from PyQt4 import QtCore, QtGui, uic
from libopensesame import debug
from libopensesame.exceptions import osexception

class base_component(object):

	"""
	desc:
		A base class for all components, notably dialogs and widgets.
	"""

	enc = u'utf-8'

	def setup(self, main_window, ui=None):

		"""
		desc:
			Constructor.

		arguments:
			main_window:	A qtopensesame object.

		keywords:
			ui:
							An id for a user-interface file. For example
							'dialogs.quick_switcher' will correspond to
							the file 'resources/ui/dialogs/quick_switcher.ui'.
		"""

		from libqtopensesame.qtopensesame import qtopensesame
		# If the main_window is actually not the main window, but a widget that
		# has the main window somewhere above it in the hierarchy, we traverse
		# upwards.
		from libqtopensesame.qtopensesame import qtopensesame
		while not isinstance(main_window, qtopensesame):
			if hasattr(main_window, u'main_window'):
				_parent = main_window.main_window
			else:
				_parent = main_window.parent()
				if _parent == None:
					raise osexception(u'Invalid main_window')
			main_window = _parent
		self.main_window = main_window
		self.load_ui(ui)
		if hasattr(self.main_window, u'theme'):
			self.main_window.theme.apply_theme(self)

	def load_ui(self, ui=None):

		"""
		desc:
			Dynamically loads the ui, if any.

		keywords:
			ui:			An id for a user-interface file, or None.
		"""

		if ui != None:
			# If the UI file has been explicitly registered, which is the case
			# for extensions
			if hasattr(self, u'experiment') and ui in self.experiment.resources:
				ui_path = self.experiment.resources[ui]
			else:
				# Dot-split the ui id, append a `.ui` extension, and assume it's
				# relative to the resources/ui subfolder.
				path_list = [u'ui'] + ui.split(u'.')
				if hasattr(self, u'experiment'):
					# If an experiment object is available, use that to find the
					# resources ...
					ui_path = self.experiment.resource(
						os.path.join(*path_list)+u'.ui')
				else:
					# ... otherwise use the static resources function.
					from libopensesame import misc
					ui_path = misc.resource(os.path.join(*path_list)+u'.ui')
			debug.msg(u'dynamically loading ui: %s' % ui_path)			
			self.ui = uic.loadUi(open(ui_path), self)
		else:
			self.ui = None
