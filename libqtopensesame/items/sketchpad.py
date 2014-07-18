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

from libqtopensesame.misc.sketchpad_canvas import sketchpad_canvas
from libqtopensesame.misc import _
from PyQt4 import QtGui, QtCore
from libopensesame.sketchpad import sketchpad as sketchpad_runtime
from libqtopensesame.widgets.sketchpad_widget import sketchpad_widget
from libqtopensesame.items.qtplugin import qtplugin
from libqtopensesame import sketchpad_elements

class sketchpad(qtplugin, sketchpad_runtime):

	"""
	desc:
		The sketchpad controls have been removed, and will re-implemented.
	"""

	def __init__(self, name, experiment, string=None):

		sketchpad_runtime.__init__(self, name, experiment, string)
		self.canvas = sketchpad_canvas(self)
		qtplugin.__init__(self)

	def init_edit_widget(self):

		qtplugin.init_edit_widget(self, False)
		self.sketchpad_widget = sketchpad_widget(self)
		self.add_widget(self.sketchpad_widget)

	def element_module(self):

		return sketchpad_elements

	def eval_text(self, s, round_float=True):

		return s

	def edit_widget(self):

		self.lock = True
		qtplugin.edit_widget(self)
		self.sketchpad_widget.draw()
		self.lock = False
		return self._edit_widget

	def selected_elements(self):

		l = []
		for element in self.elements:
			if element.selected:
				l.append(element)
		return l

	def remove_elements(self, elements):

		for element in elements:
			self.elements.remove(element)

	def move_elements(self, elements, dx=0, dy=0):

		for element in elements:
			element.move(dx, dy)

	@property
	def draw(self):
		return self.sketchpad_widget.draw

	@property
	def set_cursor_pos(self):
		return self.sketchpad_widget.set_cursor_pos

	@property
	def graphics_view(self):
		return self.sketchpad_widget.ui.graphics_view


