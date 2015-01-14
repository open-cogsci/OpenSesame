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

class gray(plain):

	def __init__(self, form):

		plain.__init__(self, form)
		self.box_checked_image = self.form.experiment.resource(os.path.join( \
			'widgets', 'gray', 'box-checked.png'))
		self.box_unchecked_image = self.form.experiment.resource(os.path.join( \
			'widgets', 'gray', 'box-unchecked.png'))

	def box(self, x, y, checked=False):

		if checked:
			self.form.canvas.image(self.box_checked_image, center=False, x=x, \
				y=y)
		else:
			self.form.canvas.image(self.box_unchecked_image, center=False, \
				x=x, y=y)

	def frame(self, x, y, w, h, style='normal'):

		if style in ('normal', 'active'):
			self.form.canvas.rect(x, y, w, h, color='#2e3436')
		self.form.canvas.line(x+1, y+1, x+w-2, y+1, color='#babdb6')
		self.form.canvas.line(x+1, y+1, x+1, y+h-2, color='#babdb6')
		self.form.canvas.line(x+1, y+h-2, x+w-2, y+h-2, color='#555753')
		self.form.canvas.line(x+w-2, y+1, x+w-2, y+h-2, color='#555753')
		if style == 'normal':
			self.form.canvas.rect(x+2, y+2, w-4, h-4, color='#888a85', fill=True)
