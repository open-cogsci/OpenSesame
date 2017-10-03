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
import textwrap
from libopensesame.widgets._widget import Widget
from openexp.canvas_elements import RichText


class Label(Widget):

	"""
	desc: |
		The `Label` widget is a non-interactive string of text.

		__Example (OpenSesame script):__

		~~~
		widget 0 0 1 1 label text='My text'
		~~~

		__Example (Python):__

		~~~ .python
		form = Form()
		label = Label(text='My text')
		form.set_widget(label, (0,0))
		form._exec()
		~~~

		[TOC]
	"""

	def __init__(self, form, text=u'label', frame=False, center=True):

		"""
		desc: |
			Constructor to create a new `Label` object. You do not generally
			call this constructor directly, but use the `Label()` factory
			function, which is described here: [/python/common/]().

		arguments:
			form:
				desc:	The parent form.
				type:	form

		keywords:
			text:
				desc:	The label text.
				type:	[str, unicode]
			frame:
				desc:	Indicates whether a frame should be drawn around the
						widget.
				type:	bool
			center:
				desc:	Indicates whether the text should be centerd.
				type:	bool
		"""

		if isinstance(frame, basestring):
			frame = frame == u'yes'
		if isinstance(center, basestring):
			center = center == u'yes'
		Widget.__init__(self, form)
		self.type = u'label'
		self.text = text
		self.frame = frame
		self.html = True
		self.center = center
		self.x_pad = 8
		self.y_pad = 8
		self.tab_str = u'    ' # Replace tab characters by four spaces

	def _init_canvas_elements(self):

		x, y, w, h = self.rect
		if self.center:
			x += w/2
			y += h/2
		else:
			x += self.x_pad
			y += self.y_pad
		w -= 2*self.x_pad
		self._text_element = RichText(self.text, center=self.center,
			x=x, y=y, max_width=w, html=self.html).construct(self.canvas)
		self.canvas.add_element(self._text_element)
		Widget._init_canvas_elements(self)

	def _update_text(self, text):

		"""
		desc:
			Draws text inside the widget.

		arguments:
			text:
				desc:	The text to draw.
				type:	[str, unicode]
		"""

		text = self.form.experiment.syntax.eval_text(text)
		text = safe_decode(text).replace(u'\t', self.tab_str)
		self._text_element.text = text

	def _update(self):

		"""
		desc:
			Draws the widget.
		"""

		if self.frame:
			self._update_frame(self.rect)
		self._update_text(self.text)


label = Label
