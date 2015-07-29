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

from libopensesame.py3compat import *
from libqtopensesame.sketchpad_elements._base_element import base_element
from libopensesame.sketchpad_elements import image as image_runtime

class image(base_element, image_runtime):

	"""
	desc:
		An image element.

		See base_element for docstrings and function descriptions.
	"""

	@classmethod
	def mouse_press(cls, sketchpad, pos):

		from libqtopensesame.widgets import pool_widget
		_file = pool_widget.select_from_pool(sketchpad.main_window,
			parent=sketchpad._edit_widget)
		if _file == u'':
			return None
		properties = {
			u'x':		pos[0],
			u'y':		pos[1],
			u'file':	_file,
			u'scale':	sketchpad.current_scale(),
			u'center':	sketchpad.current_center(),
			u'show_if': sketchpad.current_show_if()
		}
		e = image(sketchpad, properties=properties)
		return e

	@staticmethod
	def requires_center():
		return True

	@staticmethod
	def requires_scale():
		return True
