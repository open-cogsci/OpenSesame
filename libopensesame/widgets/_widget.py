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
from libopensesame.widgets._form import Form
from libopensesame.exceptions import osexception
from openexp.canvas_elements import Rect


class Widget(object):

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
		self._focus = False
		self.var = None
		# Check if the form parameter is valid
		if not isinstance(form, Form):
			raise osexception(
				u'The first parameter passed to the constructor of a form widget should be a form, not "%s"'
				% form)

	@property
	def focus(self):

		return self._focus

	@focus.setter
	def focus(self, focus):

		self._focus = focus
		self._update()

	@property
	def box_size(self):
		return self.form.theme_engine.box_size()

	@property
	def theme_engine(self):
		return self.form.theme_engine

	@property
	def canvas(self):
		return self.form.canvas

	def _inside(self, pos, rect):

		x1, y1 = pos
		x2, y2, w, h = rect
		return not (x1 < x2 or y1 < y2 or x1 > x2+w or y1 > y2+h)

	def _init_canvas_elements(self):

		"""
		desc:
			Initializes all canvas elements.
		"""

		self._frame_elements = {}

	def _update_frame(self, rect=None, style=u'normal'):

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

	def _update(self):

		"""
		desc:
			Draws the widget.
		"""

		self._update_frame(self.rect)

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
		self._update()

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

	def on_key_press(self, key):

		"""
		desc:
			Is called whenever the widget is focused and the users enters a key.

		arguments:
			key:
				desc:	A key
				type:	str
		"""

		pass

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

	def coroutine(self):

		"""
		desc:
			Implements the interaction. This can be overridden to implement more
			complicated keyboard/ mouse interactions.
		"""

		retval = None
		while True:
			d = yield retval
			if d[u'type'] == u'click':
				retval = self.on_mouse_click(d['pos'])
			elif d[u'type'] == u'key':
				retval = self.on_key_press(d[u'key'])
			elif d[u'type'] == u'stop':
				break


widget = Widget
