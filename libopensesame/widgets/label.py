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

	def __init__(self, form, text, frame=False, center=False):
	
		"""<DOC>
		Constructor
		
		Arguments:
		form -- the parent form
		text -- a string of text
		
		Keyword arguments:
		frame -- indicates whether a frame should be drawn around the widget
				 (default=False)
		center -- indicates whether the text should be centered (default=False)
		</DOC>"""
			
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
		for text in textwrap.wrap(text, self.max_len):
			if self.center:
				self.form.canvas.text(text, center=True, x=x+w/2, y=y+h/2)
			else:
				self.form.canvas.text(text, center=False, x=x+self.x_pad, \
					y=y+self.y_pad)
			y += self.text_height					
		
	def render(self):
	
		"""<DOC>
		Draws the widget
		</DOC>"""	

		if self.frame:
			self.draw_frame(self.rect)
		self.draw_text(self.text)
		
	def set_rect(self, rect):
	
		"""<DOC>
		Sets the widget geometry
		
		Arguments:
		rect -- a (left, top, width, height) tuple
		</DOC>"""
			
		widget.set_rect(self, rect)		
		# Some ugly code to determine the maximum number of characters that fit
		# into the label
		x, y, w, h = rect
		self.text_height = self.form.canvas.text_size('WWWW')[1]		
		self.max_len = 1
		while True:
			s = ''.join(['W']*self.max_len)
			if self.form.canvas.text_size(s)[0] >= w-4*self.x_pad:
				break
			self.max_len += 1
