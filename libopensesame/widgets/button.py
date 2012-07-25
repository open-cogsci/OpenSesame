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

from label import label

class button(label):

	"""A simple text button"""

	def __init__(self, form, text='button', frame=True, center=True, var=None):
	
		"""<DOC>
		Constructor
		
		Arguments:
		form -- the parent form
		
		Keyword arguments:
		text -- button text (default='button')
		frame -- indicates whether a frame should be drawn around the widget
				 (default=False)
		center -- indicates whether the text should be centered (default=False)
		var -- the name of the experimental variable that should be used to log
			   the widget status (default=None)		
		</DOC>"""	
	
		label.__init__(self, form, text, frame=frame, center=center)
		self.type = 'button'
		self.var = var
		self.set_var(False)
				
	def on_mouse_click(self, pos):
	
		"""<DOC>
		Is called whenever the user clicks on the widget. Returns the button
		text.
		
		Arguments:
		pos -- an (x, y) tuple		
		</DOC>"""		
	
		self.set_var(True)
		return self.text
