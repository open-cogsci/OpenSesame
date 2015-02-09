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

import os
import math
from libqtopensesame.misc import drag_and_drop
from libqtopensesame.misc import _
from libqtopensesame.misc.config import cfg
from PyQt4 import QtGui, QtCore

class sketchpad_canvas(QtGui.QGraphicsScene):

	"""
	desc:
		A partial implementation of a canvas, so that sketchpad elements can
		draw to the canvas just as in runtime.
	"""

	def __init__(self, sketchpad):

		"""
		desc:
			constructor.

		arguments:
			sketchpad:	A sketchpad object.
		"""

		self.sketchpad = sketchpad
		self.placeholder_color = cfg.sketchpad_placeholder_color
		self.grid = 32
		super(sketchpad_canvas, self).__init__(self.sketchpad.main_window)
		self.indicator = None

	@property
	def selected_element_tool(self):

		return self.sketchpad.sketchpad_widget.selected_element_tool

	def dragMoveEvent(self, e):

		"""
		desc:
			Accepts drag-moves to implement moving items.

		arguments:
			e:
				type:	QGraphicsSceneDragDropEvent
		"""

		data = drag_and_drop.receive(e)
		if data[u'type'] != u'sketchpad-element-move':
			e.ignore()
			return
		ex, ey = self.cursor_pos(e, grid=True)
		dx = ex-self.start_move_pos[0]
		dy = ey-self.start_move_pos[1]
		self.start_move_pos = ex, ey
		if abs(dx) < self.grid and abs(dy) < self.grid:
			e.accept()
			return
		self.sketchpad.move_elements(self.sketchpad.selected_elements(),
			dx=dx, dy=dy)
		self.sketchpad.draw()
		e.accept()

	def wheelEvent(self, e):

		"""
		desc:
			Scrolls the graphics view based on a wheel event (i.e. mouse-scroll
			event.

		arguments:
			e:
				type:	QGraphicsViewWheelEvent
		"""

		if not QtCore.Qt.ControlModifier & e.modifiers():
			return
		self.sketchpad.zoom_diff(e.delta())

	def mouseDoubleClickEvent(self, e):

		"""
		desc:
			Processes mouse-press events, to handle element selection.

		arguments:
			e:
				type:	QGraphicsSceneMouseEvent
		"""

		if not QtCore.Qt.LeftButton & e.button():
			# Only accept right clicks
			return
		# Select the pointed-at element
		element = self.element_at(e.scenePos())
		if element == None:
			return
		element.show_edit_dialog()

	def mousePressEvent(self, e):

		"""
		desc:
			Processes mouse-press events. Mouse presses can have a number of
			effects.

			- All selected elements are deselected unless Control is pressed
			- Left clicks:
				- If the pointer tool is selected, clicking an element selects
				  it.
				- If an element tool is selected, clicking gives the element
				  tool the opporunity (to start a) drawing operation.
			- Right clicks:
				- If an element is selected, a context menu is shown.

		arguments:
			e:
				type:	QMouseEvent
		"""

		# When control is not pressed, we deselect all currently selected
		# elements first
		if not QtCore.Qt.ControlModifier & e.modifiers():
			for element in self.sketchpad.elements:
				element.select(False)
		element = self.element_at(e.scenePos())
		if QtCore.Qt.RightButton & e.button() and element != None:
			# The right buttons pops up a context menu.
			element.show_context_menu(e.screenPos())
		if QtCore.Qt.LeftButton & e.button():
			# The left button selects and drags.
			if self.selected_element_tool != None:
				# When in pointer-tool mode, mouse clicks create new elements.
				self.sketchpad.add_element(
					self.selected_element_tool.mouse_press(self.sketchpad,
					self.cursor_pos(e)))
			elif element == None:
				self.sketchpad.select_pointer_tool()
			else:
				element.select()
				self.sketchpad.show_element_settings(element)
				x, y = self.cursor_pos(e, grid=False)
				self.start_move_pos = x, y
				data = {
					u'type'		: u'sketchpad-element-move',
					u'from_x'	: x,
					u'from_y'	: y
					}
				drag_and_drop.send(e.widget(), data)

	def mouseReleaseEvent(self, e):

		"""
		desc:
			Mouse-release events give elements the opportunity to finish a
			drawing operation.

		arguments:
			e:
				type:	QMouseEvent
		"""

		if self.selected_element_tool != None:
			self.sketchpad.add_element(
				self.selected_element_tool.mouse_release(self.sketchpad,
				self.cursor_pos(e)))

	def mouseMoveEvent(self, e):

		"""
		desc:
			Processes mouse-move events, to handle highlighting and cursor-
			position display.

		arguments:
			e:
				type:	QMouseEvent
		"""

		cursor_pos = self.cursor_pos(e)
		self.sketchpad.set_cursor_pos(cursor_pos)
		for element in self.sketchpad.elements:
			element.highlight(False)
		# Only highlight elements if the pointer tool is selected
		if self.selected_element_tool == None:
			element = self.element_at(e.scenePos())
			if element != None:
				element.highlight()
		else:
			self.selected_element_tool.mouse_move(self.sketchpad, cursor_pos)

	def keyPressEvent(self, e):

		"""
		desc:
			Processes key-press events, to handle deletion, movement, etc.

		arguments:
			e:
				type:	QKeyEvent
		"""

		if e.key() == QtCore.Qt.Key_Delete:
			self.sketchpad.remove_elements(self.sketchpad.selected_elements())
		elif e.key() == QtCore.Qt.Key_Up:
			self.sketchpad.move_elements(self.sketchpad.selected_elements(),
				dy=-self.grid)
		elif e.key() == QtCore.Qt.Key_Down:
			self.sketchpad.move_elements(self.sketchpad.selected_elements(),
				dy=self.grid)
		elif e.key() == QtCore.Qt.Key_Left:
			self.sketchpad.move_elements(self.sketchpad.selected_elements(),
				dx=-self.grid)
		elif e.key() == QtCore.Qt.Key_Right:
			self.sketchpad.move_elements(self.sketchpad.selected_elements(),
				dx=self.grid)
		else:
			super(sketchpad_canvas, self).keyPressEvent(e)
			return
		self.sketchpad.draw()

	def element_at(self, pos):

		"""
		desc:
			Gets the element at a specific position.

		arguments:
			pos:	An (x,y) tuple.

		returns:
			A sketchpad element (base_element) or None of no element was at pos.
		"""

		# First try to see if there's an exact position match ...
		graphics_item = self.itemAt(pos)
		# ... if not, try if there's an element that encompasses the position.
		if graphics_item == None:
			for item in self.items():
				if item.boundingRect().contains(pos):
					graphics_item = item
		# ... else don't find an element.
		if graphics_item == None:
			return None
		# If the item is part of a group, we want the group, not the invdividual
		# item, because the group has the element property.
		if graphics_item.group() != None:
			graphics_item = graphics_item.group()
		return graphics_item.element

	def cursor_pos(self, e, grid=True):

		"""
		desc:
			Gets the position of the mouse cursor.

		arguments:
			e:
				type:	QMouseEvent

		keywords:
			grid:
				desc:	Indicates whether the cursor should be locked to the
						grid.
				type:	bool

		returns:
			An (x, y) tuple with the the coordinates of the mouse cursor.
		"""

		pos = e.scenePos().toPoint()
		if grid:
			x = pos.x() + 0.5 * self.grid - self.xcenter()
			y = pos.y() + 0.5 * self.grid - self.ycenter()
			x = x - x % self.grid
			y = y - y % self.grid
		else:
			x = pos.x() - self.xcenter()
			y = pos.y() - self.ycenter()
		return x, y

	def notify(self, msg):

		"""
		desc:
			Adds a notification message.
		"""

		self.notifications.append(msg)

	def is_var(self, val):

		"""
		desc:
			Determines whether a value is a string containing variable
			references (i.e. "[my_var]").

		arguments:
			val:	A value.

		returns:
			True if val contains variable references, False otherwise.
		"""

		if not isinstance(val, basestring):
			return False
		return len(self.sketchpad.get_refs(val)) > 0

	def _pixmap(self, fname):

		"""
		desc:
			Safely returns a QPixmap.

		returns:
			A QPixmap object.
		"""

		if not os.path.exists(fname):
			self.notify(
				_(u'Image name "%s" is unknown or variably defined, using fallback image') \
				% fname)
			return self.sketchpad.theme.qpixmap(u'os-image-fallback')
		return QtGui.QPixmap(fname)

	def _pen(self, color, penwidth, alpha=255):

		color = self._color(color)
		color.setAlpha(alpha)
		p = QtGui.QPen(color)
		p.setWidth(self._penwidth(penwidth))
		return p

	def _brush(self, color):

		"""
		desc:
			Safely returns a QBrush.

		returns:
			A QBrush object.
		"""

		return QtGui.QBrush(self._color(color))

	def _penwidth(self, penwidth):

		"""
		desc:
			Safely returns a penwidth.

		returns:
			An int penwidth.
		"""

		if type(penwidth) not in (int, float):
			self.notify(
				_(u'Penwidth "%s" is unknown or variably defined, using 1') % penwidth)
			return 1
		return penwidth

	def _point(self, i, x, y, center):

		"""
		desc:
			Safely returns a QPoint.

		arguments:
			i:		A QGraphicsItem.
			x:		An X coordinate.
			y:		A Y coordinate.
			center:	A boolean indicating whether the point should reflect the
					center of i (True), or the top-left (False).

		returns:
			A QPoint object.
		"""

		x = self._x(x)
		y = self._y(y)
		if center:
			r = i.boundingRect()
			x -= r.width()/2
			y -= r.height()/2
		return QtCore.QPoint(x, y)

	def _color(self, color):

		"""
		desc:
			Safely returns a QColor.

		returns:
			A QColor object.
		"""

		if self.is_var(color):
			self.notify(
				_(u'Color "%s" is unknown or variably defined, using placeholder color') \
				% color)
			return QtGui.QColor(self.placeholder_color)
		return QtGui.QColor(color)

	def _x(self, x):

		"""
		desc:
			Safely returns an X coordinate.

		returns:
			An X coordinate.
		"""

		if type(x) not in (int, float):
			self.notify(
				_('X coordinate "%s" is unknown or variably defined, using display center') \
				% x)
			return self.xcenter()
		return x

	def _y(self, y):

		"""
		desc:
			Safely returns a Y coordinate.

		returns:
			A Y coordinate.
		"""

		if type(y) not in (int, float):
			self.notify(
				_('Y coordinate "%s" is unknown or variably defined, using display center') \
				% y)
			return self.ycenter()
		return y

	def _r(self, r):

		"""
		desc:
			Safely returns a radius

		returns:
			A radius.
		"""

		if type(r) not in (int, float):
			self.notify(
				_('Radius "%s" is unknown or variably defined, using 50') % r)
			return 50
		return r

	def _w(self, x):

		"""
		desc:
			Safely returns a width.

		returns:
			A width.
		"""

		if type(x) not in (int, float):
			self.notify(_('Width "%s" is unknown or variably defined, using 100') % x)
			return 100
		return x

	def _h(self, y):

		"""
		desc:
			Safely returns a height.

		returns:
			A height.
		"""

		if type(y) not in (int, float):
			self.notify(_('Height "%s" is unknown or variably defined, using 100') % y)
			return 100
		return y

	def _scale(self, scale):

		"""
		desc:
			Safely returns a scale.

		returns:
			A scale.
		"""

		if type(scale) not in (int, float):
			self.notify(_('Scale "%s" is unknown or variably defined, using 1.0') % scale)
			return 1.0
		return scale

	def drawBackground(self, painter, rect):

		"""
		desc:
			Draws the background and the grid.

		argumens:
			painter:	A QPainter object.
			rect:		A QRect object.
		"""

		xc = self.xcenter()
		yc = self.ycenter()
		w = 2*xc
		h = 2*yc
		painter.fillRect(QtCore.QRect(0, 0, w, h), self._color(self.bgcolor))
		painter.setPen(self._pen(cfg.sketchpad_grid_color,
			cfg.sketchpad_grid_thickness_thin, cfg.sketchpad_grid_opacity))
		painter.drawRect(QtCore.QRect(0, 0, w, h))
		# Draw all lines except for the center ones, because they should be
		# thicker
		if self.grid > 1:
			for x in range(xc, w+1, self.grid):
				painter.drawLine(x, 0, x, h)
			for x in range(xc-self.grid, -1, -self.grid):
				painter.drawLine(x, 0, x, h)
			for y in range(yc, h+1, self.grid):
				painter.drawLine(0, y, w, y)
			for y in range(yc-self.grid, -1, -self.grid):
				painter.drawLine(0, y, w, y)
		# Draw thicker central lines
		painter.setPen(self._pen(cfg.sketchpad_grid_color,
			cfg.sketchpad_grid_thickness_thick, cfg.sketchpad_grid_opacity))
		painter.drawLine(0, yc, w, yc)
		painter.drawLine(xc, 0, xc, h)

	def clear(self):

		"""Mimicks canvas api. See openexp._canvas.canvas."""

		super(sketchpad_canvas, self).clear()
		self.notifications = []
		self.elements = []
		self.set_bgcolor(self.sketchpad.get(u'background'))

	def xcenter(self):

		"""Mimicks canvas api. See openexp._canvas.canvas."""

		return self.sketchpad.get(u'width')/2

	def ycenter(self):

		"""Mimicks canvas api. See openexp._canvas.canvas."""

		return self.sketchpad.get(u'height')/2


	def set_bgcolor(self, color):

		"""Mimicks canvas api. See openexp._canvas.canvas."""

		self.bgcolor = color

	def set_font(self, style=None, size=None, italic=None, bold=None,
		underline=None):

		"""Mimicks canvas api. See openexp._canvas.canvas."""

		if bold:
			weight = QtGui.QFont.Bold
		else:
			weight = QtGui.QFont.Normal
		self._font = QtGui.QFont(style, weight=weight, italic=italic)
		self._font.setPixelSize(size)

	def text(self, text, center=True, x=None, y=None, max_width=None,
		color=None, bidi=None, html=True):

		"""Mimicks canvas api. See openexp._canvas.canvas."""

		i = self.addText(unicode(text), self._font)
		i.setDefaultTextColor(self._color(color))
		if html:
			i.setHtml(unicode(text))
		if center:
			# Source:
			# http://www.cesarbs.org/blog/2011/05/30/aligning-text-in-\
			# qgraphicstextitem/
			i.setTextWidth(i.boundingRect().width())
			fmt = QtGui.QTextBlockFormat()
			fmt.setAlignment(QtCore.Qt.AlignCenter)
			cursor = i.textCursor()
			cursor.mergeBlockFormat(fmt)
			i.setTextCursor(cursor)
		i.setPos(self._point(i, x, y, center))
		return i

	def line(self, sx, sy, ex, ey, color=None, penwidth=None, add=True):

		"""Mimicks canvas api. See openexp._canvas.canvas."""

		i = QtGui.QGraphicsLineItem(self._x(sx), self._y(sy), self._x(ex),
			self._y(ey))
		i.setPen(self._pen(color, penwidth))
		if add:
			self.addItem(i)
		return i

	def arrow(self, sx, sy, ex, ey, arrow_size=5, color=None, penwidth=None):

		"""Mimicks canvas api. See openexp._canvas.canvas."""

		a = math.atan2(ey - sy, ex - sx)
		sx1 = ex + arrow_size * math.cos(a + math.radians(135))
		sy1 = ey + arrow_size * math.sin(a + math.radians(135))
		sx2 = ex + arrow_size * math.cos(a + math.radians(225))
		sy2 = ey + arrow_size * math.sin(a + math.radians(225))
		group = QtGui.QGraphicsItemGroup()
		i = self.line(sx, sy, ex, ey, color=color, penwidth=penwidth,
			add=False)
		group.addToGroup(i)
		i = self.line(sx1, sy1, ex, ey, color=color, penwidth=penwidth,
			add=False)
		group.addToGroup(i)
		i = self.line(sx2, sy2, ex, ey, color=color, penwidth=penwidth,
			add=False)
		group.addToGroup(i)
		self.addItem(group)
		return group

	def rect(self, x, y, w, h, fill=False, color=None, penwidth=None):

		"""Mimicks canvas api. See openexp._canvas.canvas."""

		color = self._color(color)
		if fill:
			pen = self._pen(color, 1)
			brush = self._brush(color)
		else:
			pen = self._pen(color, penwidth)
			brush = QtGui.QBrush()
		i = self.addRect(self._x(x), self._y(y), self._w(w), self._h(h),
			pen=pen, brush=brush)
		return i

	def ellipse(self, x, y, w, h, fill=False, color=None, penwidth=None,
		add=True):

		"""Mimicks canvas api. See openexp._canvas.canvas."""

		color = self._color(color)
		if fill:
			pen = self._pen(color, 1)
			brush = self._brush(color)
		else:
			pen = self._pen(color, penwidth)
			brush = QtGui.QBrush()
		i = QtGui.QGraphicsEllipseItem(self._x(x), self._y(y), self._w(w),
			self._h(h))
		i.setPen(pen)
		i.setBrush(brush)
		if add:
			self.addItem(i)
		return i

	def circle(self, x, y, r, fill=False, color=None, penwidth=None):

		"""Mimicks canvas api. See openexp._canvas.canvas."""

		r = self._r(r)
		x = self._x(x) - r
		y = self._y(y) - r
		i = self.ellipse(x, y, 2*r, 2*r, fill=fill, color=color,
			penwidth=penwidth)
		return i

	def image(self, image, center=True, x=None, y=None, scale=None):

		"""Mimicks canvas api. See openexp._canvas.canvas."""

		if not isinstance(image, QtGui.QPixmap):
			image = self._pixmap(image)
		i = self.addPixmap(image)
		i.setScale(self._scale(scale))
		i.setPos(self._point(i, x, y, center))
		return i

	def gabor(self, x, y, *arglist, **kwdict):

		"""Mimicks canvas api. See openexp._canvas.canvas."""

		from openexp.canvas import gabor_file
		try:
			image = gabor_file(*arglist, **kwdict)
		except:
			self.notify(
				_(u'Some properties of a Gabor patch are unknown or variably defined, using fallback image'))
			image = self.sketchpad.theme.qpixmap(u'os-image-fallback')
		return self.image(image, x=x, y=y, scale=1)

	def noise_patch(self, x, y, *arglist, **kwdict):

		"""Mimicks canvas api. See openexp._canvas.canvas."""

		from openexp.canvas import noise_file
		try:
			image = noise_file(*arglist, **kwdict)
		except:
			self.notify(
				_(u'Some properties of a noise patch are unknown or variably defined, using fallback image'))
			image = self.sketchpad.theme.qpixmap(u'os-image-fallback')
		return self.image(image, x=x, y=y, scale=1)

	def fixdot(self, x=None, y=None, color=None, style=u'default'):

		"""Mimicks canvas api. See openexp._canvas.canvas."""

		color = self._color(color)
		x = self._x(x)
		y = self._y(y)
		group = QtGui.QGraphicsItemGroup()
		h = 2
		if style == u'default':
			style = u'open-medium'
		if u'large' in style:
			s = 16
		elif u'medium' in style:
			s = 8
		elif u'small' in style:
			s = 4
		else:
			raise osexception(u'Unknown fixdot style: %s' % self.style)
		if u'open' in style:
			i = self.ellipse(x-s, y-s, 2*s, 2*s, fill=True, color=color,
				add=False)
			group.addToGroup(i)
			i = self.ellipse(x-h, y-h, 2*h, 2*h, fill=True,
				color=self.bgcolor, add=False)
			group.addToGroup(i)
		elif u'filled' in style:
			i = self.ellipse(x-s, y-s, 2*s, 2*s, fill=True, color=color,
				add=True)
			group.addToGroup(i)
		elif u'cross' in style:
			i = self.line(x, y-s, x, y+s, color=color, add=False, penwidth=1)
			group.addToGroup(i)
			i = self.line(x-s, y, x+s, y, color=color, add=False, penwidth=1)
			group.addToGroup(i)
		else:
			raise osexception(u'Unknown fixdot style: %s' % self.style)
		self.addItem(group)
		return group
