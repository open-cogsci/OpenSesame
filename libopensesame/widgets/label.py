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

import textwrap
from widget import widget

class label(widget):

	"""A simple non-interactive text label"""

	def __init__(self, form, text='label', frame=False, center=True):

		"""<DOC>
		Constructor.
		
		Arguments:
		form -- The parent form.

		Keyword arguments:
		text -- A string of text (default='label').
		frame -- Indicates whether a frame should be drawn around the widget #
				 (default=False).
		center -- Indicates whether the text should be centered (default=True).
		</DOC>"""

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

		"""<DOC>
		Draws text in the widget.
		
		Arguments:
		text -- The text to draw.
		
		Keyword arguments:
		html -- Indicates whether HTML should be parsed (default=True).
		</DOC>"""

		if self.form.item != None:
			text = self.form.item.eval_text(text)
		else:
			text = self.form.experiment.eval_text(text)
		text = self.form.experiment.unistr(text).replace('\t', self.tab_str)
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

		"""<DOC>
		Draws the widget.
		</DOC>"""	

		if self.frame:
			self.draw_frame(self.rect)
		self.draw_text(self.text)

