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

class box_widget(widget):

	"""The base class for widgets that have a clickable box"""

	def __init__(self, box_size=16):
	
		"""<DOC>
		Constructor
		
		Keyword arguments:
		box_size -- the size of the box (default=16)
		</DOC>"""
		
	
		self.box_size = box_size
		
	def draw_box(self, checked, x, y):
	
		"""<DOC>
		Draw the box
		
		Arguments:
		checked -- indicates whether box has been checked
		x -- the left of the box
		y -- the top of the box 
		</DOC>"""		
	
		self.form.canvas.rect(x, y, self.box_size, self.box_size, fill=checked)
		
