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
		Constructor
		
		Arguments:
		form -- the parent form

		Keyword arguments:
		text -- a string of text (default='label')		
		frame -- indicates whether a frame should be drawn around the widget
				 (default=False)
		center -- indicates whether the text should be centered (default=True)
		</DOC>"""

		if type(frame) != bool:
			frame = frame == 'yes'
		if type(center) != bool:
			center = center == 'yes'			
			
		widget.__init__(self, form)
		self.type = 'label'		
		self.text = text
		self.frame = frame
		self.center = center
		self.x_pad = 8
		self.y_pad = 8
				
	def draw_text(self, text):
	
		"""<DOC>
		Draws text in the widget
		
		Arguments:
		text -- the text to draw
		</DOC>"""
	
		x, y, w, h = self.rect
		if self.center:
			x += w/2
			y += h/2
		else:
			x += self.x_pad
			y += self.y_pad
		w -= 2*self.x_pad							
		self.form.canvas.text(text, center=self.center, x=x, y=y, max_width=w)		
		
	def render(self):
	
		"""<DOC>
		Draws the widget
		</DOC>"""	

		if self.frame:
			self.draw_frame(self.rect)
		self.draw_text(self.text)

