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
from libqtopensesame.extensions import base_extension
from libqtopensesame.misc.config import cfg
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'qprogedit_preferences', category=u'extension')

class qprogedit_preferences(base_extension):

	"""
	desc:
		Shows the QProgEdit preferences in the preferences tab.
	"""

	def settings_widget(self):

		"""
		desc:
			returns the QProgEdit settings widget.

		returns:
			type:	QWidget
		"""

		# Create a temporary QProgEdit instance, add one tab, and wrap the
		# preferences widget for this tab in a group box.
		from QProgEdit import QTabManager
		tm = QTabManager(cfg=cfg)
		tm.addTab()
		w = tm.tab(0).prefs
		w.show()
		w.refresh()
		group = QtWidgets.QGroupBox(_(u'Editor preferences (QProgEdit)'),
			self.main_window)
		layout = QtWidgets.QHBoxLayout(group)
		layout.addWidget(w)
		group.setLayout(layout)
		return group
