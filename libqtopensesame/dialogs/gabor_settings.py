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

from qtpy import QtCore, QtWidgets
from libqtopensesame.dialogs.patch_settings import patch_settings
from libopensesame.py3compat import *

class gabor_settings(patch_settings):

	"""
	desc:
		A gabor settings dialog.
	"""

	def ui_file(self):

		"""
		returns:
			desc:	The ui file.
			type:	unicode
		"""

		return u'dialogs.gabor_settings'

	def get_properties(self):

		"""
		desc:
			Gets the Gabor properties.

		returns:
			desc:	A dictionary with properties.
			type:	dict
		"""

		if self.exec_() != QtWidgets.QDialog.Accepted:
			return None
		properties = {
			u'orient'	: self.ui.spinbox_orient.value(),
			u'freq'		: self.ui.spinbox_freq.value(),
			u'env'		: self.env_map[
				str(self.ui.combobox_env.currentText())],
			u'size'		: self.ui.spinbox_size.value(),
			u'stdev'	: self.ui.spinbox_stdev.value(),
			u'phase'	: self.ui.spinbox_phase.value(),
			u'color1'	: str(self.ui.edit_color1.text()),
			u'color2'	: str(self.ui.edit_color2.text()),
			u'bgmode'	: self.bgmode_map[
				str(self.ui.combobox_bgmode.currentText())]
			}
		return properties

	def set_properties(self, properties):

		"""
		desc:
			Fills the dialog controls based on a properties dictionary.

		arguments:
			properties:
				desc:	A properties dictionary.
				type:	dict
		"""

		self.ui.spinbox_orient.setValue(properties[u'orient'])
		self.ui.spinbox_size.setValue(properties[u'size'])
		self.ui.spinbox_stdev.setValue(properties[u'stdev'])
		self.ui.spinbox_freq.setValue(properties[u'freq'])
		self.ui.spinbox_phase.setValue(properties[u'phase'])
		self.ui.edit_color1.setText(properties[u'color1'])
		self.ui.edit_color2.setText(properties[u'color2'])
		# To set the comboxes we have to reverse-lookup the correct text, find
		# the corresponding index, and then set the index.
		for key, val in self.env_map.items():
			if val == properties[u'env']:
				i = self.ui.combobox_env.findText(key)
				break
		self.ui.combobox_env.setCurrentIndex(i)
		for key, val in self.bgmode_map.items():
			if val == properties[u'bgmode']:
				i = self.ui.combobox_bgmode.findText(key)
				break
		self.ui.combobox_bgmode.setCurrentIndex(i)
