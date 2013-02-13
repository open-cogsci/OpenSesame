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

from image import image

class image_button(image):

	"""A simple image button"""

	def __init__(self, form, path=None, adjust=True, frame=False, image_id=None, var=None):
	
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
		image_id -- An id to identify the image when it is clicked. If None, the #
					path to the image is used as id (default=None).
		var -- The name of the experimental variable that should be used to log #
			   the widget status (default=None).					
		</DOC>"""		
	
		image.__init__(self, form, path, adjust=adjust, frame=frame)
		if image_id == None:
			self.image_id = path
		else:
			self.image_id = image_id
		self.type = 'image_button'
		self.var = var
		self.set_var(False)				
				
	def on_mouse_click(self, pos):
	
		"""<DOC>
		Is called whenever the user clicks on the widget. Returns the image_id #
		or the path to the image if no image_id has been specified.
		
		Arguments:
		pos -- An (x, y) tuple.
		</DOC>"""	
	
		self.set_var(True)
		return self.image_id

