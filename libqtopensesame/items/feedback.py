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

import libopensesame.feedback
from libqtopensesame.items import qtplugin

class feedback(libopensesame.feedback.feedback, qtplugin.qtplugin):

	"""
	desc:
		The sketchpad controls have been removed, and will re-implemented.
	"""

	def __init__(self, name, experiment, string=None):

		libopensesame.sketchpad.sketchpad.__init__(self, name, experiment,
			string)
		qtplugin.qtplugin.__init__(self)

	def edit_widget(self):

		self.lock = True
		qtplugin.qtplugin.edit_widget(self)
		self.lock = False
		return self._edit_widget
