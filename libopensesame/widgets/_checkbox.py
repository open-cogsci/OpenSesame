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
from libopensesame.exceptions import osexception
from libopensesame.widgets._button import button

class checkbox(button):

	"""
	desc: |
		The checkbox widget is a checkable box accompanied by a string of text.

		__Example (OpenSesame script):__

		~~~
		widget 0 0 1 1 checkbox group="group" text="Option 1"
		widget 0 1 1 1 checkbox group="group" text="Option 2"
		~~~

		__Example (Python):__

		~~~ .python
		from libopensesame import widgets
		form = widgets.form(exp)
		checkbox1 = widgets.checkbox(form, text='Option 1', group='group')
		checkbox2 = widgets.checkbox(form, text='Option 2', group='group')
		form.set_widget(checkbox1, (0,0))
		form.set_widget(checkbox2, (0,1))
		~~~

		[TOC]
	"""

	def __init__(self, form, text=u'checkbox', frame=False, group=None,
		checked=False, click_accepts=False, var=None):

		"""
		desc:
			Constructor.

		arguments:
			form:
				desc:	The parent form.
				type:	form

		keywords:
			text:
				desc:	Checkbox text.
				type:	[str, unicode]
			frame:
				desc:	Indicates whether a frame should be drawn around the
						widget.
				type:	bool
			group:
				desc:	If a group is specified, checking one checkbox from the
						group will uncheck all other checkboxes in that group.
						Checkboxes that are part of a group cannot be
						unchecked, except by clicking on another checkbox in the
						group. The `group` keyword also affects how variables
						are stored (see the `var` keyword).
				type:	[str, unicode, NoneType]
			checked:
				desc:	The initial checked state of the checkbox.
				type:	bool
			click_accepts:
				desc:	Indicates whether a click press should accept and close
						the form.
				type:	bool
			var:
				desc:	The name of the experimental variable that should be
						used to log the widget status. This variable will
						contain a semi-colon separated list of the text of all
						checked checkboxes in the same group, or 'no' if no
						checkbox in the group is checked. For the purpose of the
						variable, all checkboxes that are not part of a group
						are placed in the same group. For more information about
						the use of response variables in forms, see the form
						documentation page.
				type:	[str, unicode, NoneType]
		"""

		if isinstance(checked, basestring):
			checked = checked == u'yes'
		if isinstance(click_accepts, basestring):
			click_accepts = click_accepts == u'yes'
		button.__init__(self, form, text, frame=frame, center=False)
		self.type = u'checkbox'
		self.group = group
		self.box_pad = self.x_pad
		self.x_pad += self.x_pad + self.box_size
		self.var = var
		self.click_accepts = click_accepts
		self.set_checked(checked)

	def on_mouse_click(self, pos):

		"""
		desc:
			Is called whenever the user clicks on the widget. Toggles the state
			of the checkbox.

		arguments:
			pos:
				desc:	An (x, y) coordinate tuple.
				type:	tuple
		"""

		self.theme_engine.click()
		if self.group is not None:
			# If the checkbox is part of a group than checking it will uncheck
			# all other checkboxes in the group, and check the current one
			for widget in self.form.widgets:
				if widget is not None and widget.type == u'checkbox' and \
					widget.group == self.group and self.group is not None:
					widget.set_checked(False)
			self.set_checked(True)
		else:
			# If the checkbox is not part of a group then checking it will
			# toggle its check status
			self.set_checked(not self.checked)

		if self.click_accepts:
			return self.text

	def render(self):

		"""
		desc:
			Draws the widget.
		"""

		x, y, w, h = self.rect
		self.form.theme_engine.box(x+self.box_pad, y+self.y_pad, \
			checked=self.checked)
		self.draw_text(self.text)

	def set_checked(self, checked=True):

		"""
		desc:
			Sets the checked status of the checkbox.

		keywords:
			checked:
				desc:	The checked status.
				type:	bool
		"""

		self.checked = checked
		self.set_var(checked)

	def set_var(self, val, var=None):

		"""
		desc:
			Sets an experimental variable.

		arguments:
			val:
				desc:	A value.
				type:	[str, unicode]

		keywords:
			var:
				desc:	A variable name, or `None` to use widget default.
				type:	[str, unicode, NoneType]
		"""

		if var is None:
			var = self.var
		if var is None:
			return

		# Set the response variable
		l_val = []

		# When this function is called via the constructor, the checkbox is not
		# yet part of the form. Therefore, we need to add it explicitly to the
		# widget list.
		widget_list = self.form.widgets[:]
		if self not in self.form.widgets:
			widget_list += [self]

		for widget in widget_list:
			if widget is not None and widget.type == u'checkbox' and \
				widget.var == self.var:
				if widget.group != self.group and self.group is not None:
					raise osexception(
						u'All checkbox widgets without a group or within the same group should have the same variable.')
				if widget.checked or widget.checked == u'yes':
					l_val.append(safe_decode(widget.text))
		val = u';'.join(l_val)
		if val == u'':
			val = u'no'
		button.set_var(self, val, var=var)
