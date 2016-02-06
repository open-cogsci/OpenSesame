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

from libqtopensesame.misc.base_subcomponent import base_subcomponent
from qtpy import QtCore, QtWidgets

class base_dialog(QtWidgets.QDialog, base_subcomponent):

	"""
	desc:
		A base class for dialogs.
	"""

	def __init__(self, main_window, ui=None, *arglist, **kwdict):

		"""
		desc:
			Constructor.

		arguments:
			main_window:	A qtopensesame object.

		keywords:
			ui:
							An id for a user-interface file, for example
							'dialogs.quick_switcher'.

		argument-list:
		*arglist:			A list of arguments to be passed onto QDialog.

		keyword-dict:
		*kwdict:			A dict of keywords to be passed onto QDialog.
		"""

		super(base_dialog, self).__init__(main_window, *arglist, **kwdict)
		self.setup(main_window, ui=ui)
