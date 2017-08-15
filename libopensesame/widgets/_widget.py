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
from libopensesame.widgets._form import form as _form
from libopensesame.exceptions import osexception
from openexp.canvas_elements import Rect


class widget(object):

	"""
	desc:
		The base class for all other widgets.
	"""

	def __init__(self, form):

		"""
		desc:
			Constructor.

		arguments:
			form:
				desc:	The parent form.
				type:	form
		"""

		self.type = u'widget'
		self.form = form
		self.frame = False
		self.rect = None
		self.focus = False
		self.var = None
		# Check if the form parameter is valid
		if not isinstance(form, _form):
			raise osexception(
				u'The first parameter passed to the constructor of a form widget should be a form, not "%s"' \
				% form)

	@property
	def box_size(self):
		return self.form.theme_engine.box_size()

	@property
	def theme_engine(self):
		return self.form.theme_engine

	@property
	def canvas(self):
		return self.form.canvas

	def _init_canvas_elements(self):

		"""
		desc:
			Initializes all canvas elements.
		"""

		self._frame_elements = {}

	def draw_frame(self, rect=None, style=u'normal'):

		"""
		desc:
			Draws a simple frame around the widget.

		keywords:
			rect:
				desc:	A (left, top, width, height) tuple for the frame
						geometry or `None` to use the widget geometry.
				type:	[tuple, NoneType]
			style:
				desc:	A visual style. Should be 'normal', 'active', or
						'light'.
				type:	[str, unicode]
		"""

		if not self.frame:
			return
		if style not in self._frame_elements:
			element = self.theme_engine.frame(*self.rect, style=style)
			self._frame_elements[style] = element
			self.canvas.add_element(element)
			self.canvas.lower_to_bottom(element)
		for element_style, element in self._frame_elements.items():
			element.visible = element_style == style

	def on_mouse_click(self, pos):

		"""
		desc:
			Is called whenever the user clicks on the widget.

		arguments:
			pos:
				desc:	An (x, y) coordinates tuple.
				type:	tuple
		"""

		pass

	def render(self):

		"""
		desc:
			Draws the widget.
		"""

		self.draw_frame(self.rect)

	def set_rect(self, rect):

		"""
		desc:
			Sets the widget geometry.

		arguments:
			rect:
				desc:	A (left, top, width, height) tuple.
				type:	tuple
		"""

		self.rect = rect
		self._init_canvas_elements()


	def set_var(self, val, var=None):

		"""
		desc:
			Sets an experimental variable.

		arguments:
			val:
				desc:	A value.

		keywords:
			var:
				desc:	A variable name, or None to use widget default.
				type:	[str, unicode, NoneType]
		"""

		if var is None:
			var = self.var
		if var is None:
			return
		self.form.experiment.var.set(var, val)
