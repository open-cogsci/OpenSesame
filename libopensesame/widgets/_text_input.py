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
from libopensesame.widgets._label import Label
from openexp.keyboard import keyboard


class TextInput(Label):

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
		form = Form()
		text_input = TextInput(var='response', return_accepts=True)
		form.set_widget(text_input, (0,0))
		form._exec()
		~~~

		[TOC]
	"""

	def __init__(self, form, text=u'', frame=True, center=False,
		stub=u'Type here ...', return_accepts=False, var=None, key_filter=None):

		"""
		desc: |
			Constructor to create a new `TextInput` object. You do not generally
			call this constructor directly, but use the `TextInput()` factory
			function, which is described here: [/python/common/]().

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
			key_filter:
				desc:	A function that takes a key as a single argument and
						return True if the key should be accepted and False
						otherwise. This can also filter out keys such as return
						and backspace, but not Escape.
				type:	[FunctionType, NoneType]
		"""

		if isinstance(return_accepts, basestring):
			return_accepts = return_accepts == u'yes'
		Label.__init__(self, form, text, frame=frame, center=center)
		self.type = u'text_input'
		self.stub = safe_decode(stub)
		self.prompt = u'\u2038'
		self.html = False
		self.return_accepts = return_accepts
		self.var = var
		self.text = safe_decode(text)
		self.set_var(text)
		self.caret_pos = None
		self._key_filter = (lambda k: True) if key_filter is None else key_filter

	def _update(self):

		"""
		desc:
			Draws the widget.
		"""

		if self.frame:
			if self.focus:
				self._update_frame(self.rect, style=u'active')
			else:
				self._update_frame(self.rect, style=u'light')
		if self.text == '' and not self.focus:
			self._update_text(self.stub)
		elif self.focus:
			self._update_text(self.text[:self.caret_pos] + self.prompt +
							self.text[self.caret_pos:])
		else:
			self._update_text(self.text)

	def coroutine(self):

		"""
		desc:
			Implements the interaction.
		"""

		self.caret_pos = len(self.text)
		retval = None
		while True:
			d = yield retval
			retval = None
			if d[u'type'] == u'stop':
				break
			if d[u'type'] != u'key':
				continue
			key = d[u'key']
			if not self._key_filter(key):
				continue
			if key == u'space':
				self.text = self.text[:self.caret_pos] + u' ' \
					+ self.text[self.caret_pos:]
				self.caret_pos +=1
			elif key == u'backspace':
				self.text = self.text[:self.caret_pos-1]  \
					+ self.text[self.caret_pos:]
				self.caret_pos = max(0, self.caret_pos-1)
			elif key == u'delete':
				self.text = self.text[:self.caret_pos] \
					+ self.text[self.caret_pos+1:]
			elif key in (u'return', u'enter') and self.return_accepts:
				retval = self.text
			elif key in (u'home', u'page up'):
				self.caret_pos = 0
			elif key in (u'end', u'page down'):
				self.caret_pos = len(self.text)
			elif key == u'left':
				self.caret_pos = max(0, self.caret_pos-1)
			elif key == u'right':
				self.caret_pos = min(len(self.text), self.caret_pos+1)
			elif len(key) == 1:
				self.text = self.text[:self.caret_pos] + key \
					+ self.text[self.caret_pos:]
				self.caret_pos +=1
			self._update()
			self.set_var(self.text)


text_input = TextInput
