# coding=utf-8

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

You should have received a copy of the GNU General Public Licensepass
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""

from libopensesame.py3compat import *
from openexp._canvas._element.element import Element
from qtpy.QtWidgets import QGraphicsTextItem, QStyleOptionGraphicsItem
from qtpy.QtGui import QPixmap, QPainter, QColor, QFont
from qtpy.QtCore import Qt
from PIL import Image


class RichText(Element):

	def __init__(self, canvas, text, center=True, x=None, y=None,
		max_width=None, **properties):

		x, y = canvas.none_to_center(x, y)
		properties = properties.copy()
		properties.update({
			'text' : text,
			'center' : center,
			'x' : x,
			'y' : y,
			'max_width' : max_width
			})
		Element.__init__(self, canvas, **properties)

	def size(self):

		t = self._to_qgraphicstextitem()
		rect = t.boundingRect()
		return rect.width(), rect.height()

	def _to_qgraphicstextitem(self):

		t = QGraphicsTextItem()
		t.setDefaultTextColor(QColor(self.color.colorspec))
		if self.html:
			t.setHtml(u'<div align="center">%s</div>' % self.text \
				if self.center else self.text)
		else:
			t.setPlainText(self.text)
		mw = self.max_width
		if mw is None:
			if self.uniform_coordinates:
				mw = self._canvas.width//2 - self.x
			else:
				mw = self._canvas.width - self.x
		if self.center:
			mw *= 2
		t.setTextWidth(mw)
		f = QFont(self.font_family,
			weight=QFont.Bold if self.font_bold else QFont.Normal,
			italic=self.font_italic)
		f.setPixelSize(self.font_size)
		t.setFont(f)
		return t

	def _to_qimage(self):

		t = self._to_qgraphicstextitem()
		rect = t.boundingRect()
		height = rect.height()
		width = rect.width()
		pixmap = QPixmap(width, height)
		pixmap.fill(Qt.transparent)
		painter = QPainter(pixmap)
		t.paint(painter, QStyleOptionGraphicsItem(), None)
		painter.end()
		return pixmap.toImage()

	def _to_pil(self):

		return Image.fromqimage(self._to_qimage())
