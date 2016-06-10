#-*- coding:utf-8 -*-

"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""

from libopensesame.py3compat import *

from libopensesame import type_check
from libopensesame.exceptions import osexception
from openexp.canvas import canvas
from openexp.mouse import mouse

class form(object):

	"""
	desc: |
		The `form` is a container for widgets, such as labels, etc. If you use the
		FORM_BASE plug-in in combination with OpenSesame script, you do not need
		to explicitly create a form. However, if you use Python inline code, you
		do.

		__Example__:

		~~~ .python
		from libopensesame import widgets
		form = widgets.form(exp)
		label = widgets.label(form, text='label)
		form.set_widget(label, (0,0))
		form._exec()
		~~~

		[TOC]
	"""

	def __init__(self, experiment, cols=2, rows=2, spacing=10,
		margins=(100, 100, 100, 100), theme=u'gray', item=None, timeout=None,
		clicks=False):

		"""
		desc:
			Constructor.

		arguments:
			experiment:
				desc:	An OpenSesame experiment.
				type:	experiment

		keywords:
			cols:
				desc:	The number of columns (as int) or a list that specifies
						the number and relative size of the columns. For
						example, `[1,2,1]` will create 3 columns where the
						middle one is twice as large as the outer ones.
				type:	[int, list]
			rows:
				desc:	Analogous to `cols`, but for the rows.
				type:	[int, list]
			spacing:
				desc:	The amount of empty space between widgets (in pixels).
				type:	int
			margins:
				desc:	The amount of empty space around the form. This is
						specified as a list, like so [top-margin, right-margin,
						bottom-margin, left-margin].
				type:	list
			theme:
				desc:	The theme for the widgets.
				type:	[str, unicode]
			item:
				desc:	The item of which the form is part.
				type:	[item, NoneType]
			timeout:
				desc:	A timeout value in milliseconds, or None if no timeout
						exists.
				type:	[int, float, NoneType]
			clicks:
				desc:	If enabled, an auditory click is played on user
						interactions. This can help to make interactions feel
						smoother if there is some visual lag.
				type:	bool
		"""

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
		if item is not None:
			self.item = item
		else:
			self.item = experiment
		self.timeout = timeout
		self.width = experiment.var.width
		self.height = experiment.var.height
		self.spacing = spacing
		self.clicks = clicks
		self.margins = type_check.float_list(margins, u'form margins',
			min_len=4, max_len=4)
		n_cells = len(self.cols)*len(self.rows)
		self.widgets = [None]*n_cells
		self.span = [(1,1)]*n_cells
		self.canvas = canvas(self.experiment, auto_prepare=False,
			color=self.item.var.foreground,
			background_color=self.item.var.background)
		# Dynamically load the theme object
		theme_mod = __import__(
			u'libopensesame.widgets.themes.%s' % theme, fromlist=[u'dummy'])
		theme_cls = getattr(theme_mod, theme)
		self.theme_engine = theme_cls(self)

	def __len__(self):

		"""
		visible: False

		desc:
			Implements the `len()` syntax.

		returns:
			desc:	The number of widgets in the form.
			type:	int
		"""

		return sum([w is not None for w in self.widgets])

	def _exec(self, focus_widget=None):

		"""
		desc:
			Executes the form.

		keywords:
			focus_widget:
				desc:	A widget that is in the form and should receive a
						virtual mouse click when the form is opened. This allows
						you to activate a text_input right away, for example, so
						that the user doesn't have to click on it anymore.
				type:	[widget, NoneType]

		returns:
			desc:	Gives the return value of the form, which depends on how the
					user interacted with the widgets. For example, if the user
					pressed a button, the button text will be returned. If a
					timeout occurred, None will be returned.
		"""

		self.start_time = None
		if len(self) == 0:
			raise osexception(u'The form contains no widgets')
		self.mouse = mouse(self.experiment, timeout=5)
		self.mouse.show_cursor()
		if focus_widget is not None:
			self.render()
			if self.timed_out():
				self.experiment.var.form_response = None
				return None
			resp = focus_widget.on_mouse_click(None)
			if resp is not None:
				return
		while True:
			self.render()
			if self.timed_out():
				self.experiment.var.form_response = None
				return None
			button, xy, time = self.mouse.get_click(visible=True)
			if xy is None:
				continue
			pos = self.xy_to_index(xy)
			if pos is not None:
				w = self.widgets[pos]
				if w is not None:
					resp = self.widgets[pos].on_mouse_click(xy)
					if resp is not None:
						self.experiment.var.form_response = resp
						return resp
		self.mouse.hide_cursor()

	def timed_out(self):

		"""
		visible: False

		returns:
			desc:	True if a timeout occurred, False otherwise.
			type:	bool
		"""

		if self.timeout is None:
			return False
		if self.start_time is None:
			self.start_time = self.item.clock.time()
			return False
		return self.item.clock.time()-self.start_time >= self.timeout

	def cell_index(self, pos):

		"""
		desc:
			Converts a position to a cell index. A cell index corresponds to the
			number of the cell in the form, from left-to-right, top-to-bottom.

		arguments:
			pos:
				desc:	A position in the form, which can be an index (int) or a
						(column, row) tuple.
				type:	[int, tuple]

		returns:
			desc:	A cell index.
			type:	int
		"""

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
			if self.widgets[index1] is None:
				continue
			l = self.get_cell(index1)
			colspan, rowspan = self.span[index1]
			for col in range(l[0], l[0]+colspan):
				for row in range(l[1], l[1]+rowspan):
					index2 = self.cell_index((col, row))
					if index1 == index2:
						continue
					if len(self.widgets) <= index2:
						raise osexception(
							u'The widget at position (%d, %s) falls outside of your form' \
							% (l[0], l[1]))
					if self.widgets[index2] is not None:
						raise osexception(
							u'The widget at position (%d, %d) overlaps with another widget' \
							% (l[0], l[1]))

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
		row = index // len(self.cols)
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
		row = index // len(self.cols)
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
			raise osexception(
				u'There is not enough space to show some form widgets. Please modify the form geometry!')
		x = x1+self.margins[3]
		y = y1+self.margins[0]
		if self.experiment.var.uniform_coordinates == u'yes':
			x -= self.width/2
			y -= self.height/2
		return x, y, w, h

	def render(self):

		"""
		desc:
			Draws the form and all the widgets in it.
		"""

		self.validate_geometry()
		self.canvas.clear()
		for widget in self.widgets:
			if widget is not None:
				widget.render()
		self.canvas.show()

	def set_widget(self, widget, pos, colspan=1, rowspan=1):

		"""
		desc:
			Adds a widget to the form.

		arguments:
			widget:
				desc:	The widget to add.
				type:	widget
			pos:
				desc:	The position to add the widget, which can be an index or
						a (column, row) tuple.
				type:	[int, tuple]

		keywords:
			colspan:
				desc:	The number of columns that the widget should span.
				type:	int
			rowspan:
				desc:	The number of rows that the widget should span.
				type:	int
		"""

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

		"""
		desc:
			Converts a coordinate in pixels to a cell index. This allows you to
			determine on which widget a user has clicked.

		arguments:
			xy:
				desc:	An (x,y) coordinates tuple.
				type:	tuple

		returns:
			desc:	A cell index.
			type:	int
		"""

		for index in range(len(self.widgets)):
			x, y, w, h = self.get_rect(index)
			if x <= xy[0] and x+w >= xy[0] and y <= xy[1] and y+h >= xy[1]:
				return index
		return None
