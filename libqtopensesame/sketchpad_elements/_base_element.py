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

from PyQt4 import QtGui, QtCore

class base_element(object):

	def __init__(self, sketchpad, string):

		super(base_element, self).__init__(sketchpad, string)
		self.selected = False
		self.highlighted = False

	def draw(self):

		self.graphics_item = super(base_element, self).draw()
		self.graphics_item.element = self
		self.update()

	def move(self, dx=0, dy=0):

		for var, val in self.properties.items():
			if var in [u'x', u'x1', u'x2']:
				self.properties[var] += dx
			if var in [u'y', u'y1', u'y2']:
				self.properties[var] += dy

	def update(self):

		if self.highlighted:
			self.graphics_item.setGraphicsEffect(self.highlighted_effect())
		elif self.selected:
			self.graphics_item.setGraphicsEffect(self.selected_effect())
		else:
			self.graphics_item.setGraphicsEffect(None)

	def highlight(self, highlighted=True):

		self.highlighted = highlighted
		self.update()

	def select(self, selected=True):

		self.selected = selected
		self.update()

	def selected_effect(self):

		effect = QtGui.QGraphicsDropShadowEffect()
		effect.setColor(QtGui.QColor('#00FF00'))
		effect.setBlurRadius(32)
		effect.setOffset(0,0)
		return effect

	def highlighted_effect(self):

		effect = QtGui.QGraphicsColorizeEffect()
		effect.setColor(QtGui.QColor('#00FF00'))
		effect.setStrength(0.5)
		return effect
