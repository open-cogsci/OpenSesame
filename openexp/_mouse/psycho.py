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
from openexp._mouse import mouse
from psychopy import event
import psychopy.visual

class psycho(mouse.mouse):

	"""
	desc:
		This is a mouse backend built on top of PsychoPy.
		For function specifications and docstrings, see
		`openexp._mouse.mouse`.
	"""

	def __init__(self, experiment, buttonlist=None, timeout=None,
		visible=False):
	
		if experiment.canvas_backend != "psycho":
			raise osexception( \
				"The psycho mouse backend must be used in combination with the psycho canvas backend!")
		self.experiment = experiment
		self.set_buttonlist(buttonlist)
		self.set_timeout(timeout)
		self.mouse = event.Mouse(visible=False, win=self.experiment.window)
		self.set_visible(visible)
		event.mouseButtons = [0, 0, 0]	

	def set_visible(self, visible=True):

		self.visible = visible
		self.mouse.setVisible(visible)

	def set_pos(self, pos=(0,0)):

		if psychopy.visual.openWindows[0].winType == 'pyglet':
			raise osexception(
				"Method set_pos not supported in pyglet environment (default for psycho back-end)")
		self.mouse.setPos(newPos=pos)
		
	def get_click(self, buttonlist=None, timeout=None, visible=None):
	
		if buttonlist == None:
			buttonlist = self.buttonlist
		if timeout == None:
			timeout = self.timeout
		if visible == None:
			visible = self.visible
		self.mouse.setVisible(visible)
		start_time = 1000.0 * self.experiment.clock.getTime()
		time = start_time
		button = None
		pos = None
		self.mouse.clickReset()
		while True:
			time = 1000.0 * self.experiment.clock.getTime()			
			buttons, times = self.mouse.getPressed(getTime=True)
			if buttons[0] and (buttonlist == None or 1 in buttonlist):
				button = 1
				pos = self.mouse.getPos()
				break
			if buttons[1] and (buttonlist == None or 2 in buttonlist):
				button = 2
				pos = self.mouse.getPos()
				break
			if buttons[2] and (buttonlist == None or 3 in buttonlist):
				button = 3
				pos = self.mouse.getPos()
				break
			if timeout != None and time-start_time >= timeout:
				break
		if pos != None:
			pos = pos[0]+self.experiment.width/2, \
				self.experiment.height/2-pos[1]
		self.mouse.setVisible(self.visible)
		return button, pos, time

	def get_pos(self):

		x, y = self.mouse.getPos()
		t = self.experiment.time()
		x = x + self.experiment.width/2
		y = self.experiment.height/2 - y
		return (x, y), t

	def get_pressed(self):

		return tuple(self.mouse.getPressed(getTime=False))

	def flush(self):

		event.mouseButtons = [0,0,0]
		event.clearEvents()
		return False
