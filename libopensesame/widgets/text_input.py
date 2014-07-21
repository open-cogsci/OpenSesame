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
from openexp.keyboard import keyboard

class text_input(label):

	"""A multiline text input widget"""

	def __init__(self, form, text=u'', frame=True, center=False, stub=u'Type here ...', return_accepts=False, var=None):
	
		"""<DOC>
		Constructor.
		
		Arguments:
		form -- The parent form.
		
		Keyword arguments:
		text -- The text to start with (default=u'').
		frame -- Indicates whether a frame should be drawn around the widget
				 (default=False).
		center -- Indicates whether the text should be centered (default=False).
		stub -- A text string that should be shown whenever the user has not
				entered any text (default=u'Type here ...').
		return_accepts -- Indicates whether a return press should accept and
						  close the form (default=False).
		var -- The name of the experimental variable that should be used to log
			   the widget status (default=None).
		</DOC>"""
		
		if type(return_accepts) != bool:
			return_accepts = return_accepts == u'yes'
	
		label.__init__(self, form, text, frame=frame, center=center)
		self.type = u'text_input'		
		self.stub = self.form.experiment.unistr(stub)
		self.prompt = u'_'
		self.return_accepts = return_accepts
		self.var = var
		self.text = self.form.experiment.unistr(text)
		self.set_var(text)
		
	def render(self):
	
		"""<DOC>
		Draws the widget.
		</DOC>"""	

		if self.frame:
			if self.focus:
				self.draw_frame(self.rect, style=u'active')
			else:
				self.draw_frame(self.rect, style=u'light')
		if self.text == '' and not self.focus:
			self.draw_text(self.stub, html=False)	
		elif self.focus:
			self.draw_text(self.text+self.prompt, html=False)	
		else:
			self.draw_text(self.text, html=False)	
				
	def on_mouse_click(self, pos):
	
		"""<DOC>
		Is called whenever the user clicks on the widget. Activates the text #
		input for typing text.
		
		Arguments:
		pos -- An (x, y) tuple.
		</DOC>"""	
		
		self.focus = True
		my_keyboard = keyboard(self.form.experiment)
		my_keyboard.show_virtual_keyboard(True)
		while True:		
			self.form.render()		
			resp, time = my_keyboard.get_key()
			try:
				o = ord(resp)
			except:
				o = None
			if resp == u'space':			
				self.text += ' '
			elif resp == u'backspace' or o == 8:
				self.text = self.text[:-1]
			elif resp == u'tab':
				self.focus = False
				my_keyboard.show_virtual_keyboard(False)
				return None
			elif resp == u'return':
				if self.return_accepts:
					my_keyboard.show_virtual_keyboard(False)
					return self.text
				else:
					self.focus = False
					my_keyboard.show_virtual_keyboard(False)
					return None
			elif len(resp) == 1:
				self.text += resp
			self.set_var(self.text)

