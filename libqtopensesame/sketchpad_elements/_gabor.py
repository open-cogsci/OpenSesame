#-*- coding:utf-8 -*-

"""
This file is part of openexp.

openexp is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

openexp is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with openexp.  If not, see <http://www.gnu.org/licenses/>.
"""

from libqtopensesame.dialogs.gabor_settings import gabor_settings
from libqtopensesame.sketchpad_elements._base_element import base_element
from libopensesame.sketchpad_elements import gabor as gabor_runtime

class gabor(base_element, gabor_runtime):

	def show_edit_dialog(self):

		"""
		desc:
			The show-edit dialog for the gabor shows the settings dialog.
		"""

		d = gabor_settings(self.main_window)
		d.set_properties(self.properties)
		properties = d.get_properties()
		if properties == None:
			return
		self.properties.update(properties)
		self.sketchpad.draw()

	@staticmethod
	def click(sketchpad, pos):

		d = gabor_settings(sketchpad.main_window)
		properties = d.get_properties()
		if properties == None:
			return
		properties.update({
				u'x':			pos[0],
				u'y':			pos[1],
				u'show_if' : 	sketchpad.current_show_if()
			})
		return gabor(sketchpad, properties=properties)
