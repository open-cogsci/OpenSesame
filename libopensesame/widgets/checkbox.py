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

from button import button

class checkbox(button):

	"""A checkbox widget"""

	def __init__(self, form, text='checkbox', frame=False, group=None, checked=False, click_accepts=False, var=None):
	
		"""<DOC>
		Constructor
		
		Arguments:
		form -- The parent form.
				
		Keyword arguments:
		text -- Checkbox text (default='checkbox').
		frame -- Indicates whether a frame should be drawn around the widget #
				 (default=False).
		group -- If a group is specified, checking one checkbox from the group #
				 will uncheck all other checkboxes in that group (default=None).
		checked -- The checked state of the checkbox (default=False).
		click_accepts -- Indicates whether a click press should accept and #
					     close the form (default=False).
		var -- The name of the experimental variable that should be used to log #
			   the widget status (default=None).
		</DOC>"""	
		
		if type(checked) != bool:
			checked = checked == 'yes'
		if type(click_accepts) != bool:
			click_accepts = click_accepts == 'yes'											
			
		button.__init__(self, form, text, frame=frame, center=False)
		self.type = 'checkbox'
		self.group = group		
		self.box_size = 16
		self.box_pad = self.x_pad
		self.x_pad += self.x_pad + self.box_size
		self.var = var
		self.click_accepts = click_accepts
		self.set_checked(checked)
				
	def on_mouse_click(self, pos):
	
		"""<DOC>
		Is called whenever the user clicks on the widget. Toggles the state of #
		the checkbox.
		
		Arguments:
		pos -- An (x, y) tuple.
		</DOC>"""		
	
		if self.group != None:
			for widget in self.form.widgets:
				if widget != None and widget.type == 'checkbox' and \
					widget.group == self.group:
					widget.set_checked(False)
			self.set_checked(True)
		else:
			self.set_checked(not self.checked)
			
		# Set the response variable
		l_val = []
		for widget in self.form.widgets:		
			if widget != None and widget.type == 'checkbox' and \
				widget.group == self.group:
				if widget.checked:
					l_val.append(widget.text)
		self.set_var(';'.join(l_val))
			
		if self.click_accepts:
			return self.text
				
	def render(self):
	
		"""<DOC>
		Draws the widget.
		</DOC>"""	
	
		x, y, w, h = self.rect
		self.form.theme_engine.box(x+self.box_pad, y+self.y_pad, \
			checked=self.checked)
		self.draw_text(self.text)
		
	def set_checked(self, checked=True):
	
		"""<DOC>
		Sets the checked status of the checkbox.
		
		Keyword arguments:
		checked -- The checked status (default=True).
		</DOC>"""
		
		self.checked = checked
		self.set_var(checked)

