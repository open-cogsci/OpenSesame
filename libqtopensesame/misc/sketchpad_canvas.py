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
		self.grid = 32
		super(sketchpad_canvas, self).__init__(self.sketchpad.main_window)
		self.indicator = None

	def dragLeaveEvent(self, e):

		"""
		desc:
			Accepts drops to implement moving items.

		arguments:
			e:		A QGraphicsSceneDragDropEvent object.
		"""

		cmd = unicode(e.mimeData().text())
		if cmd.startswith(u'move:'):
			l = cmd[5:].split(u',')
			if len(l) != 2:
				e.ignore()
				return
			try:
				sx = int(l[0])
				sy = int(l[1])
			except:
				e.ignore()
				return
			ex, ey = self.cursor_pos(e)
			dx = ex-sx
			dy = ey-sy
			if abs(dx) < self.grid and abs(dy) < self.grid:
				e.ignore()
				return
			self.sketchpad.move_elements(self.sketchpad.selected_elements(),
				dx=dx, dy=dy)
			self.sketchpad.draw()
			e.accept()
		else:
			e.ignore()

	def mouseMoveEvent(self, e):

		"""
		desc:
			Processes mouse-move events, to handle highlighting and cursor-
			position display.

		arguments:
			e:	A QMouseEvent.
		"""

		self.sketchpad.set_cursor_pos(self.cursor_pos(e))
		graphics_item = self.itemAt(e.scenePos())
		for element in self.sketchpad.elements:
			element.highlight(False)
		if graphics_item != None:
			graphics_item.element.highlight()

	def mousePressEvent(self, e):

		"""
		desc:
			Processes mouse-press events, to handle element selection.

		arguments:
			e:	A QMouseEvent.
		"""

		graphics_item = self.itemAt(e.scenePos())
		if not QtCore.Qt.ControlModifier & e.modifiers():
			for element in self.sketchpad.elements:
				element.select(False)
		if graphics_item != None:
			graphics_item.element.select()
			mime_data = QtCore.QMimeData()
			mime_data.setText(u'move:%d,%d' % self.cursor_pos(e))
			drag = QtGui.QDrag(e.widget())
			drag.setMimeData(mime_data)
			drag.start()

	def keyPressEvent(self, e):

		"""
		desc:
			Processes key-press events, to handle deletion, movement, etc.

		arguments:
			e:	A QKeyEvent.
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

	def cursor_pos(self, e):

		"""
		desc:
			Gets the position of the mouse cursor.

		arguments:
			e:	A QMouseEvent.

		returns:
			An (x, y) tuple with the the coordinates of the mouse cursor.
		"""

		pos = e.scenePos().toPoint()
		x = pos.x() + 0.5 * self.grid - self.xcenter()
		y = pos.y() + 0.5 * self.grid - self.ycenter()
		x = x - x % self.grid
		y = y - y % self.grid
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

		if self.is_var(fname):
			self.notify(
				_(u'Image name "%s" is variably defined, using fallback image') \
				% fname)
			return self.sketchpad.theme.qpixmap(u'fallback')
		if not os.path.exists(fname):
			self.notify(
				_(u'Image name "%s" not found, using fallback image') \
				% fname)
			return self.sketchpad.theme.qpixmap(u'fallback')
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
				_(u'Penwidth "%s" is variably defined, using 1') % penwidth)
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
				_(u'Color "%s" is variably defined, using placeholder color') \
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
				_('X coordinate "%s" is variably defined, using display center') \
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
				_('Y coordinate "%s" is variably defined, using display center') \
				% y)
			return self.ycenter()
		return y

	def _w(self, x):

		"""
		desc:
			Safely returns a width.

		returns:
			A width.
		"""

		if type(x) not in (int, float):
			self.notify(_('Width "%s" is variably defined, using 100') % x)
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
			self.notify(_('Height "%s" is variably defined, using 100') % y)
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
			self.notify(_('Scale "%s" is variably defined, using 1.0') % y)
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
		for x in range(xc, w+1, self.grid):
			painter.drawLine(x, 0, x, h)
		for x in range(self.grid, xc, self.grid):
			painter.drawLine(x, 0, x, h)
		for y in range(yc, h+1, self.grid):
			painter.drawLine(0, y, w, y)
		for y in range(self.grid, yc, self.grid):
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

		self._font = QtGui.QFont(style, size, bold, italic)

	def text(self, text, center=True, x=None, y=None, max_width=None,
		color=None, bidi=None, html=True):

		"""Mimicks canvas api. See openexp._canvas.canvas."""

		i = self.addText(text, self._font)
		i.setDefaultTextColor(self._color(color))
		if html:
			i.setHtml(text)
		i.setPos(self._point(i, x, y, center))
		return i

	def line(self, sx, sy, ex, ey, color=None, penwidth=None):

		"""Mimicks canvas api. See openexp._canvas.canvas."""

		i = self.addLine(self._x(sx), self._y(sy), self._x(ex), self._y(ey),
			pen=self._pen(color, penwidth))
		return i

	def arrow(self, sx, sy, ex, ey, arrow_size=5, color=None, penwidth=None):

		"""Mimicks canvas api. See openexp._canvas.canvas."""

		# We use a polygon instead of three separate lines, because a polygon
		# is a single object, which is easier to work with.
		a = math.atan2(ey - sy, ex - sx)
		sx1 = ex + arrow_size * math.cos(a + math.radians(135))
		sy1 = ey + arrow_size * math.sin(a + math.radians(135))
		sx2 = ex + arrow_size * math.cos(a + math.radians(225))
		sy2 = ey + arrow_size * math.sin(a + math.radians(225))
		path = [
			QtCore.QPoint(self._x(sx), self._y(sy)),
			QtCore.QPoint(self._x(ex), self._y(ey)),
			QtCore.QPoint(self._x(sx1), self._y(sy1)),
			QtCore.QPoint(self._x(ex), self._y(ey)),
			QtCore.QPoint(self._x(sx2), self._y(sy2)),
			QtCore.QPoint(self._x(ex), self._y(ey)),
			]
		i = self.addPolygon(QtGui.QPolygonF(path), pen=self._pen(color, penwidth))
		return i

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

	def ellipse(self, x, y, w, h, fill=False, color=None, penwidth=None):

		"""Mimicks canvas api. See openexp._canvas.canvas."""

		color = self._color(color)
		if fill:
			pen = self._pen(color, 1)
			brush = self._brush(color)
		else:
			pen = self._pen(color, penwidth)
			brush = QtGui.QBrush()
		i = self.addEllipse(self._x(x), self._y(y), self._w(w), self._h(h),
			pen=pen, brush=brush)
		return i

	def circle(self, x, y, r, fill=False, color=None, penwidth=None):

		"""Mimicks canvas api. See openexp._canvas.canvas."""

		i = self.ellipse(x-r, y-r, 2*r, 2*r, fill=fill, color=color,
			penwidth=penwidth)
		return i

	def image(self, fname, center=True, x=None, y=None, scale=None):

		"""Mimicks canvas api. See openexp._canvas.canvas."""

		i = self.addPixmap(self._pixmap(fname))
		i.setScale(self._scale(scale))
		i.setPos(self._point(i, x, y, center))
		return i

	def noise_patch(self, x, y, env=u'gaussian', size=96, stdev=12,
		col1=u'white', col2=u'black', bgmode=u'avg'):

		"""Mimicks canvas api. See openexp._canvas.canvas."""

		# TODO
		return self.circle(x, y, 10)

	def gabor(self, x, y, orient, freq, env=u'gaussian', size=96, stdev=12,
		phase=0, col1=u'white', col2=u'black', bgmode=u'avg'):

		"""Mimicks canvas api. See openexp._canvas.canvas."""

		# TODO
		return self.circle(x, y, 10)

	def fixdot(self, x=None, y=None, color=None, style=u'default'):

		"""Mimicks canvas api. See openexp._canvas.canvas."""

		# TODO
		return self.circle(x, y, 10)
