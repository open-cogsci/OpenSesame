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
from openexp._coordinates.psycho import psycho as psycho_coordinates
from openexp._mouse import mouse
from psychopy import event
from openexp.backend import configurable

class psycho(mouse.mouse, psycho_coordinates):

	"""
	desc:
		This is a mouse backend built on top of PsychoPy.
		For function specifications and docstrings, see
		`openexp._mouse.mouse`.
	"""

	def __init__(self, experiment, **resp_args):

		mouse.mouse.__init__(self, experiment, **resp_args)
		psycho_coordinates.__init__(self)
		self.mouse = event.Mouse(visible=False, win=self.experiment.window)
		event.mouseButtons = [0, 0, 0]

	@configurable
	def get_click(self):

		buttonlist = self.buttonlist
		timeout = self.timeout
		self.mouse.setVisible(self.visible)
		start_time = self.experiment.clock.time()
		button = None
		pos = None
		self.mouse.clickReset()
		while True:
			time = self.experiment.clock.time()
			buttons, times = self.mouse.getPressed(getTime=True)
			for i in (1,2,3):
				if buttons[i-1] and (buttonlist is None or i in buttonlist):
					button = i
					pos = self.mouse.getPos()
					break
			else:
				if timeout is not None and time-start_time >= timeout:
					break
				continue
			break
		if pos is not None:
			pos = self.from_xy(pos)
		self.mouse.setVisible(self._cursor_shown)
		return button, pos, time

	def show_cursor(self, show=True):

		self.mouse.setVisible(show)
		mouse.mouse.show_cursor(self, show=show)

	def get_pos(self):

		return self.from_xy(self.mouse.getPos()), self.experiment.time()

	def get_pressed(self):

		return tuple(self.mouse.getPressed(getTime=False))

	def flush(self):

		event.mouseButtons = [0,0,0]
		event.clearEvents()
		return False
