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

from PyQt4 import QtCore, QtGui, uic

class base_component(object):

	"""
	desc:
		A base class for all components, notably dialogs and widgets.
	"""

	def setup(self, main_window, ui=None):

		"""
		desc:
			Constructor.

		arguments:
			main_window:	A qtopensesame object.

		keywords:
			ui:
							An id for a user-interface file. For example
							'dialogs.quick_open_item' will correspond to
							the file 'resources/ui/dialogs/quick_open_item.ui'.
		"""

		self.main_window = main_window
		self.theme = main_window.theme
		self.theme.apply_theme(self)
		self.experiment = self.main_window.experiment
		print self.__class__
		if ui != None:
			ui_path = self.experiment.resource(u'ui/%s.ui' % ui.replace(u'.',
				u'/'))
			self.ui = uic.loadUi(ui_path, self)
		else:
			self.ui = None


