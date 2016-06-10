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

from libopensesame.widgets._label import label
from openexp.keyboard import keyboard

class text_input(label):

	"""
	desc: |
		The text_input widget allows the participant to enter multi-character
		responses. (This widget has no relation to the text_input plug-in, which
		was created before forms where added to OpenSesame.)

		__Example (OpenSesame script):__

		~~~
		widget 0 0 1 1 text_input var='response' return_accepts='yes'
		~~~

		__Example (Python):__

		~~~ .python
		from libopensesame import widgets
		form = widgets.form(exp)
		text_input = widgets.text_input(form, var='response',
			return_accepts=True)
		form.set_widget(text_input, (0,0))
		form._exec()
		~~~

		[TOC]
	"""

	def __init__(self, form, text=u'', frame=True, center=False,
		stub=u'Type here ...', return_accepts=False, var=None):

		"""
		desc:
			Constructor.

		arguments:
			form:
				desc:	The parent form.
				type:	form

		keywords:
			text:
				desc:	The text to start with.
				type:	[str, unicode]
			frame:
				desc:	Indicates whether a frame should be drawn around the
						widget.
				type:	bool
			center:
				desc:	Indicates whether the text should be centered.
				type:	bool
			stub:
				desc:	A text string that should be shown whenever the user has
						not entered any text.
				type:	[str, unicode]
			return_accepts:
				desc:	Indicates whether a return press should accept and close
						the form.
				type:	bool
			var:
				desc:	The name of the experimental variable that should be
						used to log the widget status.
				type:	[str, unicode, NoneType]
		"""

		if type(return_accepts) != bool:
			return_accepts = return_accepts == u'yes'

		label.__init__(self, form, text, frame=frame, center=center)
		self.type = u'text_input'
		self.stub = safe_decode(stub)
		self.prompt = u'_'
		self.return_accepts = return_accepts
		self.var = var
		self.text = safe_decode(text)
		self.set_var(text)
		self.caret_pos = None

	def render(self):

		"""
		desc:
			Draws the widget.
		"""

		if self.frame:
			if self.focus:
				self.draw_frame(self.rect, style=u'active')
			else:
				self.draw_frame(self.rect, style=u'light')
		if self.text == '' and not self.focus:
			self.draw_text(self.stub, html=False)
		elif self.focus:
			self.draw_text(self.text[:self.caret_pos] + self.prompt +
							self.text[self.caret_pos:], html=False)
		else:
			self.draw_text(self.text, html=False)

	def on_mouse_click(self, pos):

		"""
		desc:
			Is called whenever the user clicks on the widget. Activates the text
			input for typing text.

		arguments:
			pos:
				desc:	An (x, y) coordinates tuple.
				type:	tuple
		"""

		self.focus = True
		self.caret_pos = len(self.text)
		self.theme_engine.click()
		my_keyboard = keyboard(self.form.experiment, timeout=0)
		my_keyboard.show_virtual_keyboard(True)
		while True:
			self.form.render()
			if self.form.timed_out():
				return None
			resp, time = my_keyboard.get_key()
			if resp is None:
				continue
			try:
				o = ord(resp)
			except:
				o = None
			if resp == u'space':
				self.text = self.text[:self.caret_pos] + u' ' +\
							self.text[self.caret_pos:]
				self.caret_pos +=1
			elif resp == u'backspace' or o == 8:
				self.text = self.text[:self.caret_pos-1] +\
							self.text[self.caret_pos:]
				self.caret_pos = max(0,self.caret_pos-1)
			elif resp == u'delete':
				self.text = self.text[:self.caret_pos] +\
							self.text[self.caret_pos+1:]
			elif resp == u'tab':
				self.focus = False
				my_keyboard.show_virtual_keyboard(False)
				return None
			elif resp == u'return' or resp == u'enter':
				self.theme_engine.click()
				if self.return_accepts:
					my_keyboard.show_virtual_keyboard(False)
					return self.text
				else:
					self.focus = False
					my_keyboard.show_virtual_keyboard(False)
					return None
			elif resp == u'left':
				self.caret_pos = max(0,self.caret_pos-1)
			elif resp == u'right':
				self.caret_pos = min(len(self.text),self.caret_pos+1)
			elif len(resp) == 1:
				self.text = self.text[:self.caret_pos] + resp +\
							self.text[self.caret_pos:]
				self.caret_pos +=1
			self.set_var(self.text)
