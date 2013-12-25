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

from libopensesame.exceptions import osexception
from libopensesame import debug
from widget import widget

class rating_scale(widget):

	"""A simple rating scale/ Likert widget"""

	def __init__(self, form, nodes=5, click_accepts=False, orientation=u'horizontal', var=None, default=None):
	
		"""<DOC>
		Constructor.
		
		Arguments:
		form			--	The parent form.
		
		Keyword arguments:
		nodes			--	The number of nodes or a list of node identifiers (e.g., #
							['yes', 'no', 'maybe']. If a list is passed the rating scale #
							will have labels, otherwise it will just have boxes #
							(default=5).
		click_accepts	--	Indicates whether the form should close when a value #
							is selected (default=False).
		orientation		--	'horizontal' indicates a horizontally oriented
							rating scale, 'vertical' indicates a vertically
							oriented rating scale. (default=u'horizontal')
		var				--	The name of the experimental variable that should be used to log #
							the widget status. The value that is logged is the number of #
							the node that was selected, with the first node being 0. If no #
							nodes were selected, the value is 'None'. For more information #
							about the use of response variables in forms, see the form #
							documentation page.(default=None).
		default			--	The node that is selected by default, or None to #
							select no node. The value corresponds to the node #
							number, where 0 is the first node. (default=None)
		</DOC>"""	
		
		if isinstance(click_accepts, basestring):
			click_accepts = click_accepts == u'yes'
		
		widget.__init__(self, form)
		self.type = u'rating_scale'
		self.box_size = 16
		self.click_accepts = click_accepts
		self.pos_list = []
		self.var = var
		self.orientation = orientation
		if type(nodes) == int:
			self.nodes = [u'']*nodes
		elif isinstance(nodes, basestring):
			self.nodes = nodes.split(u';')
		else:
			self.nodes = nodes
		self.set_value(default)
			
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

		x, y, w, h = self.rect
		cx = x+w/2
		cy = y+h/2		
		_h = self.form.theme_engine.box_size()		
		if self.orientation == u'horizontal':
			# Some ugly maths, but basically it evenly spaces the checkboxes and
			# draws a frame around it.
			dx = (1*w-3*_h)/(len(self.nodes)-1)
			self.form.theme_engine.frame(x, cy-.5*_h, w, 2*_h, style=u'light')
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
		elif self.orientation == u'vertical':
			dy = (1*h-3*_h)/(len(self.nodes)-1)
			self.form.theme_engine.frame(cx-.5*_h, y, 2*_h, h, style=u'light')
			_y = y+_h
			i = 0
			for node in self.nodes:
				self.form.theme_engine.box(cx, _y, checked=(self.value == i))
				text_width = self.form.canvas.text_size(node)[0]
				self.form.canvas.text(node, center=True, x=cx-text_width,
					y=_y+self.box_size/2)
				self.pos_list.append( (cx, _y) )
				_y += dy
				i += 1
		else:
			raise osexception( \
				u'rating_scale orientation must be "horizontal" or "vertical", not "%s"' % \
				self.orientation)
			
	def set_value(self, val):
	
		"""<DOC>
		Sets the rating scale value.
		
		Arguments:
		val -- The value.
		</DOC>"""
		
		if val != None and (val >= len(self.nodes) or val < 0):
			raise osexception( \
				u'Trying to select a non-existing node (%s). Did you specify an incorrect default value?' \
				% val)
		self.value = val
		self.set_var(val)
