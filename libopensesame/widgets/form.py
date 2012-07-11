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

from libopensesame.exceptions import form_error
from openexp.canvas import canvas
from openexp.mouse import mouse

class form:

	"""Implements a single form that acts as a container for widgets"""

	def __init__(self, experiment, cols=2, rows=2, spacing=10, \
		margins=(100, 100, 100, 100)):
		
		"""<DOC>		
		Constructor
		
		Arguments:
		experiment -- an OpenSesame experiment
		
		Keyword arguments:
		cols -- The number of columns (as int) or a list that specifies the
				number and relative size of the columns. For example, '[1,2,1]'
				will create 3 columns where the middle one is twice as large as
				the outer ones. (default=2)
		rows -- Analogous to 'cols' (default=2)
		spacing -- The amount of empty space between the widgets (default=10)
		margins -- The amount of empty space around the form. This is specified
				   as a list, like so [top-margin, right-margin, bottom-margin,
				   left-margin]. (default=[100, 100, 100, 100])
		</DOC>"""
				
		# Normalize the column and row sizes so that they add up to 1
		if type(cols) == int:
			self.cols = [1./cols]*cols
		else:
			self.cols = [float(c)/sum(cols) for c in cols]
		if type(rows) == int:
			self.rows = [1./rows]*rows			
		else:	
			self.rows = [float(r)/sum(rows) for r in rows]			
	
		self.experiment = experiment
		self.width = experiment.get('width')
		self.height = experiment.get('height')		
		self.spacing = spacing
		self.margins = margins
		n_cells = len(self.cols)*len(self.rows)
		self.widgets = [None]*n_cells
		self.span = [(1,1)]*n_cells	
		self.canvas = canvas(self.experiment)				
		
	def _exec(self, focus_widget=None):
	
		"""<DOC>
		Executes the form
		
		Keyword arguments:
		focus_widget -- a widget that is in the form and should receive a
						virtual mouse click when the form is opened. This allows
						you to activate a text_input right away, for example, so
						that the user doesn't have to click on it anymore.
		
		Returns:
		Gives the return value of the form, which depends on how the user has
		interacted with the widgets. For example, if the user has pressed a
		button, the button text will be returned.
		</DOC>"""
			
		i = 0
		self.mouse = mouse(self.experiment)		
		if focus_widget != None:
			self.render()
			focus_widget.on_mouse_click(None)		
		while True:
			self.render()
			button, xy, time = self.mouse.get_click(visible=True)
			pos = self.xy_to_index(xy)
			if pos != None:
				resp = self.widgets[pos].on_mouse_click(xy)
				if resp != None:
					return resp		
		
	def cell_index(self, pos):
	
		"""<DOC>
		Converts a position to a cell index. A cell index corresponds to the
		number of the cell in the form, from left-to-right, top-to-bottom.
		
		Arguments:
		pos -- a position, which can be an index (int) or a column, row tuple.
		
		Returns:
		A cell index		
		</DOC>"""
	
		if type(pos) == int:
			return pos			
		if type(pos) in (tuple, list) and len(pos) == 2:
			return pos[1]*len(self.cols)+pos[0]
		raise form_error('%s is an invalid position in the form' % pos)
		
	def get_rect(self, index):
	
		"""
		Returns the boundary area for a given cell
		
		Arguments:
		index -- a cell index
		
		Returns:
		A (left, top, width, height) tuple		
		"""
	
		col = index % len(self.cols)
		row = index / len(self.cols)		
		colspan, rowspan = self.span[index]				
		effective_width = self.width-self.margins[1]-self.margins[3]
		effective_height = self.height-self.margins[0]-self.margins[2]		
		x1 = effective_width*sum(self.cols[:col])+self.spacing
		y1 = effective_height*sum(self.rows[:row])+self.spacing		
		x2 = effective_width*sum(self.cols[:col+colspan])-self.spacing
		y2 = effective_height*sum(self.rows[:row+rowspan])-self.spacing		
		w = x2-x1
		h = y2-y1
		return x1+self.margins[3], y1+self.margins[0], w, h
		
	def render(self):
	
		"""<DOC>
		Draws the form and all the widgets in it
		</DOC>"""
	
		self.canvas.clear()
		for widget in self.widgets:
			if widget != None:
				widget.render()
		self.canvas.show()				
				
	def set_widget(self, widget, pos, colspan=1, rowspan=1):
	
		"""<DOC>
		Adds a widget to the form
		
		Arguments:
		widget -- the widget to add
		pos -- the position to add the widget, which can be an index or a
			   (column, row) tuple			   
		
		Keyword arguments:
		colspan -- the number of columns that the widget should span (default=1)
		rowspan -- the number of rows that the widget should span (default=1)		
		</DOC>"""
	
		index = self.cell_index(pos)
		self.widgets[index] = widget
		self.span[index] = colspan, rowspan		
		widget.set_rect(self.get_rect(index))		
		
	def xy_to_index(self, xy):
	
		"""<DOC>
		Converts a coordinate in pixels to a cell index. This allows you to
		determine on which widget a user has clicked.
		
		Arguments:
		xy -- an (x,y) tuple
		
		Returns:
		A cell index
		</DOC>"""
	
		for index in range(len(self.widgets)):
			x, y, w, h = self.get_rect(index)
			if x <= xy[0] and x+w >= xy[0] and y <= xy[1] and y+h >= xy[1]:
				return index
		return None			
		

			
