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
from qtpy import QtWidgets
from libopensesame.python_workspace_api import xy_from_polar
from libqtopensesame.dialogs.base_dialog import base_dialog


class polar_coordinates(base_dialog):

	"""
	desc:
		A dialog for determining cartesian coordinates from polar coordinates.
	"""

	def __init__(self, main_window):

		"""
		desc:
			Constructor.

		arguments:
			main_window:	The main window object.
		"""

		base_dialog.__init__(self, main_window, ui=u'dialogs.polar_coordinates')
		self.update()

	def xy(self):

		return xy_from_polar(
			pole=(self.ui.spinbox_pole_x.value(), self.ui.spinbox_pole_y.value()),
			rho=self.ui.spinbox_rho.value(),
			phi=self.ui.spinbox_phi.value()
		)

	def update(self):

		base_dialog.update(self)
		x, y = self.xy()
		self.ui.label_cartesian_x.setText(u'%.2f px' % x)
		self.ui.label_cartesian_y.setText(u'%.2f px' % y)

	def get_xy(self):

		"""
		desc:
			Executes the dialog and gets the xy coordinates, or None if the
			dialog was cancelled.

		returns:
			type:	[tuple, NoneType]
		"""

		if self.exec_() != QtWidgets.QDialog.Accepted:
			return None
		return self.xy()
