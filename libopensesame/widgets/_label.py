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
from libopensesame.widgets._widget import widget

class label(widget):

	"""
	desc: |
		The label widget is a non-interactive string of text.

		__Example (OpenSesame script):__

		~~~
		widget 0 0 1 1 label text='My text'
		~~~

		__Example (Python):__

		~~~ .python
		from libopensesame import widgets
		form = widgets.form(exp)
		label = widgets.label(form, text='My text')
		form.set_widget(label, (0,0))
		form._exec()
		~~~

		[TOC]
	"""

	def __init__(self, form, text=u'label', frame=False, center=True):

		"""
		desc:
			Constructor.

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

		if type(frame) != bool:
			frame = frame == u'yes'
		if type(center) != bool:
			center = center == u'yes'

		widget.__init__(self, form)
		self.type = u'label'
		self.text = text
		self.frame = frame
		self.center = center
		self.x_pad = 8
		self.y_pad = 8
		self.tab_str = u'    ' # Replace tab characters by four spaces

	def draw_text(self, text, html=True):

		"""
		desc:
			Draws text inside the widget.

		arguments:
			text:
				desc:	The text to draw.
				type:	[str, unicode]

		keywords:
			html:
				desc:	Indicates whether HTML should be parsed.
				type:	bool
		"""

		text = self.form.experiment.syntax.eval_text(text)
		text = safe_decode(text).replace(u'\t', self.tab_str)
		x, y, w, h = self.rect
		if self.center:
			x += w/2
			y += h/2
		else:
			x += self.x_pad
			y += self.y_pad
		w -= 2*self.x_pad
		self.form.canvas.text(text, center=self.center, x=x, y=y, max_width=w, \
			html=html)

	def render(self):

		"""
		desc:
			Draws the widget.
		"""

		if self.frame:
			self.draw_frame(self.rect)
		self.draw_text(self.text)
