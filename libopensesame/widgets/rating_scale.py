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

from libopensesame import debug
from widget import widget

class rating_scale(widget):

	"""A simple rating scale/ Likert widget"""

	def __init__(self, form, nodes=5, click_accepts=False, var=None):
	
		"""<DOC>
		Constructor.
		
		Arguments:
		form -- The parent form.
		
		Keyword arguments:
		nodes -- The number of nodes or a list of node identifiers (e.g., #
				 ['yes', 'no', 'maybe']. If a list is passed the rating scale #
				 will have labels, otherwise it will just have boxes #
				 (default=5).
		click_accepts -- Indicates whether the form should close when a value #
						 is selected (default=False).
		var -- The name of the experimental variable that should be used to log #
			   the widget status (default=None).
		</DOC>"""	
		
		if type(click_accepts) != bool:
			click_accepts = click_accepts == 'yes'					
		
		widget.__init__(self, form)
		self.type = 'rating_scale'
		self.box_size = 16
		self.click_accepts = click_accepts
		self.pos_list = []
		self.var = var
		if type(nodes) == int:
			self.nodes = ['']*nodes
		elif type(nodes) in (str, unicode):
			self.nodes = nodes.split(';')
		else:
			self.nodes = nodes
		self.set_value(None)
			
	def on_mouse_click(self, pos):
	
		"""<DOC>
		Is called whenever the user clicks on the widget. Selects the correct #
		value from the scale and optionally closes the form.
		
		Arguments:
		pos -- An (x, y) tuple.
		</DOC>"""		
	
	
		x, y = pos
		i = 0
		for _x, _y in self.pos_list:
			if x >= _x and x <= _x+self.box_size and y >= _y and y <= \
				_y+self.box_size:
				self.set_value(i)
				if self.click_accepts:												
					return i			
				break
			i += 1
		
	def render(self):
	
		"""<DOC>
		Draws the widget.
		</DOC>"""	
		
		# Some ugly maths, but basically it evenly spaces the checkboxes and
		# draws a frame around it.
		x, y, w, h = self.rect		
		cy = y+h/2
		_h = self.form.theme_engine.box_size()				
		dx = (1*w-3*_h)/(len(self.nodes)-1)										
		self.form.theme_engine.frame(x, cy-.5*_h, w, 2*_h, style='light')		
		_x = x+_h
		i = 0
		for node in self.nodes:
			self.form.theme_engine.box(_x, cy, checked=(self.value == i))
			text_height = self.form.canvas.text_size(node)[1]
			self.form.canvas.text(node, center=True, x=_x+self.box_size/2, \
				y=cy-text_height)						
			self.pos_list.append( (_x, cy) )
			_x += dx
			i += 1
			
	def set_value(self, val):
	
		"""<DOC>
		Sets the rating scale value.
		
		Arguments:
		val -- The value.
		</DOC>"""
		
		self.value = val
		self.set_var(val)
