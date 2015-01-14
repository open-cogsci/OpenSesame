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

class plain:

	def __init__(self, form):
	
		self.form = form
		
	def box(self, x, y, checked=False):
	
		self.form.canvas.rect(x, y, 16, 16, fill=checked)
		
	def box_size(self):
	
		return 16
		
	def frame(self, x, y, w, h, style='normal'):
	
		self.form.canvas.rect(x, y, w, h)
			
