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

from widget import widget
try: # Try both import statements
	from PIL import Image
except:
	import Image
from libopensesame.exceptions import osexception
import os

class image(widget):

	"""A simple non-interactive image widget"""

	def __init__(self, form, path=None, adjust=True, frame=False):
	
		"""<DOC>
		Constructor.
		
		Arguments:
		form -- The parent form.
		
		Keyword arguments:
		path -- The full path to the image (default=None).
		adjust -- Indicates whether the image should be scaled according to the #
				  size of the widget (default=True).
		frame -- Indicates whether a frame should be drawn around the widget #
				 (default=False).
		</DOC>"""		
	
		if type(adjust) != bool:
			adjust = adjust == u'yes'			
		if type(frame) != bool:
			frame = frame == u'yes'						
	
		widget.__init__(self, form)
		self.adjust = adjust
		self.frame = frame
		self.path = path
		self.type = u'image'
				
	def render(self):
	
		"""<DOC>
		Draws the widget.
		</DOC>"""	
	
		if not os.path.exists(self.path):
			raise osexception( \
				u'No valid path has been specified in image widget')
		
		x, y, w, h = self.rect
		x += w/2
		y += h/2
		self.form.canvas.image(self.path, x=x, y=y, scale=self.scale, \
			center=True)
		if self.frame:
			self.draw_frame(self.rect)

	def set_rect(self, rect):
	
		"""<DOC>
		Sets the widget geometry.
		
		Arguments:
		rect -- A (left, top, width, height) tuple.
		</DOC>"""	
	
		self.rect = rect	
		if self.adjust:
			x, y, w, h = self.rect
			try:
				img = Image.open(self.path)
				img_w, img_h = img.size
			except:				
				try:
					import pygame
					img = pygame.image.load(self.path)
				except:
					raise osexception( \
						u'Failed to open image "%s". Perhaps the file is not an image, or the image format is not supported.' \
						% self.path)
				img_w, img_h = img.get_width()			
			scale_x = 1.*w/img_w
			scale_y = 1.*h/img_h
			self.scale = min(scale_x, scale_y)
		else:
			self.scale = 1
		
		
		
		
