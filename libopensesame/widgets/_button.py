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

from libopensesame.widgets._label import label

class button(label):

	"""
	desc: |
		The button widget is a clickable text string, by default surrounded by a
		button-like frame.

		__Example (OpenSesame script):__

		~~~
		widget 0 0 1 1 button text='Click me!' center='yes' frame='yes' var='response'
		~~~

		Defining a button widget with Python inline code:

		__Example (Python):__

		~~~ {.python}
		from libopensesame import widgets
		form = widgets.form(self.experiment)
		button = widgets.button(form, text='Click me!', frame=True, center=True,
			var='response')
		form.set_widget(button, (0,0))
		form._exec()
		~~~

		__Function list:__

		%--
		toc:
			mindepth: 2
			maxdepth: 2
		--%
	"""

	def __init__(self, form, text=u'button', frame=True, center=True, var=None):
	
		"""
		desc:
			Constructor.
		
		arguments:
			form:
				desc:	The parent form.
				type:	form
		
		keywords:
			text:
				desc:	Button text.
				type:	[str, unicode]
			frame:
				desc:	Indicates whether a frame should be drawn around the
						widget.
				type:	bool
			center:
				desc:	Indicates whether the text should be centered.
				type:	bool
			var:
				desc:	The name of the experimental variable that should be
						used to log the widget status.
				type:	[str, unicode, NoneType]
		"""
	
		label.__init__(self, form, text, frame=frame, center=center)
		self.type = u'button'
		self.var = var
		self.set_var(False)
				
	def on_mouse_click(self, pos):
	
		"""
		desc:
			Is called when the user clicks on the button. Returns the button
			text.
		
		arguments:
			pos:
				desc:	An (x, y) coordinates tuple.
				type:	tuple

		returns:
			desc:	The button text.
			type:	unicode
		"""
	
		self.set_var(True)
		return self.text
