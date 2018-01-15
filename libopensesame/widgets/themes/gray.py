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
import os
from libopensesame.widgets.themes.plain import plain
from openexp.canvas_elements import Rect, Line, Image
from openexp._canvas._element.group import Group


class gray(plain):

	def __init__(self, form):

		plain.__init__(self, form)
		self.box_checked_image = self.form.experiment.resource(os.path.join(
			u'widgets', u'gray', u'box-checked.png'))
		self.box_unchecked_image = self.form.experiment.resource(os.path.join(
			u'widgets', u'gray', u'box-unchecked.png'))

	def box(self, x, y, checked=False):

		return Image(
			self.box_checked_image if checked else self.box_unchecked_image,
			center=False, x=x, y=y).construct(self.canvas)

	def frame(self, x, y, w, h, style=u'normal'):

		elements = [
			Line(x+1, y+1, x+w-2, y+1, color=u'#babdb6'),
			Line(x+1, y+1, x+1, y+h-2, color=u'#babdb6'),
			Line(x+1, y+h-2, x+w-2, y+h-2, color=u'#555753'),
			Line(x+w-2, y+1, x+w-2, y+h-2, color=u'#555753')
			]
		if style in (u'active', u'normal'):
			elements.insert(0, Rect(x, y, w, h, color=u'#2e3436'))
		if style == u'normal':
			elements.append(
				Rect(x+2, y+2, w-4, h-4, color=u'#888a85', fill=True))
		return Group(self.canvas, elements)
