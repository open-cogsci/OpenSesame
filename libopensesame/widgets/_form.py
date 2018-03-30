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
from openexp.keyboard import keyboard
from libopensesame.widgets.widget_factory import WidgetFactory


class Form(object):

	"""
	desc: |
		The `Form` is a container for widgets, such as labels, etc. If you use
		the FORM_BASE plug-in in combination with OpenSesame script, you do not
		need to explicitly create a `Form` object. However, if you use Python
		inline code, you do.

		__Example__:

		~~~ .python
		form = Form()
		label = Label(text='label)
		form.set_widget(label, (0,0))
		form._exec()
		~~~

		[TOC]
	"""

	def __init__(self, experiment, cols=2, rows=2, spacing=10,
		margins=(100, 100, 100, 100), theme=u'gray', item=None, timeout=None,
		clicks=False, validator=None):

		"""
		desc: |
			Constructor to create a new `Form` object. You do not generally
			call this constructor directly, but use the `Form()` factory
			function, which is described here: [/python/common/]().


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
			validator:
				desc:	A function that takes no arguments and returns True if
						the form is successfully validated, and False if not.
				type: 	[FunctionType, NoneType]
		"""

		# Normalize the column and row sizes so that they add up to 1
		if isinstance(cols, int):
			self.cols = [1./cols]*cols
		else:
			cols = type_check.float_list(cols, u'form columns', min_len=1)
			self.cols = [float(c)/sum(cols) for c in cols]
		if isinstance(rows, int):
			self.rows = [1./rows]*rows
		else:
			rows = type_check.float_list(rows, u'form rows', min_len=1)
			self.rows = [float(r)/sum(rows) for r in rows]
		self.experiment = experiment
		self.item = item if item is not None else experiment
		self.timeout = timeout
		self.width = experiment.var.width
		self.height = experiment.var.height
		self.spacing = spacing
		self.clicks = clicks
		self.margins = type_check.float_list(margins, u'form margins',
			min_len=4, max_len=4)
		n_cells = len(self.cols)*len(self.rows)
		self.widgets = [None]*n_cells
		self.span = [(1, 1)]*n_cells
		self._validator = (lambda: True) if validator is None else validator
		self.canvas = canvas(
			self.experiment,
			color=self.item.var.foreground,
			background_color=self.item.var.background
		)
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

		if isinstance(focus_widget, WidgetFactory):
			focus_widget = focus_widget.construct(self)
		if len(self) == 0:
			raise osexception(u'The form contains no widgets')
		ms = mouse(self.experiment, timeout=0)
		ms.show_cursor()
		kb = keyboard(self.experiment, timeout=0)
		kb.show_virtual_keyboard()
		coroutines = {w: w.coroutine() for w in self.widgets if w is not None}
		for coroutine in coroutines.values():
			coroutine.send(None)
		self.canvas.show()
		self.start_time = None
		mousedown = False
		while True:
			if self.timed_out():
				resp = None
				break
			msg = None
			# Handle mouse clicks, including waiting until the mouse is released
			# after a mouse click.
			if mousedown:
				while any(ms.get_pressed()):
					pass
				mousedown = False
			button, xy, timestamp = ms.get_click(visible=True)
			if button is not None:
				mousedown = True
				# Switch the focus to the newly clicked widget (if any)
				widget = self.xy_to_widget(xy)
				if widget is None:
					continue
				if focus_widget is not None:
					focus_widget.focus = False
				widget.focus = True
				focus_widget = widget
				msg = {
					u'type': u'click',
					u'pos': xy,
					u'button': button,
					u'timestamp': timestamp
				}
			# Handle key presses clicks
			elif focus_widget is not None:
				key, timestamp = kb.get_key()
				if key is not None:
					msg = {
						u'type': u'key',
						u'key': key,
						u'timestamp': timestamp
					}
			# Send message (if any)
			if msg is None:
				continue
			resp = coroutines[focus_widget].send(msg)
			self.canvas.show()
			if resp is not None and self._validator():
				break
		kb.show_virtual_keyboard(False)
		ms.show_cursor(False)
		for coroutine in coroutines.values():
			try:
				coroutine.send({u'type' : u'stop'})
			except StopIteration:
				pass
		self.experiment.var.form_response = resp
		return resp

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
							u'The widget at position (%d, %s) falls outside of your form'
							% (l[0], l[1]))
					if self.widgets[index2] is not None:
						raise osexception(
							u'The widget at position (%d, %d) overlaps with another widget'
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
			raise osexception(u'There is not enough space to show some form '
				u'widgets. Please modify the form geometry!')
		x = x1+self.margins[3]
		y = y1+self.margins[0]
		if self.experiment.var.uniform_coordinates == u'yes':
			x -= self.width/2
			y -= self.height/2
		return x, y, w, h

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
			raise osexception(
				u'Widget position (%s, %s) is outside of the form' % pos)
		if not isinstance(colspan, int) or colspan < 1 or colspan > len(self.cols):
			raise osexception(
				u'Column span %s is invalid (i.e. too large, too small, or not a number)'
				% colspan)
		if not isinstance(rowspan, int) or rowspan < 1 or rowspan > len(self.rows):
			raise osexception(
				u'Row span %s is invalid (i.e. too large, too small, or not a number)'
				% rowspan)
		if isinstance(widget, WidgetFactory):
			widget = widget.construct(self)
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

	def xy_to_widget(self, xy):

		index = self.xy_to_index(xy)
		if index is None:
			return None
		return self.widgets[index]


form = Form
