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

import os
import sys
from libopensesame.py3compat import *
import warnings
from openexp._canvas._element.element import Element
from qtpy.QtWidgets import (QGraphicsTextItem, QStyleOptionGraphicsItem,
	QApplication)
from qtpy.QtGui import QPixmap, QPainter, QColor, QFont, QFontDatabase
from qtpy.QtCore import Qt, QCoreApplication
from PIL import Image

FONTS = [
	'sans',
	'serif',
	'mono',
	'arabic',
	'chinese-japanese-korean',
	'hindi',
	'hebrew'
]
font_database = None
font_substitutions = []
pyqt_initialized = False


class RichText(Element):

	def __init__(self, canvas, text, center=True, x=None, y=None,
		max_width=None, **properties):

		global pyqt_initialized

		if not pyqt_initialized:
			self._init_pyqt(canvas.experiment)
			pyqt_initialized = True
		x, y = canvas.none_to_center(x, y)
		properties = properties.copy()
		properties.update({
			'text' : safe_decode(text),
			'center' : center,
			'x' : x,
			'y' : y,
			'max_width' : max_width
		})
		Element.__init__(self, canvas, **properties)

	def _init_pyqt(self, exp):

		global app, font_database

		# Add the Qt plugin folders to the library path, if they exists. Where
		# these folders are depends on the version of Qt4, but these are two
		# possible locations.
		qt_plugin_path = os.path.join(
			os.path.dirname(sys.executable), 'Library', 'plugins')
		if os.path.isdir(qt_plugin_path):
			QCoreApplication.addLibraryPath(qt_plugin_path)
		qt_plugin_path = os.path.join(
			os.path.dirname(sys.executable), 'Library', 'lib', 'qt4', 'plugins')
		if os.path.isdir(qt_plugin_path):
			QCoreApplication.addLibraryPath(qt_plugin_path)
		# If no instance of QApplication exists, a segmentation fault seems to always
		# occur. So we create one.
		if QCoreApplication.instance() is None:
			app = QApplication([])
		# Register the fonts bundled with OpenSesame
		if font_database is None:
			font_database= QFontDatabase()
			for font in FONTS:
				try:
					path = exp.resource(font + u'.ttf')
				except:
					warnings.warn(u'Font %s not found' % font)
					continue
				font_id = font_database.addApplicationFont(path)
				if font_id < 0:
					warnings.warn(u'Failed to load font %s' % font)
					continue
				font_families = font_database.applicationFontFamilies(font_id)
				if not font_families:
					warnings.warn(u'Font %s contains no families' % font)
					continue
				font_substitutions.append((font_families[0], font))

	@property
	def size(self):

		bbox = Image.fromqimage(self._to_qimage()).getbbox()
		x1, y1, x2, y2 = (0, 0, 1, 1) if bbox is None else bbox
		y2 = max(y1+self.font_size, y2)
		return x2-x1, y2-y1

	@property
	def rect(self):

		w, h = self.size
		if self.center:
			return self.x-w//2, self.y-h//2, w, h
		return self.x, self.y, w, h

	def _to_qgraphicstextitem(self):

		t = QGraphicsTextItem()
		t.setDefaultTextColor(QColor(self.color.hexcolor))
		if self.html:
			text = self.text.replace(u'\n', u'<br />')
			t.setHtml(
				u'<div align="center">%s</div>' % text
				if self.center else text
			)
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
		for family, substitute in font_substitutions:
			f.insertSubstitution(substitute, family)
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

		im = Image.fromqimage(self._to_qimage())
		bbox = im.getbbox()
		x1, y1, x2, y2 = (0, 0, 1, 1) if bbox is None else bbox
		y1 = min(y2-self.font_size, y1)
		return im.crop((x1, y1, x2, y2))
