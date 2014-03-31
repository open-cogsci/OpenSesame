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

from libopensesame import type_check
from libopensesame.exceptions import osexception
from openexp.canvas import canvas
from openexp.mouse import mouse

class form:

	"""Implements a single form that acts as a container for widgets"""

	def __init__(self, experiment, cols=2, rows=2, spacing=10, margins=(100, 100, 100, 100), theme=u'gray', item=None):

		"""<DOC>
		Constructor

		Arguments:
		experiment -- An OpenSesame experiment.

		Keyword arguments:
		cols -- The number of columns (as int) or a list that specifies the #
				number and relative size of the columns. For example, '[1,2,1]' #
				will create 3 columns where the middle one is twice as large as #
				the outer ones (default=2).
		rows -- Analogous to 'cols' (default=2).
		spacing -- The amount of empty space between the widgets (default=10).
		margins -- The amount of empty space around the form. This is specified #
				   as a list, like so [top-margin, right-margin, bottom-margin, #
				   left-margin] (default=[100, 100, 100, 100]).
		theme -- The theme for the widgets (default='gray').
		item -- The item of which the form is part (default=None).
		</DOC>"""

		# Normalize the column and row sizes so that they add up to 1
		if type(cols) == int:
			self.cols = [1./cols]*cols
		else:
			cols = type_check.float_list(cols, u'form columns', min_len=1)
			self.cols = [float(c)/sum(cols) for c in cols]
		if type(rows) == int:
			self.rows = [1./rows]*rows
		else:
			rows = type_check.float_list(rows, u'form rows', min_len=1)
			self.rows = [float(r)/sum(rows) for r in rows]

		self.experiment = experiment
		if item != None:
			self.item = item
		else:
			self.item = experiment
		self.width = experiment.get(u'width')
		self.height = experiment.get(u'height')
		self.spacing = spacing
		self.margins = type_check.float_list(margins, u'form margins', \
			min_len=4, max_len=4)
		n_cells = len(self.cols)*len(self.rows)
		self.widgets = [None]*n_cells
		self.span = [(1,1)]*n_cells
		self.canvas = canvas(self.experiment, auto_prepare=False, fgcolor= \
			self.item.get(u'foreground'), bgcolor=self.item.get( \
			u'background'))

		if theme == u'gray':
			from themes.gray import gray
			self.theme_engine = gray(self)
		else:
			from themes.plain import plain
			self.theme_engine = plain(self)

	def _exec(self, focus_widget=None):

		"""<DOC>
		Executes the form.

		Keyword arguments:
		focus_widget -- A widget that is in the form and should receive a #
						virtual mouse click when the form is opened. This allows #
						you to activate a text_input right away, for example, so #
						that the user doesn't have to click on it anymore.

		Returns:
		Gives the return value of the form, which depends on how the user has #
		interacted with the widgets. For example, if the user has pressed a #
		button, the button text will be returned.
		</DOC>"""

		i = 0
		self.mouse = mouse(self.experiment)
		if focus_widget != None:
			self.render()
			resp = focus_widget.on_mouse_click(None)
			if resp != None:
				return
		while True:
			self.render()
			button, xy, time = self.mouse.get_click(visible=True)
			pos = self.xy_to_index(xy)
			if pos != None:
				w = self.widgets[pos]
				if w != None:
					resp = self.widgets[pos].on_mouse_click(xy)
					if resp != None:
						return resp

	def cell_index(self, pos):

		"""<DOC>
		Converts a position to a cell index. A cell index corresponds to the #
		number of the cell in the form, from left-to-right, top-to-bottom.

		Arguments:
		pos -- A position, which can be an index (int) or a column, row tuple.

		Returns:
		A cell index
		</DOC>"""

		if type(pos) == int:
			return pos
		if type(pos) in (tuple, list) and len(pos) == 2:
			return pos[1]*len(self.cols)+pos[0]
		raise osexception(u'%s is an invalid position in the form' % pos)

	def validate_geometry(self):

		"""
		Checks whether the form has a valid geometry.

		Exceptions:
		osexception		--	When the geometry is invalid.
		"""

		for index1 in range(len(self.widgets)):
			if self.widgets[index1] == None:
				continue
			l = self.get_cell(index1)
			colspan, rowspan = self.span[index1]
			for col in range(l[0], l[0]+colspan):
				for row in range(l[1], l[1]+rowspan):
					index2 = self.cell_index((col, row))
					if index1 == index2:
						continue
					print '%s, %s (%s)' % (col, row, index2)
					if len(self.widgets) <= index2:
						raise osexception( \
							u'One or more widgets fall outside of your form')
					if self.widgets[index2] != None:
						raise osexception( \
							u'Two or more widgets in your form are overlapping')

	def get_cell(self, index):

		"""
		Returns the position of a widget

		Arguments:
		index -- the index of the widget

		Returns:
		A (column, row, column_span, row_span) tuple
		"""

		index = self.cell_index(index)
		col = index % len(self.cols)
		row = index / len(self.cols)
		colspan, rowspan = self.span[index]
		return col, row, colspan, rowspan

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
		if w <= 0 or h <= 0:
			raise osexception( \
				u'There is not enough space to show some form widgets. Please modify the form geometry!')
		return x1+self.margins[3], y1+self.margins[0], w, h

	def render(self):

		"""<DOC>
		Draws the form and all the widgets in it.
		</DOC>"""

		self.validate_geometry()
		self.canvas.clear()
		for widget in self.widgets:
			if widget != None:
				widget.render()
		self.canvas.show()

	def set_widget(self, widget, pos, colspan=1, rowspan=1):

		"""<DOC>
		Adds a widget to the form.

		Arguments:
		widget -- The widget to add.
		pos -- The position to add the widget, which can be an index or a
			   (column, row) tuple.

		Keyword arguments:
		colspan -- The number of columns that the widget should span (default=1).
		rowspan -- The number of rows that the widget should span (default=1).
		</DOC>"""

		index = self.cell_index(pos)
		if index >= len(self.widgets):
			raise osexception( \
				u'Widget position (%s, %s) is outside of the form' % pos)
		if type(colspan) != int or colspan < 1 or colspan > len(self.cols):
			raise osexception( \
				u'Column span %s is invalid (i.e. too large, too small, or not a number)' \
				% colspan)
		if type(rowspan) != int or rowspan < 1 or rowspan > len(self.rows):
			raise osexception( \
				u'Row span %s is invalid (i.e. too large, too small, or not a number)' \
				% rowspan)
		self.widgets[index] = widget
		self.span[index] = colspan, rowspan
		widget.set_rect(self.get_rect(index))

	def xy_to_index(self, xy):

		"""<DOC>
		Converts a coordinate in pixels to a cell index. This allows you to #
		determine on which widget a user has clicked.

		Arguments:
		xy -- An (x,y) tuple.

		Returns:
		A cell index.
		</DOC>"""

		for index in range(len(self.widgets)):
			x, y, w, h = self.get_rect(index)
			if x <= xy[0] and x+w >= xy[0] and y <= xy[1] and y+h >= xy[1]:
				return index
		return None
