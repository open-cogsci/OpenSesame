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

__author__ = "Sebastiaan Mathot"
__license__ = "GPLv3"

import math
import os
import numbers
from libopensesame.exceptions import osexception
from libopensesame import debug
from libqtopensesame.ui import sketchpad_widget_ui, gabor_dialog_ui, \
	noise_patch_dialog_ui
from libqtopensesame.widgets import pool_widget
from libqtopensesame.misc import _
import openexp.canvas
from PyQt4 import QtCore, QtGui

class remove_item_button(QtGui.QPushButton):

	"""A button to remove items from the sketchpad"""

	def __init__(self, sketchpad_widget, item):

		"""
		Constructor

		Arguments:
		sketchpad_widget -- the sketchpad widget
		item -- the item of the sketchpad widget
		"""

		self.sketchpad_widget = sketchpad_widget
		self.item = item
		QtGui.QPushButton.__init__(self, \
			self.sketchpad_widget.sketchpad.experiment.icon("delete"), "")
		self.clicked.connect(self.remove_item)
		self.setIconSize(QtCore.QSize(16,16))

	def remove_item(self):

		"""Is called when the remove button is clicked"""

		self.sketchpad_widget.sketchpad.items.remove(self.item)
		self.sketchpad_widget.refresh()

class edit_item_button(QtGui.QPushButton):

	"""A button to edit items in the sketchpad"""

	def __init__(self, sketchpad_widget, item):

		"""
		Constructor

		Arguments:
		sketchpad_widget -- the sketchpad widget
		item -- the item of the sketchpad widget
		"""

		self.sketchpad_widget = sketchpad_widget
		self.item = item
		QtGui.QPushButton.__init__(self, \
			self.sketchpad_widget.sketchpad.experiment.icon("edit"), "")
		self.clicked.connect(self.edit_item)
		self.setIconSize(QtCore.QSize(16,16))

	def edit_item(self):

		"""Is called when the edit button is clicked"""

		self.sketchpad_widget.scene.edit_item( \
			self.sketchpad_widget.sketchpad.fix_coordinates(self.item))
		self.sketchpad_widget.sketchpad.apply_edit_changes()
		self.sketchpad_widget.refresh()

class canvas(QtGui.QGraphicsScene):

	"""The QGraphicsScene on which the sketchpad is drawn"""

	def __init__(self, sketchpad_widget, parent=None):

		"""
		Constructor

		Arguments:
		sketchpad_widget -- the sketchpad_widget of which the canvas is part

		Keyword arguments:
		parent -- the parent QWidget (default=None)
		"""

		self.sketchpad_widget = sketchpad_widget
		self.grid = 10
		self.r = 4
		self.pen = pen = QtGui.QPen()
		self.grid_color = "green"
		self.pen.setColor(QtGui.QColor(self.grid_color))
		self.oneshot = False
		self.from_pos = None
		self.grid_list = []
		QtGui.QGraphicsScene.__init__(self, parent)

	def cursor_pos(self, e):

		"""
		Gets the position of the mouse cursor. This position
		takes into account the reference frame (relative/ absolute)
		and the grid

		Arguments:
		e -- a QMouseEvent

		Returns:
		An (x, y) tuple with the the coordinates of the mouse cursor
		"""

		pos = e.scenePos().toPoint()
		x = pos.x() + 0.5 * self.grid
		y = pos.y() + 0.5 * self.grid

		if self.sketchpad_widget.sketchpad.get("coordinates") == "relative":
			x -= 0.5 * self.sketchpad_widget.sketchpad.get("width")
			y -= 0.5 * self.sketchpad_widget.sketchpad.get("height")

		x = x - x % self.grid
		y = y - y % self.grid

		return x, y

	def mouseMoveEvent(self, e):

		"""
		Update the text widget with the cursor position

		Arguments:
		e -- a QMouseEvent
		"""

		x, y = self.cursor_pos(e)
		if x == None:
			text = "(0, 0)"
		else:
			text = "(%d, %d)" % (x, y)
		self.sketchpad_widget.ui.label_mouse_pos.setText(text)

	def mousePressEvent(self, e):

		"""
		Handle mouse presses to start/ finish drawing
		or present a context menu

		Arguments:
		e -- a QMouseEvent
		"""

		if e.button() == QtCore.Qt.RightButton:
			self.context_menu(e)
		else:
			self.draw(e)

	def draw(self, e):

		"""
		Handle drawing operations

		Arguments:
		e -- a QMouseEvent
		"""

		x, y = self.cursor_pos(e)
		if x == None:
			return

		if self.sketchpad_widget.sketchpad.get("coordinates") == "relative":
			x += 0.5 * self.sketchpad_widget.sketchpad.get("width")
			y += 0.5 * self.sketchpad_widget.sketchpad.get("height")

		if x < 0 or y < 0 or x >= self.sketchpad_widget.sketchpad.get("width") \
			or y >= self.sketchpad_widget.sketchpad.get("height"):
			self.sketchpad_widget.ui.label_mouse_pos.setText( \
				_("(Out of sketchpad)"))
			return

		if self.from_pos == None and not self.oneshot:
			self.addEllipse(x - self.r, y - self.r, 2 * self.r, 2 * self.r, \
				self.pen)
			self.from_pos = x, y
		else:
			pos = self.from_pos
			self.from_pos = None
			self.sketchpad_widget.add(pos, (x, y))

	def context_menu(self, e):

		"""
		Show the context menu

		Arguments:
		e -- a QMouseEvent
		"""

		# First clear the grid, so we don't select the grid items
		for l in self.grid_list:
			self.removeItem(l)
		self.grid_list = []


		# Get the item under the cursor
		item = self.itemAt(e.scenePos())
		if item != None:

			# Get the corresponding item from the sketchpad_widget
			for g, _item in self.sketchpad_widget.item_list:
				if g == item:

					# Draw a highlight box
					brush = QtGui.QBrush()
					brush.setColor(QtGui.QColor(self.grid_color))
					brush.setStyle(QtCore.Qt.Dense2Pattern)

					# For some items the boundingrect does not appear to work
					# correctly, so we have to use the pos() function
					x = max(item.pos().x(), item.boundingRect().x()) - 4
					y = max(item.pos().y(), item.boundingRect().y()) - 4
					w = item.boundingRect().width() + 8
					h = item.boundingRect().height() + 8
					l = self.addRect(x, y, w, h, brush = brush)
					l.setOpacity(0.25)

					# Show the context menu
					menu = QtGui.QMenu()
					menu.addAction( \
						self.sketchpad_widget.sketchpad.experiment.icon( \
						"delete"), _("Delete"))
					menu.addAction( \
						self.sketchpad_widget.sketchpad.experiment.icon( \
						"edit"), _("Edit"))
					action = menu.exec_(e.screenPos())

					# Execute the chosen action
					if action != None:
						if unicode(action.text()) == _("Delete"):
							self.delete_item(_item)
						elif unicode(action.text()) == _("Edit"):
							self.edit_item(_item)

		self.sketchpad_widget.sketchpad.apply_edit_changes()
		self.sketchpad_widget.refresh()

	def delete_item(self, item):

		"""
		Delete an item from the sketchpad

		Arguments:
		item -- the item to be deleted
		"""

		s = self.sketchpad_widget.sketchpad.item_to_string(item)

		# Walk through all items and find the matching one
		for i in self.sketchpad_widget.sketchpad.items:

			# We have to fix the coordinates, because the items in the widget
			# are not relative, whereas the items in the sketchpats are
			j = self.sketchpad_widget.sketchpad.fix_coordinates(i)

			# If the strings match, delete it!
			if self.sketchpad_widget.sketchpad.item_to_string(j) == s:
				self.sketchpad_widget.sketchpad.items.remove(i)
				break

	def edit_item(self, item):

		"""
		Present an input dialog to edit an item

		Arguments:
		item -- the item to edit
		"""

		s = self.sketchpad_widget.sketchpad.item_to_string( \
			self.sketchpad_widget.sketchpad.unfix_coordinates(item))
		s = self.sketchpad_widget.sketchpad.experiment.text_input( \
			_("Edit sketchpad element"), message=_("Element script"), \
			content=s)
		if s == None:
			return
		tmp = self.sketchpad_widget.sketchpad.items[:] # Keep a backup
		self.delete_item(item)
		try:
			self.sketchpad_widget.sketchpad.from_string(s)
		except osexception as e:
			self.sketchpad_widget.sketchpad.items = tmp
			self.sketchpad_widget.sketchpad.experiment.notify(e)

	def draw_grid(self):

		"""Draw the grid"""

		self.grid_list = []

		w = self.sketchpad_widget.sketchpad.experiment.get("width")
		h = self.sketchpad_widget.sketchpad.experiment.get("height")

		pen = QtGui.QPen()
		pen.setWidth(1)
		pen.setColor(QtGui.QColor(self.grid_color))

		x1 = 0
		x2 = w
		y1 = 0
		y2 = h

		if self.sketchpad_widget.sketchpad.get("coordinates") == "relative":
			x1 -= w / 2
			y1 -= h / 2
			x1 = x1 - x1 % self.grid
			y1 = y1 - y1 % self.grid
			x1 += w / 2
			y1 += h / 2

			if x1 < w / 2:
				x1 += self.grid

			if y1 < h / 2:
				y1 += self.grid

		for x in range(x1, x2, self.grid):
			if x == w / 2:
				pen.setWidth(3)
			l = self.addLine(x, y1, x, y2, pen)
			l.setOpacity(0.25)
			self.grid_list.append(l)
			if x == w / 2:
				pen.setWidth(1)

		for y in range(y1, y2, self.grid):
			if y == h / 2:
				pen.setWidth(3)
			l = self.addLine(x1, y, x2, y, pen)
			l.setOpacity(0.25)
			self.grid_list.append(l)
			if y == h / 2:
				pen.setWidth(1)


class sketchpad_widget(QtGui.QWidget):

	"""A custom widget contain the sketchpad canvas controls, etc."""

	def __init__(self, sketchpad, parent=None, embed=True):

		"""
		Constructor

		Arguments:
		sketchpad -- a libopensesame.sketchpad instance

		Keyword arguments:
		parent -- a parent widget (default=None)
		"""

		self.main_window = sketchpad.main_window
		QtGui.QWidget.__init__(self, parent)

		# Setup the UI
		self.ui = sketchpad_widget_ui.Ui_sketchpad_widget()
		self.ui.setupUi(self)
		self.ui.view.setViewportMargins(0, 0, 0, 0)

		self.sketchpad = sketchpad
		self.embed = embed

		self.zoom = 1.0
		self.scene = canvas(self)
		self.ui.view.setScene(self.scene)
		self.item_list = []

		self.vbox_items = QtGui.QVBoxLayout()
		self.ui.widget_items.setLayout(self.vbox_items)

		# Initialize custom color and font widgets
		self.ui.edit_color.initialize(self.sketchpad.experiment, color= \
			self.sketchpad.get('foreground', _eval=False))
		QtCore.QObject.connect(self.ui.edit_color, QtCore.SIGNAL( \
			"set_color"), self.set_tool)
		self.ui.widget_font.initialize(self.sketchpad.experiment)
		QtCore.QObject.connect(self.ui.widget_font, QtCore.SIGNAL( \
			"font_changed"), self.set_tool)

		self.ui.button_line.clicked.connect(self.set_line)
		self.ui.button_rect.clicked.connect(self.set_rect)
		self.ui.button_ellipse.clicked.connect(self.set_ellipse)
		self.ui.button_circle.clicked.connect(self.set_circle)
		self.ui.button_arrow.clicked.connect(self.set_arrow)
		self.ui.button_textline.clicked.connect(self.set_textline)
		self.ui.button_fixdot.clicked.connect(self.set_fixdot)
		self.ui.button_image.clicked.connect(self.set_image)
		self.ui.button_gabor.clicked.connect(self.set_gabor)
		self.ui.button_noise_patch.clicked.connect(self.set_noise)
		self.ui.button_edit_script.clicked.connect(self.edit_script)
		self.ui.spin_penwidth.valueChanged.connect(self.set_tool)
		self.ui.spin_zoom.valueChanged.connect(self.set_tool)
		self.ui.spin_scale.valueChanged.connect(self.set_tool)
		self.ui.spin_grid.valueChanged.connect(self.set_tool)
		self.ui.spin_arrow_size.valueChanged.connect(self.set_tool)
		self.ui.checkbox_fill.stateChanged.connect(self.set_tool)
		self.ui.checkbox_center.stateChanged.connect(self.set_tool)
		self.ui.checkbox_html.stateChanged.connect(self.set_tool)
		self.ui.checkbox_show_grid.stateChanged.connect(self.set_tool)
		self.ui.edit_show_if.editingFinished.connect(self.set_tool)

		self.set_line()
		self.refresh()
		self.sketchpad.experiment.main_window.theme.apply_theme(self)

	def edit_script(self):

		"""
		Show the edit script tab and, if not embedded, close the current window
		"""

		if not self.embed:
			self.parent().accept()
		self.sketchpad.open_script_tab()

	def unset_all(self):

		"""Untoggle all buttons"""

		self.ui.button_line.setChecked(False)
		self.ui.button_rect.setChecked(False)
		self.ui.button_ellipse.setChecked(False)
		self.ui.button_circle.setChecked(False)
		self.ui.button_arrow.setChecked(False)
		self.ui.button_textline.setChecked(False)
		self.ui.button_fixdot.setChecked(False)
		self.ui.button_image.setChecked(False)
		self.ui.button_gabor.setChecked(False)
		self.ui.button_noise_patch.setChecked(False)

		self.ui.edit_color.hide()
		self.ui.spin_penwidth.hide()
		self.ui.spin_scale.hide()
		self.ui.spin_arrow_size.hide()
		self.ui.checkbox_fill.hide()
		self.ui.checkbox_center.hide()
		self.ui.checkbox_html.hide()
		self.ui.widget_font.hide()

		self.ui.label_options.hide()
		self.ui.label_color.hide()
		self.ui.label_penwidth.hide()
		self.ui.label_scale.hide()
		self.ui.label_arrow_size.hide()

	def set_rect(self):

		"""Activate the rect button"""

		self.unset_all()
		self.ui.button_rect.setChecked(True)
		self.ui.edit_color.show()
		self.ui.spin_penwidth.show()
		self.ui.checkbox_fill.show()
		self.ui.label_color.show()
		self.ui.label_penwidth.show()
		self.set_tool()

	def set_ellipse(self):

		"""Activate the ellipse button"""

		self.unset_all()
		self.ui.button_ellipse.setChecked(True)
		self.ui.edit_color.show()
		self.ui.spin_penwidth.show()
		self.ui.checkbox_fill.show()
		self.ui.label_color.show()
		self.ui.label_penwidth.show()
		self.set_tool()

	def set_line(self):

		"""Activate the line button"""

		self.unset_all()
		self.ui.button_line.setChecked(True)
		self.ui.edit_color.show()
		self.ui.spin_penwidth.show()
		self.ui.label_color.show()
		self.ui.label_penwidth.show()
		self.set_tool()

	def set_arrow(self):

		"""Activate the line button"""

		self.unset_all()
		self.ui.button_arrow.setChecked(True)
		self.ui.edit_color.show()
		self.ui.spin_penwidth.show()
		self.ui.spin_arrow_size.show()
		self.ui.label_color.show()
		self.ui.label_penwidth.show()
		self.ui.label_arrow_size.show()
		self.set_tool()

	def set_circle(self):

		"""Activate the circle button"""

		self.unset_all()
		self.ui.button_circle.setChecked(True)
		self.ui.edit_color.show()
		self.ui.spin_penwidth.show()
		self.ui.checkbox_fill.show()
		self.ui.label_color.show()
		self.ui.label_penwidth.show()
		self.set_tool()

	def set_fixdot(self):

		"""Activate the fixdot button"""

		self.unset_all()
		self.ui.button_fixdot.setChecked(True)
		self.ui.edit_color.show()
		self.ui.label_color.show()
		self.set_tool()

	def set_image(self):

		"""Activate the image button"""

		self.unset_all()
		self.ui.button_image.setChecked(True)
		self.ui.spin_scale.show()
		self.ui.checkbox_center.show()
		self.ui.label_scale.show()
		self.set_tool()

	def set_textline(self):

		"""Activate the textline button"""

		self.unset_all()
		self.ui.button_textline.setChecked(True)
		self.ui.edit_color.show()
		self.ui.checkbox_center.show()
		self.ui.checkbox_html.show()
		self.ui.label_color.show()
		self.ui.widget_font.show()
		self.set_tool()

	def set_gabor(self):

		"""Activate the textline button"""

		self.unset_all()
		self.ui.button_gabor.setChecked(True)
		self.ui.label_options.show()
		self.set_tool()

	def set_noise(self):

		"""Activate the textline button"""

		self.unset_all()
		self.ui.button_noise_patch.setChecked(True)
		self.ui.label_options.show()
		self.set_tool()

	def add(self, from_pos, to_pos):

		"""
		Add an item to the sketchpad item list

		Arguments:
		from_pos -- an (x, y) tuple containing the top-left corner
		to_pos -- an (x, y) tuple containing the bottom-right corner
		"""

		item = {}
		item["type"] = self.tool
		item["fill"] = self.fill
		item["color"] = self.color
		item["penwidth"] = self.penwidth
		item["show_if"] = self.show_if

		if self.tool in ("ellipse", "rect"):
			if to_pos[0] > from_pos[0]:
				item["x"] = from_pos[0]
				item["w"] = to_pos[0] - from_pos[0]
			else:
				item["x"] = to_pos[0]
				item["w"] = from_pos[0] - to_pos[0]

			if to_pos[1] > from_pos[1]:
				item["y"] = from_pos[1]
				item["h"] = to_pos[1] - from_pos[1]
			else:
				item["y"] = to_pos[1]
				item["h"] = from_pos[1] - to_pos[1]

		elif self.tool in ("arrow", "line"):
			item["x1"] = from_pos[0]
			item["y1"] = from_pos[1]
			item["x2"] = to_pos[0]
			item["y2"] = to_pos[1]
			item["arrow_size"] = self.arrow_size

		elif self.tool == "fixdot":
			item["x"] = to_pos[0]
			item["y"] = to_pos[1]

		elif self.tool == "circle":
			item["x"] = from_pos[0]
			item["y"] = from_pos[1]
			item["r"] = 2 * math.sqrt( (from_pos[0] - to_pos[0]) ** 2 + (from_pos[1] - to_pos[1]) ** 2 )

		elif self.tool == "textline":
			text, ok = QtGui.QInputDialog.getText(self.ui.view, \
				_("New textline"), _("Please enter a text for the textline"))
			if not ok:
				return
			item["x"] = to_pos[0]
			item["y"] = to_pos[1]
			item["text"] = self.sketchpad.experiment.sanitize(text)
			item["center"] = self.center
			item["html"] = self.html
			item["font_family"] = self.font_family
			item["font_size"] = self.font_size
			item["font_italic"] = self.sketchpad.experiment.auto_type( \
				self.font_italic)
			item["font_bold"] = self.sketchpad.experiment.auto_type( \
				self.font_bold)

		elif self.tool == "image":
			path = pool_widget.select_from_pool(self.sketchpad.experiment.main_window)
			if path == None or unicode(path) == "":
				return
			item["x"] = to_pos[0]
			item["y"] = to_pos[1]
			item["file"] = unicode(path)
			item["scale"] = self.scale
			item["center"] = self.center

		elif self.tool == "gabor":
			item["x"] = to_pos[0]
			item["y"] = to_pos[1]
			item = self.gabor_dialog(item)
			if item == None:
				return

		elif self.tool == "noise":
			item["x"] = to_pos[0]
			item["y"] = to_pos[1]
			item = self.noise_dialog(item)
			if item == None:
				return

		item = self.sketchpad.unfix_coordinates(item)
		self.sketchpad.items.append(item)
		self.sketchpad.apply_edit_changes()
		self.refresh()

	def gabor_dialog(self, item):

		"""
		Presents the Gabor dialog and adds the relevant
		parameters to an item

		Arguments:
		item -- the item to be filled in

		Returns:
		The passed item, but filled in with all the relevant parameters
		"""

		d = QtGui.QDialog(self)
		d.ui = gabor_dialog_ui.Ui_gabor_dialog()
		d.ui.setupUi(d)
		self.sketchpad.experiment.main_window.theme.apply_theme(d)
		resp = d.exec_()
		if resp == QtGui.QDialog.Accepted:
			env = ["gaussian", "linear", "circular", "rectangle"]
			bgmode = ["avg", "col2"]
			item["orient"] = d.ui.spin_orient.value()
			item["size"] = d.ui.spin_size.value()
			item["env"] = env[d.ui.combobox_env.currentIndex()]
			item["stdev"] = d.ui.spin_stdev.value()
			item["freq"] = d.ui.spin_freq.value()
			item["phase"] = d.ui.spin_phase.value()
			item["color1"] = unicode(d.ui.edit_color1.text())
			item["color2"] = unicode(d.ui.edit_color2.text())
			item["bgmode"] = bgmode[d.ui.combobox_bgmode.currentIndex()]
			return item
		return None

	def noise_dialog(self, item):

		"""
		Presents the noise dialog and adds the relevant
		parameters to an item

		Arguments:
		item -- the item to be filled in

		Returns:
		The passed item, but filled in with all the relevant parameters
		"""

		d = QtGui.QDialog(self)
		d.ui = noise_patch_dialog_ui.Ui_noise_patch_dialog()
		d.ui.setupUi(d)
		self.sketchpad.experiment.main_window.theme.apply_theme(d)
		resp = d.exec_()
		if resp == QtGui.QDialog.Accepted:
			env = ["gaussian", "linear", "circular", "rectangle"]
			bgmode = ["avg", "col2"]
			item["size"] = d.ui.spin_size.value()
			item["env"] = env[d.ui.combobox_env.currentIndex()]
			item["stdev"] = d.ui.spin_stdev.value()
			item["color1"] = unicode(d.ui.edit_color1.text())
			item["color2"] = unicode(d.ui.edit_color2.text())
			item["bgmode"] = bgmode[d.ui.combobox_bgmode.currentIndex()]
			return item
		return None

	def rect(self, x, y, w, h, pen, brush):

		"""Draw rectangle"""

		return self.scene.addRect(x, y, w, h, pen, brush)

	def ellipse(self, x, y, w, h, pen, brush):

		"""Draw ellipse"""

		return self.scene.addEllipse(x, y, w, h, pen, brush)

	def fixdot(self, x, y, color):

		"""Draw fixation dot"""

		color = QtGui.QColor(color)
		pen = QtGui.QPen()
		pen.setColor(color)
		brush = QtGui.QBrush()
		brush.setColor(color)
		brush.setStyle(QtCore.Qt.SolidPattern)
		r1 = 8
		r2 = 2
		i = self.scene.addEllipse(x - r1, y - r1, 2*r1, 2*r1, pen, brush)
		brush.setColor(QtGui.QColor(self.sketchpad.get("background", \
			_eval=False)))
		self.scene.addEllipse(x - r2, y - r2, 2*r2, 2*r2, pen, brush)
		return i

	def arrow(self, sx, sy, ex, ey, arrow_size, pen):

		"""Draw arrow"""

		i = self.scene.addLine(sx, sy, ex, ey, pen)
		a = math.atan2(ey - sy, ex - sx)
		_sx = ex + arrow_size * math.cos(a + math.radians(135))
		_sy = ey + arrow_size * math.sin(a + math.radians(135))
		self.scene.addLine(_sx, _sy, ex, ey, pen)
		_sx = ex + arrow_size * math.cos(a + math.radians(225))
		_sy = ey + arrow_size * math.sin(a + math.radians(225))
		self.scene.addLine(_sx, _sy, ex, ey, pen)
		return i

	def line(self, x1, y1, x2, y2, pen):

		"""Draw line"""

		return self.scene.addLine(x1, y1, x2, y2, pen)

	def textline(self, text, center, x, y, color, font_family, font_size, \
		font_bold, font_italic):

		"""Draw textline"""

		if font_family == "serif" and os.name == "nt":
			font_family = "times" # WINDOWS HACK: Windows doesn't recognize serif
		if font_bold:
			weight = QtGui.QFont.Bold
		else:
			weight = QtGui.QFont.Normal
		font = QtGui.QFont(font_family, font_size, weight, font_italic)
		text_item = self.scene.addText(text, font)
		text_item.setDefaultTextColor(QtGui.QColor(color))
		if center:
			r = text_item.boundingRect()
			text_item.setPos(x - 0.5 * r.width(), y - 0.5 * r.height())
		else:
			text_item.setPos(x, y)
		return text_item

	def image(self, path, center, x, y, scale):

		"""Draw image"""

		pixmap = QtGui.QPixmap(path)

		if pixmap.isNull():
			# Qt4 cannot handle certain funky bitmaps that PyGame can. So if
			# loading the image directly fails, we fall back to loading the
			# image with PyGame and converting it to a QPixmap. In addition, we
			# notify the user that he/ she is using a funky bitmap.
			import pygame
			im = pygame.image.load(path)
			data = pygame.image.tostring(im, "RGBA")
			size = im.get_size()
			image = QtGui.QImage(data, size[0], size[1], \
				QtGui.QImage.Format_ARGB32)
			pixmap = QtGui.QPixmap.fromImage(image)
			self.notifications.append( \
				_("Funky image alert: '%s' has a non-standard format. It is recommended to convert this image to .png format, for example with Gimp <http://www.gimp.org/>.") \
				% os.path.basename(path))

		w = pixmap.width()*scale
		pixmap = pixmap.scaledToWidth(w)
		_item = self.scene.addPixmap(pixmap)
		if center:
			_item.setPos(x - 0.5 * pixmap.width(), y - 0.5 * pixmap.height())
		else:
			_item.setPos(x, y)
		return _item

	def gabor(self, item):

		"""Draw gabor patch"""

		path = openexp.canvas.gabor_file(item["orient"], item["freq"], \
			item["env"], item["size"], item["stdev"], item["phase"], \
			item["color1"], item["color2"], item["bgmode"])
		pixmap = QtGui.QPixmap(path)
		_item = self.scene.addPixmap(pixmap)
		_item.setPos(item["x"]-0.5*pixmap.width(), \
			item["y"]-0.5*pixmap.height())
		return _item

	def noise(self, item):

		"""Draw noise patch"""

		path = openexp.canvas.noise_file(item["env"], item["size"], \
			item["stdev"], item["color1"], item["color2"], item["bgmode"])
		pixmap = QtGui.QPixmap(path)
		_item = self.scene.addPixmap(pixmap)
		_item.setPos(item["x"]-0.5*pixmap.width(), \
			item["y"]-0.5*pixmap.height())
		return _item

	def refresh(self):

		"""(Re)draws the canvas and fill the item list."""

		self.scene.clear()
		self.ui.view.setMouseTracking(True)
		w = self.sketchpad.get(u'width')
		h = self.sketchpad.get(u'height')
		# Apply the zoom level
		self.ui.view.setFixedSize(self.zoom*w+60, self.zoom*h+60)
		self.ui.view.resetTransform()
		self.ui.view.scale(self.zoom, self.zoom)
		# Set the foreground
		self.ui.edit_color.initialize(self.sketchpad.experiment, color= \
			self.color)
		# Set the background
		brush = QtGui.QBrush()
		brush.setColor(QtGui.QColor(self.sketchpad.get(u'background', \
			_eval=False)))
		brush.setStyle(QtCore.Qt.SolidPattern)
		self.ui.view.setBackgroundBrush(brush)
		# Optionally draw a grid
		if self.show_grid and self.zoom * self.scene.grid >= 5:
			self.scene.draw_grid()
		# Initialize the notifications
		self.notifications = []
		static_items = self.sketchpad.static_items()
		not_shown = len(self.sketchpad.items) - len(static_items)
		if not_shown > 1:
			self.notifications.append( \
				_(u"%d objects are not shown, because they are defined using variables.") \
				% not_shown)
		elif not_shown == 1:
			self.notifications.append( \
				_(u"One object is not shown, because it is defined using variables."))
		if self.sketchpad.items_out_of_bounds() > 0:
			self.notifications.append( \
				_(u"Some objects will not be visible (or partly) because they fall outside of the screen boundaries."))
		# Walk through all items and show them
		self.item_list = []
		for item in static_items:
			g = None
			try:
				s = self.sketchpad.item_to_string(item)
				item = self.sketchpad.fix_coordinates(item)

				# Set the pen and the brush
				pen = QtGui.QPen()
				pen.setWidth(item["penwidth"])
				pen.setColor(QtGui.QColor(item["color"]))
				brush = QtGui.QBrush()
				if item["fill"] == 1:
					brush.setColor(QtGui.QColor(item["color"]))
					brush.setStyle(QtCore.Qt.SolidPattern)

				if item["type"] == "rect":
					g = self.rect(item["x"], item["y"], item["w"], item["h"], \
						pen, brush)
				elif item["type"] == "circle":
					g = self.ellipse(item["x"]-0.5*item["r"], \
						item["y"]-0.5*item["r"], item["r"], item["r"], pen, \
						brush)
				elif item["type"] == "ellipse":
					g = self.ellipse(item["x"], item["y"], item["w"], \
						item["h"], pen, brush)
				elif item["type"] == "fixdot":
					g = self.fixdot(item["x"], item["y"], item["color"])
				elif item["type"] == "arrow":
					g = self.arrow(item["x1"], item["y1"], item["x2"], \
						item["y2"], item["arrow_size"], pen)
				elif item["type"] == "line":
					g = self.line(item["x1"], item["y1"], item["x2"], \
						item["y2"], pen)
				elif item["type"] == "textline":
					g = self.textline(item["text"], item["center"]==1, \
						item["x"], item["y"], item["color"], \
						item["font_family"], item["font_size"], \
						item['font_bold'] == 'yes', item['font_italic'] == 'yes')
				elif item["type"] == "image":
					g = self.image(self.sketchpad.experiment.get_file( \
						item["file"]), item["center"]==1, item["x"], \
						item["y"], item["scale"])
				elif item["type"] == "gabor":
					g = self.gabor(item)
				elif item["type"] == "noise":
					g = self.noise(item)
				else:
					print("Could not find", item["type"])

			except Exception as e:
				debug.msg("exception caught: %s" % e)
				self.notifications.append( \
					_("Failed to parse the following item (use 'Edit script' to fix/ remove this line):\n'%s'") \
					% s)

			# Add a tooltip to the scene element
			if g != None:
				g.setToolTip(s)
				self.item_list.append( (g, item) )

		# Show the notifications (if any)
		if len(self.notifications) > 0:
			self.ui.frame_notification.setVisible(True)
			self.ui.label_notification.setText("\n- ".join(["Notifications:"] + \
				self.notifications))
		else:
			self.ui.frame_notification.setVisible(False)

		# Add the items to the list below the sketchpad
		self.sketchpad.experiment.clear_widget(self.ui.widget_items)
		row = 0
		for item in self.sketchpad.items:
			edit = QtGui.QLineEdit(self.sketchpad.item_to_string(item))
			edit.setReadOnly(True)
			hbox = QtGui.QHBoxLayout()
			hbox.setContentsMargins(0, 0, 0, 0)
			hbox.addWidget(edit_item_button(self, item))
			hbox.addWidget(edit)
			hbox.addWidget(remove_item_button(self, item))
			widget = QtGui.QWidget()
			widget.setLayout(hbox)
			self.vbox_items.addWidget(widget)
		self.vbox_items.addStretch()

		return True

	def set_tool(self, dummy=None):

		"""
		Sets the current tool according to the options in the widget.

		Keyword argument:
		dummy	--	DEPRECATED.
		"""

		self.penwidth = self.ui.spin_penwidth.value()
		self.color = self.sketchpad.experiment.sanitize( \
			self.ui.edit_color.text())
		refs = []
		try:
			refs = self.sketchpad.experiment.get_refs(self.color)
			self.sketchpad.experiment.color_check(self.color)
		except Exception as e:
			if len(refs) == 0:
				self.sketchpad.experiment.notify(e)
				self.ui.edit_color.setText(u'white')
				self.color = u'white'

		self.show_grid = self.ui.checkbox_show_grid.isChecked()

		if self.ui.checkbox_fill.isChecked():
			self.fill = 1
		else:
			self.fill = 0
		if self.ui.checkbox_center.isChecked():
			self.center = 1
		else:
			self.center = 0
		self.arrow_size = self.ui.spin_arrow_size.value()
		self.scale = self.ui.spin_scale.value() * 0.01
		self.scene.grid = self.ui.spin_grid.value()
		self.zoom = self.ui.spin_zoom.value() * 0.01
		self.font_family = self.ui.widget_font.family
		self.font_size = self.ui.widget_font.size
		self.font_italic = self.ui.widget_font.italic
		self.font_bold = self.ui.widget_font.bold
		self.show_if = self.sketchpad.clean_cond(self.ui.edit_show_if.text())
		self.ui.edit_show_if.setText(self.show_if)
		if self.ui.checkbox_html.isChecked():
			self.html = u'yes'
		else:
			self.html = u'no'

		if self.ui.button_line.isChecked():
			self.tool = u'line'
			self.scene.oneshot = False
		elif self.ui.button_arrow.isChecked():
			self.tool = u'arrow'
			self.scene.oneshot = False
		elif self.ui.button_rect.isChecked():
			self.tool = u'rect'
			self.scene.oneshot = False
		elif self.ui.button_ellipse.isChecked():
			self.tool = u'ellipse'
			self.scene.oneshot = False
		elif self.ui.button_circle.isChecked():
			self.tool = u'circle'
			self.scene.oneshot = False
		elif self.ui.button_fixdot.isChecked():
			self.tool = u'fixdot'
			self.scene.oneshot = True
		elif self.ui.button_image.isChecked():
			self.tool = u'image'
			self.scene.oneshot = True
		elif self.ui.button_textline.isChecked():
			self.tool = u'textline'
			self.scene.oneshot = True
		elif self.ui.button_gabor.isChecked():
			self.tool = u'gabor'
			self.scene.oneshot = True
		elif self.ui.button_noise_patch.isChecked():
			self.tool = u'noise'
			self.scene.oneshot = True
		self.refresh()




