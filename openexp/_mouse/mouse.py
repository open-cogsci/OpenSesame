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

# If available, use the yaml.inherit metaclass to copy the docstrings from
# mouse onto the back-end-specific implementations of this class
# (legacy, etc.)
try:
	from yamldoc import inherit as docinherit
except:
	docinherit = type

from libopensesame.exceptions import osexception

class mouse(object):

	"""
	desc: |
		The `mouse` class is used to collect mouse input.

		__Important note:__

		When using a `mouse` all coordinates are specified relative to the
		top-left of the display, and not, as in `sketchpad`s, relative to the
		display center. For example, the following script will determine the
		deviation of a mouse click relative to the display center.

		__Example:__

		~~~ {.python}
		from openexp.mouse import mouse
		from openexp.canvas import canvas
		my_mouse = mouse(exp)
		my_canvas = canvas(exp)
		while True:
			button, position, timestamp = my_mouse.get_click(timeout=20)
			if button is not None:
				break
			pos, time = my_mouse.get_pos()
			my_canvas.clear()
			my_canvas.fixdot(pos[0], pos[1])
			my_canvas.show()
		~~~

		__Function list:__

		%--
		toc:
			mindepth: 2
			maxdepth: 2
		--%

		%--
		constant:
			arg_buttonlist:
				A list of buttons that are accepted or `None` to accept all
				buttons.
			arg_timeout:
				A numeric value specifying a timeout in milliseconds or `None`
				for no (i.e. infinite) timeout.
			arg_visible: |
				`True` to show the cursor, `False` to hide. (If you are using the
				*legacy* back-end, you may find that the mouse cursor is not
				visible. For a workaround, see
				<http://osdoc.cogsci.nl/back-ends/legacy/>.)
		--%
	"""

	__metaclass__ = docinherit

	def __init__(self, experiment, buttonlist=None, timeout=None,
		visible=False):

		"""
		desc:
			Intializes the mouse object.

		arguments:
			experiment:
				desc:		The experiment object.
				type:		experiment

		keywords:
			buttonlist:
				desc:		"%arg_buttonlist"
				type:		[list, NoneType]
			timeout:
				desc:		"%arg_timeout"
				type:		[int, float, NoneType]
			visible:
				desc:		"%arg_visible"
				type:		bool

		example: |
			from openexp.mouse import mouse
			my_mouse = mouse(exp)
		"""

		raise NotImplementedError()

	def set_buttonlist(self, buttonlist=None):

		"""
		desc:
			Sets a list of accepted buttons.

		keywords:
			buttonlist:
				desc:	"%arg_buttonlist"
				type:	[list, NoneType]

		example: |
			from openexp.mouse import mouse
			my_mouse = mouse(exp)
			my_mouse.set_buttonlist( [1,2] )
		"""

		if buttonlist is None:
			self.buttonlist = None
		else:
			self.buttonlist = []
			try:
				for b in buttonlist:
					self.buttonlist.append(int(b))
			except:
				raise osexception(
					"The list of mousebuttons must be a list of numeric values")

	def set_timeout(self, timeout=None):

		"""
		desc:
			Sets a timeout.

		keywords:
			timeout:
				desc:	"%arg_timeout"
				type:	[int, float, NoneType]

		example: |
			from openexp.mouse import mouse
			my_mouse = mouse(exp)
			my_mouse.set_timeout(2000)
		"""

		self.timeout = timeout

	def set_visible(self, visible=True):

		"""
		desc:
			Sets the visibility of the cursor.

		keywords:
			visible:
				desc:	"%arg_visible"
				type:	bool

		example: |
			from openexp.mouse import mouse
			my_mouse = mouse(exp)
			my_mouse.set_visible()
		"""

		raise NotImplementedError()

	def set_pos(self, pos=(0,0)):

		"""
		desc:
			Sets the position of the mouse cursor.

		keywords:
			pos:
				desc:	An (x,y) tuple for the new mouse coordinates.
				type:	tuple

		example: |
			from openexp.mouse import mouse
			my_mouse = mouse(exp)
			my_mouse.set_pos(pos=(0,0))
		"""

		raise NotImplementedError()

	def get_click(self, buttonlist=None, timeout=None, visible=None):

		"""
		desc:
			Waits for mouse input.

		keywords:
			buttonlist:
				desc:		"%arg_buttonlist"
				type:		[list, NoneType]
			timeout:
				desc:		"%arg_timeout"
				type:		[int, float, NoneType]
			visible:
				desc:		"%arg_visible"
				type:		bool

		returns:
			desc:			A (button, position, timestamp) tuple. The button
							and position are `None` if a timeout occurs.
							Position is an (x, y) tuple in screen coordinates.
			type:			tuple

		example: |
			from openexp.mouse import mouse
			my_mouse = mouse(exp)
			button, position, timestamp = my_mouse.get_click()
			if button is None:
				print('A timeout occurred!')
		"""

		raise NotImplementedError()

	def get_pos(self):

		"""
		desc:
			Returns the current position of the cursor.

		returns:
			desc:	A (position, timestamp) tuple.
			type:	tuple

		example: |
			from openexp.mouse import mouse
			my_mouse = mouse(exp)
			position, timestamp = my_mouse.get_pos()
			x, y = position
			print('The cursor was at (%d, %d)' % (x, y))
		"""

		raise NotImplementedError()

	def get_pressed(self):

		"""
		desc:
			Returns the current state of the mouse buttons. A True value means
			the button is currently being pressed.

		returns:
			desc:	A (button1, button2, button3) tuple of boolean values.
			type:	tuple.

		example: |
			from openexp.mouse import mouse
			my_mouse = mouse(exp)
			buttons = my_mouse.get_pressed()
			b1, b2, b3 = buttons
			print('Currently pressed mouse buttons: (%d,%d,%d)' % (b1,b2,b3))
		"""

		raise NotImplementedError()

	def flush(self):

		"""
		desc:
			Clears all pending input, not limited to the mouse.

		returns:
			desc:	True if a button had been clicked (i.e., if there was
					something to flush) and False otherwise.
			type:	bool

		example: |
			from openexp.mouse import mouse
			my_mouse = mouse(exp)
			my_mouse.flush()
			button, position, timestamp = my_mouse.get_click()
		"""

		raise NotImplementedError()

	def synonyms(self, button):

		"""
		desc:
			Gives a list of synonyms for a mouse button. For example, 1 and
			'left_click' are synonyms.

		arguments:
			button:
				desc:	A button value.
				type:	[int, str, unicode]

		returns:
			desc:	A list of synonyms.
			type:	list
		"""

		button_map = [
			(1, u"left_button"),
			(2, u"middle_button"),
			(3, u"right_button"),
			(4, u"scroll_up"),
			(5, u"scroll_down")
			]
		for bm in button_map:
			if button in bm:
				return bm
		return []
