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

from PyQt4 import QtCore, QtGui
from libqtopensesame.misc.base_subcomponent import base_subcomponent

class base_validator(base_subcomponent, QtGui.QValidator):

	"""
	desc:
		A base class for input validators.
	"""

	def __init__(self, main_window, default):

		self.default = default
		super(base_validator, self).__init__(main_window)
		self.setup(main_window)

	def is_valid(self, val):

		return True

	def set_text(self, val, text):

		val.remove(0, len(val))
		val.insert(0, text)

	def validate(self, val, pos):

		if self.is_valid(unicode(val)):
			return (self.Acceptable, pos)
		else:
			return (self.Intermediate, pos)

	def fixup(self, val):

		if not self.is_valid(unicode(val)):
			self.set_text(val, self.default)
