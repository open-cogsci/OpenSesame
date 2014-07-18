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

from libqtopensesame.widgets.base_widget import base_widget

class sketchpad_widget(base_widget):

	"""
	desc:
		The sketchpad controls. Most of the actual work is handled by
		libqtopensesame.misc.sketchpad_canvas.
	"""

	def __init__(self, sketchpad):

		"""
		desc:
			Constructor.

		arguments:
			sketchpad:		A sketchpad object.
		"""

		super(sketchpad_widget, self).__init__(sketchpad.main_window,
			ui=u'widgets.sketchpad')
		self.sketchpad = sketchpad
		self.zoom = 1.
		self.canvas = self.sketchpad.canvas
		self.ui.graphics_view.setScene(self.canvas)
		self.set_size()

	def set_size(self):

		"""
		desc:
			Sets the size of the QGraphicsView to the experiment resolution.
		"""

		w = self.sketchpad.get(u'width')
		h = self.sketchpad.get(u'height')
		self.ui.graphics_view.setFixedSize(self.zoom*w, self.zoom*h)

	def draw(self):

		"""
		desc:
			Clears and redraws the sketchpad canvas.
		"""

		self.canvas.clear()
		for element in self.sketchpad.elements:
			element.draw()
		self.sketchpad.user_hint_widget.clear()
		if len(self.canvas.notifications) > 0:
			self.sketchpad.user_hint_widget.add_user_hint(u'\n'.join(
				self.canvas.notifications))
		self.sketchpad.user_hint_widget.refresh()

	def set_cursor_pos(self, xy):

		"""
		desc:
			Updates the cursor-position indicator.

		arguments:
			xy:		An (x,y) tuple with the cursor position.
		"""

		self.ui.label_coordinates.setText(u'(%s, %s)' % xy)
