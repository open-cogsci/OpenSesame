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

from form import form as _form
from libopensesame.exceptions import osexception

class widget:

	"""The base class for all other widgets"""

	def __init__(self, form):

		"""<DOC>
		Constructor.

		Arguments:
		form -- The parent form.
		</DOC>"""

		self.type = u'widget'
		self.form = form
		self.rect = None
		self.focus = False
		self.var = None

		# Check if the form parameter is valid
		if not isinstance(form, _form):
			raise osexception( \
				u'The first parameter passed to the constructor of a form widget should be a form, not "%s"' \
				% form)

	def draw_frame(self, rect=None, style=u'normal'):

		"""<DOC>
		Draws a simple frame around the widget.

		Keyword arguments:
		rect -- A (left, top, width, height) tuple for the frame geometry or
				None to use the widget geometry (default=None).
		style -- 'normal', 'active', 'light' (default='normal').
		</DOC>"""

		x, y, w, h = rect
		self.form.theme_engine.frame(x, y, w, h, style=style)

	def on_mouse_click(self, pos):

		"""<DOC>
		Is called whenever the user clicks on the widget

		Arguments:
		pos -- An (x, y) tuple
		</DOC>"""

		pass

	def render(self):

		"""<DOC>
		Draws the widget.
		</DOC>"""

		if self.focus:
			self.draw_frame(self.rect, focus=True)
		else:
			self.draw_frame(self.rect)

	def set_rect(self, rect):

		"""<DOC>
		Sets the widget geometry.

		Arguments:
		rect -- A (left, top, width, height) tuple.
		</DOC>"""

		self.rect = rect

	def set_var(self, val, var=None):

		"""<DOC>
		Sets an experimental variable.

		Arguments:
		val -- A value.

		Keyword arguments:
		var -- A variable name, or None to use widget default (default=None).
		</DOC>"""

		if var == None:
			var = self.var
		if var == None:
			return
		self.form.experiment.set(var, val)
