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

from libqtopensesame.misc import _
from libqtopensesame.widgets.header_widget import header_widget

class general_header_widget(header_widget):

	"""
	desc:
		The widget containing the clickable title and description of the
		experiment.
	"""

	def __init__(self, general_tab, main_window):

		"""
		desc:
			Constructor.

		arguments:
			general_tab:	A general_properties object.
			main_window:	A qtopensesame object.
		"""

		header_widget.__init__(self, main_window, main_window.experiment)
		self.general_tab = general_tab
		self.label_name.setText(
			_(u"<font size='5'><b>%s</b> - Experiment</font>&nbsp;&nbsp;&nbsp;<font color='gray'><i>Click to edit</i></font>") \
			% self.item.get(u"title", _eval=False))

	def restore_name(self):

		"""
		desc:
			Applies the name change, hides the editable title and shows the
			label.
		"""

		self.general_tab.apply_changes()
		self.label_name.setText(_(
			u"<font size='5'><b>%s</b> - Experiment</font>&nbsp;&nbsp;&nbsp;<font color='gray'><i>Click to edit</i></font>") \
			% self.item.get(u"title", _eval=False))
		self.label_name.show()
		self.edit_name.setText(self.item.get(u"title", _eval=False))
		self.edit_name.hide()

	def restore_desc(self):

		"""
		desc:
			Applies the description change, hides the editable description and
			shows the label.
		"""

		self.general_tab.apply_changes()
		self.label_desc.setText(self.item.get(u"description", _eval=False))
		self.label_desc.show()
		self.edit_desc.setText(self.item.get(u"description", _eval=False))
		self.edit_desc.hide()
